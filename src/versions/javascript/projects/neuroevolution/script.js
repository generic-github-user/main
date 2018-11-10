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

var population = 10;

function update() {
      var generation = network.evolve({
            "iterations": 1,
            "population": population,
            "inputs": x,
            "outputs": y,
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

      var row = $("<div>");
      for (var i = 0; i < population; i++) {
            var cell = $("<div>");
            cell.addClass("cell");
            cell.width((100 / population) + "%");

            var text = $("<p>");
            text.text(generation.population[i].score);
            cell.append(text);
            row.append(cell);
      }
      $("body").append(row);
}

setInterval(update, 1000);