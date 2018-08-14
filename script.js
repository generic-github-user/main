const random = function (minimum, maximum) {
      return minimum + (Math.random() * (maximum - minimum));
}
const random_item = function (array) {
      return array[Math.floor(Math.random() * array.length)];
}

class Node {
      constructor(type) {
            this.type = type;
            this.inputs = [];
            this.output;
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
