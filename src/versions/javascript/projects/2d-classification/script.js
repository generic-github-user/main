// Set up canvas to render/display graphics on
canvas = document.getElementById("canvas");
context = canvas.getContext("2d");
// Set width to be equal to window width
context.canvas.width = window.innerWidth;
// Set height to be equal to window height
context.canvas.height = window.innerHeight;

var inputs = [];
var outputs = [];
var resolution = 50;

for (var i = 0; i < 2; i++) {
      for (var j = 0; j < 2; j++) {
            var input = [
                  Math.random() * (canvas.width / 1000),
                  Math.random() * (canvas.height / 1000),
            ];

            inputs.push(input);
            outputs.push([Math.round(cs.random())]);
      }
}
const colors = [0, 100];

n = 2;

var network = new cs.network({
      "inputs": 2,
      "outputs": 1,
      "nodes": {
            "Value": {
                  "num": n,
                  "init": [-1, 1]
            },
            "Addition": {
                  "num": n
            },
            "Multiplication": {
                  "num": n
            },
            "Tanh": {
                  "num": n
            },
            "Sine": {
                  "num": n
            },
            "Cosine": {
                  "num": n
            },
            "Abs": {
                  "num": n
            }
      },
      "connections": {
            "num": 100,
            "init": [-1, 1]
      }
});

var update_settings = {
      "iterations": 5,
      "limit": {
            "min": -10e3,
            "max": 10e3
      }
};

var a = 0;

function evolve() {
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
                              "limit": 10,
                              "init": [-1, 1],
                              "value": {
                                    "mutation_rate": 0.5,
                                    "mutation_size": 1
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
                        "Tanh": {
                              "add": [0, a],
                              "remove": [0, a],
                              "limit": 10
                        },
                        "Sine": {
                              "add": [0, a],
                              "remove": [0, a],
                              "limit": 10
                        },
                        "Cosine": {
                              "add": [0, a],
                              "remove": [0, a],
                              "limit": 10
                        },
                        "Abs": {
                              "add": [0, a],
                              "remove": [0, a],
                              "limit": 10
                        }
                  },
                  "connections": {
                        "add": [0, 10],
                        "remove": [0, 10],
                        "limit": 100,
                        "init": [-1, 1],
                        "value": {
                              "mutation_rate": 0.5,
                              "mutation_size": 1
                        }
                  }
            },
            "update": update_settings,
            "log": true,
            "return": "network"
      });

      for (var i = 0; i < canvas.height; i += resolution) {
            for (var j = 0; j < canvas.width; j += resolution) {
                  var input = [
                        j / 100,
                        i / 100
                  ];
                  //var hue = Math.round(evaluate(0, input)[0]) * 1000;
                  var output = network.evaluate({
                        "input": input,
                        "update": update_settings
                  })[0];

                  var hue = Math.tanh(output) * 100;

                  // if (output < 0.5) {
                  //       hue = colors[0];
                  // } else {
                  //       hue = colors[1];
                  // }
                  context.fillStyle = "hsla(" + hue + ", 100%, 50%, 1)";
                  context.fillRect(j, i, resolution, resolution);

            }
      }

      for (var i = 0; i < inputs.length; i++) {
            var output = network.evaluate({
                  "input": inputs[i],
                  "update": update_settings
            })[0];
            var x = inputs[i][0] * 1000;
            var y = inputs[i][1] * 1000;

            context.fillStyle = "hsla(0, 0%, " + outputs[i][0] * 100 + "%, 1)";
            context.beginPath();
            context.arc(x, y, 5, 0, 2 * Math.PI);
            context.fill();

            var text = output.toFixed(5)
            var textx = x + 10;
            var texty = y - 20;
            context.font = "20px Roboto";
            context.fillText(text, textx, texty);
      }
}

var interval = window.setInterval(evolve, 100);