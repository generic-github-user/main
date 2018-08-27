const replace = function (string, find, replace) {
	string = string.replace(find, replace);
      return string;
}
var note_index = 1;

const jump_up = function (id) {
      document.getElementById("note-" + id).scrollIntoView({behavior: "smooth", block: "start", inline: "nearest"});
}
const jump_down = function (id) {
      document.getElementById("footnote-" + id).scrollIntoView({behavior: "smooth", block: "start", inline: "nearest"});
}

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
      padding: 1vw;\n\
      margin: 0.1vw;\n\
      position: absolute;\n\
      visibility: hidden;\n\
      \n\
      transition: background-color 1s ease 0.25s, border-radius 1s ease 0.25s, box-shadow 1s ease 0.25s, opacity 1s ease, visibility 0s ease 1s;\n\
}\n\
.note:hover {\n\
      background-color: #ffffff;\n\
      border-radius: 15px;\n\
      /* box-shadow: 6px 6px 16px 2px #888; */\n\
      \n\
      opacity: 1;\n\
      visibility: visible;\n\
      transition: background-color 1s ease 0s, border-radius 1s ease 0s, box-shadow 1s ease 0s, opacity 1s ease, display 0s ease 0s;\n\
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
                  visibility: visible;\n\
                  transition: background-color 1s ease 0.25s, border-radius 1s ease 0.25s, box-shadow 1s ease 0.25s, opacity 1s ease, display 0s ease 0s;\n\
            }\n\
      \n";
      document.body.innerHTML = replace(
            document.body.innerHTML,
            "{note}",
            "<sup class='number' id='number-" + note_index + "' onclick='jump_down(" + note_index + ");'>" + note_index + "</sup><span class='note' id='note-" + note_index + "'>"
      );
      document.body.innerHTML = replace(
            document.body.innerHTML,
            "{/note}",
            "</span>"
      );

      note_index ++;
} while (document.body.innerHTML.indexOf("{note}") !== -1)

for (var i = 1; i < document.body.getElementsByClassName("note").length + 1; i ++) {
      var footnote_content = document.body.querySelector("#note-" + i).innerHTML;
      footnotes.innerHTML += "<span class='number' id='footnote-" + i + "' onclick='jump_up(" + i + ")'>" + i + ". </span><span class='footnote-content'>" + footnote_content + "</span>";
      footnotes.innerHTML += "<br />";
}

document.body.innerHTML += "<br />";
document.body.appendChild(footnotes);
