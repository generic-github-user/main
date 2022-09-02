function startGame(){
	
	canvas = document.getElementById("canvas1");
	ctx = canvas.getContext("2d");
	ctx.canvas.width  = window.innerWidth - 25;
	ctx.canvas.height = window.innerHeight - 25;

	playerY = canvas.height/2;
	playerMotionY = 0;
	obstacles = {
		x:[],
		y:[]
	};
	for(i=0;i<10;i++){
		obstacles.x.push(canvas.width + Math.random()*canvas.width);
		obstacles.y.push(Math.random()*canvas.height);
	}
	score = 0;
	gameSpeed = 1;
	gameOver = false;
	
}

function draw(){
		
	ctx.fillStyle = "rgba(255,255,255,1)";
	ctx.fillRect(0,0,canvas.width,canvas.height);
	ctx.fillStyle = "rgba(0,0,0,1)";
	ctx.arc(250,playerY,25,0,2*Math.PI);
	ctx.fill();
	//Fill obstacles
	ctx.fillStyle = "rgba(200,200,200,1)";
	for(i=0;i<obstacles.x.length;i++){
		ctx.fillRect(obstacles.x[i],obstacles.y[i],100,100);
	}
	ctx.font="30px Verdana";
	ctx.fillText("Score: " + Math.round(score),10,30);
		
}
		
function calculatePositions(){

	if(playerMotionY < -0.5){
		playerMotionY = -1;
	}
	else if(playerMotionY > 0.5){
		playerMotionY = 1;
	}
	else{
		playerMotionY = 0;
	}
	for(i=0;i<obstacles.x.length;i++){
		obstacles.x[i] -= gameSpeed;
		if(obstacles.x[i] < -100){
			obstacles.x[i] = canvas.width + Math.random()*canvas.width;
			obstacles.y[i] = Math.random()*canvas.height;
		}
		if(250-obstacles.x[i]<100 && 250>obstacles.x[i] && playerY-obstacles.y[i]<100 && playerY>obstacles.y[i]){
			gameOver = true;
		}
	}
	gameSpeed += 0.001;
	score += gameSpeed/100;
	
	playerY += playerMotionY;
	if(playerY < 25){
		playerY = 25;
	}
	else if(playerY > canvas.height-25){
		playerY = canvas.height-25;
	}
	
}

function fullStep(){
	draw();
	calculatePositions();
}