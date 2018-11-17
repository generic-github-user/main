// Adapted from http://www.chartjs.org/samples/latest/charts/line/basic.html

var degree = 3;

var coefficients = [];
for (var i = 0; i < degree + 1; i++) {
      coefficients.push(cs.random());
}

function f1(x) {
      var y = 0;
      for (var i = 0; i < coefficients.length; i++) {
            y += coefficients[i] * (x ** (coefficients.length - i - 1));
      }
      return y;
}

var y2 = [];
var network = new cs.network({
      "inputs": 1,
      "outputs": 1,
      "nodes": {
            "Value": {
                  "num": 3,
                  "init": [-1, 1]
            },
            "Addition": {
                  "num": 3
            },
            "Multiplication": {
                  "num": 3
            },
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
            "num": 10,
            "init": [-1, 1]
      }
});

var x = [];
var y1 = [];
for (var i = 0; i < 20; i++) {
      x.push(i - 10);
      y1.push(f1(i - 10));
}

var input_data = [];
var output_data = [];
for (var i = 0; i < x.length; i++) {
      input_data.push([x[i]]);
      output_data.push([y1[i]]);
}

var update_settings = {
      "iterations": degree,
      "limit": {
            "min": -10e3,
            "max": 10e3
      }
};

function f2(x) {
      var y = network.evaluate({
            "input": [x],
            "update": update_settings
      });
      return y[0];
}

a = 0;

function update() {
      network = network.evolve({
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
                              "limit": 10,
                              "init": [-1, 1],
                              "value": {
                                    "mutation_rate": 0.5,
                                    "mutation_size": 1,
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
                        // "Tanh": {
                        //       "add": [0, a],
                        //       "remove": [0, a],
                        //       "limit": 10
                        // },
                        // "Sine": {
                        //       "add": [0, a],
                        //       "remove": [0, a],
                        //       "limit": 10
                        // },
                        // "Cosine": {
                        //       "add": [0, a],
                        //       "remove": [0, a],
                        //       "limit": 10
                        // },
                        // "Abs": {
                        //       "add": [0, a],
                        //       "remove": [0, a],
                        //       "limit": 10
                        // }
                  },
                  "connections": {
                        "add": [0, 10],
                        "remove": [0, 10],
                        "limit": 100,
                        "init": [-1, 1],
                        "value": {
                              "mutation_rate": 0.5,
                              "mutation_size": 1,
                        }
                  }
            },
            "update": update_settings,
            "log": true,
            "return": "network"
      });

      y2 = [];
      for (var i = 0; i < 20; i++) {
            y2.push(f2(i - 10));
      }
      config.data.datasets[1].data = y2;

      chart.update();
}

var config = {
      type: "line",
      data: {
            labels: [],
            datasets: [{
                        label: "Real Data",
                        backgroundColor: window.chartColors.red,
                        borderColor: window.chartColors.red,
                        data: [],
                        fill: false,
                  },
                  {
                        label: "Generated Data",
                        backgroundColor: window.chartColors.blue,
                        borderColor: window.chartColors.blue,
                        data: [],
                        fill: false,
                  }
            ]
      },
      options: {
            responsive: true,
            title: {
                  display: true,
                  text: "Curve Fitting"
            },
            tooltips: {
                  mode: 'index',
                  intersect: false,
            },
            hover: {
                  mode: 'nearest',
                  intersect: true
            },
            scales: {
                  xAxes: [{
                        display: true,
                        scaleLabel: {
                              display: true,
                              labelString: "x"
                        }
                  }],
                  yAxes: [{
                        display: true,
                        scaleLabel: {
                              display: true,
                              labelString: "y"
                        }
                  }]
            }
      }
};

config.data.labels = x;
config.data.datasets[0].data = y1;

window.onload = function() {
      var ctx = document.getElementById("canvas").getContext('2d');
      window.chart = new Chart(ctx, config);
};

setInterval(update, 100);