const replace = function (string, find, replace) {
	string = string.replace(find, replace);
      return string;
}
var note_index = 1;

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
      \n\
      max-width: 0vw;\n\
      max-height: 0vw;\n\
      padding: 0vw;\n\
      position: absolute;\n\
      overflow: hidden;\n\
      \n\
      transition: opacity 0.5s ease, max-width 1s ease, max-height 1s ease;\n\
}\n\
.note:hover {\n\
      opacity: 1;\n\
      max-width: 25vw;\n\
      max-height: 25vw;\n\
      transition: opacity 0.5s ease, max-width 1s ease, max-height 1s ease;\n\
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
      document.head.querySelector("style").innerHTML += "\n\
            #number-" + note_index + ":hover ~ #note-" + note_index + "{\n\
                  opacity: 1;\n\
                  max-width: 25vw;\n\
                  max-height: 25vw;\n\
            }\n\
      \n";
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
      note_index ++;
} while (document.body.innerHTML.indexOf("{note}") !== -1)
