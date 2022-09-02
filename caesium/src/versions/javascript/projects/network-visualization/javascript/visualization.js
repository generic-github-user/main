// Change the brightness of a hexadecimal color value
// https://stackoverflow.com/a/13542669
const shade_color = function(color, percent) {
      var f = parseInt(color.slice(1), 16),
            t = percent < 0 ? 0 : 255,
            p = percent < 0 ? percent * -1 : percent,
            R = f >> 16,
            G = f >> 8 & 0x00FF,
            B = f & 0x0000FF;
      return "#" + (0x1000000 + (Math.round((t - R) * p) + R) * 0x10000 + (Math.round((t - G) * p) + G) * 0x100 + (Math.round((t - B) * p) + B)).toString(16).slice(1);
}

const to_percent = {
      "w": function(number, property) {
            return (number / svg.getBoundingClientRect().width) * 100;
      },
      "h": function(number, property) {
            return (number / svg.getBoundingClientRect().height) * 100;
      }
}

const to_pixels = {
      "w": function(number, property) {
            return (number / 100) * svg.getBoundingClientRect().width;
      },
      "h": function(number, property) {
            return (number / 100) * svg.getBoundingClientRect().height;
      }
}

const round = function(number, decimals) {
      var factor = 10 ** decimals;
      return Math.round(number * factor) / factor;
}

var num_nodes = 30;
num_nodes /= 5;

var network = new cs.network({
      "nodes": {
            "Input": {
                  "num": num_nodes
            },
            "Output": {
                  "num": num_nodes
            },
            "Value": {
                  "num": num_nodes,
                  "init": [-1, 1]
            },
            "Addition": {
                  "num": num_nodes
            },
            "Multiplication": {
                  "num": num_nodes
            }
      },
      "connections": {
            "num": num_nodes ** 2,
            "init": [-1, 1]
      }
});

var node_colors = [
      // Green
      "#3f9b41",
      // Light blue
      "#afcfff",
      // Orange
      "#ff8300",
      // Purple
      "#c854ff",
      // Red
      "#f92c2c"
];
for (var i = 0; i < node_colors.length; i++) {
      cs.settings.node_types[i].color = node_colors[i];
}
var visualization_settings = {};
// Update program settings from user inputs
const update_settings = function() {
      visualization_settings.label = document.querySelector("#controls-visualization-label").checked;
      visualization_settings.size = document.querySelector("#controls-visualization-size").checked;
      visualization_settings.brightness = document.querySelector("#controls-visualization-brightness").checked;
      visualization_settings.type = document.querySelector("#controls-visualization-type").checked;
}
update_settings();

var svg = document.querySelector("#network-visualization");

var sidebar = document.querySelector("#control-panel");
var sidebar_hover = false;
var sidebar_x = 0;
var sidebar_y = 0;
sidebar.addEventListener("mouseover", () => {
      sidebar_hover = true
});
sidebar.addEventListener("mouseout", () => {
      sidebar_hover = false
});

var body_hover = false;
var body_x = 0;
var body_y = 0;
document.body.addEventListener("mouseover", () => {
      body_hover = true
});
document.body.addEventListener("mouseout", () => {
      body_hover = false
});

var speed = 0.025;
const update_backgrounds = function() {
      if (sidebar_hover) {
            sidebar_x += speed;
            sidebar_y += speed;
      }
      if (body_hover && !sidebar_hover) {
            body_x -= speed;
            body_y -= speed;
      }

      sidebar.style.backgroundPositionX = sidebar_x + "%";
      sidebar.style.backgroundPositionY = sidebar_y + "%";

      document.body.style.backgroundPositionX = body_x + "%";
      document.body.style.backgroundPositionY = body_y + "%";
}
setInterval(update_backgrounds, 10);

// Display visualization of network
// This function is only used the first time the network is displayed, as it generates the SVG elements used in the visualization
network.display = function() {
      svg.innerHTML = "";

      // Loop through each connection in network
      for (var attr in this.nodes) {
            var node = this.nodes[attr];

            node.display = {};

            var circle = document.createElement("circle");
            circle.className = "node";

            // Randomly select an x coordinate
            var x = cs.random(
                  // Minimum x value - the left side of the screen (with the circle's radius and margin added)
                  (5 + 3),
                  // Maximum x value - the right side of the screen (minus the circle's radius and margin)
                  (100 - 5 - 3)

            );

            // Randomly select a y coordinate
            var y = cs.random(
                  // Minimum y value - the top of the screen
                  (5 + 3),
                  // Maximum y value - the bottom side of the screen
                  (100 - 5 - 3)
            );

            // Set x position of circle element within SVG element
            circle.setAttribute("cx", (x + "%"));
            // Set y position of circle
            circle.setAttribute("cy", (y + "%"));

            var id = cs.UUID();
            circle.setAttribute("id", id);
            // Store a pointer to the circle element in corresponding connection object
            // This must be done by retrieving the id of the element to create a link between the variable and the element
            node.display.circle = id;

            // Add circle element to SVG element's HTML; this must be done with innerHTML or the SVG element will not be updated
            svg.innerHTML += circle.outerHTML;


            if (visualization_settings.label) {
                  var text = document.createElement("text");
                  text.className = "value-label";

                  var id = cs.UUID();
                  text.setAttribute("id", id);
                  node.display.text = id;

                  svg.innerHTML += text.outerHTML;
            }
      }

      // Render connections
      // Loop through each connection in network
      this.connections.forEach(
            (connection) => {
                  connection.display = {};

                  // Create a new SVG line element
                  var line = document.createElement("line");
                  // Apply "connection" CSS class to line element
                  line.className = "connection";

                  // Origin of line (first node)
                  line.setAttribute("x1", document.getElementById(this.nodes[connection.source].display.circle).getAttribute("cx"));
                  line.setAttribute("y1", document.getElementById(this.nodes[connection.source].display.circle).getAttribute("cy"));
                  // Destination of line (second node)
                  line.setAttribute("x2", document.getElementById(this.nodes[connection.destination].display.circle).getAttribute("cx"));
                  line.setAttribute("y2", document.getElementById(this.nodes[connection.destination].display.circle).getAttribute("cy"));

                  line.style.stroke = "#00243e";

                  // Store reference to line element in corresponding connection object
                  var id = cs.UUID();
                  line.setAttribute("id", id);
                  connection.display.line = id;

                  // Add line HTML to SVG element before circle elements
                  svg.innerHTML = line.outerHTML + svg.innerHTML;
            }
      );
}

network.update_display = function() {
      // Render nodes
      // https://stackoverflow.com/a/4020842

      var min = this.min_node().value;
      var max = this.max_node().value;

      this.loop_nodes(
            (node) => {
                  var circle = document.getElementById(node.display.circle);

                  // Default radius is 2%
                  var radius = 2;
                  // Check if node size is enabled in visualization settings
                  if (visualization_settings.size) {
                        // Map node values to a 1 to 5 percent range
                        radius = cs.map(node.value, min, max, 1, 5);
                  }
                  // Set radius of circle as percentage
                  circle.setAttribute("r", radius + "%");

                  cs.settings.node_types.forEach(
                        (node_type) => {
                              if (node.type == node_type.name) {
                                    var color;
                                    if (visualization_settings.type) {
                                          color = node_type.color;
                                    } else {
                                          color = "#7ab7fc";
                                    }
                                    if (visualization_settings.brightness) {
                                          color = shade_color(
                                                color,
                                                cs.map(node.value, min, max, -0.75, 0.75)
                                          );
                                    }
                                    circle.style.fill = color;
                              }
                        }
                  );

                  var text = document.getElementById(node.display.text);
                  if (visualization_settings.label) {
                        text.style.display = "";
                        text.innerHTML = round(node.value, 3);

                        // To pixels
                        radius = to_pixels.w(radius);
                        text.style.fontSize = radius / 2;

                        // Don't use parseInt
                        var x = parseFloat(circle.getAttribute("cx"));
                        var y = parseFloat(circle.getAttribute("cy"));
                        x -= to_percent.w(text.getBBox().width / 2);
                        y += to_percent.h(text.getBBox().height / 3);
                        // Set x position of text element within SVG element
                        text.setAttribute("x", (x + "%"));
                        // Set y position of text
                        text.setAttribute("y", (y + "%"));
                  } else {
                        text.style.display = "none";
                  }
            }
      );

      this.loop_connections(
            (connection) => {
                  var line = document.getElementById(connection.display.line);
                  line.setAttribute(
                        "opacity",
                        cs.map(
                              connection.weight,
                              this.min_weight(),
                              this.max_weight(),
                              0, 1
                        )
                  );
            }
      );
}

const update = function() {
      network.set_inputs({
            "inputs": new Array(num_nodes).fill(cs.random())
      });
      network.update();
      network.update_display();
}

network.display();
network.update_display();