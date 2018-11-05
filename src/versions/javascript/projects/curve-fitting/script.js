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
      coefficients.push(cs.random(-1, 1));
}

function f(x) {
      var y = 0;
      for (var i = 0; i < coefficients.length; i++) {
            y += coefficients[i] * (x ** (coefficients.length - i - 1));
      }
      return y;
}

var network = new cs.network({
      "inputs": 1,
      "outputs": 1,
      "nodes": {
            "Data/Value": {
                  "num": 2,
                  "init": {
                        "min": -1,
                        "max": 1
                  }
            },
            "Operation/Addition": {
                  "num": 2
            },
            "Operation/Multiplication": {
                  "num": 2
            }
      },
      "connections": 1
});
network = network.evolve({
      "iterations": 10,
      "population": 50,
      "inputs": input_data,
      "outputs": output_data,
      "mutate": {
            "mutation_rate": 0.5,
            "mutation_size": 0.1,
            "nodes": {
                  "Data/Value": {
                        "add": 0,
                        "remove": 0
                  },
                  "Operation/Addition": {
                        "add": 0,
                        "remove": 0
                  },
                  "Operation/Multiplication": {
                        "add": 0,
                        "remove": 0
                  }
            },
            "connections": {
                  "add": 0,
                  "remove": 0
            }
      },
      "update": {
            "iterations": 5,
            "limit": {
                  "min": -10e6,
                  "max": 10e6
            }
      },
      "log": true
});
var config = {
      type: "line",
      data: {
            labels: [1, 2, 3],
            datasets: [{
                  label: "Real Data",
                  backgroundColor: window.chartColors.red,
                  borderColor: window.chartColors.red,
                  data: [],
                  fill: false,
            }]
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

for (var i = 0; i < 50; i++) {
      config.data.labels.push(i - 25);
      config.data.datasets[0].data.push(f(i - 25));
}

window.onload = function() {
      var ctx = document.getElementById("canvas").getContext('2d');
      window.myLine = new Chart(ctx, config);
};