//Tsunami

//Print out finished network
//Clean up long repeated equations
//Write documentation
//Fix mutations code
//Include neural net backups?
//Add genetic crossover
//JSON.parse(JSON.stringify

function createNeuralNetworks(neuralNetworksNumber,inputNodesNumber,hiddenNodesNumber,outputNodesNumber,startingMutationSize){
	
	console.log("Creating neural networks with given parameters.");
	
	neuralNetworks = [];
	neuralNetworksBackup = [];
	
	for(i=0;i<neuralNetworksNumber;i++){
		neuralNetworks.push(
		{inputNodes:[],
		transferWeights1:[],
		hiddenNodes:[],
		transferWeights2:[],
		outputNodes:[],
		score:0
		});
	
		for(j=0;j<inputNodesNumber;j++){
			neuralNetworks[i].inputNodes.push(0);
		}
		
		for(j=0;j<inputNodesNumber;j++){
			neuralNetworks[i].transferWeights1.push([]);
			for(t=0;t<hiddenNodesNumber;t++){
				neuralNetworks[i].transferWeights1[j].push((Math.random()-0.5)*startingMutationSize);
			}
		}
		
		for(j=0;j<hiddenNodesNumber;j++){
			neuralNetworks[i].hiddenNodes.push(0);
		}
		
		for(j=0;j<hiddenNodesNumber;j++){
			neuralNetworks[i].transferWeights2.push([]);
			for(t=0;t<outputNodesNumber;t++){
				neuralNetworks[i].transferWeights2[j].push((Math.random()-0.5)*startingMutationSize);
			}
		}
		
		for(j=0;j<outputNodesNumber;j++){
			neuralNetworks[i].outputNodes.push(0);
		}
		
	}
	
	Object.assign(neuralNetworksBackup,neuralNetworks);
	
	console.log("Neural networks created: ");
	console.log(neuralNetworks);
	
}

function evolveNeuralNetworks(scoreType,mutationsNumber,mutationSize){
	
	if(scoreType == "min"){
		if(neuralNetworks[0].score>neuralNetworksBackup[0].score){
			neuralNetworks = JSON.parse(JSON.stringify(neuralNetworksBackup));
		}
	}
	else if(scoreType == "max"){
		if(neuralNetworks[0].score<neuralNetworksBackup[0].score){
			neuralNetworks = JSON.parse(JSON.stringify(neuralNetworksBackup));
		}
	}
	
	Object.assign(neuralNetworksBackup,neuralNetworks);
	
	var currentBestScore = 0;
	var bestScoreNeuralNetwork = neuralNetworks[0];
	
	for(i=0;i<neuralNetworks.length;i++){
		if(scoreType == "min"){
			if(neuralNetworks[i].score<currentBestScore){
				currentBestScore = neuralNetworks[i].score;
				bestScoreNeuralNetwork = neuralNetworks[i];
			}
		}
		else if(scoreType == "max"){
			if(neuralNetworks[i].score>currentBestScore){
				currentBestScore = neuralNetworks[i].score;
				bestScoreNeuralNetwork = neuralNetworks[i];
			}
		}
		else{
			console.log("Incorrect neural network scoring type.");
		}
	}
	
	for(i=0;i<neuralNetworks.length;i++){
		neuralNetworks[i] = JSON.parse(JSON.stringify(bestScoreNeuralNetwork));
	}
	
	for(i=0;i<neuralNetworks.length;i++){
		for(j=0;j<mutationsNumber;j++){
			neuralNetworks[i].transferWeights1[Math.floor(Math.random()*neuralNetworks[i].transferWeights1.length)][Math.floor(Math.random()*neuralNetworks[i].hiddenNodes.length)] += (Math.random()-0.5) * mutationSize;
		}
		for(j=0;j<mutationsNumber;j++){
			neuralNetworks[i].transferWeights2[Math.floor(Math.random()*neuralNetworks[i].transferWeights2.length)][Math.floor(Math.random()*neuralNetworks[i].outputNodes.length)] += (Math.random()-0.5) * mutationSize;
		}
	}
	
}

function evaluateNeuralNetwork(neuralNetworkLabel,inputs){
	
	for(i=0;i<neuralNetworks[neuralNetworkLabel].inputNodes.length;i++){
		neuralNetworks[neuralNetworkLabel].inputNodes[i] = inputs[i];
	}
	
	for(i=0;i<neuralNetworks[neuralNetworkLabel].hiddenNodes.length;i++){
		neuralNetworks[neuralNetworkLabel].hiddenNodes[i] = 0;
		for(j=0;j<neuralNetworks[neuralNetworkLabel].inputNodes.length;j++){
			neuralNetworks[neuralNetworkLabel].hiddenNodes[i] += neuralNetworks[neuralNetworkLabel].inputNodes[j] * neuralNetworks[neuralNetworkLabel].transferWeights1[j][i];	
		}
	}
	
	for(i=0;i<neuralNetworks[neuralNetworkLabel].outputNodes.length;i++){
		neuralNetworks[neuralNetworkLabel].outputNodes[i] = 0;
		for(j=0;j<neuralNetworks[neuralNetworkLabel].hiddenNodes.length;j++){
			neuralNetworks[neuralNetworkLabel].outputNodes[i] += neuralNetworks[neuralNetworkLabel].hiddenNodes[j] * neuralNetworks[neuralNetworkLabel].transferWeights2[j][i];	
		}
	}
	
	return(neuralNetworks[neuralNetworkLabel].outputNodes);
	
}

function assignScore(neuralNetworkLabel,score){
	neuralNetworks[neuralNetworkLabel].score = score;
}