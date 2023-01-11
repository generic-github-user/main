from __future__ import annotations

import json
from option import Option
from result import Result
from pathlib import Path
import itertools
import random

from pylist import List
from pydict import Dict
from box import Box

from typing_extensions import Protocol
from typing import TypeVar, Generic, Optional
T = TypeVar('T')
S = TypeVar('S', covariant=True)


class Settings:
    def serializer(z): return json.dumps(z, indent=4)
    cache_size = 10e6
    block_size = 10e5
    # nlp = spacy.load('en_core_web_lg')


class Graphlike(Protocol[S]):
    def get(self, id_) -> Result[Node]:
        ...

    def contains(self, node) -> bool:
        ...

    def to_list(self) -> List[Node]:
        ...

    def map(self, f) -> Graphlike:
        ...

    def filter(self, f) -> Graphlike:
        ...

    def to_string(self, depth=1) -> str:
        ...

    def print(self) -> None:
        ...

    def is_empty(self) -> bool:
        ...

    def find(self, key: T) -> Option[Node]:
        ...

    def order(self) -> int:
        ...

    def ids(self) -> set[int]:
        ...

    def add(self, node: Node) -> Graphlike:
        ...


# class Graph(Generic[T], Graphlike):
class Graph(Graphlike[T]):
    """A generalized graph in which edges can connect multiple nodes (i.e., a
    hypergraph) and edges can contain other edges (nodes and edges are
    undifferentiated; this is sometimes referred to as a metagraph). Each
    entity (node) in the graph is therefore an (optional) piece of data
    attached to a set, which can contain any of the graph's nodes, including
    itself.

    The canonical graph representation is stored in a series of files on disk
    (called "blocks"), each containing a limited number of nodes. Frequently
    used nodes are cached in an in-RAM dictionary. The `Node` class provides a
    functional wrapper around nodes; generally, only a small fraction of the
    nodes in the database will actually be stored by the interpreter as `Node`
    instances.

    `Graph` is optimized for highly efficient inference and reliablity; the API
    also aims to be highly scalable, supporting databases on the order of 10^11
    nodes and at least 10^12 connections. It is being designed specifically for
    the Eva symbolic artificial intelligence project and the interface is
    expected to change frequently.

    Each node in the graph has a globally unique index (a positive integer)
    that identifies it. This is used as a hash map key in many cases for rapid
    retrieval within an individual block."""

    def __init__(self, path: Option[Path], size: int, blocks: List[Path],
                 index: int, block_index: int):
        """Initialize a new graph instance; this is an internal method and API
        users should generally prefer either `Graph.new` or `Graph.load`
        instead."""

        self.path = path
        self.size = size
        self.blocks = blocks
        self.index = index
        self.block_index = block_index

        self.nodes: Dict[int, Node] = Dict()

    @staticmethod
    def load(path: Path) -> Result[Graph]:
        """Loads a graph stored in the specified directory; note that this only
        creates a "view" on the saved data and most nodes will not be loaded
        into memory until they are needed"""

        try:
            info = Box(json.loads((path / 'root.json').read_text()))
            return Result.Ok(Graph(Option.some(path), info.size,
                                   List(info.blocks).map(Path), info.index,
                                   info.block_index))
        except FileNotFoundError as e:
            return Result.Err(e)

    def clean(self) -> bool:
        """Returns true iff the on-disk representation of the graph is
        up-to-date (i.e., synced) with any modifications stored in RAM"""

        return List(self.nodes.values()).all(lambda n: n.clean)

    def write(self) -> Result:
        """Completes a "full write", syncing every unclean node in memory with
        its on-disk version"""

        try:
            self.path.unwrap().mkdir(exist_ok=True)
            (self.path.unwrap() / 'root.json').write_text(
                Settings.serializer(self.metadata()))

            batches = List(self.nodes.values()).filter(lambda x: not x.clean)\
                .partition('block')
            # .map(lambda x: x.block.value)
            for k, v in batches.items():
                self.write_block(k.unwrap(), v)
            return Result.Ok(None)

        except FileNotFoundError as e:
            print(e)
            return Result.Err(e)

    def close(self) -> Result:
        return Result.Ok(None)

    @staticmethod
    def new(path: Option[Path]) -> Graph:
        """Returns a new, empty graph."""
        return Graph(path, 0, List(), 0, 0)

    @staticmethod
    def from_list(source: List[T]) -> Graph[T]:
        result = Graph.new(Option.none())
        source.for_each(result.node)
        return result

    def get_attrs(self, attrs) -> dict:
        return {a: getattr(self, a) for a in attrs}

    def metadata(self) -> dict:
        """Returns a standard Python dictionary containing high-level
        information about this graph; this will typically be serialized to
        root.json"""

        return self.get_attrs(['size', 'index', 'block_index']) | {'path': str(
            self.path.unwrap()), 'blocks': list(self.blocks.map(str))}

    def add(self, node: Node) -> Graph:
        # self.nodes.append(node)
        self.nodes[node.id] = node
        self.size += 1
        assert self.contains(node)
        return self

    # def remove(self, id_: int) -> Graph:
    def remove(self, node: Node) -> Graph:
        self.size -= 1
        assert not self.contains(node)
        return self

    def filter(self, f) -> Graphlike:
        """Returns an unrealized graph (i.e., a graph view) containing only the
        nodes in `self` for which `f` returns True (specifically, when `f` is
        called on the data in each node; so a Node<T> will be included in the
        output iff the predicate f: T -> bool is true).

        The returned Graph is a subgraph of `self` and therefore uses the same
        namespace."""

        return FilterGraph(self, f)

    def map(self, f) -> Graphlike:
        """Returns a `MapGraph` wrapping `self`; `get` calls will be passed on
        to the enclosed graph. The namespace of the result will be identical to
        that of the input, and the two graphs will have the same size.

        By default, `Y` is an "ephemeral" graph with no on-disk
        representation."""

        return MapGraph(self, f)

    @staticmethod
    def union(graphs: List[Graph]) -> Graphlike:
        # TODO: figure out how to handle namespaces (particularly, designing a
        # robust scheme that naturally allows for inherited/wrapped graphs)

        return UnionGraph(graphs)

    def load_block(self, path: Path) -> Graphlike:
        """Internal method for fetching the nodes from the block stored at
        `path` and caching them in memory"""

        print(f'Loading block at {path}')
        self.prune()
        block = json.loads(path.read_text())
        for node in block.values():
            # if node['id'] not in self.nodes:
            if not self.nodes.contains(node['id']):
                # TODO
                self.nodes[node['id']] = Node.from_dict(node, self,
                                                        Option.some(path))
        return self

    def iter_block(self, path: Path) -> List[Node]:
        block = json.loads(path.read_text())
        return List(block.values()).map(
            lambda node: Node.from_dict(node, self, Option.some(path)))

    def write_block(save, path: Path, batch: List[Node[T]]):
        batch_dict = {x.id: x.dict() for x in batch}
        try:
            block = json.loads(path.read_text())
            # print(block, batch_dict)
            path.write_text(Settings.serializer(block | batch_dict))
            batch.set('clean', True)
        except FileNotFoundError as e:
            print(e)
            path.write_text(Settings.serializer(batch_dict))

    def prune(self):
        pass

    def get(self, id_) -> Result[Node]:
        """Retrieve the node designated by `id_`, loading the relevant block
        from secondary storage if necessary"""

        # breakpoint()
        if self.nodes.contains(id_):
            return Result.Ok(self.nodes[id_].unwrap())
        else:
            if not self.path.is_some:
                return Result.Err(None)
            b = self.path.unwrap() / f'{self.get_block(id_)}.json'
            found = False
            self.load_block(b)
            if self.nodes.contains(id_):
                found = True
            for block in set(self.blocks) - set([b]):
                self.load_block(block)
                if self.nodes.contains(id_):
                    found = True
                    break
            if found:
                result = self.nodes[id_].unwrap()
                result.freq += 1
                return Result.Ok(result)
            print(f'Not found: {id_}')
            return Result.Err(None)

    def get_block(self, i):
        return int(i // Settings.block_size)

    def iter(self):
        """Returns an iterator over the nodes in this graph"""

        # class GraphIter:
        #     def __iter__(inner):
        # return GraphIter()
        if self.path.is_some:
            # return itertools.chain(self.blocks.map(self.iter_block))
            return itertools.chain.from_iterable(
                self.blocks.map(self.iter_block))
        else:
            return self.nodes.values()

    def to_list(self) -> List[Node]:
        # return List(self.nodes.values())
        return List(self.iter())

    def contains(self, node) -> bool:
        return self.get(node.id).ok

    def node(self, value: T, group: Optional[Graphlike[T]] = None) -> Node[T]:
        """Returns a new node bound to this graph and adds it to the graph.
        Newly created nodes will be assigned a "default" block, which will be
        the first one checked if the node needs to be paged into memory."""

        if group is None:
            group = Graph.new(Option.none())

        self.index += 1
        if self.path.is_some:
            block_index = self.get_block(self.index)
            path = self.path.unwrap() / f'{block_index}.json'
            if path not in self.blocks:
                self.blocks.append(path)
            path_ = Option.some(path)
        else:
            path_ = Option.none()
        node = Node(
            self.index,
            value,
            group,
            self,
            False,
            path_,
            List(
                group.ids()))
        # ?
        self.add(node)
        return node

    def order(self) -> int:
        return self.to_list().length()

    def is_empty(self) -> bool:
        """Returns true if the graph contains no nodes and false otherwise"""

        return self.to_list().length() == 0

    def find(self, key: T) -> Option[Node[T]]:
        """Search for a node matching `key`; returns a none-Option if not
        found."""

        matches = self.filter(lambda x: x.value == key)
        if matches.is_empty():
            return Option.none()
        else:
            return Option.some(matches.to_list()[0])

    # @staticmethod
    def from_dict(self: Graph[Optional[int | str]], source: dict | list | int |
                  str, root: Node[T]) -> Node:
        """Load data from a simple, acyclic JSON-like dictionary (which can
        also include ordered lists). Dicts will become `None` nodes joined to
        their values by an edge corresponding to each key; lists will be
        converted similarly, using the integer index of each element in place
        of the key. This method works recursively."""

        # ???
        # result = Graph.new(Option.none())
        result = self
        if isinstance(source, (int, str)):
            return result.node(source)
        elif isinstance(source, list):
            for i, x in enumerate(source):
                result.node(i).add(root).add(
                    self.from_dict(x, self.node(None)))
        elif isinstance(source, dict):
            # rootnode = result.node(root)
            for k, v in source.items():
                assert isinstance(k, str)
                result.node(k).add(root).add(
                    self.from_dict(v, self.node(None)))
        else:
            raise TypeError('Cannot convert this type of object')
        return root

    def ids(self) -> set[int]:
        return set(self.to_list().get('id'))

    def random(self) -> Result[Node[T]]:
        # return random.choice(self.iter())
        return self.get(random.choice(list(self.ids())))

    def to_string(self, depth=1):
        return f'Graph [{self.to_list().to_string(depth=depth-1) if depth > 0 else "..."}]'

    def print(self) -> None:
        print(self.to_string())

    def __str__(self) -> str:
        return self.to_string()

    __repr__ = __str__


def methods(x):
    return set([func for func in dir(x) if callable(getattr(x, func))
                # and not func.startswith("__")])
                and func not in ['__class__']])


def GraphWrapper(graphclass):
    # class WrapperClass(Graph):
    class WrapperClass(Graphlike):
        pass
    for method in ['filter', 'map', 'is_empty', 'print', 'to_string',
                   'contains', 'find', 'order']:
        setattr(WrapperClass, method, getattr(Graph, method))
    for method in methods(graphclass):
        setattr(WrapperClass, method, getattr(graphclass, method))
    return WrapperClass


@GraphWrapper
class FilterGraph(Graphlike):
    def __init__(self, source, f):
        self.source = source
        self.f = f

    def to_list(self) -> List[Node]:
        # do we also need to filter out grouped nodes that don't match the
        # predicate (see, e.g., MapGraph.get)?
        #
        # also, should we remap the returned nodes to reference the instance of
        # the wrapper class? return List(self.source.iter()).filter(self.f)
        return self.source.to_list().filter(self.f)

    def get(self, id_) -> Result[Node]:
        x = self.source.get(id_)
        # TODO: rewrite using functional API
        if not x.ok:
            return x
        if self.f(x.unwrap().value):
            # TODO: fix this
            return x
        return Result.Err(None)


@GraphWrapper
class MapGraph(Graphlike):
    def __init__(self, source, f):
        self.source = source
        self.f = f

    def to_list(self) -> List[Node]:
        return self.source.to_list().map(self.f)

    def get(self, id_) -> Result[Node]:
        x = self.source.get(id_)
        if not x.ok:
            return x
        # ?
        return Result.Ok(Node(x.unwrap().id, self.f(x.unwrap().value),
                              x.unwrap().grouped().map(self.f), self, False,
                              Option.none(), x.group_ids))


@GraphWrapper
class UnionGraph(Graphlike):
    def __init__(self, sources):
        self.sources = sources


def compose(f, g):
    return lambda *args, **kwargs: f(g(*args, **kwargs))


class Node(Generic[T]):
    """A lightweight wrapper that provides a functional interface to common
    graph operations without storing massive collections of Python objects in
    memory. Instances are generally bound to a specific graph, which gives
    meaning to their id attribute (as an identifier in the host graph's
    namespace). The `Node` API currently supports mutating operations; this may
    change in the future."""

    def __init__(self, id_: int, value: Optional[T], group: Graphlike[T],
                 graph: Graphlike[T], clean: bool, block: Option[Path],
                 group_ids: Optional[List[int]] = None):
        # An integer that identifies this node in a graph
        self.id = id_
        # The data the node stores (generic in `T`)
        self.value = value
        # A list of integers designating the nodes contained in this one (when
        # interpreted as a hyperedge)
        self.group_ids = group_ids
        # A graph containing the actual nodes corresponding to `self.group_ids`
        # (potentially obsolete)
        self.group = group
        # The graph that this node is bound to
        self.graph = graph
        # A cache (graph) with all the nodes that contain this one
        self.refs_ = Option.none()
        # A boolean flag indicating whether modifications made to the node have
        # been synced to secondary storage (i.e., a database block)
        self.clean = clean
        # The path this node is stored persistently at
        self.block = block
        # The number of times this node was accessed during the most recent
        # session/caching window
        self.freq: int = 0

        assert isinstance(self.block, Option), type(self.block)

    @staticmethod
    def from_dict(node: dict, graph: Graph[T], block: Option[Path]) -> Node[T]:
        # TODO: resolve node IDs to actual nodes
        # is this the best/cleanest way?
        return Node(node['id'], node['value'], Option.none(),
                    # Graph.from_list(List(node['group'])).map(
                    #    compose(Result.unwrap, graph.get)),
                    graph, True, block, List(node['group']))

    def refs(self) -> Graphlike[T]:
        """Returns a graph containing only nodes that contain this one"""

        self.freq += 1
        if not self.refs_.is_some:
            self.refs_ = Option.some(self.graph.filter(
                lambda x: x.grouped().contains(self)))
        return self.refs_.unwrap()

    def grouped(self) -> Graphlike[T]:
        @GraphWrapper
        class LazyGraph:
            def __init__(inner, source):
                inner.source = source

            def to_list(inner) -> List[Node[T]]:
                return inner.source.map(lambda i: inner.get(i).unwrap())

            def get(inner, id_) -> Result[Node[T]]:
                # assert id_ < List(inner.source).length(), id_
                # return self.graph.get(inner.source[id_])
                return self.graph.get(id_)
        return LazyGraph(self.group_ids)

    def get(self, id_: int) -> Result[Node[T]]:
        return self.grouped().get(id_)

    def add(self, node: Node[T]) -> Node[T]:
        """Adds a node to this node's "group", the set of nodes it contains (if
        viewed as a hyperedge which can group other nodes or hyperedges)"""

        assert node.graph == self.graph
        # node.refs().add(self)
        self.group.add(node)
        self.clean = False
        assert self.grouped().contains(node)
        return self

    def adjacent(self) -> Graphlike[T]:
        """Returns a graph containing adjacent nodes (in the generalized sense
        corresponding to the metagraph model), those which are contained by
        nodes/edges that also contain this node (including the node itself)"""

        self.freq += 1
        return Graph.union(self.refs().map(Node.grouped).to_list())

    def edges(self) -> Graphlike[T]:
        """Returns all incident nodes with exactly 2 children"""

        return self.refs().filter(lambda node: node.grouped().order() == 2)

    def in_edges(self) -> Graphlike[T]:
        """Returns all edges pointing into this node"""

        return self.edges().filter(lambda node: node.get(1) == self)

    def out_edges(self) -> Graphlike[T]:
        """Returns all edges pointing from this node into another"""

        return self.edges().filter(lambda node: node.get(0) == self)

    def property(self, key: T) -> Option[Node[T]]:
        """A convenience method for inference engines and database operations;
        searches for a directed edge labelled with `key` and returns the node
        it points to (if such an edge exists)"""

        return self.out_edges().find(key).then(lambda node: node.get(1))

    def dict(self) -> dict:
        """Returns a dictionary containing the node's basic attributes; used to
        generate a serialized representation of a node during the syncing
        stage"""

        return {'id': self.id,
                'value': self.value,
                'group': list(self.group.to_list().map(lambda x: x.id))}

    def to_string(self, depth=1) -> str:
        return f'Node <{self.value}> [{self.grouped().to_string(depth-1)}]'

    def __str__(self) -> str:
        return self.to_string()

    __repr__ = __str__
