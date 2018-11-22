var charset = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", ",", ".", "/", "<", ">", "?", " "];

var output_chars = 5;

var network = new cs.network({
      "nodes": {
            "Input": {
                  "num": charset.length
            },
            "Output": {
                  "num": charset.length
            },
            // "Value": {
            //       "num": 3,
            //       "init": [-1, 1]
            // },
            // "Addition": {
            //       "num": 3
            // },
            // "Multiplication": {
            //       "num": 3
            // },
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
            "num": 1000,
            "init": [-1, 1]
      }
});

var update_settings = {
      "iterations": 1,
      "limit": {
            "min": -10e5,
            "max": 10e5
      }
};

var input_data = [];
var output_data = [];
for (var i = 0; i < data.length; i++) {
      var input_set = [];
      for (var j = 0; j < data[i].input.length; j++) {
            input_set.push(cs.encode.one_hot(data[i].input[j], charset, 1));
      }
      input_data.push(input_set);
      output_data.push(cs.encode.one_hot(data[i].output, charset, data[i].output.length));
}

// Maximum of output values
// don't use evaluate - reset
const predict = function(input) {
      var output = "";
      network.reset();
      for (var i = 0; i < input.length; i++) {
            network.set_inputs({
                  "inputs": cs.encode.one_hot(
                        input[i],
                        charset,
                        1
                  )
            });
            network.update(update_settings);
      }
      for (var i = 0; i < output_chars; i++) {
            network.update(update_settings);
            output += cs.decode.one_hot(
                  cs.apply(
                        network.get_outputs(),
                        Math.round
                  ),
                  charset
            );
      }
      return output;
}

const evaluate = function(network, input, output) {
      var outputs = [];
      for (var i = 0; i < input.length; i++) {
            network.set_inputs({
                  "inputs": input[i]
            });
            network.update(update_settings);
      }
      for (var i = 0; i < output.length / charset.length; i++) {
            network.update(update_settings);
            outputs.push(...network.get_outputs());
      }
      return outputs;
}

var a = 1;

const update = function() {
      network = network.evolve({
            "iterations": 1,
            "population": 100,
            "inputs": input_data,
            "outputs": output_data,
            "mutate": {
                  "iterations": 1,
                  "nodes": {
                        "Value": {
                              "add": [0, a],
                              "remove": [0, a],
                              "limit": 100,
                              "init": [-1, 1],
                              "value": {
                                    "mutation_rate": 1,
                                    "mutation_size": 0.001,
                              }
                        },
                        "Addition": {
                              "add": [0, a],
                              "remove": [0, a],
                              "limit": 100
                        },
                        "Multiplication": {
                              "add": [0, a],
                              "remove": [0, a],
                              "limit": 100
                        },
                        "Tanh": {
                              "add": [0, a],
                              "remove": [0, a],
                              "limit": 100
                        },
                        "Sine": {
                              "add": [0, a],
                              "remove": [0, a],
                              "limit": 100
                        },
                        "Cosine": {
                              "add": [0, a],
                              "remove": [0, a],
                              "limit": 100
                        },
                        "Abs": {
                              "add": [0, a],
                              "remove": [0, a],
                              "limit": 100
                        }
                  },
                  "connections": {
                        "add": [0, 1],
                        "remove": [0, 1],
                        "limit": 5000,
                        "init": [-1, 1],
                        "value": {
                              "mutation_rate": 1,
                              "mutation_size": 0.001,
                        }
                  }
            },
            "evaluate": evaluate,
            "log": true,
            "return": "network"
      });

      document.getElementById("output").innerText = predict("Hello.");
}

setInterval(update, 100);