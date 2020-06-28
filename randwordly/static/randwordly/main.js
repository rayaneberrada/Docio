const answers = document.getElementsByTagName("button");
const xhttp = new XMLHttpRequest(); 
const arrows = document.getElementsByClassName("arrow");


// manage fav animation and request
const fav = document.getElementsByClassName("fav")[0];
console.log(fav)
const add_to_liste = function (self) {
	let form_data = new FormData();
	form_data.append('word_id', document.getElementsByClassName("word")[0].id);

	liste_options = document.getElementsByTagName('select')[0]
	for(let option in liste_options){
		if (liste_options[option].selected == true) {
			form_data.append("listes", liste_options[option].value);
			xhttp.open("POST", "http://127.0.0.1:8000/add_favorite", true);
			xhttp.send(form_data);
			break;	
		}
	}
}
if (typeof fav !== 'undefined'){
	fav.addEventListener('click', add_to_liste)
}
// manage moving backward and forward on answers
const random_definition = function (self) {
	xhttp.open("POST", "http://127.0.0.1:8000/", true);
	xhttp.send();

	xhttp.onreadystatechange = function() {
  		if (this.readyState == 4 && this.status == 200) {
    		const response = JSON.parse(xhttp.responseText);
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
	}
};

const update_def = (response) => {
	document.getElementsByClassName("word")[0].innerHTML = response["word"];
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
		"word": document.getElementsByClassName("word")[0].innerHTML,
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

