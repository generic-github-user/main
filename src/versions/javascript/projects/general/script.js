var charset = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", ",", ".", "/", "<", ">", "?", " "];

var chars = 5;
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
            //       "num": chars * 2,
            //       "init": [-1, 1]
            // },
            // "Addition": {
            //       "num": chars * 2
            // },
            // "Multiplication": {
            //       "num": chars * 2
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
            "num": 0, //(chars * 5) ** 2,
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

var inputs = [];
var outputs = [];
for (var i = 0; i < data.length; i++) {
      inputs.push(cs.encode.one_hot(data[i].input, charset, 1));
      outputs.push(cs.encode.one_hot(data[i].output, charset, 1));
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

var a = 1;

const update = function() {
      network = network.evolve({
            "iterations": 1,
            "population": 100,
            "inputs": inputs,
            "outputs": outputs,
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
            "update": update_settings,
            "log": true,
            "return": "network"
      });

      document.getElementById("output").innerText = predict("5+5=");
}

setInterval(update, 1);