// Adapted from http://www.chartjs.org/samples/latest/charts/line/basic.html

var chartColors = {
      red: 'rgb(255, 99, 132)',
      orange: 'rgb(255, 159, 64)',
      yellow: 'rgb(255, 205, 86)',
      green: 'rgb(75, 192, 192)',
      blue: 'rgb(54, 162, 235)',
      purple: 'rgb(153, 102, 255)',
      grey: 'rgb(201, 203, 207)'
};

var coefficients = [];
for (var i = 0; i < 4; i++) {
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
            "Data/Value": {
                  "num": 2,
                  "init": [-1, 1]
            },
            "Operation/Addition": {
                  "num": 2
            },
            "Operation/Multiplication": {
                  "num": 2
            }
      },
      "connections": 10
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

function f2(x) {
      var y = network.evaluate({
            "input": [x],
            "update": {
                  "iterations": 4,
                  "limit": {
                        "min": -10e3,
                        "max": 10e3
                  }
            }
      });
      return y[0];
}

function update() {
      network = network.evolve({
            "iterations": 1,
            "population": 100,
            "inputs": input_data,
            "outputs": output_data,
            "mutate": {
                  "iterations": 1,
                  "mutation_rate": 0.5,
                  "mutation_size": 1,
                  "nodes": {
                        "Data/Value": {
                              "add": [0, 1],
                              "remove": [0, 1],
                              "limit": 10,
                              "init": [-1, 1]
                        },
                        "Operation/Addition": {
                              "add": [0, 1],
                              "remove": [0, 1],
                              "limit": 10
                        },
                        "Operation/Multiplication": {
                              "add": [0, 1],
                              "remove": [0, 1],
                              "limit": 10
                        }
                  },
                  "connections": {
                        "add": [0, 10],
                        "remove": [0, 10],
                        "limit": 100
                  }
            },
            "update": {
                  "iterations": 4,
                  "limit": {
                        "min": -10e6,
                        "max": 10e6
                  }
            },
            "log": true
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