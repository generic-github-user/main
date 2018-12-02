// Based on https://www.chartjs.org/samples/latest/charts/scatter/basic.html

window.randomScalingFactor = function() {
      return cs.random(-100, 100);
};

var color = Chart.helpers.color;
var scatterChartData = {
      datasets: [{
            label: "Loss",
            borderColor: window.chartColors.red,
            backgroundColor: color(window.chartColors.red).alpha(0.2).rgbString(),
            data: []
      }]
};

window.onload = function() {
      var ctx = document.getElementById('canvas').getContext('2d');
      window.myScatter = Chart.Scatter(ctx, {
            data: scatterChartData,
            options: {
                  title: {
                        display: true,
                        text: 'Chart.js Scatter Chart'
                  }
            }
      });
};