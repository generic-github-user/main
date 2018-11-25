//Tsunami V

//Print out finished network(s)
//Clean up long repeated equations
//Write documentation
//Fix mutations code
//Add more console logs (loading)
//Add approximation
//-0
//Types of training
//GAN
//Not GAN
	//Back-propagation

var neuralNetworks = [];
var neuralNetworksClone = [];

function create(inputLayerSize,hiddenLayersSizes,outputLayerSize,startingWeightSize){
	
	neuralNetworks.push({});
	var index = neuralNetworks.length - 1;
	
	//Create input nodes
	neuralNetworks[index].inputNodes = [];
	for(ii=0;ii<inputLayerSize;ii++){
		neuralNetworks[index].inputNodes.push(0);
	}
		
	//Create output nodes
	neuralNetworks[index].outputNodes = [];
	for(ii=0;ii<outputLayerSize;ii++){
		neuralNetworks[index].outputNodes.push(0);
	}
	
	//Create hidden layers and transfer weight layers
	neuralNetworks[index].hiddenLayers = [];
	
	neuralNetworks[index].hiddenLayers.push([]);
	for(ii=0;ii<neuralNetworks[index].inputNodes.length;ii++){
		neuralNetworks[index].hiddenLayers[0].push([]);
		for(jj=0;jj<hiddenLayersSizes[0];jj++){
			neuralNetworks[index].hiddenLayers[0][ii].push((Math.random()-0.5)*startingWeightSize);
		}
	}
	for(ii=0;ii<hiddenLayersSizes.length;ii++){
		
		var layer;
		
		neuralNetworks[index].hiddenLayers.push([]);
		layer = neuralNetworks[index].hiddenLayers.length - 1;
		for(jj=0;jj<hiddenLayersSizes[ii];jj++){
			neuralNetworks[index].hiddenLayers[layer].push(0);
		}
		
		neuralNetworks[index].hiddenLayers.push([]);
		layer = neuralNetworks[0].hiddenLayers.length - 1;
		for(jj=0;jj<hiddenLayersSizes[layer - 2];jj++){
			neuralNetworks[index].hiddenLayers[layer].push([]);
			for(tt=0;tt<neuralNetworks[index].outputNodes.length;tt++){
				neuralNetworks[index].hiddenLayers[layer][jj].push((Math.random()-0.5)*startingWeightSize);
			}
		}
		
	}
	
	neuralNetworksClone.push(JSON.parse(JSON.stringify(neuralNetworks[index])));

}

function evolve(index,scoreType,mutationsNumber,mutationSize){

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
	
	for(ii=0;ii<mutationsNumber;ii++){
		if(Math.random() < 0.5){
			neuralNetworks[index].hiddenLayers[0][Math.floor(Math.random()*neuralNetworks[index].hiddenLayers[0].length)][Math.floor(Math.random()*neuralNetworks[index].hiddenLayers[1].length)] += (Math.random()-0.5) * (mutationSize/(neuralNetworks[index].hiddenLayers[0][0].length));
		}
		else{
			neuralNetworks[index].hiddenLayers[2][Math.floor(Math.random()*neuralNetworks[index].hiddenLayers[2].length)][Math.floor(Math.random()*neuralNetworks[index].outputNodes.length)] += (Math.random()-0.5) * (mutationSize/neuralNetworks[index].hiddenLayers[2].length);
		}
	}
	
}

function evaluate(index,inputs){
	
	//Transfer input data to input nodes
	for(ii=0;ii<neuralNetworks[index].inputNodes.length;ii++){
		neuralNetworks[index].inputNodes[ii] = inputs[ii];
	}
	
	for(ii=0;ii<neuralNetworks[index].hiddenLayers[1].length;ii++){
		neuralNetworks[index].hiddenLayers[1][ii] = 0;
		for(jj=0;jj<neuralNetworks[index].inputNodes.length;jj++){
			neuralNetworks[index].hiddenLayers[1][ii] += neuralNetworks[index].inputNodes[jj] * neuralNetworks[index].hiddenLayers[0][jj][ii];	
		}
	}
	
	for(ii=0;ii<neuralNetworks[index].outputNodes.length;ii++){
		neuralNetworks[index].outputNodes[ii] = 0;
		for(jj=0;jj<neuralNetworks[index].hiddenLayers[1].length;jj++){
			neuralNetworks[index].outputNodes[ii] += neuralNetworks[index].hiddenLayers[1][jj] * neuralNetworks[index].hiddenLayers[2][jj][ii];
		}
	}
	
	//Return output(s)
	return(neuralNetworks[index].outputNodes);
	
}

function assignScore(index,score){
	//Assign score to neural network
	neuralNetworks[index].score = score;
}