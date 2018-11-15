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

cs.node_types = function(name) {
      // Log error message to console
      console.error("Node type " + name + " does not exist. Please select a node type from the list of supported node types.");
      // List supported node types in console
      console.log("Supported node types:");
      for (var i = 2; i < cs.settings.node_types.length; i++) {
            console.log(cs.settings.node_types[i].name);
      }
}

cs.help = function() {
      console.log("Find documentation for Caesium on the GitHub page.", "https://github.com/generic-github-user/Caesium");
      // console.log("Full list of available help commands:");
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
      return id;
}

// Node class
cs.node = class {
      constructor(config) {
            this.type = config.type;

            // Create value node
            if (this.type == "Value") {
                  this.value = config.value;
            } else {
                  this.value = 0;
            }
      }
}

// Connection class
cs.connection = class {
      // Constructor for creating a connection between two nodes within a network
      constructor(config) {
            this.id = cs.UUID();
            this.weight = config.weight;

            this.source = config.source;
            this.destination = config.destination;
      }
}

// Network class
cs.network = class {
      // Constructor for creating a network or computation graph
      constructor(config) {
            // Assign a random ID to the the new network object
            this.id = cs.UUID();
            // Number of input nodes in the network
            this.inputs = config.inputs;
            // Number of output nodes in the network
            this.outputs = config.outputs;

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
            for (var i = 0; i < cs.settings.node_types.length; i++) {
                  this.node_types[cs.settings.node_types[i].name] = [];
            }

            this.add_node = function(config) {
                  // Create UUID for node
                  var id = cs.UUID();

                  var node = new cs.node({
                        "type": config.type,
                        "value": config.value
                  });
                  this.nodes[id] = node;

                  // Create input node
                  if (node.type == "Input" || node.type == "Value") {
                        this.node_outputs.push(id);
                  } else {
                        this.node_inputs.push(id);
                        this.node_outputs.push(id);
                  }

                  this.node_types[node.type].push(id);
            }

            for (var i = 0; i < this.inputs; i++) {
                  this.add_node({
                        "type": "Input"
                  });
            }
            for (var i = 0; i < this.outputs; i++) {
                  this.add_node({
                        "type": "Output"
                  });
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
                                    "value": cs.min_max(config.nodes[attr].init)
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
            // Remove a node from the network, given its ID
            this.remove_node = function(id) {
                  // Remove node from main network nodes list
                  delete this.nodes[id];
                  // Remove node ID from node type lists
                  for (var attr in this.node_types) {
                        cs.remove(this.node_types[attr], id);
                  }
                  // // Remove() all instances

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
            // Remove a connection from the network, given its ID
            this.remove_connection = function(id) {
                  this.connections.splice(this.connections.indexOf(this.find_connection(id)), 1);
            }

            // Generate random connections between nodes
            for (var i = 0; i < Math.round(cs.min_max(config.connections.num)); i++) {
                  this.add_connection({
                        "weight": cs.min_max(config.connections.init)
                  });
            }

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
                              this.nodes[this.node_types["Input"][i]].value = inputs[i];
                        }
                        return this;
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
                        // var network_buffer = cs.clone(this);
                        var network_buffer = this;
                        // Reset node values
                        for (var attr in this.nodes) {
                              var node = this.nodes[attr];
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
                              var input_value = network_buffer.nodes[network_buffer.connections[j].source].value * this.connections[j].weight;
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
                        for (attr in this.nodes) {
                              var node = this.nodes[attr];

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
                  // Reset mutable network values
                  this.reset();
                  // Set values of input nodes of network to input data set
                  this.set_inputs(config.input);
                  // Update the network
                  this.update(config.update);
                  // Return outputs from network
                  return this.get_outputs();
            }

            // Mutate node values and topology/structure of network
            this.mutate = function(config) {
                  if (!config) {
                        var config = {};
                  }
                  if (!config.mutation_rate) {
                        config.mutation_rate = 0.5;
                  }
                  if (!config.mutation_size) {
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

                  if (typeof(config.mutation_rate) != "number") {
                        console.error("Mutation rate must be a number.");
                  } else if (config.mutation_rate < 0) {
                        console.error("Mutation rate of " + config.mutation_rate + " is too low. Mutation rate must be between 0 and 1.");
                  } else if (config.mutation_rate > 1) {
                        console.error("Mutation rate of " + config.mutation_rate + " is too high. Mutation rate must be between 0 and 1.");
                  } else {
                        for (var i = 0; i < config.iterations; i++) {
                              for (var j = 0; j < this.node_types["Value"].length; j++) {
                                    if (cs.random() < config.mutation_rate) {
                                          this.nodes[this.node_types["Value"][j]].value += cs.random(-config.mutation_size, config.mutation_size);
                                    }
                              }

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
                                                            "value": cs.min_max(config.nodes[attr].init)
                                                      });
                                                }
                                          }
                                          // Remove nodes from network
                                          for (var j = 0; j < Math.round(cs.min_max(config.nodes[attr].remove)); j++) {
                                                // Check if network has any nodes
                                                if (this.node_types[node_type.name].length > 0) {
                                                      this.remove_node(cs.random_item(this.node_types[node_type.name]));
                                                }
                                          }
                                    }
                                    // If the node type does not exist, log an error
                                    else {
                                          cs.node_types(attr);
                                    }
                              }

                              // Add connections to network
                              for (var j = 0; j < Math.round(cs.min_max(config.connections.add)); j++) {
                                    // Check if total number of connections in network reaches the limit
                                    if (this.connections.length < config.connections.limit) {
                                          this.add_connection({
                                                "weight": cs.min_max(config.connections.init)
                                          });
                                    }
                              }
                              // Remove connections from network
                              for (var j = 0; j < Math.round(cs.min_max(config.connections.remove)); j++) {
                                    // Check if network has any connections
                                    if (this.connections.length > 0) {
                                          this.remove_connection(cs.random_item(this.connections).id);
                                    }
                              }

                              for (var j = 0; j < this.connections.length; j++) {
                                    if (cs.random() < config.connections.value.mutation_rate) {
                                          this.connections[j].value += cs.random(-config.connections.value.mutation_size, config.connections.value.mutation_size);
                                    }
                              }
                        }
                  }

                  // Return mutated network
                  return this;
            };

            // Evolve network using supervised learning to match a given set of inputs to a given set of outputs
            this.evolve = function(config) {
                  var start_time = performance.now();
                  if (config.log) {
                        console.log("Training network.", this);
                  }
                  // Temporary network object to store best network from population in
                  var network = this;
                  // Repeat evolution process for provided number of iterations (generations)
                  for (var i = 0; i < config.iterations; i++) {
                        // Create array to store "population" of networks in
                        var population = new Array(config.population);
                        // Fill population array with clones of network
                        for (var j = 0; j < population.length; j++) {
                              population[j] = cs.clone(network);
                        }
                        // Loop through entire population
                        for (var j = 0; j < population.length; j++) {
                              // Mutate network
                              population[j].mutate(config.mutate);

                              // Reset network score/fitness
                              population[j].score = 0;
                              // Loop through each set of inputs
                              for (var r = 0; r < config.inputs.length; r++) {
                                    var y = population[j].evaluate({
                                          "input": config.inputs[r],
                                          "update": config.update
                                    });
                                    // Calculate fitness score of network
                                    // |avg(y - x)|
                                    population[j].score += cs.average(
                                          cs.apply(
                                                cs.difference(
                                                      y,
                                                      config.outputs[r]
                                                ),
                                                Math.abs
                                          )
                                    ) / config.inputs.length;
                              }
                        }

                        // Find best score from population
                        // Find network of population with best score
                        var best_network = population[0];
                        for (var j = 0; j < population.length; j++) {
                              if (population[j].score < best_network.score) {
                                    best_network = population[j];
                              }
                        }

                        network = cs.clone(best_network);
                        if (config.log) {
                              console.log("Iteration " + (i + 1) + " complete.", network.score, network);
                        }
                  }
                  var end_time = performance.now();

                  if (config.log) {
                        console.log(config.iterations + " training iterations complete in " + Math.round(end_time - start_time) + " milliseconds.", network);
                        // console.log(network.evaluate({
                        //       "input": config.inputs[0],
                        //       "update": update_settings
                        // }));
                  }
                  if (config.return == "all") {
                        return {
                              "population": population,
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