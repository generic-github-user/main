main = document.getElementById("mainGraph");
mainCtx = main.getContext("2d");
//main.canvas.width = window.innerWidth;
//main.canvas.height = window.innerHeight;

loss = document.getElementById("lossGraph");
lossCtx = loss.getContext("2d");

var mainConfig = {
	type: "line",
	data: {
		labels: [],
		datasets: [
			{
				label: "Actual Value",
				backgroundColor: "rgba(200,100,100,1)",
				borderColor: "rgba(200,50,50,1)",
				data: [],
				fill: false,
			},
			{
				label: "Calculated Value",
				backgroundColor: "rgba(100,100,200,1)",
				borderColor: "rgba(50,50,200,1)",
				data: [],
				fill: false,
			}
		]
	},
	options: {
		responsive: true,
		title: {
			display: true,
			text: "Neural Network Data Projection"
		},
		tooltips: {
			mode: "index",
			intersect: false,
		},
		hover: {
			mode: "nearest",
			intersect: true
		},
		scales: {
			xAxes: [{
				display: true,
				scaleLabel: {
					display: true,
					labelString: "X Value",
				},
				ticks: {
					autoSkip: true,
					maxTicksLimit: 10
				}
			}],
			yAxes: [{
				display: true,
				scaleLabel: {
					display: true,
					labelString: "Y Value"
				}
			}]
		},
		elements: {
			point: {
				radius: 0
			}
		}
	}
};

var lossConfig = {
	type: "line",
	data: {
		labels: [],
		datasets: [
			{
				label: "Loss (Error)",
				backgroundColor: "rgba(100,200,100,1)",
				borderColor: "rgba(50,200,50,1)",
				data: [],
				fill: false,
			}
		]
	},
	options: {
		responsive: true,
		title: {
			display: true,
			text: "Neural Network Loss"
		},
		tooltips: {
			mode: "index",
			intersect: false,
		},
		hover: {
			mode: "nearest",
			intersect: true
		},
		scales: {
			xAxes: [{
				display: true,
				scaleLabel: {
					display: true,
					labelString: "Iteration",
				},
				ticks: {
					autoSkip: true,
					maxTicksLimit: 11
				}
			}],
			yAxes: [{
				display: true,
				scaleLabel: {
					display: true,
					labelString: "Loss",
				},
				ticks: {
					beginAtZero: true
				}
			}]
		},
		elements: {
			point: {
				radius: 0
			}
		}
	}
};

window.onload = function() {
	window.mainGraph = new Chart(main, mainConfig);
	window.lossGraph = new Chart(lossCtx, lossConfig);
};

var data = {
	"year":[1881,1882,1883,1884,1885,1886,1887,1888,1889,1890,1891,1892,1893,1894,1895,1896,1897,1898,1899,1900,1901,1902,1903,1904,1905,1906,1907,1908,1909,1910,1911,1912,1913,1914,1915,1916,1917,1918,1919,1920,1921,1922,1923,1924,1925,1926,1927,1928,1929,1930,1931,1932,1933,1934,1935,1936,1937,1938,1939,1940,1941,1942,1943,1944,1945,1946,1947,1948,1949,1950,1951,1952,1953,1954,1955,1956,1957,1958,1959,1960,1961,1962,1963,1964,1965,1966,1967,1968,1969,1970,1971,1972,1973,1974,1975,1976,1977,1978,1979,1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017],
	"temperature":[-0.1,-0.1,-0.19,-0.28,-0.31,-0.32,-0.35,-0.18,-0.11,-0.37,-0.24,-0.27,-0.32,-0.32,-0.22,-0.11,-0.12,-0.28,-0.18,-0.09,-0.15,-0.3,-0.39,-0.49,-0.28,-0.23,-0.4,-0.44,-0.48,-0.44,-0.43,-0.36,-0.35,-0.16,-0.12,-0.33,-0.43,-0.28,-0.27,-0.25,-0.17,-0.27,-0.24,-0.25,-0.21,-0.09,-0.2,-0.19,-0.35,-0.15,-0.1,-0.17,-0.3,-0.14,-0.21,-0.16,-0.04,-0.03,-0.03,0.11,0.18,0.05,0.07,0.21,0.09,-0.07,-0.04,-0.11,-0.11,-0.19,-0.07,0.01,0.07,-0.15,-0.14,-0.2,0.04,0.07,0.03,-0.02,0.06,0.04,0.07,-0.2,-0.1,-0.05,-0.02,-0.07,0.07,0.03,-0.09,0.01,0.16,-0.08,-0.02,-0.11,0.17,0.06,0.16,0.27,0.33,0.13,0.31,0.16,0.12,0.18,0.33,0.41,0.28,0.44,0.41,0.22,0.24,0.31,0.44,0.33,0.47,0.62,0.4,0.4,0.54,0.62,0.61,0.53,0.67,0.62,0.64,0.52,0.63,0.7,0.57,0.61,0.64,0.73,0.86,0.99,0.9],
	"temperatureAverage":[-0.14,-0.17,-0.21,-0.24,-0.26,-0.27,-0.27,-0.27,-0.26,-0.26,-0.27,-0.27,-0.27,-0.24,-0.23,-0.21,-0.19,-0.17,-0.18,-0.21,-0.24,-0.27,-0.3,-0.32,-0.35,-0.37,-0.38,-0.4,-0.41,-0.41,-0.39,-0.35,-0.32,-0.3,-0.29,-0.28,-0.28,-0.28,-0.28,-0.26,-0.25,-0.24,-0.22,-0.21,-0.21,-0.2,-0.2,-0.19,-0.18,-0.19,-0.19,-0.18,-0.18,-0.17,-0.15,-0.12,-0.08,-0.03,0.01,0.05,0.08,0.09,0.09,0.07,0.03,0,-0.04,-0.07,-0.09,-0.08,-0.08,-0.08,-0.08,-0.07,-0.06,-0.05,-0.04,-0.01,0.02,0.03,0.02,0,-0.02,-0.03,-0.04,-0.05,-0.04,-0.03,-0.01,0,0,0,-0.01,0,0.01,0.03,0.07,0.12,0.16,0.19,0.21,0.22,0.21,0.21,0.23,0.25,0.28,0.31,0.34,0.34,0.33,0.33,0.33,0.34,0.37,0.4,0.43,0.45,0.48,0.5,0.52,0.55,0.58,0.6,0.61,0.61,0.61,0.62,0.62,0.62,0.63,0.67,0.71,0.77,0.83,0.89,0.95]
};
for (var i = 0; i < data.year.length; i++) {
	mainConfig.data.labels.push(data.year[i]);
	mainConfig.data.datasets[0].data.push(data.temperature[i]);
}
var information = {
	output: [],
	loss: []
}

function condenseData(source, index){
	return [((source[index]-source[0])/source.length*2)+0.1];
}

var loss;
var iterations = 1000;

var log = document.getElementById("log");
var dataType = document.getElementById("data-type");

function update(){

	if (dataType == "function") {
		create([1,20,20,1]);
		log.innerHTML = ("\
			<p>Running neural network training algorithm . . .</p>\
			<p>Beginning neural network training.</p>\
		");
		for(var i=0;i<iterations;i++){
			train.evolve.mutate(0,10,1,10);
			for(var j=0;j<population.length;j++){
				loss = 0;
				for(var r=0;r<data.year.length;r++){
					loss += Math.abs(train.evolve.evaluate(j, condenseData(data.year, r))[0] - data.temperature[r]) / data.year.length;
				}
				train.evolve.assignScore(j, loss);
			}
			train.evolve.iterate(0,"min",10);
			
			log.innerHTML += "<p>Iteration " + (i+1) + " complete. Neural network score: " + neuralNetworks[0].score + "</p>";
			information.loss.push(neuralNetworks[0].score);
			
			lossConfig.data.labels.push(i);
			lossConfig.data.datasets[0].data.push(information.loss[i]);
		}
		log.innerHTML += ("<p>Neural network training complete.</p>")
		log.innerHTML += ("<p>Finished neural network: " + JSON.stringify(neuralNetworks[0]) + "</p>");
		console.log(neuralNetworks[0]);
	}

	//Record additional debugging information
	for(var i = 0; i < data.year.length; i ++){
		information.output.push(evaluate(0, condenseData(data.year, i))[0]);
		mainConfig.data.datasets[1].data.push(information.output[i]);
	}
	for(var i = 0; i < 20; i ++){
		
	}

}

lossConfig.data.datasets[0].borderWidth = 2;