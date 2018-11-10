// var x = [1, 2, 3, 4, 5];
var x = [
      [1],
      [2],
      [3],
      [4],
      [5]
];
var y = [
      [1],
      [4],
      [9],
      [16],
      [25]
];

var network = new cs.network({
      "inputs": 1,
      "outputs": 1,
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

var update_settings = {
      "iterations": 4,
      "limit": {
            "min": -10e3,
            "max": 10e3
      }
};

function update() {
      var generation = network.evolve({
            "iterations": 1,
            "population": 10,
            "inputs": input_data,
            "outputs": output_data,
            "mutate": {
                  "iterations": 1,
                  "mutation_rate": 0.5,
                  "mutation_size": 1,
                  "nodes": {
                        "Data/Value": {
                              "add": [0, 0],
                              "remove": [0, 0],
                              "limit": 10,
                              "init": [-1, 1]
                        },
                        "Operation/Addition": {
                              "add": [0, 0],
                              "remove": [0, 0],
                              "limit": 10
                        },
                        "Operation/Multiplication": {
                              "add": [0, 0],
                              "remove": [0, 0],
                              "limit": 10
                        }
                  },
                  "connections": {
                        "add": [0, 10],
                        "remove": [0, 10],
                        "limit": 25
                  }
            },
            "update": update_settings,
            "log": false,
            "return": "all"
      });
}

setInterval(update, 1000);