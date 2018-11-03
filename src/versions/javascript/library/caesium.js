// Caesium

"use strict";

// Generate a random number in between a minimum value and a maximum value
const random = function(minimum, maximum) {
      return minimum + (Math.random() * (maximum - minimum));
}
// Select a random element from a given array
const random_item = function(array) {
      return array[Math.floor(Math.random() * array.length)];
}
// Deep clone an object so that the new object does not contain a reference to the original object; either object may be altered without affecting the other
// IDs of nodes and connections cloned networks do not need to be regenerated because they are only used to find nodes and connections from that specific network
// https://stackoverflow.com/a/728694
const clone = function(object) {
      var copy;

      // Handle the 3 simple types, and null or undefined
      if (null == object || "object" != typeof object) return object;

      // Handle Date
      if (object instanceof Date) {
            copy = new Date();
            copy.setTime(object.getTime());
            return copy;
      }

      // Handle Array
      if (object instanceof Array) {
            copy = [];
            for (var i = 0, len = object.length; i < len; i++) {
                  copy[i] = clone(object[i]);
            }
            return copy;
      }

      // Handle Object
      if (object instanceof Object) {
            copy = {};
            for (var attr in object) {
                  if (object.hasOwnProperty(attr)) copy[attr] = clone(object[attr]);
            }
            return copy;
      }

      throw new Error("Unable to copy obj! Its type isn't supported.");
}

const clone_network = function(network) {
      var cloned = clone(network);
      cloned.id = cs.UUID();
      return cloned;
}

// Find a network globally given its ID
const get_network = function(id) {
      return cs.all.networks.find(x => x.id == id);
}

const difference = function(array_1, array_2) {
      return array_2.map(
            (element, i) => {
                  return element - array_1[i];
            }
      )
}

const remove = function(array, element) {
      var index = array.indexOf(element);
      if (index != -1) {
            array.splice(index, 1);
      }
}

const sum = function(array) {
      var sum = 0;
      for (var i = 0; i < array.length; i++) {
            sum += array[i];
      };
      return sum;
}

const average = function(array) {
      return sum(array) / array.length;
}

const cs = {
      "all": {
            // List of all nodes
            "nodes": [],
            // List of all connections
            "connections": [],
            // List of all networks
            "networks": []
      },
      // Settings for networks
      "settings": {
            "node_types": [{
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
            ]
      }
};

// ASCII logo art displayed in console
// http://www.network-science.de/ascii/
cs.caesium = function() {
      console.log("%c\
    _____            ______   _____  _____  _    _  __  __   \n\
   / ____|    /\\    |  ____| / ____||_   _|| |  | ||  \\/  |  \n\
  | |        /  \\   | |__   | (___    | |  | |  | || \\  / |  \n\
  | |       / /\\ \\  |  __|   \\___ \\   | |  | |  | || |\\/| |  \n\
  | |____  / ____ \\ | |____  ____) | _| |_ | |__| || |  | |  \n\
   \\_____|/_/    \\_\\|______||_____/ |_____| \\____/ |_|  |_|  \n\
                                                             \
", "background: #e8efff; color: #4319ff; font-weight: 1000;");
}

// Generate a random UUID
// Based on https://stackoverflow.com/a/105074
var uuids = [];
cs.UUID = function() {
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

// Node class
cs.node = class {
      constructor(config) {
            // Create UUID for node
            this.id = cs.UUID();
            this.type = config.type;

            // Create input node
            if (config.type == "Data/Input") {
                  config.network.node_types.input.push(this.id);

                  // Cannot be undefined
                  this.value = 0;
                  config.network.node_outputs.push(this.id);
            }
            // Create output node
            else if (config.type == "Data/Output") {
                  config.network.node_types.output.push(this.id);

                  config.network.node_inputs.push(this.id);
                  this.value = config.value;
                  config.network.node_outputs.push(this.id);
            }
            // Create value node
            else if (config.type == "Data/Value") {
                  config.network.node_types.value.push(this.id);

                  this.value = config.value;
                  config.network.node_outputs.push(this.id);
            }
            // Create addition node
            else if (config.type == "Operation/Addition") {
                  config.network.node_inputs.push(this.id);
                  this.value = 0;
                  config.network.node_outputs.push(this.id);
            }
            // Create multiplication node
            else if (config.type == "Operation/Multiplication") {
                  config.network.node_inputs.push(this.id);
                  this.value = 0;
                  config.network.node_outputs.push(this.id);
            }
            // Log error: node type not found
            else {
                  console.error("'" + config.type + "'" + "is not a valid node type. Please use 'Data/Input', 'Data/Output', 'Data/Value', 'Operation/Addition', or 'Operation/Multiplication'.");
            }

            // Add node to global nodes list
            cs.all.nodes.push(this);
      }
}

// Connection class
cs.connection = class {
      // Constructor for creating a connection between two nodes within a network
      constructor(config) {
            this.id = cs.UUID();

            this.source = config.source;
            this.destination = config.destination;

            cs.all.connections.push(this);
      }
}

// Network class
cs.network = class {
      // Constructor for creating a network or computation graph
      constructor(config) {
            // Assign a random ID to the the new network object
            this.id = cs.UUID();

            this.inputs = config.inputs;
            this.outputs = config.outputs;
            this.nodes = [];

            this.node_inputs = [];
            this.node_outputs = [];

            // Score used for evolutionary optimization algorithm
            this.score = 0;

            this.node_types = {
                  // List of output nodes
                  "input": [],
                  // List of output nodes
                  "output": [],
                  // List of value (bias) nodes
                  "value": []
            }
            for (var i = 0; i < this.inputs; i++) {
                  this.nodes.push(
                        new cs.node({
                              "network": this,
                              "type": "Data/Input"
                        })
                  );
            }
            for (var i = 0; i < this.outputs; i++) {
                  this.nodes.push(
                        new cs.node({
                              "network": this,
                              "type": "Data/Output",
                              "value": 0
                        })
                  );
            }
            // Add value nodes to network
            for (var i = 0; i < Math.round(random(1, 2)); i++) {
                  this.nodes.push(
                        new cs.node({
                              "network": this,
                              "type": "Data/Value",
                              "value": random(-1, 1)
                        })
                  );
            }
            // Add addition nodes to network
            for (var i = 0; i < Math.round(random(1, 2)); i++) {
                  this.nodes.push(
                        new cs.node({
                              "network": this,
                              "type": "Operation/Addition"
                        })
                  );
            }
            // Add multiplication nodes to network
            for (var i = 0; i < Math.round(random(1, 2)); i++) {
                  this.nodes.push(
                        new cs.node({
                              "network": this,
                              "type": "Operation/Multiplication"
                        })
                  );
            }

            // These functions must be defined before the connection generation code so they can be used there
            // Get a node from the network given the node's ID
            this.find_node = function(id) {
                  // Search network's node list for a connection with the matching ID
                  var node = this.nodes.find(x => x.id == id);
                  // If node cannot be found, log an error
                  if (!node) {
                        console.error("Node with id " + id + " could not be found.");
                  }
                  // If node is found, return the node object
                  else {
                        return node;
                  }
            }
            // Get a node from the network given the connection's ID
            this.find_connection = function(id) {
                  // Search network's connection list for a connection with the matching ID
                  var connection = this.connections.find(x => x.id == id);
                  // If connection cannot be found, log an error
                  if (!connection) {
                        console.error("Connection with id " + id + " could not be found.");
                  }
                  // If connection is found, return the node object
                  else {
                        return connection;
                  }
            }
            this.remove_node = function(id) {
                  remove(this.nodes, this.find_node(id));
                  remove(this.node_types.value, id);

                  remove(this.node_inputs, id);
                  remove(this.node_outputs, id);

                  var dead_connections = this.connections.filter(x => x.source == id);
                  for (var i = 0; i < dead_connections.length; i++) {
                        remove(this.connections, dead_connections[i]);
                  }
                  dead_connections = this.connections.filter(x => x.destination == id);
                  for (var i = 0; i < dead_connections.length; i++) {
                        remove(this.connections, dead_connections[i]);
                  }
            }
            this.remove_connection = function(id) {
                  this.connections.splice(this.connections.indexOf(this.find_connection(id)), 1);
            }

            // Generate random connections between nodes
            var connections = [];
            for (var i = 0; i < Math.round(random(20, 20)); i++) {
                  connections.push(
                        // Create a new connection with the constructor function
                        new cs.connection({
                              // Connection sources must be nodes with outputs
                              "source": this.find_node(random_item(this.node_outputs)).id,
                              // Connection destinations must be nodes with inputs
                              "destination": this.find_node(random_item(this.node_inputs)).id
                        })
                  );
            }
            this.connections = connections;

            // Function for setting input data of network
            this.set_inputs = function(inputs) {
                  var num_inputs = this.inputs;
                  if (inputs.length < num_inputs) {
                        console.error("The number of inputs you have provided (" + inputs.length + ") is fewer than the number of input nodes in the network (" + num_inputs + "). Please provide " + num_inputs + " inputs.");
                        return false;
                  } else if (inputs.length > num_inputs) {
                        console.error("The number of inputs you have provided (" + inputs.length + ") is greater than the number of input nodes in the network (" + num_inputs + "). Please provide " + num_inputs + " inputs.");
                        return false;
                  } else if (inputs.length == num_inputs) {
                        for (var i = 0; i < inputs.length; i++) {
                              this.find_node(this.node_types.input[i]).value = inputs[i];
                        }
                        return this;
                  }
            }

            // Function for retrieving outputs from network
            this.get_outputs = function() {
                  // Create array to store outputs in
                  var outputs = [];
                  // Loop through all output nodes in network
                  for (var i = 0; i < this.node_types.output.length; i++) {
                        // Add value of output node to array
                        outputs.push(this.find_node(this.node_types.output[i]).value);
                  }
                  // Return array of outputs
                  return outputs;
            }

            // Run one iteration of calculations for node values in network
            this.update = function(config) {
                  // If config object is missing, create one
                  if (!config) {
                        config = {};
                  }
                  // If no number of iterations is provided, set to default (1)
                  if (!config.iterations) {
                        config.iterations = 1;
                  }
                  // If number of iterations is provided and is not a number, log an error and set to default (1)
                  else if (typeof(config.iterations) != "number") {
                        console.error("Number of iterations must be a number.");
                        config.iterations = 1;
                  }
                  // If no console log status is provided, set to default (false)
                  if (!config.logs) {
                        config.logs = false;
                  }
                  for (var i = 0; i < config.iterations; i++) {
                        // Create a clone of the network so that all nodes can be updated simultaneously, without affecting other values
                        var network_buffer = clone(this);
                        // Reset node values
                        for (var j = 0; j < this.nodes.length; j++) {
                              var node = this.nodes[j];
                              var type = node.type;
                              if (type == "Data/Output" || type == "Operation/Addition") {
                                    node.value = 0;
                              }
                              // Set value of multiplication nodes to 1 so that they can be multiplied by the value of each source node to calculate the product
                              else if (type == "Operation/Multiplication") {
                                    node.value = 1;
                              }
                        }
                        for (var j = 0; j < this.connections.length; j++) {
                              // Store type of node in variable
                              var type = this.find_node(this.connections[j].destination).type;
                              // Values for output and addition nodes can be calculated by adding together all of their inputs
                              if (type == "Data/Output" || type == "Operation/Addition") {
                                    this.find_node(this.connections[j].destination).value +=
                                          network_buffer.find_node(network_buffer.connections[j].source).value;
                              }
                              // Values for multiplication nodes can be calculated by multiplying together all of their inputs
                              else if (type == "Operation/Multiplication") {
                                    this.find_node(this.connections[j].destination).value *=
                                          network_buffer.find_node(network_buffer.connections[j].source).value;
                              }
                        }
                        // Remove placeholder value from multiplication nodes
                        for (var j = 0; j < this.nodes.length; j++) {
                              var node = this.nodes[j];
                              if (node.type == "Operation/Multiplication" && node.value == 1) {
                                    node.value = 0;
                              }
                        }
                        // Log current iteration number and network to console
                        if (config.logs) {
                              console.log("Iteration " + (i + 1) + " complete.", this);
                        }
                  }
                  // Log network to console after updating process is completed
                  if (config.logs) {
                        console.log("Node values updated for " + config.iterations + " iterations.", this);
                  }
                  // Return updated network object
                  return this;
            }

            // Mutate node values and topology/structure of network
            this.mutate = function(config) {
                  if (typeof(config.mutation_rate) !== "number") {
                        console.error("Mutation rate must be a number.");
                  } else if (config.mutation_rate < 0) {
                        console.error("Mutation rate of " + config.mutation_rate + " is too low. Mutation rate must be between 0 and 1.");
                  } else if (config.mutation_rate > 1) {
                        console.error("Mutation rate of " + config.mutation_rate + " is too high. Mutation rate must be between 0 and 1.");
                  } else {
                        for (var i = 0; i < this.node_types.value.length; i++) {
                              if (random(0, 1) < config.mutation_rate) {
                                    this.find_node(this.node_types.value[i]).value += random(-config.mutation_size,
                                          config.mutation_size
                                    );
                              }
                        }
                        // for (var i = 0; i < 5; i++) {
                        //       array.splice(Math.round(random(0, )), 1);
                        // }

                        // Add nodes to network
                        // Add value nodes to network
                        for (var i = 0; i < Math.round(random(1, 2)); i++) {
                              this.nodes.push(
                                    new cs.node({
                                          "network": this,
                                          "type": "Data/Value",
                                          "value": random(-1, 1)
                                    })
                              );
                        }
                        // Add addition nodes to network
                        for (var i = 0; i < Math.round(random(1, 2)); i++) {
                              this.nodes.push(
                                    new cs.node({
                                          "network": this,
                                          "type": "Operation/Addition"
                                    })
                              );
                        }
                        // Add multiplication nodes to network
                        for (var i = 0; i < Math.round(random(1, 2)); i++) {
                              this.nodes.push(
                                    new cs.node({
                                          "network": this,
                                          "type": "Operation/Multiplication"
                                    })
                              );
                        }
                        // Remove nodes from network
                        for (var i = 0; i < Math.round(random(1, 2)); i++) {
                              if (this.node_types.value.length > 0) {
                                    this.remove_node(random_item(this.node_types.value));
                              }
                        }

                        // Add connections to network
                        for (var i = 0; i < Math.round(random(1, 2)); i++) {
                              this.connections.push(
                                    // Create a new connection with the constructor function
                                    new cs.connection({
                                          // Connection sources must be nodes with outputs
                                          "source": this.find_node(random_item(this.node_outputs)).id,
                                          // Connection destinations must be nodes with inputs
                                          "destination": this.find_node(random_item(this.node_inputs)).id
                                    })
                              );
                        }
                        // Remove connections from network
                        for (var i = 0; i < Math.round(random(1, 2)); i++) {
                              this.remove_connection(random_item(this.connections).id);
                        }
                  }

                  // Return mutated network
                  return this;
            };

            // Evolve network using supervised learning to match a given set of inputs to a given set of outputs
            this.evolve = function(config) {
                  var network = this;
                  for (var i = 0; i < config.iterations; i++) {
                        var population = new Array(config.population);
                        for (var j = 0; j < population.length; j++) {
                              population[j] = clone(network);
                        }
                        // Loop through entire population
                        for (var j = 0; j < population.length; j++) {
                              // Mutate network
                              population[j].mutate({
                                    "mutation_rate": 0.5,
                                    "mutation_size": 0.001
                              });

                              // Reset network score/fitness
                              population[j].score = 0;
                              for (var r = 0; r < config.inputs.length; r++) {
                                    population[j].set_inputs(config.inputs[r]);
                                    population[j].update({
                                          "iterations": 1
                                    });
                                    population[j].score += Math.abs(average(difference(population[j].get_outputs(), config.outputs[r]))) / config.inputs.length;
                              }
                        }
                        // Find best score from population
                        var best_score = Math.min.apply(
                              Math, population.map(
                                    function(x) {
                                          return x.score;
                                    }
                              )
                        );
                        // Find network of population with best score
                        var best_network = population.find(
                              function(x) {
                                    return x.score == best_score;
                              }
                        );
                        console.log(best_score);
                        network = best_network;
                  }
                  return network;
            }

            // Add network to global list of networks
            cs.all.networks.push(this);
      }
}