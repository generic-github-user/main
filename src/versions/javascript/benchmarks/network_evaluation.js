// network_evaluation.js

var start, end, average, inputs, outputs;
var times = [];
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
var update_settings = {
      "iterations": 10,
      "limit": {
            "min": -10e3,
            "max": 10e3
      }
};

for (var i = 0; i < 100; i++) {
      inputs = [];
      for (var j = 0; j < 20; j++) {
            inputs.push(cs.random());
      }

      network.reset();
      start = performance.now();
      outputs = network.evaluate({
            "input": inputs,
            "update": update_settings
      })
      end = performance.now();
      times.push(end - start);
}
average = cs.average(times);

console.log("Tests took average of " + average + " milliseconds each.", times);