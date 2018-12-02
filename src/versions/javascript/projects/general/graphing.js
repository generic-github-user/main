// Based on https://www.chartjs.org/samples/latest/charts/scatter/basic.html

window.randomScalingFactor = function() {
      return cs.random(-100, 100);
};

var color = Chart.helpers.color;
var chart_data = {
      datasets: [{
                  label: "Individual Loss",
                  borderColor: window.chartColors.red,
                  backgroundColor: color(window.chartColors.red).alpha(0.2).rgbString(),
                  data: []
            },
            {
                  label: "Best Network",
                  borderColor: window.chartColors.blue,
                  backgroundColor: color(window.chartColors.blue).alpha(0.2).rgbString(),
                  data: []
            },
            {
                  label: "Average",
                  borderColor: window.chartColors.green,
                  backgroundColor: color(window.chartColors.green).alpha(0.2).rgbString(),
                  data: []
            }
      ]
};

window.onload = function() {
      var ctx = document.getElementById("canvas").getContext("2d");
      chart = Chart.Scatter(ctx, {
            data: chart_data,
            options: {
                  title: {
                        display: true,
                        text: "Network Loss"
                  }
            }
      });
};