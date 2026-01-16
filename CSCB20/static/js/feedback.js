var r = document.getElementsByClassName("review");
var i;
for (i = 0; i < r.length; i++) {
	r[i].addEventListener("click", function() {
	alert("wdwd";)
	this.classList.toggle("active");
	var content = this.nextElementSibling;
	if (content.style.display === "block") {
		content.style.display = "none";
	} else {
		content.style.display = "block";
	}
});
}
