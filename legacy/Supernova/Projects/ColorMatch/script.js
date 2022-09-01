var color = [0,0,0];
var trainingData = [[[255,255,255],[1,1,1]],[[132,179,255],[0,48,127]],[[173,0,0],[1,1,1]],[[191,229,255],[0,12,66]],[[0,35,0],[45,135,45]]];
var score = 0;

create([3,5,5,3]);
for(p=0;p<1000;p++){
	train.evolve.mutate(0,10,10,1);
	for(i=0;i<population.length;i++){
		score = 0;
		for(j=0;j<trainingData.length;j++){
			var output = train.evolve.evaluate(i,trainingData[j][0]);
			for(r=0;r<3;r++){
				score += Math.abs(output[r]-trainingData[j][1][r])/trainingData.length/3;
			}
		}
		train.evolve.assignScore(i,score);
	}
	train.evolve.iterate(0,"min",10);
	console.log(score);
}
//while(neuralNetworks[0].score > 0.01)
	
function update(){
	var input = JSON.parse(document.getElementById("colorInput").value);
	var output = "rgba("+Math.abs(Math.round(evaluate(0,input)[0]))+", "+Math.abs(Math.round(evaluate(0,input)[1]))+", "+Math.abs(Math.round(evaluate(0,input)[2]))+", 1)";
	
	document.getElementById("colorDisplay").style.backgroundColor = output;
	document.getElementById("colorOutput").innerHTML = output;
}