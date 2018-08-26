const replace = function (string, substring_f, substring_r) {
      var substring_index;
      var output;
	do {
		substringIndex = string.indexOf(substring_f);
		output = string.replace(substring_f, substring_r);
	} while (substringIndex !== -1)
	return output;
}
const styles = "\n\
* {\n\
  box-sizing: border-box;\n\
  -moz-box-sizing: border-box;\n\
  -webkit-box-sizing: border-box;\n\
}\n\
\n\
.note {\n\
      background-color: #FFF;\n\
      \n\
      opacity: 0;\n\
      transition: opacity 1s ease;\n\
      \n\
      max-width: 25vw;\n\
      max-height: 25vw;\n\
      position: absolute;\n\
}\n\
\n";

if (document.querySelector("style")) {
      document.head.querySelector("style").innerHTML += styles;
}
else {
      var style = document.createElement("style");
      style.innerHTML += styles;
      document.head.appendChild(style);
}
