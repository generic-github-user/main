//Tsunami 3

//Print out finished network
//Clean up long repeated equations
//Write documentation
//Fix mutations code
//Include neural net Clones?
//Add genetic crossover
//Multiple layers
//Different settings
//Alter/change networks
//JSON.parse(JSON.stringify
//Add more console logs (loading)

console.log("Tsunami 3 successfully loaded.");

var neuralNetworks = [];
var neuralNetworksClone = [];

var lastItem;
var neuralNetworkScoreTemp;

function createNeuralNetwork(inputNodesNumber,hiddenNodesNumber,outputNodesNumber,startingMutationSize){
	
	console.log("Creating neural network with given parameters...");
	
	console.log("Populating neural network...");
	console.log("Creating neural network object attributes...");
	neuralNetworks.push(
	{inputNodes:[],
	transferWeights1:[],
	hiddenNodes:[],
	transferWeights2:[],
	outputNodes:[],
	score:0
	});
	neuralNetworksClone.push({});
	
	lastItem = (neuralNetworks.length - 1);

	console.log("Creating input nodes...");
	for(jj=0;jj<inputNodesNumber;jj++){
		neuralNetworks[lastItem].inputNodes.push(0);
	}
	
	console.log("Creating transfer weights set 1...");
	for(jj=0;jj<inputNodesNumber;jj++){
		neuralNetworks[lastItem].transferWeights1.push([]);
		for(tt=0;tt<hiddenNodesNumber;tt++){
			neuralNetworks[lastItem].transferWeights1[jj].push((Math.random()-0.5)*startingMutationSize);
		}
	}
	
	console.log("Creating hidden nodes set "+1+"...");
	for(jj=0;jj<hiddenNodesNumber;jj++){
		neuralNetworks[lastItem].hiddenNodes.push(0);
	}
	
	for(jj=0;jj<hiddenNodesNumber;jj++){
		neuralNetworks[lastItem].transferWeights2.push([]);
		for(tt=0;tt<outputNodesNumber;tt++){
			neuralNetworks[lastItem].transferWeights2[jj].push((Math.random()-0.5)*startingMutationSize);
		}
	}
	
	for(jj=0;jj<outputNodesNumber;jj++){
		neuralNetworks[lastItem].outputNodes.push(0);
	}
	
	console.log("Cloning neural network...");
	neuralNetworksClone[lastItem] = Object.assign({},neuralNetworks[lastItem]);
	console.log("Cloning complete.");
	
	console.log("Neural network created with given parameters: ");
	console.log(neuralNetworks);
	
}

function evolve(index,scoreType,mutationNumber,mutationSize){

	

	if(scoreType == "min"){
		if(neuralNetworks[index].score > neuralNetworksClone[index].score){
			neuralNetworkScoreTemp = neuralNetworks[index].score;
			neuralNetworks[index] = Object.assign({},neuralNetworksClone[index]);
			neuralNetworks[index].score = neuralNetworkScoreTemp;
			console.log(true);
		}
	}
	else if(scoreType == "max"){
		if(neuralNetworks[index].score < neuralNetworksClone[index].score){
			//neuralNetworkScoreTemp = neuralNetworks[index].score;
			neuralNetworks[index] = Object.assign({},neuralNetworksClone[index]);
			//neuralNetworks[index].score = neuralNetworkScoreTemp;
		}
	}
	
	neuralNetworksClone[0] = Object.assign({},neuralNetworks[0]);

	for(ii=0;ii<mutationNumber;ii++){
		if(Math.random() < 0.5){
			neuralNetworks[index].transferWeights1[Math.floor(Math.random()*neuralNetworks[index].transferWeights1.length)][Math.floor(Math.random()*neuralNetworks[index].hiddenNodes.length)] += (Math.random()-0.5) * mutationSize;
		}
		else{
			neuralNetworks[index].transferWeights2[Math.floor(Math.random()*neuralNetworks[index].transferWeights2.length)][Math.floor(Math.random()*neuralNetworks[index].outputNodes.length)] += (Math.random()-0.5) * mutationSize;
		}
	}
	
}

function evaluate(index,inputs){
	
	for(ii=0;ii<neuralNetworks[index].inputNodes.length;ii++){
		neuralNetworks[index].inputNodes[ii] = inputs[ii];
	}
	
	for(ii=0;ii<neuralNetworks[index].hiddenNodes.length;ii++){
		neuralNetworks[index].hiddenNodes[ii] = 0;
		for(jj=0;jj<neuralNetworks[index].inputNodes.length;jj++){
			neuralNetworks[index].hiddenNodes[ii] += neuralNetworks[index].inputNodes[jj] * neuralNetworks[index].transferWeights1[jj][ii];	
		}
	}
	
	for(ii=0;ii<neuralNetworks[index].outputNodes.length;ii++){
		neuralNetworks[index].outputNodes[ii] = 0;
		for(jj=0;jj<neuralNetworks[index].hiddenNodes.length;jj++){
			neuralNetworks[index].outputNodes[ii] += neuralNetworks[index].hiddenNodes[jj] * neuralNetworks[index].transferWeights2[jj][ii];	
		}
	}
	
	return(neuralNetworks[index].outputNodes);
	
}

function assignScore(index,score){
	neuralNetworks[index].score = score;
}