var charset = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"] //, "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", ",", ".", "/", "<", ">", "?", " "];

var output_chars = 10;

var network = new cs.network({
      "nodes": {
            "Input": {
                  "num": charset.length
            },
            "Output": {
                  "num": charset.length
            },
            // "Value": {
            //       "num": charset.length * 3,
            //       "init": [-1, 1]
            // },
            "Addition": {
                  "num": charset.length * 3
            },
            // "Multiplication": {
            //       "num": charset.length * 3
            // },
            // "Tanh": {
            //       "num": 0
            // },
            // "Sine": {
            //       "num": 30
            // },
            // "Cosine": {
            //       "num": 30
            // },
            // "Abs": {
            //       "num": 30
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
      network.set_inputs({
            "inputs": new Array(charset.length).fill(0)
      });
      for (var i = 0; i < output_chars; i++) {
            network.update(update_settings);
            output += cs.decode.one_hot(
                  network.get_outputs(),
                  charset
            );
      }
      return output;
}

const evaluate = function(network_, input, output) {
      var outputs = [];
      network_.reset();
      for (var i = 0; i < input.length; i++) {
            network_.set_inputs({
                  "inputs": input[i]
            });
            network_.update(update_settings);
      }
      network_.set_inputs({
            "inputs": new Array(charset.length).fill(0)
      });
      for (var i = 0; i < output.length / charset.length; i++) {
            network_.update(update_settings);
            outputs.push(...network_.get_outputs());
      }
      return outputs;
}

var a = 0;
var epoch = 0;

const update = function() {
      var generation = network.evolve({
            "iterations": 1,
            "population": 50,
            "inputs": input_data,
            "outputs": output_data,
            "mutate": {
                  "iterations": 1,
                  "nodes": {
                        "Value": {
                              "add": [0, a],
                              "remove": [0, a],
                              "limit": 1000,
                              "init": [-1, 1],
                              "value": {
                                    "mutation_rate": 0,
                                    "mutation_size": 0,
                              }
                        },
                        "Addition": {
                              "add": [0, a],
                              "remove": [0, a],
                              "limit": 1000
                        },
                        "Multiplication": {
                              "add": [0, a],
                              "remove": [0, a],
                              "limit": 1000
                        },
                        // "Tanh": {
                        //       "add": [0, a],
                        //       "remove": [0, a],
                        //       "limit": 100
                        // },
                        // "Sine": {
                        //       "add": [0, a],
                        //       "remove": [0, a],
                        //       "limit": 100
                        // },
                        // "Cosine": {
                        //       "add": [0, a],
                        //       "remove": [0, a],
                        //       "limit": 100
                        // },
                        // "Abs": {
                        //       "add": [0, a],
                        //       "remove": [0, a],
                        //       "limit": 100
                        // }
                  },
                  "connections": {
                        "add": [0, 10],
                        "remove": [0, 10],
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
            "return": "all"
      });

      network = generation.network;
      // scatterChartData.datasets[0].data = [];
      for (var i = 0; i < generation.population.length; i++) {
            scatterChartData.datasets[0].data.push({
                  x: epoch,
                  y: generation.population[i].score
            })
      }
      window.myScatter.update();

      document.getElementById("output").innerText = predict("abc");
      epoch++;
}

setInterval(update, 100);