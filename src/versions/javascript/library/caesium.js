// Caesium

"use strict";

// Global Caesium library object
window.cs = {
      // List of all networks
      "networks": [],
      // Settings for networks
      "settings": {
            "node_types": [{
                        "name": "Input"
                  },
                  {
                        "name": "Output"
                  },
                  {
                        "name": "Value"
                  },
                  {
                        "name": "Addition"
                  },
                  {
                        "name": "Multiplication"
                  },
                  {
                        "name": "Tanh"
                  },
                  {
                        "name": "Sine"
                  },
                  {
                        "name": "Cosine"
                  },
                  {
                        "name": "Abs"
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

cs.alias = function(variable) {
      window[variable] = cs;
}

// Generate a random number in between a minimum value and a maximum value
cs.random = function(minimum, maximum) {
      if (minimum == undefined && maximum == undefined) {
            return Math.random();
      } else {
            return minimum + (Math.random() * (maximum - minimum));
      }
}

// Select a random element from a given array
cs.random_item = function(array) {
      return array[Math.floor(Math.random() * array.length)];
}

// Deep clone an object so that the new object does not contain a reference to the original object; either object may be altered without affecting the other
// IDs of nodes and connections cloned networks do not need to be regenerated because they are only used to find nodes and connections from that specific network
// https://stackoverflow.com/a/728694
cs.clone = function(object) {
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
                  copy[i] = cs.clone(object[i]);
            }
            return copy;
      }

      // Handle Object
      if (object instanceof Object) {
            copy = {};
            for (var attr in object) {
                  if (object.hasOwnProperty(attr)) copy[attr] = cs.clone(object[attr]);
            }
            return copy;
      }

      throw new Error("Unable to copy obj! Its type isn't supported.");
}

cs.clone_2 = function(object) {
      return JSON.parse(JSON.stringify(object));
}

cs.clone_network = function(network) {
      var cloned = cs.clone(network);
      cloned.id = cs.UUID();
      return cloned;
}

// Find a network globally given its ID
cs.get_network = function(id) {
      return cs.networks.find(x => x.id == id);
}

// Find the difference between two arrays and return another array
cs.difference = function(array_1, array_2) {
      return array_2.map(
            (element, i) => {
                  return element - array_1[i];
            }
      )
}

// Find the sum of all elements of an array of numbers
cs.sum = function(array) {
      var sum = 0;
      for (var i = 0; i < array.length; i++) {
            sum += array[i];
      };
      return sum;
}

// Find the average of all elements of an array of numbers
cs.average = function(array) {
      return cs.sum(array) / array.length;
}

// Remove a given element from an array
cs.remove = function(array, element) {
      var index = array.indexOf(element);
      if (index != -1) {
            array.splice(index, 1);
      }
}

cs.min_max = function(variable) {
      var num;
      if (variable instanceof Array) {
            num = cs.random(
                  variable[0],
                  variable[1]
            );
      } else if (variable instanceof Object) {
            num = cs.random(
                  variable.min,
                  variable.max
            );
      } else if (typeof(variable) == "number") {
            num = variable;
      }
      return num;
}

cs.apply = function(array, func) {
      return array.map(x => func(x));
}

cs.encode = {};
cs.decode = {};

cs.encode.integer = function(input, charset, length) {
      var output = [];
      for (var i = 0; i < length; i++) {
            output.push(charset.indexOf(input[i]));
      }
      return output;
}

cs.decode.integer = function(input, charset) {
      var output = "";
      for (var i = 0; i < input.length; i++) {
            var character = charset[input[i]];
            if (!character) {
                  character = "";
            }
            output += character;
      }
      return output;
}

// Converting a string to and from a one-hot encoded binary vector

// Accepts a string and returns an array of 1s and 0s
cs.encode.one_hot = function(input, charset, length) {
      // Define output as a variable containing an empty array
      var output = [];
      // Loop through each character of the input string
      for (var i = 0; i < length; i++) {
            // Loop through each possible character
            charset.forEach(
                  char => {
                        // Check for a match between the current input character and the current character from the list; if there is a match, add a 1 to the output array
                        if (input[i] == char) {
                              output.push(1);
                        }
                        // If there is no match, add a 0 to the output array
                        else {
                              output.push(0);
                        }
                  }
            )
      }
      // Return output array
      return output;
}

// Accepts an array of 1s and 0s as an input and returns a string
cs.decode.one_hot = function(input, charset) {
      // Define output as a variable containing an empty string
      var output = "";
      // Loop through each character of the input string
      for (var i = 0; i < input.length; i++) {
            // Check value of current element of input array
            if (input[i] == 1) {
                  output += charset[i % charset.length];
            }
      }
      // Return output string
      return output;
}

cs.node_types = function(name) {
      // Log error message to console
      console.error("Node type " + name + " does not exist. Please select a node type from the list of supported node types.");
      // List supported node types in console
      console.log("Supported node types:");
      for (var i = 2; i < cs.settings.node_types.length; i++) {
            console.log(cs.settings.node_types[i].name);
      }
}

cs.help = function(thing) {
      if (thing == undefined) {
            console.log("Find documentation for Caesium on the GitHub page.", "https://github.com/generic-github-user/Caesium");
            console.log("Use either cs.help(function) or function.help() to get help with a specific Caesium function.");

            console.log("Full list of available help commands:");
            console.log("cs.node.help()");
            console.log("cs.connection.help()");
            console.log("cs.network.help()");
      } else {
            thing.help();
      }
}

// Generate a random UUID
// Based on https://stackoverflow.com/a/105074
cs.UUID = function() {
      // Generate a random string of four hexadecimal digits
      function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
                  .toString(16)
                  .substring(1);
      }
      // Generate UUID from substrings
      var id = s4() + s4() + "-" + s4() + "-" + s4() + "-" + s4() + "-" + s4() + s4() + s4();
      // Return generated ID
      return id;
}

// Node class
cs.node = class {
      // Node constructor object
      constructor(config) {
            if (config == undefined) {
                  // Error is logged instead of creating a config object because certain parameters must be provided
                  console.error("Please provide a config object.");
            }
            // Only check for node type if config object was provided
            else if (config.type == undefined) {
                  console.error("Please provide a node type.");
            }
            // Valid config object with node type was provided
            else {
                  // Set type of node
                  this.type = config.type;

                  // Create value (bias) node
                  if (this.type == "Value") {
                        // If no value is provided, set to default value (1)
                        if (config.value == undefined) {
                              config.value = 1;
                        }
                        // Set value of value node
                        this.value = cs.min_max(config.value);
                  } else {
                        // Non-value nodes start with a value of 0
                        this.value = 0;
                  }
            }
      }
      // help: function() {
      //       console.log("Node help");
      // }
}

// Connection class
cs.connection = class {
      // Constructor for creating a connection between two nodes within a network
      constructor(config) {
            // Check for config object
            if (config == undefined) {
                  console.error("Please provide a config object.");
            }
            // Connection source and destination only need to be checked if a config object was provided
            else if (config.source == undefined) {
                  console.error("Please provide a source node for the connection.");
            } else if (config.destination == undefined) {
                  console.error("Please provide a config object.");
            }
            // Valid config object with source and destination node IDs was provided
            else {
                  // If no weight value is provided, set to default value (1)
                  if (config.weight == undefined) {
                        config.weight = 1;
                  }

                  // Generate random ID for connection
                  this.id = cs.UUID();
                  // Set connection weight
                  this.weight = cs.min_max(config.weight);

                  // Set source node of connection
                  this.source = config.source;
                  // Set destination node of connection
                  this.destination = config.destination;
            }
      }
}

// Network class
cs.network = class {
      // Constructor for creating a network or computation graph
      constructor(config) {
            // if (config == undefined) {
            //       console.error("Please provide a config object.");
            // }
            // else if () {

            // Assign a random ID to the the new network object
            this.id = cs.UUID();

            // List of nodes in network
            this.nodes = {};
            // List of connections in network
            this.connections = [];

            // List of nodes with inputs in network
            this.node_inputs = [];
            // List of nodes with outputs in network
            this.node_outputs = [];

            // Score used for evolutionary optimization algorithm
            this.score = 0;

            // Lists of specific node types in the network
            this.node_types = {};
            // Loop through all node types in settings
            for (var i = 0; i < cs.settings.node_types.length; i++) {
                  // Create array to store type of node
                  this.node_types[cs.settings.node_types[i].name] = [];
            }

            // Add a node to the network
            this.add_node = function(config) {
                  if (config == undefined) {
                        console.error("Please provide a config object.");
                  } else {
                        // Create UUID for node
                        var id = cs.UUID();

                        // Create a node with config object using the node constructor
                        var node = new cs.node(config);
                        // Set node as value of property of network.nodes
                        this.nodes[id] = node;

                        // Input nodes and value nodes only have outputs
                        if (node.type == "Input" || node.type == "Value") {
                              this.node_outputs.push(id);
                        }
                        // All other nodes have inputs and outputs
                        else {
                              this.node_inputs.push(id);
                              this.node_outputs.push(id);
                        }

                        // Add node ID to respective node type list
                        this.node_types[node.type].push(id);
                  }
            }

            // Loop through all defined node types in config object
            for (var attr in config.nodes) {
                  // Search node types list for node type
                  var node_type = cs.settings.node_types.find(x => x.name == attr);
                  // If the node type does exist, add the set number of nodes to the network
                  if (node_type != undefined) {
                        // Add nodes to network
                        for (var i = 0; i < Math.round(cs.min_max(config.nodes[attr].num)); i++) {
                              // Create new node
                              this.add_node({
                                    "type": attr,
                                    "value": config.nodes[attr].init
                              });
                        }
                  }
                  // If the node type does not exist, log an error
                  else {
                        cs.node_types(attr);
                  }
            }

            // These functions must be defined before the connection generation code so they can be used there
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
            // Add a new random connection to the network
            this.add_connection = function(config) {
                  // If config object is missing, log an error
                  if (config == undefined) {
                        console.error("Please provide a config object.");
                  } else {
                        // Push connection to network's connection array
                        this.connections.push(
                              // Create a new connection with the constructor function
                              new cs.connection({
                                    "weight": config.weight,
                                    // Connection sources must be nodes with outputs
                                    "source": cs.random_item(this.node_outputs),
                                    // Connection destinations must be nodes with inputs
                                    "destination": cs.random_item(this.node_inputs)
                              })
                        );
                  }
            }
            // Remove a node from the network, given its ID
            this.remove_node = function(config) {
                  // If config object is missing, log an error
                  if (config == undefined) {
                        console.error("Please provide a config object.");
                  } else if (config.id == undefined) {
                        console.error("Missing ID of node to remove from network.");
                  } else {
                        var id = config.id;

                        // Remove node from main network nodes list
                        delete this.nodes[id];
                        // Remove node ID from node type lists
                        for (var attr in this.node_types) {
                              cs.remove(this.node_types[attr], id);
                        }

                        // Remove node ID from list of nodes with inputs
                        cs.remove(this.node_inputs, id);
                        // Remove node ID from list of nodes with outputs
                        cs.remove(this.node_outputs, id);

                        // Find connections that have the removed node as a source
                        var dead_connections = this.connections.filter(x => x.source == id).concat(this.connections.filter(x => x.destination == id));
                        // Loop through list of dead connections
                        for (var i = 0; i < dead_connections.length; i++) {
                              // Remove connection
                              cs.remove(this.connections, dead_connections[i]);
                        }
                  }
            }
            // Remove a connection from the network, given its ID
            this.remove_connection = function(config) {
                  // If config object is missing, log an error
                  if (config == undefined) {
                        console.error("Please provide a config object.");
                  } else if (config.id == undefined) {
                        console.error("Missing ID of connection to remove from network.");
                  } else {
                        this.connections.splice(this.connections.indexOf(this.find_connection(config.id)), 1);
                  }
            }

            // Generate random connections between nodes
            for (var i = 0; i < Math.round(cs.min_max(config.connections.num)); i++) {
                  this.add_connection({
                        "weight": config.connections.init
                  });
            }

            // Function for setting input data of network
            this.set_inputs = function(config) {
                  if (config.inputs == undefined) {
                        console.error("Inputs for the network must be provided.");
                  } else {
                        var num_inputs = this.node_types["Input"].length;

                        if (config.inputs.length < num_inputs) {
                              console.error("The number of inputs you have provided (" + config.inputs.length + ") is fewer than the number of input nodes in the network (" + num_inputs + "). Please provide " + num_inputs + " inputs.");
                              return false;
                        } else if (config.inputs.length > num_inputs) {
                              console.error("The number of inputs you have provided (" + config.inputs.length + ") is greater than the number of input nodes in the network (" + num_inputs + "). Please provide " + num_inputs + " inputs.");
                              return false;
                        } else if (config.inputs.length == num_inputs) {
                              for (var i = 0; i < config.inputs.length; i++) {
                                    this.nodes[this.node_types["Input"][i]].value = config.inputs[i];
                              }
                              return this;
                        }
                  }
            }

            // Function for retrieving outputs from network
            this.get_outputs = function() {
                  // Create array to store outputs in
                  var outputs = [];
                  // Loop through all output nodes in network
                  for (var i = 0; i < this.node_types["Output"].length; i++) {
                        // Add value of output node to array
                        outputs.push(this.nodes[this.node_types["Output"][i]].value);
                  }
                  // Return array of outputs
                  return outputs;
            }

            // Reset values of mutable nodes in network
            this.reset = function() {
                  // Loop through network node list
                  for (var attr in this.nodes) {
                        // Store node in variable
                        var node = this.nodes[attr];
                        // If node is not a value node, reset value of node to 0
                        if (node.type != "Value") {
                              node.value = 0;
                        }
                  }
                  // Return updated network object
                  return this;
            }

            // Run one iteration of calculations for node values in network
            this.update = function(config) {
                  // If config object is missing, create one
                  if (config == undefined) {
                        config = {};
                  }
                  // If no number of iterations is provided, set to default (1)
                  if (config.iterations == undefined) {
                        config.iterations = 1;
                  }
                  // If number of iterations is provided and is not a number, log an error and set to default (1)
                  else if (typeof(config.iterations) != "number") {
                        console.error("Number of iterations must be a number.");
                        config.iterations = 1;
                  }
                  if (config.buffer == undefined) {
                        config.buffer = true;
                  }
                  // If no console log status is provided, set to default (false)
                  if (config.logs == undefined) {
                        config.logs = false;
                  }

                  for (var i = 0; i < config.iterations; i++) {
                        // Create a clone of the network so that all nodes can be updated simultaneously, without affecting other values
                        // var network_buffer = cs.clone(this);
                        if (config.buffer) {
                              var network_buffer = {};
                        }

                        // Reset node values
                        for (var attr in this.nodes) {
                              var node = this.nodes[attr];
                              if (config.buffer) {
                                    network_buffer[attr] = node.value;
                              }

                              var type = node.type;
                              if (type == "Output" || type == "Addition" || type == "Tanh" || type == "Sine" || type == "Cosine" || type == "Abs") {
                                    node.value = 0;
                              }
                              // Set value of multiplication nodes to 1 so that they can be multiplied by the value of each source node to calculate the product
                              else if (type == "Multiplication") {
                                    node.value = 1;
                              }
                        }
                        for (var j = 0; j < this.connections.length; j++) {
                              // Store type of node in variable
                              var type = this.nodes[this.connections[j].destination].type;
                              var input_value;
                              if (config.buffer) {
                                    input_value = network_buffer[this.connections[j].source];
                              } else {
                                    input_value = this[this.connections[j].source].value;
                              }
                              input_value *= this.connections[j].weight;
                              // Values for output and addition nodes can be calculated by adding together all of their inputs
                              if (type == "Output" || type == "Addition" || type == "Tanh" || type == "Sine" || type == "Cosine" || type == "Abs") {
                                    this.nodes[this.connections[j].destination].value +=
                                          input_value;
                              }
                              // Values for multiplication nodes can be calculated by multiplying together all of their inputs
                              else if (type == "Multiplication") {
                                    this.nodes[this.connections[j].destination].value *=
                                          input_value;
                              }
                        }
                        // Loop through all nodes
                        for (attr in this.nodes) {
                              var node = this.nodes[attr];

                              // Apply mathematical operations to nodes
                              if (node.type == "Tanh") {
                                    node.value = Math.tanh(node.value);
                              } else if (node.type == "Sine") {
                                    node.value = Math.sin(node.value);
                              } else if (node.type == "Cosine") {
                                    node.value = Math.cos(node.value);
                              } else if (node.type == "Abs") {
                                    node.value = Math.abs(node.value);
                              }

                              // Remove placeholder value from multiplication nodes
                              if (node.type == "Multiplication" && node.value == 1) {
                                    node.value = 0;
                              }

                              if (node.value == NaN || node.value < config.limit.min || node.value > config.limit.max) {
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

            // Run a prediction using the network on a set of input data to produce an output
            this.evaluate = function(config) {
                  if (config.input == undefined) {
                        console.error("No config object was provided.");
                  } else {
                        // Reset mutable network values
                        this.reset();
                        // Set values of input nodes of network to input data set
                        this.set_inputs({
                              "inputs": config.input
                        });
                        // Update the network
                        this.update(config.update);
                        // Return outputs from network
                        return this.get_outputs();
                  }
            }

            // Mutate node values and topology/structure of network
            this.mutate = function(config) {
                  if (config == undefined) {
                        var config = {};
                  }
                  if (config.mutation_rate == undefined) {
                        config.mutation_rate = 0.5;
                  }
                  if (config.mutation_size == undefined) {
                        config.mutation_size = 0.1;
                  }

                  // if (!config.nodes) {
                  //       config.nodes = {};
                  // }
                  // if (typeof(config.nodes) == "object") {
                  //       if (!config.nodes.value) {
                  //             config.nodes.value = {};
                  //       }
                  //       if (typeof(config.nodes.value) == "object") {
                  //             if (!config.nodes.value.add) {
                  //                   config.nodes.value.add = {};
                  //             }
                  //             if (typeof(config.nodes.value.add) == "object") {
                  //                   if (!config.nodes.value.add.min) {
                  //                         config.nodes.value.add.min = 0;
                  //                   }
                  //                   if (config.nodes.value.add.min < 0) {
                  //                         console.error("Minimum number of value nodes to add must be at least 0.");
                  //                         config.nodes.value.add.min = 0;
                  //                   }
                  //
                  //                   if (!config.nodes.value.add.max) {
                  //                         config.nodes.value.add.max = 2;
                  //                   }
                  //                   if (config.nodes.value.add.max < 0) {
                  //                         console.error("Maximum number of value nodes to add must be at least 0.");
                  //                         config.nodes.value.add.max = 2;
                  //                   }
                  //             } else if (typeof(config.nodes.value.add) == "number") {
                  //                   if (config.nodes.value.add < 0) {
                  //                         console.error("Number of value nodes to add must be at least 0.");
                  //                         config.nodes.value.add = 1;
                  //                   }
                  //             }
                  //
                  //             if (!config.nodes.value.remove) {
                  //                   config.nodes.value.remove = {};
                  //             }
                  //             if (typeof(config.nodes.value.remove) == "object") {
                  //                   if (!config.nodes.value.remove.min) {
                  //                         config.nodes.value.remove.min = 0;
                  //                   }
                  //                   if (config.nodes.value.remove.min < 0) {
                  //                         console.error("Minimum number of value nodes to remove must be at least 0.");
                  //                         config.nodes.value.remove.min = 0;
                  //                   }
                  //
                  //                   if (!config.nodes.value.remove.max) {
                  //                         config.nodes.value.remove.max = 2;
                  //                   }
                  //                   if (config.nodes.value.remove.max < 0) {
                  //                         console.error("Maximum number of value nodes to remove must be at least 0.");
                  //                         config.nodes.value.remove.max = 2;
                  //                   }
                  //             } else if (typeof(config.nodes.value.remove) == "number") {
                  //                   if (config.nodes.value.remove < 0) {
                  //                         console.error("Number of value nodes to remove must be at least 0.");
                  //                         config.nodes.value.remove = 1;
                  //                   }
                  //             }
                  //       } else if (typeof(config.nodes.value) == "number") {
                  //             if (config.nodes.value < 0) {
                  //                   console.error("Number of value nodes to add or remove must be at least 0.");
                  //             }
                  //       }
                  // }

                  // if (!config.connections) {
                  //       config.connections = {};
                  // }
                  // if (typeof(config.connections) == "object") {
                  //       if (!config.connections.add) {
                  //             config.connections.add = {};
                  //       }
                  //       if (typeof(config.connections.add) == "object") {
                  //             if (!config.connections.add.min) {
                  //                   config.connections.add.min = 0;
                  //             } else if (config.connections.add.min < 0) {
                  //                   console.error("Minimum number of connections to add must be at least 0.");
                  //                   config.connections.add.min = 0;
                  //             }
                  //
                  //             if (!config.connections.add.max) {
                  //                   config.connections.add.max = 2;
                  //             } else if (config.connections.add.max < 0) {
                  //                   console.error("Maximum number of connections to add must be at least 0.");
                  //                   config.connections.add.max = 2;
                  //             }
                  //       } else if (typeof(config.connections.add) == "number") {
                  //             if (config.connections.add < 0) {
                  //                   console.error("Number of connections to add must be at least 0.");
                  //                   config.connections.add = 1;
                  //             }
                  //       }
                  //
                  //       if (!config.connections.remove) {
                  //             config.connections.remove = {};
                  //       }
                  //       if (typeof(config.connections.remove) == "object") {
                  //             if (!config.connections.remove.min) {
                  //                   config.connections.remove.min = 0;
                  //             } else if (config.connections.remove.min < 0) {
                  //                   console.error("Minimum number of connections to remove must be at least 0.");
                  //             }
                  //
                  //             if (!config.connections.remove.max) {
                  //                   config.connections.remove.max = 2;
                  //             } else if (config.connections.remove.max < 0) {
                  //                   console.error("Maximum number of connections to remove must be at least 0.");
                  //             }
                  //       } else if (typeof(config.connections.remove) == "number") {
                  //             if (config.connections.remove < 0) {
                  //                   console.error("Number of connections to remove must be at least 0.");
                  //                   config.connections.remove = 1;
                  //             }
                  //       }
                  // } else if (typeof(config.connections) == "number") {
                  //       if (config.connections < 0) {
                  //             console.error("Number of connections to add and remove must be at least 0.");
                  //             config.connections = 1;
                  //       }
                  // }

                  // if (typeof(config.mutation_rate) != "number") {
                  //       console.error("Mutation rate must be a number.");
                  // } else if (config.mutation_rate < 0) {
                  //       console.error("Mutation rate of " + config.mutation_rate + " is too low. Mutation rate must be between 0 and 1.");
                  // } else if (config.mutation_rate > 1) {
                  //       console.error("Mutation rate of " + config.mutation_rate + " is too high. Mutation rate must be between 0 and 1.");
                  // } else {
                  for (var i = 0; i < config.iterations; i++) {
                        // Loop through all defined node types in config object
                        for (var attr in config.nodes) {
                              // Search node types list for node type
                              var node_type = cs.settings.node_types.find(x => x.name == attr);
                              // If the node type does exist, add and remove the set number of nodes
                              if (node_type != undefined) {
                                    // Add nodes to network
                                    for (var j = 0; j < Math.round(cs.min_max(config.nodes[attr].add)); j++) {
                                          // Check if total number of nodes in network reaches the limit
                                          if (this.node_types[node_type.name].length < config.nodes[attr].limit) {
                                                this.add_node({
                                                      "type": attr,
                                                      "value": config.nodes[attr].init
                                                });
                                          }
                                    }
                                    // Remove nodes from network
                                    for (var j = 0; j < Math.round(cs.min_max(config.nodes[attr].remove)); j++) {
                                          // Check if network has any nodes
                                          if (this.node_types[node_type.name].length > 0) {
                                                this.remove_node({
                                                      "id": cs.random_item(this.node_types[node_type.name])
                                                });
                                          }
                                    }
                              }
                              // If the node type does not exist, log an error
                              else {
                                    cs.node_types(attr);
                              }
                        }

                        // Mutate values of value nodes
                        for (var j = 0; j < this.node_types["Value"].length; j++) {
                              // Randomly decide whether to mutate value or not
                              if (cs.random() < config.nodes["Value"].value.mutation_rate) {
                                    // Add random/subtract amount to value
                                    this.nodes[this.node_types["Value"][j]].value += cs.random(-config.nodes["Value"].value.mutation_size, config.nodes["Value"].value.mutation_size);
                              }
                        }

                        // Add connections to network
                        for (var j = 0; j < Math.round(cs.min_max(config.connections.add)); j++) {
                              // Check if total number of connections in network reaches the limit
                              if (this.connections.length < config.connections.limit) {
                                    this.add_connection({
                                          "weight": config.connections.init
                                    });
                              }
                        }
                        // Remove connections from network
                        for (var j = 0; j < Math.round(cs.min_max(config.connections.remove)); j++) {
                              // Check if network has any connections
                              if (this.connections.length > 0) {
                                    this.remove_connection({
                                          "id": cs.random_item(this.connections).id
                                    });
                              }
                        }

                        // Mutate connection weight values
                        for (var j = 0; j < this.connections.length; j++) {
                              // Randomly decide whether to mutate weight
                              if (cs.random() < config.connections.value.mutation_rate) {
                                    // Mutate weight value by a random amount
                                    this.connections[j].weight += cs.random(-config.connections.value.mutation_size, config.connections.value.mutation_size);
                              }
                        }
                  }
                  // }

                  // Return mutated network
                  return this;
            };

            // Evolve network using supervised learning to match a given set of inputs to a given set of outputs
            this.evolve = function(config) {
                  // Record start time of envolution function for optimization and logging purposes
                  var start_time = performance.now();
                  if (config.log) {
                        console.log("Training network.", this);
                  }
                  if (config.update == undefined) {
                        config.update = {
                              "iterations": 1,
                              "limit": {
                                    "min": -10e9,
                                    "max": 10e9
                              }
                        };
                  }
                  if (config.evaluate == undefined) {
                        config.evaluate = function(network, input, output) {
                              return network.evaluate({
                                    "input": input,
                                    "update": config.update
                              })
                        }
                  }
                  // Temporary network object to store best network from population in
                  var network = this;
                  // Repeat evolution process for provided number of iterations (generations)
                  for (var i = 0; i < config.iterations; i++) {
                        // Create array to store "population" of networks in
                        var population = new Array(config.population);
                        // Fill population array with clones of network
                        for (var j = 0; j < population.length; j++) {
                              // Deep clone network
                              population[j] = cs.clone(network);
                        }
                        // Loop through entire population
                        for (var j = 0; j < population.length; j++) {
                              // Mutate network
                              population[j].mutate(config.mutate);

                              // Reset network score/fitness
                              population[j].score = 0;
                              // Loop through each set (batch) of inputs
                              for (var r = 0; r < config.inputs.length; r++) {
                                    // Evaluate population with batch of inputs
                                    var y = config.evaluate(population[j], config.inputs[r], config.outputs[r]);
                                    // Calculate fitness score of network
                                    // avg(|y - x|)
                                    population[j].score += cs.average(
                                          // Absolute value of each x-y loss value
                                          cs.apply(
                                                // Difference of xs and ys in batch
                                                cs.difference(
                                                      y,
                                                      // x value
                                                      config.outputs[r]
                                                ),
                                                Math.abs
                                          )
                                    ) / config.inputs.length;
                              }
                        }

                        // Find network from population with best score
                        // Start with first network
                        var best_network = population[0];
                        // Loop through population of networks
                        for (var j = 0; j < population.length; j++) {
                              // If score of current network is better than the score of the best network, set the best network to be the current network
                              if (population[j].score < best_network.score) {
                                    best_network = population[j];
                              }
                        }

                        network = cs.clone(best_network);
                        if (config.log) {
                              console.log("Iteration " + (i + 1) + " complete.", network.score, network);
                        }
                  }
                  // Record end time of evolution function
                  var end_time = performance.now();

                  if (config.log) {
                        console.log(config.iterations + " training iterations complete in " + Math.round(end_time - start_time) + " milliseconds.", network);
                  }
                  if (config.return == "all") {
                        // Return all relevant information from neuroevolution process
                        return {
                              // Population of networks
                              "population": population,
                              // Trained network
                              "network": network
                        }
                  } else {
                        // Return trained network after neuroevolution process
                        return network;
                  }
            }

            // Add network to global list of networks
            cs.networks.push(this);
      }
}