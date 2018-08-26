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
a {\n\
.note {\n\
      background-color: #FFF;\n\
      \n\
      opacity: 0;\n\
      \n\
      max-width: 0vw;\n\
      max-height: 0vh;\n\
      padding: 0vw;\n\
      margin: 0vw;\n\
      position: absolute;\n\
      overflow: hidden;\n\
      \n\
      transition: opacity 1s ease, max-width 0s ease 1s, max-height 0s ease 1s;\n\
}\n\
.note:hover {\n\
      opacity: 1;\n\
      max-width: 100vw;\n\
      max-height: 100vh;\n\
      transition: opacity 1s ease, max-width 0s ease, max-height 0s ease;\n\
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
                  max-width: 100vw;\n\
                  max-height: 100vh;\n\
                  transition: opacity 1s ease, max-width 0s ease, max-height 0s ease;\n\
            }\n\
      \n";
      document.body.innerHTML = replace(
            document.body.innerHTML,
            "{note}",
            "<sup class='number' id='number-" + note_index + "'><a href='#footnote-" + note_index + "'>" + note_index + "</a></sup><span class='note' id='note-" + note_index + "'>"
      );
      document.body.innerHTML = replace(
            document.body.innerHTML,
            "{/note}",
            "</span>"
      );

      var footnote_content = document.body.querySelector("#note-" + note_index).innerHTML;
      document.body.innerHTML += "<a href='#note-" + note_index + "'><p id='footnote-" + note_index + "'>" + note_index + ". </p></a>";

      note_index ++;
} while (document.body.innerHTML.indexOf("{note}") !== -1)
