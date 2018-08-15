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
      function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
      }
      return s4() + s4() + "-" + s4() + "-" + s4() + "-" + s4() + "-" + s4() + s4() + s4();
}
// Clone an object so that the new object does not contain a reference to the original object; either object may be altered without affecting the other
const clone = function (object) {
      return JSON.parse(JSON.stringify(object));
}

// Find a node globally given its ID
const get_node = function (id) {
      return nodes.find(x => x.id == id);
}

var nodes = [];
var node_inputs = [];
var node_outputs = [];
class node {
      constructor(information) {
            this.type = information.type;
            if (information.type == "Data/Input") {
                  this.output = 0;
                  node_outputs.push(this);
            }
            else if (information.type == "Data/Output") {
                  this.inputs = [];
                  node_inputs.push(this);
                  this.output = 0;
                  node_outputs.push(this);
            }
            else if (information.type == "Data/Value") {
                  this.output = information.value;
                  node_outputs.push(this);
            }
            else if (information.type == "Operation/Addition") {
                  this.inputs = [];
                  node_inputs.push(this);
                  this.output = 0;
                  node_outputs.push(this);
            }
            else if (information.type == "Operation/Multiplication") {
                  this.inputs = [];//
                  node_inputs.push(this);
                  this.output = 1;
                  node_outputs.push(this);
            }
            else {

            }

            var id = UUID();
            do {id = UUID();}
            while (nodes.find(x => x.id == id) !== undefined)

            this.id = id;
            nodes.push(this);
      }
}

class connection {
      constructor(source, destination) {
            this.source = source;
            this.destination = destination;
      }
}

class network {
      constructor(inputs, outputs) {
            var nodes = [];
            node_inputs = [];
            node_outputs = [];
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

            var connections = [];
            for (var i = 0; i < Math.round(random(100, 200)); i ++) {
                  connections.push(
                        new connection(
                              random_item(node_outputs),
                              random_item(node_inputs)
                        )
                  );
            }
            this.connections = connections;

            this.update = function () {
                  var network_buffer = clone(this);
                  for (var i = 0; i < network_buffer.connections.length; i ++) {
                        // This or network_buffer
                        var type = this.connections[i].destination.type;
                        if (type == "Data/Output" || type == "Operation/Addition") {
                              this.connections[i].destination.output +=
                              network_buffer.connections[i].source.output;
                        }
                        else if (type == "Operation/Multiplication") {
                              this.connections[i].destination.output *=
                              network_buffer.connections[i].source.output;
                        }
                  }
                  return this;
            }
      }
}

var settings = {
      "population_size": 100
};

var population = [];

for (var i = 0; i < settings.population_size; i ++) {
      population.push(new network(5, 5));
}
