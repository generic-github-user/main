//

//Check score assignment
//Add "disqualification"
//Add generation reset
//Disappearing bots
//Add trails
//"Canvas./2" shortening

canvas = document.getElementById("canvas");
ctx = canvas.getContext("2d");
ctx.canvas.width  = window.innerWidth - 25;
ctx.canvas.height = window.innerHeight - 25;

var botsNumber = 100;
var foodNumber = 1;
var generationLength = 1000;
var delay = 10;

var generation = 0;
var time = 0;
var averageScore = 0;

var data = {
	bots:[],
	food:[]
}
for(q=0;q<botsNumber;q++){
	data.bots.push({location:{x:Math.round(canvas.width/2),y:Math.round(canvas.height/2)},velocity:{x:0,y:0},score:0});
}
for(q=0;q<foodNumber;q++){
	data.food.push({location:{x:(Math.floor(Math.random()*canvas.width)),y:(Math.floor(Math.random()*canvas.height))}});
}

//Create neural networks
create([2+(foodNumber*2),(2+(foodNumber*2))*2,2]);
var inputs = [];
for(q=0;q<botsNumber;q++){
	inputs.push([]);
}

//Handles display of simulation
function draw(){
	ctx.canvas.width  = window.innerWidth - 25;
	ctx.canvas.height = window.innerHeight - 25;
	
	ctx.font = "25px Calibri";
	ctx.fillText("Simulation information:",10,20);
	ctx.fillText("Generation: " + generation,10,60);
	ctx.fillText("Time: " + time,10,90);
	ctx.fillText("Average score: " + averageScore,10,120);
	
	for(q=0;q<botsNumber;q++){
		ctx.fillStyle = "rgba(0,0,0,1)";
		ctx.fillRect(data.bots[q].location.x,data.bots[q].location.y,10,10);
	}
	for(q=0;q<data.food.length;q++){
		ctx.fillStyle = "rgba(0,200,0,1)";
		ctx.fillRect(data.food[q].location.x,data.food[q].location.y,10,10);
	}
}

function calculate(){
	averageScore = 0;
	for(q=0;q<botsNumber;q++){
		inputs[q] = [];
		inputs[q].push(data.bots[q].location.x,data.bots[q].location.y);
		for(w=0;w<data.food.length;w++){
			inputs[q].push(data.food[w].location.x,data.food[w].location.y);
		}
		
		data.bots[q].velocity.x = train.evolve.evaluate(q,inputs[q])[0];
		data.bots[q].velocity.y = train.evolve.evaluate(q,inputs[q])[1];

		data.bots[q].location.x += data.bots[q].velocity.x;
		data.bots[q].location.y += data.bots[q].velocity.y;
		
		for(w=0;w<data.food.length;w++){
			if(Math.abs(data.bots[q].location.x-data.food[w].location.x)<10&&Math.abs(data.bots[q].location.y-data.food[w].location.y)<10){
				data.bots[q].score += 100;
				data.food.splice(w,1);
			}
		}	
		
		if(data.bots[q].location.x < 0 || data.bots[q].location.x > canvas.width || data.bots[q].location.y < 0 || data.bots[q].location.y > canvas.height){
			data.bots[q].location.x = Math.round(canvas.width/2);
			data.bots[q].location.y = Math.round(canvas.height/2);
			data.bots[q].score -= 100;
		}
		
		averageScore+=data.bots[q].score/botsNumber;
	}
		
	time++;
	if(time > generationLength){
		//Increase generation by 1
		generation++;
		//Reset time
		time = 0;
		
		for(q=0;q<botsNumber;q++){
			assignScore(q,data.bots[q].score);
		}
		train.evolve.mutate(0,"max",1,1);
		console.log("Generation " + generation + " complete. Average score: " + averageScore);
		
		data = {
			bots:[],
			food:[]
		}
		for(q=0;q<botsNumber;q++){
			data.bots.push({location:{x:Math.round(canvas.width/2),y:Math.round(canvas.height/2)},velocity:{x:0,y:0},score:0});
		}
		for(q=0;q<foodNumber;q++){
			data.food.push({location:{x:(Math.floor(Math.random()*canvas.width)),y:(Math.floor(Math.random()*canvas.height))}});
		}
	}
}

function update(){
	draw();
	calculate();
}

var intervalID = window.setInterval(update,delay);