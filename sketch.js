let img_side = 28;
let canvasLength = img_side*img_side*5/7;
let size = 32;
let pen = true;
let class_name = ['cat', 'helicopter', 'octopus', 'popsicle', 'tractor']

let doodleLayer;
let model;

let predictCount = 0;

function setup() {
	createCanvas(canvasLength, canvasLength);
	doodleLayer = createGraphics(canvasLength, canvasLength);
	doodleLayer.clear();
	LoadModel();
}

function draw() {
	if(predictCount > frameRate()/10) {
		predictAns();
		predictCount = 0;
	}
	predictCount++;

	background(0);

	Draw();
	image(doodleLayer, 0, 0);

	// print(tf.memory().numTensors);
}

function predictAns() {
	img = doodleLayer.get();
	img.loadPixels();
	img.resize(img_side, img_side);

	let input_img = []
	for(let i = 0; i < img_side*img_side; i++) {
		input_img[i] = img.pixels[4*i];
	}

	input_img_tensor = tf.tensor(input_img, shape = [1, 28, 28]);
	if(model == undefined) return;
	const prediction =  model.predict(input_img_tensor);
	const prediction_val = prediction.dataSync();

	tf.dispose(input_img_tensor);
	tf.dispose(prediction);

	OutputResult(prediction_val);
}
async function LoadModel() {
		model = await tf.loadLayersModel('./tfjs_files/model.json');
}
function OutputResult(prediction_val) {
	let prediction_print = '';

	if(prediction_val.length != class_name.length) {
		prediction_print = 'error';
	} else {

			let a = [];

			for(let i = 0; i<class_name.length; i++) {
				let num = Math.trunc(prediction_val[i]*100)/100;
				a[i] = [num, i];
			}
			a.sort();
			a.reverse();
			for(let i = 0; i<class_name.length; i++) {
				prediction_print = prediction_print + class_name[a[i][1]] + `:  ${a[i][0]}<br/>`
			}

	}

	document.getElementById("model_prediction").innerHTML = prediction_print;
	return;
}
function Draw() {
	if(pen) {
		fill(255);
	} else {
		fill(0);
	}

	circle(mouseX, mouseY, size);
}
function mousePressed() {
	let strokeCol = 255;
	if (!pen) strokeCol = 0;
	doodleLayer.stroke(strokeCol);
	doodleLayer.strokeWeight(size);
	doodleLayer.point(mouseX, mouseY);
}
function mouseDragged() {
	let strokeCol = 255;
	if (!pen) strokeCol = 0;
	doodleLayer.stroke(strokeCol);
	doodleLayer.strokeWeight(size);
	doodleLayer.point(mouseX, mouseY);
}
function keyTyped() {
	if(key == 'c') {
		doodleLayer.background(0);
		doodleLayer.clear();
	}
	if(key == 'e') {
		pen = !pen;
	}
}
