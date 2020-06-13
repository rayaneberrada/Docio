const answers = document.getElementsByTagName("button")
document.getElementById("demo").innerHTML = "My First JavaScript";
const xhttp = new XMLHttpRequest(); 

const random_definition = function (self) {
	xhttp.open("POST", "http://127.0.0.1:8000/", true);
	xhttp.send();

	xhttp.onreadystatechange = function() {
  		if (this.readyState == 4 && this.status == 200) {
    		const responses = JSON.parse(xhttp.responseText)
			console.log("idiot");
    		
    		
			if (self.target.id == "True"){
				//self.target.style.backgroundColor = "rgb(101, 246, 0)";
			}
			else {
				//self.target.style.backgroundColor = "rgb(225, 0, 0)";
				const righ_answer = document.getElementBY
				confirm("La bonne réponse était: " + document.getElementById('True').textContent);
			}

			document.getElementById("word").innerHTML = responses["word"];
    		for (let i in answers){
    			answers[i].removeAttribute("id");
    			answers[i].innerHTML = responses["definitions"][i]["description"];

    			if (responses["definitions"][i].hasOwnProperty("right_answer")){
    				answers[i].id = "True";
    			}
    		}
  		}
	};
}

for (const i in answers){
	if (answers[i].tagName= "BUTTON"){
		answers[i].addEventListener("click", random_definition);
	}
}


if (window.XMLHttpRequest) { // Mozilla, Safari, IE7+...
    httpRequest = new XMLHttpRequest();
}