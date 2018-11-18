// neuroevolution.js

// Initialize variables
var start, end, average, network, inputs, outputs;
// List of times for benchmark testing
var times = [];

// Update settings for network evaluation
var update_settings = {
      "iterations": 5,
      "limit": {
            "min": -10e3,
            "max": 10e3
      }
};

for (var i = 0; i < 100; i++) {
      // Reset input training data array
      inputs = [
            []
      ];
      // Reset output training data array
      outputs = [
            []
      ];
      // Populate input and output training data arrays with randomly generated data
      for (var j = 0; j < 20; j++) {
            inputs[0].push(cs.random());
            outputs[0].push(cs.random());
      }

      // Create a new network to train using neuroevolution
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

      // Start timer
      start = performance.now();
      // Evolve network given input and output training data
      network = network.evolve({
            "iterations": 1,
            "population": 1,
            "inputs": inputs,
            "outputs": outputs,
            "mutate": {
                  "iterations": 1,
                  "nodes": {
                        "Value": {
                              "add": [0, 1],
                              "remove": [0, 1],
                              "limit": 10,
                              "init": [-1, 1],
                              "value": {
                                    "mutation_rate": 1,
                                    "mutation_size": 0.5
                              }
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
                        "limit": 50,
                        "value": {
                              "mutation_rate": 0,
                              "mutation_size": 0
                        }
                  }
            },
            "update": update_settings,
            "log": false,
            "return": "network"
      });
      // Stop timer
      end = performance.now();
      // Calculate time elapsed during test
      times.push(end - start);
}
// Find average duration of all tests
average = cs.average(times);

// Log information about benchmark testing
console.log("Tests took average of " + average + " milliseconds each.", times);