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
      constructor(type) {
            this.type = type;
            this.inputs = [];
            this.output = undefined;

            var id = UUID();

            do {
                  id = UUID();
            }
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
                  nodes.push(new Node("Data/Input"));
            }
            for (var i = 0; i < outputs; i ++) {
                  nodes.push(new Node("Data/Output"));
            }
            this.nodes = nodes;
      }
}
