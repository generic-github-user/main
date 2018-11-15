// lookup.js


// Test 1

// Generate list of 100 random nodes
var nodes = new Array(100).fill({
      "id": cs.UUID(),
      "value": cs.random()
});
var node;

// Start timer
console.time("Test 1");
// Find node by ID
node = nodes.find(x => x.id == nodes[49].id);
// Stop timer
console.timeEnd("Test 1");

// Test 2

nodes = {};
// Initialize ID variable
var id;
// Generate 100 nodes
for (var i = 0; i < 100; i++) {
      // Generate random UUID
      id = cs.UUID();
      // Set node as property of nodes object
      nodes[id] = {
            "id": id,
            "value": cs.random()
      };
}

// Start timer
console.time("Test 2");
// Get node with object key
node = nodes[nodes[id].id];
// Stop timer
console.timeEnd("Test 2");

// TODO:
// Add testing loop
// Run benchmark and collect data