
//Hurricane, a simple feedforward neural network in JavaScript



{  //Defines variables

	var inputCount = 20;
	var hiddenNodesCount = 10;
	var stepSize = 10000;
	var trainingData = [];
	
	var currentIteration = 0;
	var maxIterations = 1;

	var trainingDataSetLength = inputCount + 1; //Length of a set of training data
	var input = []; //Creates array to store values for the input layer
	for(u=0;u<inputCount;u++){
		input.push(0);
	}
	var synapse1 = []; //Creates array to store values for the first layer of synapses
	for(k=0;k<input.length*hiddenNodesCount;k++){ //Adds synapses for each input
		synapse1.push(0); //Adds synapse
	}
	var hidden = []; //Creates array to store values for hidden layer
	for(j=0;j<hiddenNodesCount;j++){
		hidden.push(0);
	}
	var synapse2 = []; //Creates array to store values for the second layer of synapses
	for(d=0;d<hiddenNodesCount;d++){
		synapse2.push(0);
	}
	var output = [0]; //Creates array to store output
	var randSynapse = Math.floor(Math.random()*synapse1.length); //Picks a random synapse from synapse layer 1 to mutate
	var trainingDataSet = Math.floor(Math.random()*(trainingData.length/trainingDataSetLength)); //Picks a random set of training data to use for synapse layer 1
	var oldDifference = 0; //Error of previous mutation
	var cost = 0; //Error of current mutation
	var randMutation = (Math.random()/10000)*stepSize - (Math.random()/10000)*stepSize;
	var done = 0;
	var outputChange = output[0];

}

function runNeuralNet(){

		for(d=0;d<hidden.length;d++){
			hidden[d] = 0;
		}
		for(j=0;j<input.length;j++){
			for(w=0;w<hidden.length;w++){
				hidden[w] = hidden[w] + input[j] * synapse1[j*hiddenNodesCount+w];
			}
		}
		output[0] = 0;
		for(e=0;e<hidden.length;e++){
			output[0] = output[0] + (hidden[e] * synapse2[e]);
		}

	}

function logData(){ //Logs neural network data for reference

	console.log("Hurricane:"); //Clears console
	console.log("");
	console.log("");

	console.log(input); //Logs input
	console.log(synapse1); //Logs synapse layer 1
	console.log(hidden); //Logs hidden layer
	console.log(synapse2); //Logs synapse layer 2
	console.log(output); //Logs output

	console.log("");
	console.log("");

	console.log("Output = " + output) //Logs output

}



function train(inputCount,hiddenNodesCount,stepSize,accuracy,maxIterations,trainingData){ //Trains neural network
	
	currentIteration = 0;

	trainingDataSetLength = inputCount + 1; //Length of a set of training data
	input = []; //Creates array to store values for the input layer
	for(u=0;u<inputCount;u++){
		input.push(0);
	}
	synapse1 = []; //Creates array to store values for the first layer of synapses
	for(k=0;k<input.length*hiddenNodesCount;k++){ //Adds synapses for each input
		synapse1.push(0); //Adds synapse
	}
	hidden = []; //Creates array to store values for hidden layer
	for(j=0;j<hiddenNodesCount;j++){
		hidden.push(0);
	}
	synapse2 = []; //Creates array to store values for the second layer of synapses
	for(d=0;d<hiddenNodesCount;d++){
		synapse2.push(0);
	}
	output = [0]; //Creates array to store output
	randSynapse = Math.floor(Math.random()*synapse1.length); //Picks a random synapse from synapse layer 1 to mutate
	trainingDataSet = Math.floor(Math.random()*(trainingData.length/trainingDataSetLength)); //Picks a random set of training data to use for synapse layer 1
	oldDifference = 0; //Error of previous mutation
	cost = 0; //Error of current mutation
	randMutation = (Math.random()/10000)*stepSize - (Math.random()/10000)*stepSize;
	done = 0;


	do{ //Mutates and tests synapses




			randSynapse = Math.floor(Math.random()*synapse1.length); //Picks random synapse from layer 1 of synapses to mutate

			oldDifference = 0;
			trainingDataSet = 0; //Picks random set of training data to use in training
			for(qv=0;qv<(trainingData.length/trainingDataSetLength);qv++){
				for(g=0;g<input.length;g++){
					input[g] = trainingData[(trainingDataSet*trainingDataSetLength)+g];
				}
				runNeuralNet();
				oldDifference += Math.abs(output[0] - trainingData[(trainingDataSet*trainingDataSetLength)+input.length]);
				trainingDataSet++;

			}


			randMutation = (Math.random()/10000)*stepSize - (Math.random()/10000)*stepSize;
			synapse1[randSynapse] += randMutation;


			cost = 0;
			trainingDataSet = 0; //Picks random set of training data to use in training
				for(qw=0;qw<(trainingData.length/trainingDataSetLength);qw++){
					for(g=0;g<input.length;g++){
						input[g] = trainingData[(trainingDataSet*trainingDataSetLength)+g];
					}
					runNeuralNet();
					cost += Math.abs(output[0] - trainingData[(trainingDataSet*trainingDataSetLength)+input.length]);
					trainingDataSet++;

				}

			if(cost > oldDifference){
				synapse1[randSynapse] -= 2*randMutation;
			}
			if(cost / (trainingData.length/trainingDataSetLength) < accuracy){
				done = 1;
			}





			randSynapse = Math.floor(Math.random()*synapse2.length); //Picks random synapse from layer 1 of synapses to mutate

			oldDifference = 0;
			trainingDataSet = 0; //Picks random set of training data to use in training
			for(qv=0;qv<(trainingData.length/trainingDataSetLength);qv++){
				for(g=0;g<input.length;g++){
					input[g] = trainingData[(trainingDataSet*trainingDataSetLength)+g];
				}
				runNeuralNet();
				oldDifference += Math.abs(output[0] - trainingData[(trainingDataSet*trainingDataSetLength)+input.length]);
				trainingDataSet++;

			}



			cost = 0;
			trainingDataSet = 0; //Picks random set of training data to use in training
				for(qw=0;qw<(trainingData.length/trainingDataSetLength);qw++){
					for(g=0;g<input.length;g++){
						input[g] = trainingData[(trainingDataSet*trainingDataSetLength)+g];
					}
					runNeuralNet();
					cost += Math.abs(output[0] - trainingData[(trainingDataSet*trainingDataSetLength)+input.length]);
					trainingDataSet++;

				}


				synapse2[randSynapse] += stepSize;
				runNeuralNet();
				outputChange = output[0];
				synapse2[randSynapse] -= stepSize;
				runNeuralNet();
				outputChange -= output[0];

				if(outputChange > 0){
					synapse2[randSynapse] -= stepSize;
				}
				else{
					synapse2[randSynapse] += stepSize;
				}


			if(cost / (trainingData.length/trainingDataSetLength) < accuracy || currentIteration > maxIterations){
				done = 1;
			}

			currentIteration++;

	}while(done == 0)

}

function run(inputValues){ //Activates neural network use

	input = [];
	for(i=0;i<inputValues.length;i++){ //Fills array with a "0" for every input
		input.push(inputValues[i]);
	}
	runNeuralNet();
	logData();
	return(output[0]);

}
