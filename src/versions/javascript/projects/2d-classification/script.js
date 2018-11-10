// Set up canvas to render/display graphics on
canvas = document.getElementById("canvas");
context = canvas.getContext("2d");
// Set width to be equal to window width
context.canvas.width = window.innerWidth;
// Set height to be equal to window height
context.canvas.height = window.innerHeight;

var inputs = [];
var outputs = [];

for (var i = 0; i < 2; i++) {
      for (var j = 0; j < 3; j++) {
            var input = [
                  Math.random() * (canvas.width / 1000),
                  Math.random() * (canvas.height / 1000),
            ];
            var output = [];

            for (var r = 0; r < 2; r++) {
                  output.push(-1);
            }
            output[i] = 1;

            inputs.push(input);
            outputs.push(output);
      }
}
const colors = [0, 100];

var network = new cs.network({
      "inputs": 2,
      "outputs": 2,
      "nodes": {
            "Data/Value": {
                  "num": 3,
                  "init": [-1, 1]
            },
            "Operation/Addition": {
                  "num": 3
            },
            "Operation/Multiplication": {
                  "num": 3
            }
      },
      "connections": 0
});

function evolve() {
      var score = 0;
      for (var i = 0; i < 50; i++) {
            train.evolve.mutate(0, 10, 10, 0.01);
            //(score / 10)
            for (var j = 0; j < population.length; j++) {
                  score = 0;
                  for (var q = 0; q < trainingData.length; q++) {
                        //optimize
                        for (var w = 0; w < trainingData[q].output.length; w++) {
                              var output = (train.evolve.evaluate(j, trainingData[q].input)[w]);
                              score += Math.abs(output - trainingData[q].output[w]);
                        }
                  }
                  train.evolve.assignScore(j, score);
            }
            train.evolve.iterate(0, "min", 10);
            //var score = neuralNetworks[0].score;
            //console.log(score);
      }

      for (var i = 0; i < canvas.height; i += 10) {
            for (var j = 0; j < canvas.width; j += 10) {
                  var input = [
                        j / 100,
                        i / 100
                  ];
                  //var hue = Math.round(evaluate(0, input)[0]) * 1000;
                  var output = evaluate(0, input);
                  if (output[0] < 0.5) {
                        var hue = 0;
                  } else {
                        var hue = 200;
                  }

                  //hue = output * 10000000000;
                  var hue = Math.tanh(output[0]) * 100;
                  //var lightness = Math.tanh(output[1]) * 100;
                  var hue = 0;
                  hue += colors[0] * output[0];
                  hue += colors[1] * output[1];
                  if (output[0] > output[1]) {
                        //hue = colors[0];
                  } else {
                        //hue = colors[1];
                  }
                  //hue = Math.tanh(hue) * 100;
                  //hue *= 10;
                  context.fillStyle = "hsla(" + hue + ", 100%, 50%, 1)";
                  context.fillRect(j, i, 10, 10);

            }
      }

      for (var i = 0; i < trainingData.length; i++) {
            var output = evaluate(0, trainingData[i].input);
            var x = trainingData[i].input[0] * 1000;
            var y = trainingData[i].input[1] * 1000;

            context.fillStyle = "hsla(0, 0%, " + trainingData[i].output[0] * 100 + "%, 1)";
            context.beginPath();
            context.arc(x, y, 5, 0, 2 * Math.PI);
            context.fill();

            var outputNumber = trainingData[i].output.length
            for (var j = 0; j < outputNumber; j++) {
                  var text = output[j].toFixed(5)
                  var textx = x + 10;
                  var texty = y - (outputNumber * 20) + (j * 20);
                  context.font = "20px Roboto";
                  context.fillText(text, textx, texty);
            }
      }
      console.log(neuralNetworks[0].score);
}

var interval = window.setInterval(evolve, 10);

function round(number, digits) {
      return Math.round(number * (10 ** digits)) / (10 ** digits);
}