hamlet = nltk.corpus.gutenberg.sents('shakespeare-hamlet.txt')
def words_to_sent(w):
    s = w[0]
    s += ''.join([t if t in string.punctuation else ' '+t for t in w[1:]])
    return s
hamlet = list(map(words_to_sent, hamlet))
hamlet = list(filter(lambda l: len(l) >= 10, hamlet))

w = 800
def clip(x):
    return x[:20]

c = random.choices(hamlet, k=w*2)
a = c[:w]
b = c[w:]

a, b = map(clip, a), map(clip, b)
pairs = []
limit = 1000
for x, y in itertools.product(a, b):
    dist = fuzz.token_sort_ratio(x, y)
    if 60 < dist < 97:
        pairs.append([dist, x, y])
    if len(pairs) >= limit:
        break

pprinter = pprint.PrettyPrinter()
pprinter.pprint(pairs[:5])
print(len(pairs))



symbols = '++--'
num = [dict(cat='num')]
op = [dict(unique=False), dict(unique=False)]
# G = Graph(nodes=[1, 1], duplicate=True, metadata=num)

L = 6
#     start_values = [2, 12, 4, 32, 7]
start_values = [random.randint(-10, 10) for i in range(6)]
G = Graph(start_values, False, False, metadata=num)
# G.evolve(lambda x: x.branch(lambda y: y+))
# print(G.nodes)
buffer = [v for v in G.nodes]
for i in range(30):
#         s = sorted(G.find(cat='num').nodes, key=lambda k: k.value, reverse=True)[:3]
    s = buffer[-L:]

#     print(s, G.nodes)
#         print([a.value for a in s])
#         j = G.add_node(sum(n.value for n in s), metadata=num)
    s = [v.value for v in s]
    j = G.add_node(((s[-1]+s[-3])-s[-4])-(abs(s[-5])+1), metadata=num, duplicate=True)
    buffer.append(j)
    buffer.pop(0)
#         G.add_node(['+', s[0], j], metadata=op, duplicate=False)
#         G.add_node(['+', s[1], j], metadata=op)
    for l in range(4):
#             G.add_node(Node('+', [s[l], j], graph=G), duplicate=False)
#             breakpoint()
        Node(symbols[l], [s[l], j], graph=G, duplicate=False)
#     *s?
G.visualize(width=1000, height=1000, directed=True, node_options={'shape': 'circle'})


R = RandomGraph(100, 100, weighted=True)
print(random.choice(R.nodes).weight)
# R.visualize(width=1000, height=1000, node_options={'shape': 'circle'})


R = RandomGraph(30, 30, weighted=True)
plt.imshow(R.AdjacencyMatrix())
