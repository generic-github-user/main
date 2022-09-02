inputCanvas = document.getElementById("inputCanvas");
inputCtx = inputCanvas.getContext("2d");

displayCanvas1 = document.getElementById("displayCanvas1");
displayCtx1 = displayCanvas1.getContext("2d");

displayCanvas2 = document.getElementById("displayCanvas2");
displayCtx2 = displayCanvas2.getContext("2d");

outputCanvas = document.getElementById("outputCanvas");
outputCtx = outputCanvas.getContext("2d");

//Incorrect training method for GANs?
//GAN and standard variations
//Function library

//Define variables
var trainingData = [];
var mouse = "up";
var brushSize = 25;
const canvasWidth = inputCanvas.width;
const canvasHeight = inputCanvas.height;
var resolution = prompt("Grid resolution? (~25)");
if(resolution < 5 || resolution == "" || resolution == undefined){
	resolution = 27;
}

clear();
refreshDisplay();
exportCanvas();

//Pre-calculate the number of pixels in the canvas, based on the canvas size and resolution
var pixelNumber = Math.round(canvasWidth/resolution) * Math.round(canvasHeight/resolution);

//Create "generator" neural network fsd
create((pixelNumber*4),[((pixelNumber*4)/2)],(pixelNumber*4),1);
//Create "discriminator" neural network s
create((pixelNumber*4),[((pixelNumber*4)/2)],1,0.05);

function draw(event){
	var mouseX = window.event.clientX;
	var mouseY = window.event.clientY;
	
	var brush = document.getElementById("brushSize").value;
	if(brush == "" || brush == undefined){
		brushSize = 25;
	}
	else{
		brushSize = brush;
	}
	var brushType = document.getElementById("brushType").value;
	var brushShape = document.getElementById("brushShape").value;
	
	if(mouse == "down"){
		if(brushType == "brush"){
			inputCtx.fillStyle = "rgba(0,0,0,1)";
		}
		else if(brushType == "eraser"){
			inputCtx.fillStyle = "rgba(255,255,255,1)";
		}
		
		if(brushShape == "circle"){
			inputCtx.beginPath();
			inputCtx.arc(mouseX-10,mouseY-10,brushSize/2,0,2*Math.PI);
			inputCtx.fill();
		}
		else if(brushShape == "square"){
			inputCtx.fillRect(mouseX-(brushSize/2),mouseY-(brushSize/2),brushSize,brushSize);
		}
	}
	
	refreshDisplay();
	exportCanvas();
}

//If mouse is pressed, change "mouse" variable to "down"
document.body.onmousedown = function mouseDown(){
	mouse = "down";
}
//If mouse is released, change "mouse" variable to "up"
document.body.onmouseup = function mouseUp(){
	mouse = "up";
}

//Get image data from drawing canvas and display canvas layout information
function getImageData(canvas){
	var imageData = [];
	for(a=0;a<Math.round(canvasHeight/resolution);a++){
		imageData.push([]);
		for(s=0;s<Math.round(canvasWidth/resolution);s++){
			imageData[a].push([]);
			for(r=0;r<4;r++){
				imageData[a][s].push(canvas.getImageData(a*resolution,s*resolution,1,1).data[r]);
			}
		}
	}
	return imageData;
}

//Refresh display, including sampling display canvas
function refreshDisplay(){
	var pixelType = document.getElementById("pixelType").value;
	if(pixelType == "average"){
		var checkerBoardColor = 100;
	}
	var imageData = getImageData(inputCtx);
	displayCtx2.fillStyle = "rgba(255,255,255,1)";
	displayCtx2.fillRect(0,0,canvasWidth,canvasHeight);
	
	for(q=0;q<Math.round(canvasHeight/resolution);q++){
		for(w=0;w<Math.round(canvasWidth/resolution);w++){
			var color = "rgba("+imageData[q][w][0]+","+imageData[q][w][1]+","+imageData[q][w][2]+","+imageData[q][w][3]+")";
			displayCtx1.fillStyle = color;
			displayCtx1.fillRect(q*resolution,w*resolution,resolution,resolution);
			
			displayCtx2.fillStyle = color;
			displayCtx2.fillRect(q*resolution,w*resolution,resolution,resolution);
			
			if(pixelType == "sample"){
				displayCtx2.fillStyle = "rgba(255,0,0,1)";
				displayCtx2.fillRect(q*resolution,w*resolution,resolution/5,resolution/5);
			}
			
			if(pixelType == "average"){
				if(checkerBoardColor == 100){
					checkerBoardColor = 200;
				}
				else if(checkerBoardColor == 200){
					checkerBoardColor = 100;
				}
				displayCtx2.fillStyle = "rgba(0,"+checkerBoardColor+",0,0.25)";
				displayCtx2.fillRect(q*resolution,w*resolution,resolution,resolution);
			}
		}
	}
}

//Clear canvas and 
function clear(){
	inputCtx.fillStyle = "rgba(255,255,255,1)";
	inputCtx.fillRect(0,0,canvasWidth,canvasHeight);
	
	displayCtx1.fillStyle = "rgba(255,255,255,1)";
	displayCtx1.fillRect(0,0,canvasWidth,canvasHeight);
}

function addDrawing(){
	trainingData.push({data: convertCanvasData(getImageData(inputCtx)), type: 1});
}

function addGenerated(){
	trainingData.push({data: convertCanvasData(getImageData(outputCtx)), type: -1});
}

function exportCanvas(){
	var exportCanvas = document.getElementById("exportCanvas").value;
	var exportType = document.getElementById("exportType").value;
	if(exportType == "array"){
		document.getElementById("exportCanvasOutput").value = JSON.stringify(getImageData(window[exportCanvas]));
	}
	else if(exportType == "rawValues"){
		document.getElementById("exportCanvasOutput").value = convertCanvasData(getImageData(window[exportCanvas]));
	}
}

function train(){
	
	var iterationsInput = document.getElementById("iterations").value;
	var iterations;
	if(iterationsInput == "" || iterationsInput == undefined){
		iterations = 100;
	}
	else{
		iterations = iterationsInput;
	}
	
	var accuracyInput = document.getElementById("accuracy").value;
	var accuracy;
	if(accuracyInput == "" || accuracyInput == undefined){
		accuracy = 10;
	}
	else{
		accuracy = accuracyInput;
	}
	
	var generatorScore;
	var discriminatorScore;

	for(z=0;z<iterations;z++){
		//Train generator neural network
		generatorScore = 0;
		for(x=0;x<accuracy;x++){
			var output = evaluate(0,generateNoise());
			generatorScore += (evaluate(1,output)/accuracy);
		}
		assignScore(0,generatorScore);
		evolve(0,"max",1,100);
		console.log("Generator neural network score: " + neuralNetworks[0].score);
		
		//Train discriminator neural network
		discriminatorScore = 0;
		for(x=0;x<accuracy;x++){
			var trainingDataIndex = Math.floor(Math.random()*trainingData.length);
			discriminatorScore += (Math.abs((trainingData[trainingDataIndex].type) - (evaluate(1,trainingData[trainingDataIndex].data)))/accuracy);
		}
		assignScore(1,discriminatorScore);
		evolve(1,"min",1,0.01);
		console.log("Discriminator neural network score: " + neuralNetworks[1].score);
	}
	if(document.getElementById("regenerate").checked == true){
		generate();
	}

}

function convertCanvasData(data){
	var convertedData = [];
	for(i=0;i<Math.round(canvasHeight/resolution);i++){
		for(j=0;j<Math.round(canvasWidth/resolution);j++){
			for(r=0;r<4;r++){
				convertedData.push(data[i][j][r]);
			}
		}
	}
	return convertedData;
}

//Generate input noise to be processed in neural network
function generateNoise(){
	var inputNoise = [];
	for(g=0;g<(pixelNumber*4);g++){
		inputNoise.push(Math.random()*10);
	}
	return inputNoise;
}

//Generate new drawing/image with neural network
function generate(){
	outputCtx.fillStyle = "rgba(255,255,255,1)";
	outputCtx.fillRect(0,0,canvasWidth,canvasHeight);

	function getValue(number){
		return Math.round(output[(index+number)]);
	}
	output = evaluate(0,generateNoise());
	for(v=0;v<Math.round(canvasHeight/resolution);v++){
		for(b=0;b<Math.round(canvasWidth/resolution);b++){
			var index = (((v*(Math.round(canvasHeight/resolution)))+b)*4);
			var color = "rgba("+getValue(0)+","+getValue(1)+","+getValue(2)+","+(output[(index+3)]/255)+")";
			outputCtx.fillStyle = color;
			outputCtx.fillRect(v*resolution,b*resolution,resolution,resolution);
		}
	}
	
	exportCanvas();
}

generate();