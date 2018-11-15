// Adapted from http://www.chartjs.org/samples/latest/charts/line/basic.html

var config = {
      type: "line",
      data: {
            labels: [],
            datasets: [{
                  label: "Data",
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
                  text: "Combined Benchmark"
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

window.onload = function() {
      var ctx = document.getElementById("canvas").getContext('2d');
      window.chart = new Chart(ctx, config);
};