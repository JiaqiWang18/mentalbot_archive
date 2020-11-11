function init() {
	document.getElementById("sendButton").addEventListener("click", getResponse);

}


//get response from api with input

function writeResponse(){
	var list = document.getElementById("cbox");  
	list.removeChild(list.lastChild);
	var date = new Date()
	var conversationbox = document.getElementById("cbox")
	
	try{
		obj = JSON.parse(this.responseText)
		console.log("is obj")
		for (x in obj){
			var min = date.getMinutes()
			if (parseInt(min)<10){
				min = "0".concat(min)
			}
			var title = document.createTextNode(x)
			var summary = document.createTextNode(obj[x][1])
			var activelink = obj[x][0].link(obj[x][0])
			var div = document.createElement("div")
			var timeSpan = document.createElement("span")
			var titleP = document.createElement("h4")
			var sumP = document.createElement("p")
			var linkP = document.createElement("p")
			var time = document.createTextNode(date.getHours()+":"+min)
			timeSpan.appendChild(time)
			timeSpan.setAttribute("class","time-left")
			titleP.appendChild(title)
			sumP.appendChild(summary)
			linkP.innerHTML = activelink
			div.appendChild(titleP)
			div.appendChild(sumP)
			div.appendChild(linkP)
			div.appendChild(timeSpan)
			div.setAttribute("class","container")
			conversationbox.appendChild(div)
		}
		
	}
	
	catch(err){
	console.log(this.responseText)
	var input = "Bot: " + this.responseText
	//var input = "debugger"
	var min = date.getMinutes()
	if (parseInt(min)<10){
		min = "0".concat(min)
	}
	var div = document.createElement("div")
	var span = document.createElement("span")
	var p = document.createElement("p")
	var textNode = document.createTextNode(input)
	var time = document.createTextNode(date.getHours()+":"+min)
	
	p.appendChild(textNode)
	p.setAttribute("class","bottext")
	span.appendChild(time)
	span.setAttribute("class","time-left")
	div.appendChild(p)
	div.appendChild(span)
	div.setAttribute("class","container")
	conversationbox.appendChild(div)
	
	}
	document.getElementById("sendButton").disabled = false

	conversationbox.scrollTo(0,document.querySelector(".cbox").scrollHeight);
	console.log(document.querySelector(".cbox").scrollHeight)
}

function getResponse() {
	var date = new Date()
	var conversationbox = document.getElementById("cbox")
	var input = document.getElementById("inputbox").value
	if(/\S/.test(input)==false){
		alert("input cannot be empty!")
		return
	}

	document.getElementById("inputbox").value = ""
	var textNode = document.createTextNode(input)
	var min = date.getMinutes()
	if (parseInt(min)<10){
		min = "0".concat(min)
	}
	var time = document.createTextNode(date.getHours()+":"+ min)
	var div = document.createElement("div")
	var span = document.createElement("span")
	var p = document.createElement("p")
	document.getElementById("sendButton").disabled = true

	p.appendChild(textNode)
	p.setAttribute("class","usertext")
	span.appendChild(time)
	span.setAttribute("class","time-right")
	div.appendChild(p)
	div.appendChild(span)
	div.setAttribute("class","usercontainer")
	conversationbox.appendChild(div)

	var xhr = new XMLHttpRequest();
	xhr.addEventListener("load",writeResponse)
	// use the REST api
	
	try{
		xhr.open("GET", "/chat?key=wfefh4jyt&input=" + input);
		xhr.send();
		var thkp = document.createElement("p")
		thkp.appendChild(document.createTextNode("bot thinking..."))
		thkp.setAttribute("id","thk")
		thkp.setAttribute("class","thking")
		conversationbox.appendChild(thkp)
		conversationbox.scrollTo(0,document.querySelector(".cbox").scrollHeight);

	}
	catch(err){
		console.log("error")
		alert("bot is under maintenance, come back later")
	}
}
// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

init()