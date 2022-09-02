var network = new cs.network({
      "inputs": 20,
      "outputs": 20,
      "nodes": {
            "Value": {
                  "num": 20,
                  "init": [-1, 1]
            },
            "Addition": {
                  "num": 20
            },
            "Multiplication": {
                  "num": 20
            },
            "Tanh": {
                  "num": 20
            }
      },
      "connections": 500
});


console.time("1");
for (var attr in network.nodes) {
      if (network.nodes.hasOwnProperty(attr)) {
            a = network.nodes[attr]
      }
}
console.timeEnd("1");

console.time("2");
Object.keys(network.nodes).forEach(
      (k) => {
            a = network.nodes[k]
      }
);
console.timeEnd("2");

b = Object.keys(network.nodes);
// b = Array(120).fill(cs.random());
console.time("3");
for (var i = 0; i < b.length; i++) {
      // a = network.nodes[b[i]];
      a = b[i];
}
console.timeEnd("3");