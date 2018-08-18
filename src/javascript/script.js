// ASCII logo art displayed in console
// http://www.network-science.de/ascii/
console.log("%c\
    _____            ______   _____  _____  _    _  __  __   \n\
   / ____|    /\\    |  ____| / ____||_   _|| |  | ||  \\/  |  \n\
  | |        /  \\   | |__   | (___    | |  | |  | || \\  / |  \n\
  | |       / /\\ \\  |  __|   \\___ \\   | |  | |  | || |\\/| |  \n\
  | |____  / ____ \\ | |____  ____) | _| |_ | |__| || |  | |  \n\
   \\_____|/_/    \\_\\|______||_____/ |_____| \\____/ |_|  |_|  \n\
                                                             \
", "background: #e8efff; color: #4319ff; font-weight: 1000;");



// Settings for networks
var settings = {
      "node_types": [
            {
                  "name": "Data/Input",
                  // Green
                  "color": "#3f9b41"
            },
            {
                  "name": "Data/Output",
                  // Light blue
                  "color": "#afcfff"
            },
            {
                  "name": "Data/Value",
                  // Orange
                  "color": "#ff8300"
            },
            {
                  "name": "Operation/Addition",
                  // Purple
                  "color": "#c854ff"
            },
            {
                  "name": "Operation/Multiplication",
                  // Red
                  "color": "#f92c2c"
            }
      ],
      "population_size": 100,
      "visualization": {
            "size": undefined,
            "brightness": undefined
      }
};

// Generate a random number in between a minimum value and a maximum value
const random = function (minimum, maximum) {
      return minimum + (Math.random() * (maximum - minimum));
}
// Select a random element from a given array
const random_item = function (array) {
      return array[Math.floor(Math.random() * array.length)];
}
// Generate a random UUID
// Based on https://stackoverflow.com/a/105074
var uuids = [];
const UUID = function () {
      // Generate a random string of four hexadecimal digits
      function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
      }
      // Generate UUID from substrings
      var id;
      do {
            id = s4() + s4() + "-" + s4() + "-" + s4() + "-" + s4() + "-" + s4() + s4() + s4();
      }
      while (uuids.indexOf(id) !== -1)

      uuids.push(id);
      return id;
}
// Clone an object so that the new object does not contain a reference to the original object; either object may be altered without affecting the other
const clone = function (object) {
      // Convert JSON object to a string, then parse it back into a new object and return the object
      return JSON.parse(JSON.stringify(object));
}
// Map one range of numbers to another, given an input value and the two ranges
// https://stackoverflow.com/a/23202637
const map = function (num, in_min, in_max, out_min, out_max) {
      return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
// Find a node globally given its ID
const get_node = function (id) {
      return nodes.find(x => x.id == id);
}
// Change the brightness of a hexadecimal color value
// https://stackoverflow.com/a/13542669
const shade_color = function (color, percent) {
    var f=parseInt(color.slice(1),16),t=percent<0?0:255,p=percent<0?percent*-1:percent,R=f>>16,G=f>>8&0x00FF,B=f&0x0000FF;
    return "#"+(0x1000000+(Math.round((t-R)*p)+R)*0x10000+(Math.round((t-G)*p)+G)*0x100+(Math.round((t-B)*p)+B)).toString(16).slice(1);
}
const round = function (number, decimals) {
      var factor = 10 ** decimals
      return Math.round(number * factor) / factor;
}
const to_percent = {
      "w": function(number, property) {
            return (number / svg.getBBox().width) * 100;
      },
      "h": function(number, property) {
            return (number / svg.getBBox().height) * 100;
      }
}
const to_pixels = {
      "w": function(number, property) {
            return (number / 100) * svg.getBBox().width;
      },
      "h": function(number, property) {
            return (number / 100) * svg.getBBox().height;
      }
}


// Update program settings from user inputs
const update_settings = function () {
      settings.visualization.size = document.querySelector("#controls-visualization-size").checked;
      settings.visualization.brightness = document.querySelector("#controls-visualization-brightness").checked;
}
update_settings();

var svg = document.querySelector("#network-visualization");

// List of all nodes
var nodes = [];
// List of nodes with inputs
var node_inputs = [];
// List of nodes with outputs
var node_outputs = [];
// List of output nodes
var input_nodes = [];
// List of output nodes
var output_nodes = [];
class node {
      constructor(information) {
            this.type = information.type;
            if (information.type == "Data/Input") {
                  input_nodes.push(this);

                  // Cannot be undefined
                  this.value = 0;
                  node_outputs.push(this);
            }
            else if (information.type == "Data/Output") {
                  output_nodes.push(this);

                  node_inputs.push(this);
                  this.value = 0;
                  node_outputs.push(this);
            }
            else if (information.type == "Data/Value") {
                  this.value = information.value;
                  node_outputs.push(this);
            }
            else if (information.type == "Operation/Addition") {
                  node_inputs.push(this);
                  this.value = 0;
                  node_outputs.push(this);
            }
            else if (information.type == "Operation/Multiplication") {
                  node_inputs.push(this);
                  this.value = 0;
                  node_outputs.push(this);
            }
            else {
                  console.error("'" + information.type + "'" + "is not a valid node type. Please use 'Data/Input', 'Data/Output', 'Data/Value', 'Operation/Addition', or 'Operation/Multiplication'.");
            }

            var id = UUID();
            this.id = id;
            nodes.push(this);
      }
}

class connection {
      // Constructor for creating a connection between two nodes within a network
      constructor(source, destination) {
            this.source = source;
            this.destination = destination;
      }
}

class network {
      // Constructor for creating a network or computation graph
      constructor(inputs, outputs) {

            this.inputs = inputs;
            this.outputs = outputs;

            var nodes = [];
            node_inputs = [];
            node_outputs = [];
            input_nodes = [];
            output_nodes = [];
            for (var i = 0; i < inputs; i ++) {
                  nodes.push(
                        new node({
                              "type": "Data/Input"
                        })
                  );
            }
            for (var i = 0; i < outputs; i ++) {
                  nodes.push(
                        new node({
                              "type": "Data/Output"
                        })
                  );
            }
            for (var i = 0; i < Math.round(random(10, 20)); i ++) {
                  nodes.push(
                        new node({
                              "type": "Data/Value",
                              "value": random(-1, 1)
                        })
                  );
            }
            for (var i = 0; i < Math.round(random(10, 20)); i ++) {
                  nodes.push(
                        new node({
                              "type": "Operation/Addition"
                        })
                  );
            }
            for (var i = 0; i < Math.round(random(10, 20)); i ++) {
                  nodes.push(
                        new node({
                              "type": "Operation/Multiplication"
                        })
                  );
            }
            this.nodes = nodes;
            this.node_inputs = node_inputs;
            this.node_outputs = node_outputs;
            this.input_nodes = input_nodes;
            this.output_nodes = output_nodes;

            var connections = [];
            for (var i = 0; i < Math.round(random(50, 100)); i ++) {
                  connections.push(
                        // Create a new connection with the constructor function
                        new connection(
                              // Connection sources must be nodes with outputs
                              random_item(node_outputs),
                              // Connection destinations must be nodes with inputs
                              random_item(node_inputs)
                        )
                  );
            }
            this.connections = connections;

            this.inputs = function (inputs) {
                  var num_inputs = this.input_nodes.length;
                  if (inputs.length < num_inputs) {
                        console.error("The number of inputs you have provided (" + num_inputs + ") is fewer than the number of input nodes in the network (" + num_inputs + "). Please provide " + num_inputs + " inputs.");
                        return false;
                  }
                  else if (inputs.length > num_inputs) {
                        console.error("The number of inputs you have provided (" + num_inputs + ") is fewer than the number of input nodes in the network (" + num_inputs + "). Please provide " + num_inputs + " inputs.");
                        return false;
                  }
                  else if (inputs.length == num_inputs) {
                        for (var i = 0; i < inputs.length; i ++) {
                              this.input_nodes[i].value = inputs[i];
                        }
                        return inputs;
                  }
            }

            this.outputs = function () {
                  var outputs = [];
                  this.output_nodes.forEach(
                        (node) => {
                              outputs.push(node.value);
                        }
                  );
                  return outputs;
            }

            // Run one iteration of calculations for node values in network
            this.update = function () {
                  // Create a clone of the network so that all nodes can be updated simultaneously, without affecting other values
                  var network_buffer = clone(this);
                  this.nodes.forEach(
                        (node) => {
                              var type = node.type;
                              if (type == "Data/Output" || type == "Operation/Addition") {
                                    node.value = 0;
                              }
                              else if (type == "Operation/Multiplication") {
                                    node.value = 1;
                              }
                        }
                  );
                  for (var i = 0; i < network_buffer.connections.length; i ++) {
                        var type = this.connections[i].destination.type;
                        if (type == "Data/Output" || type == "Operation/Addition") {
                              this.connections[i].destination.value +=
                              network_buffer.connections[i].source.value;
                        }
                        else if (type == "Operation/Multiplication") {
                              this.connections[i].destination.value *=
                              network_buffer.connections[i].source.value;
                        }
                  }
                  this.nodes.forEach(
                        (node) => {
                              if (node.type == "Operation/Multiplication" && node.value == 1) {
                                    node.value = 0;
                              }
                        }
                  );

                  // Return updated network object
                  return this;
            }

            // Display visualization of network
            // This function is only used the first time the network is displayed, as it generates the SVG elements used in the visualization
            this.display = function () {
                  svg.innerHTML = "";

                  // Loop through each connection in network
                  this.nodes.forEach(
                        (node) => {
                              var circle = document.createElement("circle");
                              circle.className = "node";

                              // Randomly select an x coordinate
                              var x = random(
                                    // Minimum x value - the left side of the screen (with the circle's radius and margin added)
                                    (5 + 3),
                                    // Maximum x value - the right side of the screen (minus the circle's radius and margin)
                                    (100 - 5 - 3)

                              );

                              // Randomly select a y coordinate
                              var y = random(
                                    // Minimum y value - the top of the screen
                                    (5 + 3),
                                    // Maximum y value - the bottom side of the screen
                                    (100 - 5 - 3)
                              );

                              // Set x position of circle element within SVG element
                              circle.setAttribute("cx", (x + "%"));
                              // Set y position of circle
                              circle.setAttribute("cy", (y + "%"));

                              var id = UUID();
                              circle.setAttribute("id", id);
                              // Store a pointer to the circle element in corresponding connection object
                              // This must be done by retrieving the id of the element to create a link between the variable and the element
                              node.element = id;

                              // Add circle element to SVG element's HTML; this must be done with innerHTML or the SVG element will not be updated
                              svg.innerHTML += circle.outerHTML;


                              var text = document.createElement("text");
                              text.className = "value-label";

                              var id = UUID();
                              text.setAttribute("id", id);
                              node.text = id;

                              svg.innerHTML += text.outerHTML;
                        }
                  );

                  // Render connections
                  // Loop through each connection in network
                  this.connections.forEach(
                        (connection) => {
                              // Create a new SVG line element
                              var line = document.createElement("line");
                              // Apply "connection" CSS class to line element
                              line.className = "connection";

                              // Origin of line (first node)
                              line.setAttribute("x1", document.getElementById(connection.source.element).getAttribute("cx"));
                              line.setAttribute("y1", document.getElementById(connection.source.element).getAttribute("cy"));
                              // Destination of line (second node)
                              line.setAttribute("x2", document.getElementById(connection.destination.element).getAttribute("cx"));
                              line.setAttribute("y2", document.getElementById(connection.destination.element).getAttribute("cy"));

                              // Store reference to line element in corresponding connection object
                              connection.element = line;
                              // Add line HTML to SVG element before circle elements
                              svg.innerHTML = line.outerHTML + svg.innerHTML;
                        }
                  );
            }

            this.update_display = function () {
                  // Render nodes
                  // https://stackoverflow.com/a/4020842
                  var min = Math.min.apply(Math, this.nodes.map(function(x) { return x.value; }));
                  var max = Math.max.apply(Math, this.nodes.map(function(x) { return x.value; }));

                  this.nodes.forEach(
                        (node) => {
                              var element = document.getElementById(node.element);

                              // Default radius is 2%
                              var radius = 25;
                              // Check if node size is enabled in visualization settings
                              if (settings.visualization.size) {
                                    // Map node values to a 1 to 5 percent range
                                    radius = map(node.value, min, max, 1, 5);
                              }
                              // Set radius of circle as percentage
                              element.setAttribute("r", radius + "%");

                              settings.node_types.forEach(
                                    (node_type) => {
                                          if (node.type == node_type.name) {
                                                var color = node_type.color;
                                                if (settings.visualization.brightness) {
                                                      color = shade_color(
                                                            color,
                                                            map(node.value, min, max, -0.75, 0.75)
                                                      );
                                                }
                                                element.style.fill = color;
                                          }
                                    }
                              );


                              var text = document.getElementById(node.text);
                              text.innerHTML = round(node.value, 3);

                              // To pixels
                              radius = to_pixels.w(radius);
                              // text.style.fontSize = radius / (box.height / box.width);
                              // text.style.fontSize = 2 * Math.sqrt((radius ** 2) - ((text.getBBox().width / 2) ** 2));
                              text.style.fontSize = radius / 2;
                              console.log(radius / 2);

                              // Don't use parseInt
                              var x = parseFloat(element.getAttribute("cx"));
                              var y = parseFloat(element.getAttribute("cy"));
                              x -= to_percent.w(text.getBBox().width / 2);
                              y += to_percent.h(text.getBBox().height / 2);
                              // Set x position of text element within SVG element
                              text.setAttribute("x", (x + "%"));
                              // Set y position of text
                              text.setAttribute("y", (y + "%"));
                        }
                  );
            }
      }
}

var population = [];

for (var i = 0; i < settings.population_size; i ++) {
      population.push(new network(5, 5));
}

population[0].display();
population[0].update_display();
