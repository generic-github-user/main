const replace = function (string, find, replace) {
	string = string.replace(find, replace);
      return string;
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

do {
      document.body.innerHTML = replace(
            document.body.innerHTML,
            "{note}",
            "<sup class='number' id='number-" + note_index + "'>" + note_index + "</sup><span class='note' id='note-" + note_index + "'>"
      );
      document.body.innerHTML = replace(
            document.body.innerHTML,
            "{/note}",
            "</span>"
      );
} while (document.body.innerHTML.indexOf("{note}") !== -1)
