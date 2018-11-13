# Benchmarks
[`caesium/src/versions/javascript/benchmarks`](https://github.com/generic-github-user/Caesium/tree/master/src/versions/javascript/benchmarks)

A series of short benchmark scripts used for determining the speed of different operations in the JavaScript version of the Caesium AI library. These are meant to be used for optimization purposes, especially comparing different methods of performing operations and determining which parts of the library are the most computationally expensive.

Each file contains a different benchmarking script. More information about each script can be found below. These scripts can be executed in the browser console on a page with Caesium loaded, or as a JavaScript file embedded in a web page with the Caesium library script.

# List of Benchmark Scripts

## Lookup
[`caesium/src/versions/javascript/benchmarks/lookup.js`](https://github.com/generic-github-user/Caesium/tree/master/src/versions/javascript/benchmarks/lookup.js)

`lookup.js` compares the speed of two alternate methods of storing and retrieving nodes in the network object's node list, `network.nodes`.

The first method is to store each node as an object in the `network.nodes` array, then use `array.prototype.find` to find a specific node by its unique UUID.
```javascript
node = nodes.find(x => x.id == nodes[49].id);
```

The second method is to store each node as a property of the `network.nodes` object, with the node's ID as the property key. This allows us to directly reference the node by its ID:
```javascript
node = nodes[nodes[id].id];
```
This method is much faster than the first method.
