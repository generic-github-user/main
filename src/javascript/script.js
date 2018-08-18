// ASCII logo art displayed in console
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
                  // Yellow-Orange
                  "color": "#ffbb00"
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
      "population_size": 100
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
const UUID = function () {
      // Generate a random string of four hexadecimal digits
      function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
      }
      // Generate UUID from substrings
      return s4() + s4() + "-" + s4() + "-" + s4() + "-" + s4() + "-" + s4() + s4() + s4();
}
// Clone an object so that the new object does not contain a reference to the original object; either object may be altered without affecting the other
const clone = function (object) {
      // Convert JSON object to a string, then parse it back into a new object and return the object
      return JSON.parse(JSON.stringify(object));
}
const map = function (num, in_min, in_max, out_min, out_max) {
      return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

// Find a node globally given its ID
const get_node = function (id) {
      return nodes.find(x => x.id == id);
}

const shade_color = function (color, percent) {
    var f=parseInt(color.slice(1),16),t=percent<0?0:255,p=percent<0?percent*-1:percent,R=f>>16,G=f>>8&0x00FF,B=f&0x0000FF;
    return "#"+(0x1000000+(Math.round((t-R)*p)+R)*0x10000+(Math.round((t-G)*p)+G)*0x100+(Math.round((t-B)*p)+B)).toString(16).slice(1);
}

var nodes = [];
var node_inputs = [];
var node_outputs = [];
var input_nodes = [];
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
            do {id = UUID();}
            while (nodes.find(x => x.id == id) !== undefined)

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
            for (var i = 0; i < Math.round(random(5, 10)); i ++) {
                  nodes.push(
                        new node({
                              "type": "Data/Value",
                              "value": random(-1, 1)
                        })
                  );
            }
            for (var i = 0; i < Math.round(random(5, 10)); i ++) {
                  nodes.push(
                        new node({
                              "type": "Operation/Addition"
                        })
                  );
            }
            for (var i = 0; i < Math.round(random(5, 10)); i ++) {
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
            for (var i = 0; i < Math.round(random(25, 50)); i ++) {
                  connections.push(
                        new connection(
                              // Connection sources must be nodes with outputs
                              random_item(node_outputs),
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

            this.display = function () {
                  var svg = document.querySelector("#network-visualization");
                  svg.innerHTML = "";

                  // Render nodes
                  var min = Math.min.apply(Math, this.nodes.map(function(x) { return x.value; }));
                  var max = Math.max.apply(Math, this.nodes.map(function(x) { return x.value; }));
                  // Loop through each connection in network
                  this.nodes.forEach(
                        (node) => {
                              var circle = document.createElement("circle");
                              circle.className = "node";

                              var radius = map(node.value, min, max, 1, 5);
                              circle.setAttribute("r", radius + "%");

                              circle.setAttribute(
                                    "cx", Math.round(
                                          random(
                                                (radius + 3),
                                                (100 - radius - 3)
                                          )
                                    ) + "%"
                              );
                              circle.setAttribute(
                                    "cy", Math.round(
                                          random(
                                                (radius + 3),
                                                (100 - radius - 3)
                                          )
                                    ) + "%"
                              );

                              settings.node_types.forEach(
                                    (node_type) => {
                                          if (node.type == node_type.name) {
                                                circle.style.fill = shade_color(
                                                      node_type.color,
                                                      map(node.value, min, max, -1, 1)
                                                );
                                          }
                                    }
                              );

                              node.element = circle;
                              svg.innerHTML += circle.outerHTML;
                        }
                  );

                  // Render connections
                  // Loop through each connection in network
                  this.connections.forEach(
                        (connection) => {
                              var line = document.createElement("line");
                              line.className = "connection";

                              line.setAttribute("x1", connection.source.element.getAttribute("cx"));
                              line.setAttribute("y1", connection.source.element.getAttribute("cy"));
                              line.setAttribute("x2", connection.destination.element.getAttribute("cx"));
                              line.setAttribute("y2", connection.destination.element.getAttribute("cy"));

                              connection.element = line;
                              // Add line HTML to SVG element before circle elements
                              svg.innerHTML = line.outerHTML + svg.innerHTML;
                        }
                  );
            }
      }
}

var population = [];

for (var i = 0; i < settings.population_size; i ++) {
      population.push(new network(5, 5));
}
