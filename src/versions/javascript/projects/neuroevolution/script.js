// var x = [1, 2, 3, 4, 5];
var x = [
      [1],
      [2],
      [3],
      [4],
      [5]
];
var y = [
      [1],
      [4],
      [9],
      [16],
      [25]
];

var network = new cs.network({
      "inputs": 1,
      "outputs": 1,
      "nodes": {
            "Data/Value": {
                  "num": 3,
                  "init": [-1, 1]
            },
            "Operation/Addition": {
                  "num": 3
            },
            "Operation/Multiplication": {
                  "num": 3
            }
      },
      "connections": 0
});