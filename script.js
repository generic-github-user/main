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
      return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
}
const get_node = function (id) {
      return nodes.find(x => x.id == id);
}

var nodes = [];
class Node {
      constructor(information) {
            this.type = information.type;
            if (information.type == "Data/Input") {
                  this.output = undefined;
            }
            else if (information.type == "Data/Output") {
                  this.inputs = [];
                  this.output = undefined;
            }
            else if (information.type == "Data/Value") {
                  this.output = value;
            }
            else if (information.type == "Operation/Addition") {
                  this.inputs = [];
                  this.output = undefined;
            }
            else if (information.type == "Operation/Multiplication") {
                  this.inputs = [];
                  this.output = undefined;
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
      }
}

class Network {
      constructor(inputs, outputs) {
            var nodes = [];
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
            for (var i = 0; i < Math.floor(random(0, 5)); i ++) {
                  nodes.push(
                        new Node({
                              "type": "Data/Value",
                              "value": random(0, 1)
                        })
                  );
            }
            this.nodes = nodes;
      }
}
