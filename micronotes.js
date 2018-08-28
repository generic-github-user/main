// Replace parts of a string, given a string to search, a substring to find, a string to replace it with
const replace = function (string, find, replace) {
	// Replace the first instance of the string to find found within the string to search
	string = string.replace(find, replace);
	// Return the resulting string
      return string;
}

// Jump up from a link in the footnote listing at the bottom of the page to the corresponding footnote
const jump_up = function (id) {
	// Scroll up to the corresponding note element
      document.getElementById("note-" + id).scrollIntoView({behavior: "smooth", block: "start", inline: "nearest"});
}
// Jump down from a footnote number in the page to the corresponding footnote below
const jump_down = function (id) {
	// Scroll down to the corresponding footnote element
      document.getElementById("footnote-" + id).scrollIntoView({behavior: "smooth", block: "start", inline: "nearest"});
}

// Define global style information and transitions for footnotes and numbers
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
      transition: background-color 1s ease 0s, border-radius 1s ease 0s, box-shadow 1s ease 0s, opacity 1s ease;\n\
}\n\
\n";

// Check if style element exists in page
if (document.querySelector("style")) {
	// If a style element already exists, add the style information defined above
      document.head.querySelector("style").innerHTML += styles;
}
else {
	// If the style element does not exist, create it
      var style = document.createElement("style");
	// Add the defined CSS style information to the style element
      style.innerHTML += styles;
	// Add the style element to the header section of the page
      document.head.appendChild(style);
}

// Create a div to store footnote listing in
var footnotes = document.createElement("div");
// Set ID for footnotes section so that it can be styled using CSS
footnotes.id = "footnotes-box";
// Number for current footnote
var note_index = 1;
do {
	// Add style information to head of page that defines what should happen to what note box when what number is hovered over
      document.head.querySelector("style").innerHTML += "\n\
            #number-" + note_index + ":hover ~ #note-" + note_index + "{\n\
                  background-color: #f9f9f9;\n\
                  border-radius: 10px;\n\
                  /* box-shadow: 4px 4px 10px 2px #888; */\n\
                  \n\
                  opacity: 1;\n\
                  visibility: visible;\n\
                  transition: background-color 1s ease 0.25s, border-radius 1s ease 0.25s, box-shadow 1s ease 0.25s, opacity 1s ease;\n\
            }\n\
      \n";
	// Replace opening footnote tag ({note}) with note box HTML content
      document.body.innerHTML = replace(
            document.body.innerHTML,
		// Footnote opening tag
            "{note}",
		// Superscript with current footnote number, link to footnote in footnote listing, and opening <span> tag that will contain the content of the footnote
            "<sup class='number' id='number-" + note_index + "' onclick='jump_down(" + note_index + ");'>" + note_index + "</sup><span class='note' id='note-" + note_index + "'>"
      );
	// Add closing HTML for note box element in place of closing footnote tag ({/note})
      document.body.innerHTML = replace(
            document.body.innerHTML,
            "{/note}",
		// Closing <span> tag for footnote box content
            "</span>"
      );

	// Increment index of current footnote by 1
      note_index ++;
// Continue looping through footnotes until no {note} shortcodes remain in the page
} while (document.body.innerHTML.indexOf("{note}") !== -1)

// Loop through all note boxes in the page
for (var i = 1; i < document.body.getElementsByClassName("note").length + 1; i ++) {
	// Get HTML content from footnote
      var footnote_content = document.body.querySelector("#note-" + i).innerHTML;
	// Add footnote to listing at the bottom of page, including footnote number and HTML content
      footnotes.innerHTML += "<span class='number' id='footnote-" + i + "' onclick='jump_up(" + i + ")'>" + i + ". </span><span class='footnote-content'>" + footnote_content + "</span>";
	// Add line break in between footnotes
      footnotes.innerHTML += "<br />";
}

// Add line break before footnotes section
document.body.innerHTML += "<br />";
// Add footnotes listing to end of body section of page
document.body.appendChild(footnotes);
