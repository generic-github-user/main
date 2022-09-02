console.log("Loading script.js");
console.log("");

console.log("Defining utility functions . . .");

// Generate a random number in between a minimum value and a maximum value
const random = function(minimum, maximum) {
      return minimum + (Math.random() * (maximum - minimum));
}
// Select a random element from a given array
const random_item = function(array) {
      return array[Math.floor(Math.random() * array.length)];
}
// Generate a random UUID
const UUID = function() {
      function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
                  .toString(16)
                  .substring(1);
      }
      return s4() + s4() + "-" + s4() + "-" + s4() + "-" + s4() + "-" + s4() + s4() + s4();
}
// Clone an object so that the new object does not contain a reference to the original object; either object may be altered without affecting the other
const clone = function(object) {
      return JSON.parse(JSON.stringify(object));
}

// Find a node globally given its ID
const get_node = function(id) {
      return nodes.find(x => x.id == id);
}

console.log("Functions defined successfully.");
console.log("");

var nodes = [];
var node_inputs = [];
var node_outputs = [];
var input_nodes = [];
var output_nodes = [];
class node {
      constructor(information) {
            console.log("Creating node . . .");

            this.type = information.type;
            if (information.type == "Data/Input") {
                  input_nodes.push(this);

                  this.value = 0;
                  node_outputs.push(this);
            } else if (information.type == "Data/Output") {
                  output_nodes.push(this);

                  node_inputs.push(this);
                  this.value = 0;
                  node_outputs.push(this);
            } else if (information.type == "Data/Value") {
                  this.value = information.value;
                  node_outputs.push(this);
            } else if (information.type == "Operation/Addition") {
                  node_inputs.push(this);
                  this.value = 0;
                  node_outputs.push(this);
            } else if (information.type == "Operation/Multiplication") {
                  node_inputs.push(this);
                  this.value = 1;
                  node_outputs.push(this);
            } else {
                  console.error("'" + information.type + "'" + "is not a valid node type. Please use 'Data/Input', 'Data/Output', 'Data/Value', 'Operation/Addition', or 'Operation/Multiplication'.");
            }

            var id = UUID();
            do {
                  id = UUID();
            }
            while (nodes.find(x => x.id == id) !== undefined)

            this.id = id;
            nodes.push(this);

            console.log("Node created successfully.");
            console.log("");
      }
}

class connection {
      constructor(source, destination) {
            console.log("Creating connection . . .");
            this.source = source;
            this.destination = destination;
            console.log("Connection created successfully.");
            console.log("");
      }
}

class network {
      constructor(inputs, outputs) {
            console.log("Creating new network . . .");

            this.inputs = inputs;
            this.outputs = outputs;

            console.log("Creating nodes . . .");
            var nodes = [];
            node_inputs = [];
            node_outputs = [];
            input_nodes = [];
            output_nodes = [];
            for (var i = 0; i < inputs; i++) {
                  nodes.push(
                        new node({
                              "type": "Data/Input"
                        })
                  );
            }
            for (var i = 0; i < outputs; i++) {
                  nodes.push(
                        new node({
                              "type": "Data/Output"
                        })
                  );
            }
            for (var i = 0; i < Math.round(random(5, 10)); i++) {
                  nodes.push(
                        new node({
                              "type": "Data/Value",
                              "value": random(-1, 1)
                        })
                  );
            }
            for (var i = 0; i < Math.round(random(5, 10)); i++) {
                  nodes.push(
                        new node({
                              "type": "Operation/Addition"
                        })
                  );
            }
            for (var i = 0; i < Math.round(random(5, 10)); i++) {
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
            console.log("Nodes created successfully.");
            console.log("");

            console.log("Creating connections . . .")
            var connections = [];
            for (var i = 0; i < Math.round(random(25, 50)); i++) {
                  connections.push(
                        new connection(
                              random_item(node_outputs),
                              random_item(node_inputs)
                        )
                  );
            }
            this.connections = connections;
            console.log("Connections created successfully.");
            console.log("");

            console.log("Creating input function . . .");
            this.inputs = function(inputs) {
                  var num_inputs = this.input_nodes.length;
                  if (inputs.length < num_inputs) {
                        console.error("The number of inputs you have provided (" + num_inputs + ") is fewer than the number of input nodes in the network (" + num_inputs + "). Please provide " + num_inputs + " inputs.");
                        return false;
                  } else if (inputs.length > num_inputs) {
                        console.error("The number of inputs you have provided (" + num_inputs + ") is fewer than the number of input nodes in the network (" + num_inputs + "). Please provide " + num_inputs + " inputs.");
                        return false;
                  } else if (inputs.length == num_inputs) {
                        for (var i = 0; i < inputs.length; i++) {
                              input_nodes[i].value = inputs[i];
                        }
                        return inputs;
                  }
            }
            console.log("Input function created successfully.");
            console.log("");

            console.log("Creating output function . . .");
            this.outputs = function() {
                  var outputs = [];
                  this.output_nodes.forEach(
                        (node) => {
                              outputs.push(node.output);
                        }
                  );
                  return outputs;
            }
            console.log("Output function created successfully.");
            console.log("");

            console.log("Creating update function . . .");
            this.update = function() {
                  var network_buffer = clone(this);
                  for (var i = 0; i < network_buffer.connections.length; i++) {
                        var type = this.connections[i].destination.type;
                        if (type == "Data/Output" || type == "Operation/Addition") {
                              this.connections[i].destination.value = 0;
                              this.connections[i].destination.value +=
                                    network_buffer.connections[i].source.output;
                        } else if (type == "Operation/Multiplication") {
                              this.connections[i].destination.value = 1;
                              this.connections[i].destination.value *=
                                    network_buffer.connections[i].source.output;
                        }
                  }
                  return this;
            }
            console.log("Update function created successfully.");
            console.log("");

            console.log("Network created successfully.");
            console.log(this);
            console.log("");
      }
}

var settings = {
      "population_size": 100
};

var population = [];

for (var i = 0; i < settings.population_size; i++) {
      population.push(new network(5, 5));
}

console.log("script.js loaded successfully");