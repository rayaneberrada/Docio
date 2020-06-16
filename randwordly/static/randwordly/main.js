const answers = document.getElementsByTagName("button");
const xhttp = new XMLHttpRequest(); 
const arrows = document.getElementsByClassName("arrow");


const random_definition = function (self) {
	xhttp.open("POST", "http://127.0.0.1:8000/", true);
	xhttp.send();

	xhttp.onreadystatechange = function() {
  		if (this.readyState == 4 && this.status == 200) {
    		const response = JSON.parse(xhttp.responseText)
			arrows[0].children[0].removeAttribute("hidden");
			arrows[0].children[0].addEventListener("click", arrow_def_update);
			arrows[1].children[0].hidden = true;
			previous_def = save_def_in_memory();
    		
			if (self.target.id == "True"){
				//self.target.style.backgroundColor = "rgb(101, 246, 0)";
			}
			else {
				//self.target.style.backgroundColor = "rgb(225, 0, 0)";
				const righ_answer = document.getElementBY
				confirm("La bonne réponse était: " + document.getElementById('True').textContent);
			}
			update_def(response);
  		}
	};
};

const update_def = (response) => {
	document.getElementById("word").innerHTML = response["word"];
	for (let i in answers){
		answers[i].removeAttribute("id");
		answers[i].innerHTML = response["definitions"][i]["description"];

		if (response["definitions"][i].hasOwnProperty("right_answer")){
			answers[i].id = "True";
		}
	}
}

const arrow_def_update = (event) => {
	console.log(arrows[0].children[0].hidden);
	if(arrows[0].children[0].hidden){
		previous_def = save_def_in_memory();
		arrows[1].children[0].hidden = true;
		arrows[0].children[0].removeAttribute("hidden");
		arrows[0].children[0].addEventListener("click", arrow_def_update);
		update_def(next_def);
	}
	else{
		next_def = save_def_in_memory();
		arrows[0].children[0].hidden = true;
		arrows[1].children[0].removeAttribute("hidden");
		arrows[1].children[0].addEventListener("click", arrow_def_update);
		update_def(previous_def);
	}
}

const save_def_in_memory = () => {
	def_in_memory = {
		"word": document.getElementById("word").innerHTML,
		"definitions": []
	}
	for (let i = 0; i < 4; i++){
		if (answers[i].hasAttribute("id")){
			def_in_memory["definitions"].push({"description": answers[i].innerHTML, "right_answer": "True"});
		}
		else{
			def_in_memory["definitions"].push({"description": answers[i].innerHTML});
		}
	}
	return def_in_memory
}
let previous_def = save_def_in_memory();
let next_def = null;


for (const i in answers){
	if (answers[i].tagName= "BUTTON"){
		answers[i].addEventListener("click", random_definition);
	}
}