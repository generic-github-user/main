var charset = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", " "];

var network = new cs.network({
      "nodes": {
            "Input": {
                  "num": charset.length * 20
            },
            "Output": {
                  "num": charset.length * 20
            },
            "Value": {
                  "num": 3,
                  "init": [-1, 1]
            },
            "Addition": {
                  "num": 3
            },
            "Multiplication": {
                  "num": 3
            },
            // "Tanh": {
            //       "num": 3
            // },
            // "Sine": {
            //       "num": 3
            // },
            // "Cosine": {
            //       "num": 3
            // },
            // "Abs": {
            //       "num": 3
            // }
      },
      "connections": {
            "num": 10,
            "init": [-1, 1]
      }
});

var update_settings = {
      "iterations": 2,
      "limit": {
            "min": -10e3,
            "max": 10e3
      }
};

var inputs = [];
var outputs = [];
for (var i = 0; i < data.length; i++) {
      inputs.push(encodeString(data[i].input, charset, chars));
      outputs.push(encodeString(data[i].output, charset, chars));
}

a = 0;

network = network.evolve({
      "iterations": 10,
      "population": 50,
      "inputs": inputs,
      "outputs": outputs,
      "mutate": {
            "iterations": 1,
            "nodes": {
                  "Value": {
                        "add": [0, a],
                        "remove": [0, a],
                        "limit": 10,
                        "init": [-1, 1],
                        "value": {
                              "mutation_rate": 0.5,
                              "mutation_size": 1,
                        }
                  },
                  "Addition": {
                        "add": [0, a],
                        "remove": [0, a],
                        "limit": 10
                  },
                  "Multiplication": {
                        "add": [0, a],
                        "remove": [0, a],
                        "limit": 10
                  },
                  // "Tanh": {
                  //       "add": [0, a],
                  //       "remove": [0, a],
                  //       "limit": 10
                  // },
                  // "Sine": {
                  //       "add": [0, a],
                  //       "remove": [0, a],
                  //       "limit": 10
                  // },
                  // "Cosine": {
                  //       "add": [0, a],
                  //       "remove": [0, a],
                  //       "limit": 10
                  // },
                  // "Abs": {
                  //       "add": [0, a],
                  //       "remove": [0, a],
                  //       "limit": 10
                  // }
            },
            "connections": {
                  "add": [0, 0],
                  "remove": [0, 0],
                  "limit": 50,
                  "init": [-1, 1],
                  "value": {
                        "mutation_rate": 0.5,
                        "mutation_size": 0.1,
                  }
            }
      },
      "update": update_settings,
      "log": true,
      "return": "network"
});

// don't use evaluate
const predict = function(input) {
      return decodeString(
            network.evaluate({
                  "input": encodeString(input, charset, 20),
                  "update": update_settings
            }),
            charset
      );
}