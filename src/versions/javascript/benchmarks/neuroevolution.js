// neuroevolution.js

var start, end, average, network, inputs, outputs;
var times = [];

var update_settings = {
      "iterations": 5,
      "limit": {
            "min": -10e3,
            "max": 10e3
      }
};

for (var i = 0; i < 100; i++) {
      inputs = [
            []
      ];
      outputs = [
            []
      ];
      for (var j = 0; j < 20; j++) {
            inputs[0].push(cs.random());
            outputs[0].push(cs.random());
      }

      network = new cs.network({
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

      start = performance.now();
      network = network.evolve({
            "iterations": 1,
            "population": 1,
            "inputs": inputs,
            "outputs": outputs,
            "mutate": {
                  "iterations": 1,
                  "mutation_rate": 0.5,
                  "mutation_size": 1,
                  "nodes": {
                        "Value": {
                              "add": [0, 1],
                              "remove": [0, 1],
                              "limit": 10,
                              "init": [-1, 1]
                        },
                        "Addition": {
                              "add": [0, 1],
                              "remove": [0, 1],
                              "limit": 10
                        },
                        "Multiplication": {
                              "add": [0, 1],
                              "remove": [0, 1],
                              "limit": 10
                        },
                        "Tanh": {
                              "add": [0, 1],
                              "remove": [0, 1],
                              "limit": 10
                        }
                  },
                  "connections": {
                        "add": [0, 10],
                        "remove": [0, 10],
                        "limit": 50
                  }
            },
            "update": update_settings,
            "log": false,
            "return": "network"
      });
      end = performance.now();
      times.push(end - start);
}
average = cs.average(times);

console.log("Tests took average of " + average + " milliseconds each.", times);