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
.number {\n\
      text-decoration: none;\n\
      color: #2b5cad;\n\
      transition: color 1s ease;\n\
}\n\
.number:hover {\n\
      color: #6799ea;\n\
      transition: color 1s ease;\n\
}\n\
.number:active {\n\
      color: #96beff;\n\
      transition: color 0.1s ease;\n\
}\n\
.note {\n\
      background-color: #efefef;\n\
      border-radius: 5px;\n\
      box-shadow: 4px 4px 10px 2px #999;\n\
      \n\
      opacity: 0;\n\
      \n\
      max-width: 0vw;\n\
      max-height: 0vh;\n\
      padding: 1vw;\n\
      margin: 0.1vw;\n\
      position: absolute;\n\
      visibility: hidden;\n\
      \n\
      transition: background-color 1s ease 0.25s, border-radius 1s ease 0.25s, box-shadow 1s ease 0.25s, opacity 1s ease, max-width 0s ease 1s, max-height 0s ease 1s, visibility 0s ease 1s;\n\
}\n\
.note:hover {\n\
      background-color: #ffffff;\n\
      border-radius: 15px;\n\
      /* box-shadow: 6px 6px 16px 2px #888; */\n\
      \n\
      opacity: 1;\n\
      max-width: 100vw;\n\
      max-height: 100vh;\n\
      visibility: visible;\n\
      transition: background-color 1s ease 0s, border-radius 1s ease 0s, box-shadow 1s ease 0s, opacity 1s ease, max-width 0s ease 0s, max-height 0s ease 0s, display 0s ease 0s;\n\
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

var footnotes = document.createElement("div");
footnotes.id = "footnotes-box";
do {
      document.head.querySelector("style").innerHTML += "\n\
            #number-" + note_index + ":hover ~ #note-" + note_index + "{\n\
                  background-color: #f9f9f9;\n\
                  border-radius: 10px;\n\
                  /* box-shadow: 4px 4px 10px 2px #888; */\n\
                  \n\
                  opacity: 1;\n\
                  max-width: 100vw;\n\
                  max-height: 100vh;\n\
                  visibility: visible;\n\
                  transition: background-color 1s ease 0.25s, border-radius 1s ease 0.25s, box-shadow 1s ease 0.25s, opacity 1s ease, max-width 0s ease 0s, max-height 0s ease 0s, display 0s ease 0s;\n\
            }\n\
      \n";
      document.body.innerHTML = replace(
            document.body.innerHTML,
            "{note}",
            "<sup class='number' id='number-" + note_index + "'><a href='#footnote-" + note_index + "' class='number'>" + note_index + "</a></sup><span class='note' id='note-" + note_index + "'>"
      );
      document.body.innerHTML = replace(
            document.body.innerHTML,
            "{/note}",
            "</span>"
      );

      var footnote_content = document.body.querySelector("#note-" + note_index).innerHTML;
      footnotes.innerHTML += "<a href='#note-" + note_index + "' class='number' id='footnote-" + note_index + "'>" + note_index + ". </a><span class='footnote-content'>" + footnote_content + "</span>";
      footnotes.innerHTML += "<br />";

      note_index ++;
} while (document.body.innerHTML.indexOf("{note}") !== -1)
document.body.appendChild(footnotes);
