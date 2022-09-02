//Tsunami 2

//Print out finished network
//Clean up long repeated equations
//Write documentation
//Fix mutations code
//Include neural net backups?
//JSON.parse(JSON.stringify
//text/tsunami
//Change variable names
//Add more console logs (loading)
//Add approximation
//-0
//Types of training

function createNeuralNetwork(inputNodesNumber,hiddenNodesNumber,outputNodesNumber){
	
	console.log("Creating neural network with given parameters.");	
	
	neuralNetwork =
	{inputNodes:[],
	transferWeights1:[],
	hiddenNodes:[],
	transferWeights2:[],
	outputNodes:[]
	};

	for(j=0;j<inputNodesNumber;j++){
		neuralNetwork.inputNodes.push(0);
	}
	
	for(j=0;j<inputNodesNumber;j++){
		neuralNetwork.transferWeights1.push([]);
		for(t=0;t<hiddenNodesNumber;t++){
			neuralNetwork.transferWeights1[j].push(0);
		}
	}
	
	for(j=0;j<hiddenNodesNumber;j++){
		neuralNetwork.hiddenNodes.push(0);
	}
	
	for(j=0;j<hiddenNodesNumber;j++){
		neuralNetwork.transferWeights2.push([]);
		for(t=0;t<outputNodesNumber;t++){
			neuralNetwork.transferWeights2[j].push(0);
		}
	}
	
	for(j=0;j<outputNodesNumber;j++){
		neuralNetwork.outputNodes.push(0);
	}
	
	neuralNetworkBackup = [];
	Object.assign(neuralNetworkBackup,neuralNetwork);
	
	console.log("Neural network created: ");
	console.log(neuralNetwork);
	
}

function evolveNeuralNetwork(scoreType,mutationsNumber,mutationSize){
	
	if(scoreType == "min"){
		if(neuralNetwork.score>neuralNetworkBackup.score){
			Object.assign(neuralNetwork,neuralNetworkBackup);
		}
	}
	else if(scoreType == "max"){
		if(neuralNetwork.score<neuralNetworkBackup.score){
			Object.assign(neuralNetwork,neuralNetworkBackup);
		}
	}
	
	Object.assign(neuralNetworkBackup,neuralNetwork);
	
	for(j=0;j<mutationsNumber;j++){
		if(Math.random()<0.5){
			neuralNetwork.transferWeights1[Math.floor(Math.random()*neuralNetwork.transferWeights1.length)][Math.floor(Math.random()*neuralNetwork.hiddenNodes.length)] += (Math.random()-0.5) * mutationSize;
		}
		else{
			neuralNetwork.transferWeights2[Math.floor(Math.random()*neuralNetwork.transferWeights2.length)][Math.floor(Math.random()*neuralNetwork.outputNodes.length)] += (Math.random()-0.5) * mutationSize;
		}
	}
	
}

function evaluateNeuralNetwork(inputs){
	
	for(i=0;i<neuralNetwork.inputNodes.length;i++){
		neuralNetwork.inputNodes[i] = inputs[i];
	}
	
	for(i=0;i<neuralNetwork.hiddenNodes.length;i++){
		neuralNetwork.hiddenNodes[i] = 0;
		for(j=0;j<neuralNetwork.inputNodes.length;j++){
			neuralNetwork.hiddenNodes[i] += neuralNetwork.inputNodes[j] * neuralNetwork.transferWeights1[j][i];	
		}
	}
	
	for(i=0;i<neuralNetwork.outputNodes.length;i++){
		neuralNetwork.outputNodes[i] = 0;
		for(j=0;j<neuralNetwork.hiddenNodes.length;j++){
			neuralNetwork.outputNodes[i] += neuralNetwork.hiddenNodes[j] * neuralNetwork.transferWeights2[j][i];
		}
	}
	
	return(neuralNetwork.outputNodes);
	
}

function assignScore(score){
	neuralNetwork.score = score;
}