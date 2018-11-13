//Supernova

//Print out finished network(s)
//Clean up long repeated equations
//Write documentation
//Fix mutations code
//Add more console logs (loading)
//Add approximation
//-0
//GAN
//Not GAN
	//Back-propagation
	//Guess-and-check
//adaptive mutations
//Targeted adjustment
//Activation functions
//Combine evaluation functions
//supernova.
//Multiple populations
//Crossover

//Create array to store neural network data

//Create object to store functions and variables
var train = {
	random:undefined,
	evolve:{
		mutate:undefined,
		iterate:undefined
	}
	
	
	
};

var neuralNetworks = [];

var neuralNetworksClone = [];

//Create a new neural network with given layer sizes
function create(nodes){
	
	//Create a new neural network object
	neuralNetworks.push({});

	//Create aray to store neural network nodes
	neuralNetworks[neuralNetworks.length-1].nodes = [];
	for(var i=0;i<nodes.length;i++){
		//Create new hidden layer
		neuralNetworks[neuralNetworks.length-1].nodes.push([]);
		for(var j=0;j<nodes[i];j++){
			//Fill hidden layer with placeholder values
			neuralNetworks[neuralNetworks.length-1].nodes[i].push(Math.random());
		}
	}
	
	//Create aray to store transfer weight layers
	neuralNetworks[neuralNetworks.length-1].weights = [];
	
	//Create transfer weights between hidden layers
	for(var i=0;i<nodes.length-1;i++){
		//Create new transfer weight layer
		neuralNetworks[neuralNetworks.length-1].weights.push([]);
		for(var j=0;j<nodes[i];j++){
			//Create new sub-aray to store weights
			neuralNetworks[neuralNetworks.length-1].weights[i].push([]);
			for(var r=0;r<nodes[i+1];r++){
				//Fill transfer weight layer with placeholder values
				neuralNetworks[neuralNetworks.length-1].weights[i][j].push(Math.random());
			}
		}
	}
	
	//Create score property for neural network
	neuralNetworks[neuralNetworks.length-1].score = 0;
	
	neuralNetworksClone.push(JSON.parse(JSON.stringify(neuralNetworks[neuralNetworks.length-1])));
	
}

//Assign given weight to all neural network weights
function assignWeights(index,value){
	//Loop through all weight layers in "weights" aray
	for(var i=0;i<neuralNetworks[index].weights.length;i++){
		for(var j=0;j<neuralNetworks[index].weights[i].length;j++){
			for(var r=0;r<neuralNetworks[index].weights[i][j].length;r++){
				//Assign value to weight
				neuralNetworks[index].weights[i][j][r] = value;
			}
		}
	}
}

//"Guess-and-check" evolution of neural network weights
train.random = function(index,scoreType,mutationsNumber,mutationSize){
	//Check neural network score against clone of neural network from previous iteration
	if(scoreType == "min"){
		if(neuralNetworks[index].score > neuralNetworksClone[index].score){
			neuralNetworks[index] = JSON.parse(JSON.stringify(neuralNetworksClone[index]));
		}
	}
	else if(scoreType == "max"){
		if(neuralNetworks[index].score < neuralNetworksClone[index].score){
			neuralNetworks[index] = JSON.parse(JSON.stringify(neuralNetworksClone[index]));
		}
	}
	
	//Clone neural network (again) before mutating; if neural network score has decreased it will already have been reverted to the previous version of the neural network
	neuralNetworksClone[index] = JSON.parse(JSON.stringify(neuralNetworks[index]));
	
	for(var i=0;i<mutationsNumber;i++){
		var layer = Math.floor(Math.random()*neuralNetworks[index].weights.length);
		var set = Math.floor(Math.random()*neuralNetworks[index].weights[layer].length);
		var weight = Math.floor(Math.random()*neuralNetworks[index].weights[layer].length);
		
		neuralNetworks[index].weights[layer][set][weight] += (Math.random()-0.5) * (mutationSize/(neuralNetworks[index].weights[layer].length*neuralNetworks[index].weights[layer][set].length));
	}
}

//Train neural networks using neuroevolution (genetic algorithm)

//Create and mutate copies of neural network
train.evolve.mutate = function(index,populationSize,mutationsNumber,mutationSize){
	population = [];
	//Create copies of neural network
	for(var i=0;i<populationSize;i++){
		population.push(JSON.parse(JSON.stringify(neuralNetworks[index])));
		//Mutate copy of neural network
		for(var j=0;j<mutationsNumber;j++){
			var layer = Math.floor(Math.random()*population[population.length-1].weights.length);
			var set = Math.floor(Math.random()*population[population.length-1].weights[layer].length);
			var weight = Math.floor(Math.random()*population[population.length-1].weights[layer][set].length);
			
			population[population.length-1].weights[layer][set][weight] += (Math.random()-0.5) * (mutationSize/(population[population.length-1].weights[layer].length*population[population.length-1].weights[layer][set].length));
		}
	}
}

//Evaluate copy of neural network
train.evolve.evaluate = function(index,input){
	//Transfer input data to input nodes
	for(var i=0;i<population[index].nodes[0].length;i++){
		population[index].nodes[0][i] = input[i];
	}
	
	//Calculate values of hidden layers
	for(var i=1;i<population[index].nodes.length;i++){
		for(var j=0;j<population[index].nodes[i].length;j++){
			//Reset values of current hidden layer
			population[index].nodes[i][j] = 0;
			for(var r=0;r<population[index].nodes[i-1].length;r++){
				//Add product of previous hidden node layer and weight to current hidden node
				population[index].nodes[i][j] += population[index].nodes[i-1][r] * population[index].weights[i-1][r][j];
			}
			if(i < population[index].nodes[i].length){
				population[index].nodes[i][j] = Math.tanh(population[index].nodes[i][j]);
			}
			if(population[index].nodes[i][j] < 0){
				//population[index].nodes[i][j] = -1;
			}
		}
	}
	
	//Return output(s)
	return(population[index].nodes[population[index].nodes.length-1]);
}

train.evolve.assignScore = function(index,score){
	population[index].score = score;
}

train.evolve.iterate = function(index,scoreType,crossoverSize){
	//Create "best score" and "best network" variables
	var bestScore = population[0].score;
	var bestNetwork = 0;
	//Loop through all copies of neural network (except the first one)
	for(var i=1;i<population.length;i++){
		if(scoreType == "min"){
			if(population[i].score < bestScore){
				bestScore = population[i].score;
				bestNetwork = i;
			}
		}
		else if(scoreType == "max"){
			if(population[i].score > bestScore){
				bestScore = population[i].score;
				bestNetwork = i;
			}
		}
	}
	
	neuralNetworks[index] = JSON.parse(JSON.stringify(population[bestNetwork]));
}

function backpropagate(index,target){
	
}

function evaluate(index,input){
	
	//Transfer input data to input nodes
	for(var i=0;i<neuralNetworks[index].nodes[0].length;i++){
		neuralNetworks[index].nodes[0][i] = input[i];
	}
	
	//Calculate values of hidden layers
	for(var i=1;i<neuralNetworks[index].nodes.length;i++){
		for(var j=0;j<neuralNetworks[index].nodes[i].length;j++){
			//Reset values of current hidden layer
			neuralNetworks[index].nodes[i][j] = 0;
			for(var r=0;r<neuralNetworks[index].nodes[i-1].length;r++){
				//Add product of previous hidden node layer and weight to current hidden node
				neuralNetworks[index].nodes[i][j] += neuralNetworks[index].nodes[i-1][r] * neuralNetworks[index].weights[i-1][r][j];
			}
			if(i < neuralNetworks[index].nodes[i].length){
				neuralNetworks[index].nodes[i][j] = Math.tanh(neuralNetworks[index].nodes[i][j]);
			}
			if(neuralNetworks[index].nodes[i][j] < 0){
				//neuralNetworks[index].nodes[i][j] = -1;
			}
		}
	}
	
	//Return output(s)
	return(neuralNetworks[index].nodes[neuralNetworks[index].nodes.length-1]);
	
}

function assignScore(index,score){
	//Assign score to neural network
	neuralNetworks[index].score = score;
}