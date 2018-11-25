//Tsunami 4

//Print out finished network
//Clean up long repeated equations
//Write documentation
//Fix mutations code
//Include neural net Clones?
//text/tsunami
//Add more console logs (loading)
//Add approximation
//-0
//Types of training

var neuralNetworks = [];
var neuralNetworksClone = [];

function create(inputNodesNumber,hiddenNodesNumber,outputNodesNumber){
	
	console.log("Creating neural network with given parameters.");	
	
	neuralNetworks.push({
		inputNodes:[],
		transferWeights1:[],
		hiddenNodes:[],
		transferWeights2:[],
		outputNodes:[],
		score:0
	});

	const lastIndex = neuralNetworks.length - 1;
	
	for(jj=0;jj<inputNodesNumber;jj++){
		neuralNetworks[lastIndex].inputNodes.push(0);
	}
	
	for(jj=0;jj<inputNodesNumber;jj++){
		neuralNetworks[lastIndex].transferWeights1.push([]);
		for(tt=0;tt<hiddenNodesNumber;tt++){
			neuralNetworks[lastIndex].transferWeights1[jj].push(0);
		}
	}
	
	for(jj=0;jj<hiddenNodesNumber;jj++){
		neuralNetworks[lastIndex].hiddenNodes.push(0);
	}
	
	for(jj=0;jj<hiddenNodesNumber;jj++){
		neuralNetworks[lastIndex].transferWeights2.push([]);
		for(tt=0;tt<outputNodesNumber;tt++){
			neuralNetworks[lastIndex].transferWeights2[jj].push(0);
		}
	}
	
	for(jj=0;jj<outputNodesNumber;jj++){
		neuralNetworks[lastIndex].outputNodes.push(0);
	}
	
	
	console.log("Cloning neural network...");
	
	neuralNetworksClone.push({});
	neuralNetworksClone[lastIndex] = JSON.parse(JSON.stringify(neuralNetworks[lastIndex]));
	console.log("Cloning complete.");
	console.log(neuralNetworksClone[lastIndex]);
	
	console.log("Neural network created: ");
	console.log(neuralNetworks[lastIndex]);
	
}

function evolve(index,scoreType,mutationsNumber,mutationSize){
	
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
	
	neuralNetworksClone[index] = JSON.parse(JSON.stringify(neuralNetworks[index]));
	
	for(jj=0;jj<mutationsNumber;jj++){
		if(Math.random()<0.5){
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