// network_evaluation.js

// Initialize variables
var start, end, average, inputs, outputs;
// List of time each test took
var times = [];
// Create network to use for testing
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
// Update settings for network evaluation
var update_settings = {
      "iterations": 5,
      "limit": {
            "min": -10e3,
            "max": 10e3
      }
};

// Run 100 speed tests
for (var i = 0; i < 100; i++) {
      inputs = [];
      for (var j = 0; j < 20; j++) {
            inputs.push(cs.random());
      }

      // Reset values of nodes in network
      network.reset();
      // Start timer
      start = performance.now();
      // Evaluate network to find outputs given input data
      outputs = network.evaluate({
            "input": inputs,
            "update": update_settings
      });
      // Stop timer
      end = performance.now();
      // Calculate elapsed time during test and add to list of times
      times.push(end - start);
}
// Find average of test times
average = cs.average(times);

// Log information about benchmark tests
console.log("Tests took average of " + average + " milliseconds each.", times);