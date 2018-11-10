// Map number in one range to another range
// https://stackoverflow.com/a/23202637
function map(num, in_min, in_max, out_min, out_max) {
      return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

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
      network = generation.network;

      var scores = [];
      for (var i = 0; i < population; i++) {
            scores.push(generation.population[i].score);
      }
      var max = Math.max(...scores);
      var min = Math.min(...scores);

      var row = $("<div>");
      for (var i = 0; i < population; i++) {
            var lightness = map(generation.population[i].score, min, max, 95, 50);
            if (isNaN(lightness)) {
                  lightness = 50;
            }
            // Create color string in hsla format
            var color = "hsla(200, 100%, " + lightness + "%, 1)";

            var cell = $("<div>");
            cell.addClass("cell");
            cell.width((100 / population) + "%");
            // Set background color of cell
            cell.css("background-color", color);

            var text = $("<p>");
            text.text(generation.population[i].score.toFixed(2));
            cell.append(text);
            row.append(cell);
      }
      $("body").append(row);
}

setInterval(update, 1000);