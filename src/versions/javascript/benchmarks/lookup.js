// lookup.js

var nodes = new Array(100).fill({
      "id": cs.UUID(),
      "value": cs.random()
});
var node;

console.time("Test 1");
node = nodes.find(x => x.id == nodes[49].id);
console.timeEnd("Test 1");

nodes = {};
var id;
for (var i = 0; i < 100; i++) {
      id = cs.UUID();
      nodes[id] = {
            "id": id,
            "value": cs.random()
      };
}

console.time("Test 2");
node = nodes[nodes[id].id];
console.timeEnd("Test 2");