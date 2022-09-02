
//Hurricane, a simple feedforward neural network in JavaScript



{  //Defines variables

	var inputCount_ = 20;
	var hiddenNodesCount_ = 10;
	var stepSize_ = 10000;
	var trainingData_ = [];

	var trainingDataSetLength = inputCount_ + 1; //Length of a set of training data
	var input = []; //Creates array to store values for the input layer
	for(u=0;u<inputCount_;u++){
		input.push(0);
	}
	var synapse1 = []; //Creates array to store values for the first layer of synapses
	for(k=0;k<input.length*hiddenNodesCount_;k++){ //Adds synapses for each input
		synapse1.push(0); //Adds synapse
	}
	var hidden = []; //Creates array to store values for hidden layer
	for(j=0;j<hiddenNodesCount_;j++){
		hidden.push(0);
	}
	var synapse2 = []; //Creates array to store values for the second layer of synapses
	for(d=0;d<hiddenNodesCount_;d++){
		synapse2.push(0);
	}
	var output = [0]; //Creates array to store output
	var randSynapse = Math.floor(Math.random()*synapse1.length); //Picks a random synapse from synapse layer 1 to mutate
	var trainingDataSet = Math.floor(Math.random()*(trainingData_.length/trainingDataSetLength)); //Picks a random set of training data to use for synapse layer 1
	var oldDifference = 0; //Error of previous mutation
	var newDifference = 0; //Error of current mutation
	var randW = Math.floor(Math.random()*2); //Determines whether to mutate layer 1 or layer 2 of synapses
	var randMutation = (Math.random()/10000)*stepSize_ - (Math.random()/10000)*stepSize_;
	var done = 0;

}

function runNeuralNet(){

		for(d=0;d<hidden.length;d++){
			hidden[d] = 0;
		}
		for(j=0;j<input.length;j++){
			for(w=0;w<hidden.length;w++){
				hidden[w] = hidden[w] + input[j] * synapse1[j*hiddenNodesCount_+w];
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



function train(inputCount,hiddenNodesCount,stepSize,accuracy,trainingData){ //Trains neural network

	inputCount_ = inputCount;
	hiddenNodesCount_ = hiddenNodesCount;
	stepSize_ = stepSize;
	trainingData_ = trainingData;

	trainingDataSetLength = inputCount_ + 1; //Length of a set of training data
	input = []; //Creates array to store values for the input layer
	for(u=0;u<inputCount_;u++){
		input.push(0);
	}
	synapse1 = []; //Creates array to store values for the first layer of synapses
	for(k=0;k<input.length*hiddenNodesCount_;k++){ //Adds synapses for each input
		synapse1.push(0); //Adds synapse
	}
	hidden = []; //Creates array to store values for hidden layer
	for(j=0;j<hiddenNodesCount_;j++){
		hidden.push(0);
	}
	synapse2 = []; //Creates array to store values for the second layer of synapses
	for(d=0;d<hiddenNodesCount_;d++){
		synapse2.push(0);
	}
	output = [0]; //Creates array to store output
	randSynapse = Math.floor(Math.random()*synapse1.length); //Picks a random synapse from synapse layer 1 to mutate
	trainingDataSet = Math.floor(Math.random()*(trainingData_.length/trainingDataSetLength)); //Picks a random set of training data to use for synapse layer 1
	oldDifference = 0; //Error of previous mutation
	newDifference = 0; //Error of current mutation
	randW = Math.floor(Math.random()*2); //Determines whether to mutate layer 1 or layer 2 of synapses
	randMutation = (Math.random()/10000)*stepSize_ - (Math.random()/10000)*stepSize_;
	done = 0;


	do{ //Mutates and tests synapses

		randW = Math.floor(Math.random()*2); //Determines whether to mutate layer 1 or layer 2 of synapses

		if(randW == 0){ //Mutates synapse layer 1

			randSynapse = Math.floor(Math.random()*synapse1.length); //Picks random synapse from layer 1 of synapses to mutate

			oldDifference = 0;
			trainingDataSet = 0; //Picks random set of training data to use in training
			for(qv=0;qv<(trainingData_.length/trainingDataSetLength);qv++){
				for(g=0;g<input.length;g++){
					input[g] = trainingData_[(trainingDataSet*trainingDataSetLength)+g];
				}
				runNeuralNet();
				oldDifference += Math.abs(output[0] - trainingData_[(trainingDataSet*trainingDataSetLength)+input.length]);
				trainingDataSet++;

			}


			randMutation = (Math.random()/10000)*stepSize_ - (Math.random()/10000)*stepSize_;
			synapse1[randSynapse] += randMutation;


			newDifference = 0;
			trainingDataSet = 0; //Picks random set of training data to use in training
				for(qw=0;qw<(trainingData_.length/trainingDataSetLength);qw++){
					for(g=0;g<input.length;g++){
						input[g] = trainingData_[(trainingDataSet*trainingDataSetLength)+g];
					}
					runNeuralNet();
					newDifference += Math.abs(output[0] - trainingData_[(trainingDataSet*trainingDataSetLength)+input.length]);
					trainingDataSet++;

				}

			if(newDifference > oldDifference){
				synapse1[randSynapse] -= 2*randMutation;
			}
			if(newDifference / (trainingData_.length/trainingDataSetLength) < accuracy){
				done = 1;
			}

		}

		if(randW == 1){ //Mutates synapse layer 2

			randSynapse = Math.floor(Math.random()*synapse2.length); //Picks random synapse from layer 1 of synapses to mutate

			oldDifference = 0;
			trainingDataSet = 0; //Picks random set of training data to use in training
			for(qv=0;qv<(trainingData_.length/trainingDataSetLength);qv++){
				for(g=0;g<input.length;g++){
					input[g] = trainingData_[(trainingDataSet*trainingDataSetLength)+g];
				}
				runNeuralNet();
				oldDifference += Math.abs(output[0] - trainingData_[(trainingDataSet*trainingDataSetLength)+input.length]);
				trainingDataSet++;

			}


			randMutation = (Math.random()/10000)*stepSize_ - (Math.random()/10000)*stepSize_;
			synapse2[randSynapse] += randMutation;


			newDifference = 0;
			trainingDataSet = 0; //Picks random set of training data to use in training
				for(qw=0;qw<(trainingData_.length/trainingDataSetLength);qw++){
					for(g=0;g<input.length;g++){
						input[g] = trainingData_[(trainingDataSet*trainingDataSetLength)+g];
					}
					runNeuralNet();
					newDifference += Math.abs(output[0] - trainingData_[(trainingDataSet*trainingDataSetLength)+input.length]);
					trainingDataSet++;

				}

			if(newDifference > oldDifference){
				synapse2[randSynapse] -= 2*randMutation;
			}
			if(newDifference / (trainingData_.length/trainingDataSetLength) < accuracy){
				done = 1;
			}

		}


	}while(done == 0)

}

function run(inputValues){ //Activates neural network use

	input = [];
	for(i=0;i<inputValues.length;i++){ //Fills array with a "0" for every input
		input.push(inputValues[i]);
	}
	runNeuralNet();
	logData();
	return(output[0]); //Displays output

}
