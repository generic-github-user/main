const random = function (minimum, maximum) {
      return minimum + (Math.random() * (maximum - minimum));
}
const random_item = function (array) {
      return array[Math.floor(Math.random() * array.length)];
}
const UUID = function () {
      function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
      }
      return s4() + s4() + "-" + s4() + "-" + s4() + "-" + s4() + "-" + s4() + s4() + s4();
}
const get_node = function (id) {
      return nodes.find(x => x.id == id);
}

var nodes = [];
var node_inputs = [];
var node_outputs = [];
class Node {
      constructor(information) {
            this.type = information.type;
            if (information.type == "Data/Input") {
                  this.output = undefined;
                  node_outputs.push(this.output);
            }
            else if (information.type == "Data/Output") {
                  this.inputs = [];
                  node_inputs.push(this.inputs);
                  this.output = 0;
                  node_outputs.push(this.output);
            }
            else if (information.type == "Data/Value") {
                  this.output = information.value;
                  node_outputs.push(this.output);
            }
            else if (information.type == "Operation/Addition") {
                  this.inputs = [];
                  node_inputs.push(this.inputs);
                  this.output = undefined;
                  node_outputs.push(this.output);
            }
            else if (information.type == "Operation/Multiplication") {
                  this.inputs = [];
                  node_inputs.push(this.inputs);
                  this.output = undefined;
                  node_outputs.push(this.output);
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

class Connection {
      constructor(source, destination) {
            this.source = source;
            this.destination = destination;
      }
}

class Network {
      constructor(inputs, outputs) {
            var nodes = [];
            node_inputs = [];
            node_outputs = [];
            for (var i = 0; i < inputs; i ++) {
                  nodes.push(
                        new Node({
                              "type": "Data/Input"
                        })
                  );
            }
            for (var i = 0; i < outputs; i ++) {
                  nodes.push(
                        new Node({
                              "type": "Data/Output"
                        })
                  );
            }
            for (var i = 0; i < Math.round(random(0, 5)); i ++) {
                  nodes.push(
                        new Node({
                              "type": "Data/Value",
                              "value": random(0, 1)
                        })
                  );
            }
            for (var i = 0; i < Math.round(random(0, 5)); i ++) {
                  nodes.push(
                        new Node({
                              "type": "Operation/Addition"
                        })
                  );
            }
            for (var i = 0; i < Math.round(random(0, 5)); i ++) {
                  nodes.push(
                        new Node({
                              "type": "Operation/Multiplication"
                        })
                  );
            }
            this.nodes = nodes;
            this.node_inputs = node_inputs;
            this.node_outputs = node_outputs;

            var connections = [];

            for (var i = 0; i < Math.round(random(0, 5)); i ++) {
                  connections.push(
                        new Connection(
                              random_item(node_outputs),
                              random_item(node_inputs)
                        )
                  );
            }
            this.connections = connections;
      }
}

var settings = {
      "population_size": 100
};

var population = [];

for (var i = 0; i < settings.population_size; i ++) {
      population.push(new Network(5, 5));
}
