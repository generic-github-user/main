// network_creation.js

var network, start, end, average;
var times = [];

for (var i = 0; i < 100; i++) {
      start = performance.now();
      network = new cs.network({
            "nodes": {
                  "Input": {
                        "num": 20
                  },
                  "Output": {
                        "num": 20
                  },
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
      end = performance.now();
      times.push(end - start);
}
average = cs.average(times);

console.log("Tests took average of " + average + " milliseconds each.", times);