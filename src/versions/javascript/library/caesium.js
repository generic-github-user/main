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



// Generate a random number in between a minimum value and a maximum value
const random = function (minimum, maximum) {
      return minimum + (Math.random() * (maximum - minimum));
}
// Select a random element from a given array
const random_item = function (array) {
      return array[Math.floor(Math.random() * array.length)];
}
// Clone an object so that the new object does not contain a reference to the original object; either object may be altered without affecting the other
const clone = function (object) {
      // Convert JSON object to a string, then parse it back into a new object and return the object
      return JSON.parse(JSON.stringify(object));
}
// Find a node globally given its ID
const get_node = function (id) {
      return all_nodes.find(x => x.id == id);
}

// Settings for networks
var settings = {
      "node_types": [
            {
                  "name": "Data/Input"
            },
            {
                  "name": "Data/Output"
            },
            {
                  "name": "Data/Value"
            },
            {
                  "name": "Operation/Addition",
            },
            {
                  "name": "Operation/Multiplication"
            }
      ],
      "population_size": 100
};

const cs = {
      "all": {
            // List of all nodes
            "nodes": [],
            "connections": [],
            "networks": []
      },
      "temp": {
            // These must be declared outside of the scope of a network object so that the node constructor can add nodes to them
            // List of nodes with inputs
            "node_inputs": [],
            // List of nodes with outputs
            "node_outputs": [],
            // List of output nodes
            "input_nodes": [],
            // List of output nodes
            "output_nodes": []
      }
};

// Generate a random UUID
// Based on https://stackoverflow.com/a/105074
var uuids = [];
cs.UUID = function () {
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

cs.node = class {
      constructor(information) {
            this.type = information.type;
            if (information.type == "Data/Input") {
                  cs.temp.input_nodes.push(this);

                  // Cannot be undefined
                  this.value = 0;
                  cs.temp.node_outputs.push(this);
            }
            else if (information.type == "Data/Output") {
                  cs.temp.output_nodes.push(this);

                  cs.temp.node_inputs.push(this);
                  this.value = 0;
                  cs.temp.node_outputs.push(this);
            }
            else if (information.type == "Data/Value") {
                  this.value = information.value;
                  cs.temp.node_outputs.push(this);
            }
            else if (information.type == "Operation/Addition") {
                  cs.temp.node_inputs.push(this);
                  this.value = 0;
                  cs.temp.node_outputs.push(this);
            }
            else if (information.type == "Operation/Multiplication") {
                  cs.temp.node_inputs.push(this);
                  this.value = 0;
                  cs.temp.node_outputs.push(this);
            }
            else {
                  console.error("'" + information.type + "'" + "is not a valid node type. Please use 'Data/Input', 'Data/Output', 'Data/Value', 'Operation/Addition', or 'Operation/Multiplication'.");
            }

            var id = cs.UUID();
            this.id = id;
            cs.all.nodes.push(this);
      }
}

cs.connection = class {
      // Constructor for creating a connection between two nodes within a network
      constructor(source, destination) {
            this.source = source;
            this.destination = destination;

            var id = cs.UUID();
            this.id = id;
            cs.all.connections.push(this);
      }
}

cs.network = class {
      // Constructor for creating a network or computation graph
      constructor(inputs, outputs) {
            this.inputs = inputs;
            this.outputs = outputs;
            this.nodes = [];

            cs.temp.node_inputs = [];
            cs.temp.node_outputs = [];
            cs.temp.input_nodes = [];
            cs.temp.output_nodes = [];
            for (var i = 0; i < inputs; i ++) {
                  this.nodes.push(
                        new cs.node({
                              "type": "Data/Input"
                        })
                  );
            }
            for (var i = 0; i < outputs; i ++) {
                  this.nodes.push(
                        new cs.node({
                              "type": "Data/Output"
                        })
                  );
            }
            for (var i = 0; i < Math.round(random(10, 20)); i ++) {
                  this.nodes.push(
                        new cs.node({
                              "type": "Data/Value",
                              "value": random(-1, 1)
                        })
                  );
            }
            for (var i = 0; i < Math.round(random(10, 20)); i ++) {
                  this.nodes.push(
                        new cs.node({
                              "type": "Operation/Addition"
                        })
                  );
            }
            for (var i = 0; i < Math.round(random(10, 20)); i ++) {
                  this.nodes.push(
                        new cs.node({
                              "type": "Operation/Multiplication"
                        })
                  );
            }
            this.node_inputs = cs.temp.node_inputs;
            this.node_outputs = cs.temp.node_outputs;
            this.input_nodes = cs.temp.input_nodes;
            this.output_nodes = cs.temp.output_nodes;

            var connections = [];
            for (var i = 0; i < Math.round(random(50, 100)); i ++) {
                  connections.push(
                        // Create a new connection with the constructor function
                        new cs.connection(
                              // Connection sources must be nodes with outputs
                              random_item(this.node_outputs),
                              // Connection destinations must be nodes with inputs
                              random_item(this.node_inputs)
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

            var id = cs.UUID();
            this.id = id;
            cs.all.networks.push(this);
      }
}

// var population = [];
//
// for (var i = 0; i < settings.population_size; i ++) {
//       population.push(new cs.network(5, 5));
// }
