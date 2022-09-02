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
      "nodes": {
            "Input": {
                  "num": 1
            },
            "Output": {
                  "num": 1
            },
            "Value": {
                  "num": 3,
                  "init": [-1, 1]
            },
            "Addition": {
                  "num": 3
            },
            "Multiplication": {
                  "num": 3
            }
      },
      "connections": {
            "num": 0,
            "init": [-1, 1]
      }
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
                  "nodes": {
                        "Value": {
                              "add": [0, 0],
                              "remove": [0, 0],
                              "limit": 10,
                              "init": [-1, 1],
                              "value": {
                                    "mutation_rate": 0.5,
                                    "mutation_size": 1,
                              }
                        },
                        "Addition": {
                              "add": [0, 0],
                              "remove": [0, 0],
                              "limit": 10
                        },
                        "Multiplication": {
                              "add": [0, 0],
                              "remove": [0, 0],
                              "limit": 10
                        }
                  },
                  "connections": {
                        "add": [0, 10],
                        "remove": [0, 10],
                        "limit": 25,
                        "init": [-1, 1],
                        "value": {
                              "mutation_rate": 0.5,
                              "mutation_size": 1,
                        }
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
            var lightness = cs.map(generation.population[i].score, min, max, 95, 50);
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
            // text.html("Network " + (i + 1) + "<br />" +
            // generation.population[i].score.toFixed(2) + "<br />" +
            // generation.population[i].nodes.length + " nodes" + "<br />" +
            // generation.population[i].connections.length + " connections");
            cell.append(text);
            row.append(cell);
      }
      $("body").append(row);
      window.scrollBy({
            top: 1000,
            left: 0,
            behavior: "smooth"
      });
}

setInterval(update, 1000);