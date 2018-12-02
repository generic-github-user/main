# Caesium

An evolutionary neural network implementation, inspired by [Neuroevolution of Augmenting Topologies](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf). The Caesium library is currently available for JavaScript. Python and Node.js implementations are planned.

# Design

## Architecture

The neural network architecture used for Caesium deviates substantially from that of a traditional neural network.

For one, there are no "weights" used in the synapses. This is perhaps the most integral part of a neural network, and the one that most closely mimics a biological neural network. Caesium's goal is not to imitate biological neural networks, but to take advantage of the unique abilities of computational processing to create a new kind of data model.

Caesium aims to create as basic as possible a framework for the evolutionary optimization strategy to build a model with. At the highest level, this is reflected by Caesium's NEAT architecture, which uses individual nodes and connections to represent the flow of data, instead of linear stacks of "layers".

### Operations

Caesium uses basic operations performed on data to represent its computations, instead of a traditional model with weights, biases, activation functions, and other properties of traditional neural networks. Operations are completed in nodes, and there are currently two types: addition and multiplication. Both nodes can have an infinite number of inputs and an infinite number of outputs. The addition node takes several scalar values as input and returns the sum of all these values as its output. The multiplication node returns the product of all of its inputs.



A more basic representation of operations performed on data allows for more flexible, versatile models.

### Data



### Delays

The flow of data through neural networks in Caesium is regulated by delays, stored in the connections between nodes.

## Evaluation

The value of each node is evaluated simultaneously based on a buffer of the stored values of each node. Similarly to a biological neural network, the entire network is constantly being updated and re-evaluated, as opposed to a traditional model, in which each layer would be evaluated sequentially, until the output layer is calculated. This would not be feasible for the organic style of Caesium's networks, in which input and output nodes are spread throughout the network. Constant evaluation also allows for the network to constantly "think" about problems that may require more than one computational iteration to solve, and allows the network to recursively apply dynamic mathematical operations and functions on data to iteratively transform it.

For example, instead of stacking several multiplication nodes together to approximate an exponent function, the network could develop a "multiplication loop" that multiplies the result of a computation by another number, then repeats this operation on the output of the function until another signal tells the network to end the loop and send the output to the global output node, theoretically allowing for more efficiency and smaller networks.

## Evolutionary Development of Models

### Training

### Limits

A hard limit can be placed on the number of nodes and/or connections that the neuroevolution algorithm can add to the network. This prevents the network growing indefinitely in size and reduces memory usage. It also encourages the evolution-based optimization algorithm to find better solutions to problems with fewer nodes, therefore reducing overfitting and improving generalization.

# Implementation

This is a technical guide to specific aspects of the Caesium library implementation in different programming languages for development reference purposes. Full documentation will be created soon.

## JavaScript

The JavaScript implementation of the Caesium library. This is the main version of Caesium. It currently is only meant for use in the browser as a script tag embedded in an HTML file. A [Node.js implementation](https://github.com/generic-github-user/Caesium/issues/97) is planned.

### Classes

#### Network

The main neural network class. This object contains all of the data and methods necessary to train and use a neural network.

##### Constructor

A new network object can be created using the `new cs.network` constructor.

Config:

- Nodes
  - Inputs
    - The number of input nodes (`data/input`) to be added to the new network.
    - Optional? `Yes`
    - Default value: `5`
    - Example: `{"input": 128}`
    - Property name: `config.input`
  - Outputs
    - The number of output nodes (`data/output`) to be added to the new network.
    - Optional? `Yes`
    - Default value: `5`
    - Example: `{"output": 128}`
    - Property name: `config.output`
  - Value
    - Information about the value nodes (`data/value`) to be added to the new network.
    - Optional? `Yes`
    - Example: `{"value": {"num": 5, "value": }}`
    - Property name: `config.value`
    - Number
      - The number of value nodes to be added to the new network. This must be at least 0. This can either be formatted as a constant value or as a minimum and maximum value that will be randomly selected between from a uniform distribution, non-inclusive, and rounded to the nearest integer.
      - Optional? `Yes`
      - Default value: `10`
      - Example
        - `{"value": {"num": 10}}`
        - `{"value": {"num": {"min": 5, "max": 15}}}`
      - Property name: `config.value.num`
      - Minimum
        - The lower bound for the number of value nodes. This is not needed if a constant value is provided.
        - Optional? `Yes`
        - Default value: `5`
        - Property name: `config.value.num.min`
      - Maximum
        - The upper bound for the number of value nodes. This is not needed if a constant value is provided.
        - Optional? `Yes`
        - Default value: `15`
        - Property name: `config.value.num.max`
    - Value
      - The starting value of value nodes can either be formatted as a constant value or as a minimum and maximum value that will be randomly selected between from a uniform distribution, non-inclusive. A normal (Gaussian) distribution option is planned.
      - Optional? `Yes`
      - Default value: `0`
      - Example
        - `{"value": {"value": 0}}`
        - `{"value": {"value": {"min": -1, "max": 1}}}`
      - Property name: `config.value.value`
      - Minimum
        - The lower bound for a randomly selected value for value nodes. This is not needed if a constant value is provided.
        - Optional? `Yes`
        - Default value: `-1`
        - Property name: `config.value.value.min`
      - Maximum
        - The upper bound for a randomly selected value for value nodes. This is not needed if a constant value is provided.
        - Optional? `Yes`
        - Default value: `1`
        - Property name: `config.value.value.max`

Example:

The following code will create a new network with 5 input nodes and 5 output nodes and store it in a new variable called `network`.

```javascript
var network = new cs.network({
      "nodes": {
            "input": 5,
            "output": 5,
            "value": {
                  "num": {
                        "min": 5,
                        "max": 10
                  },
                  "value": {
                        "min": -1,
                        "max": 1
                  }
            }
      }
});
```

##### Data

###### ID

The unique global ID of a network object, used to identify the networks. The ID of any given network is stored at `network.id`. It should be noted that the network ID is not essential information, as networks can be differentiated as distinct objects because, unlike nodes and connections, they are top-level objects.

###### Nodes

All the nodes that are contained within the structure of the network. Along with connections, these comprise the model architecture. To avoid object reference issues when duplicating entire network objects, each node object is only stored once in the network object and once in the global node list, `cs.all.nodes`. The full list of original connection objects can be found in `network.nodes`.

###### Connections

All the connections that are contained within the structure of the network. Along with nodes, these comprise the model architecture. To avoid object reference issues when duplicating entire network objects, each connections object is only stored once in the network object and once in the global connection list, `cs.all.connections`. The full list of original connection objects can be found in `network.connections`.

##### Methods

Methods are listed in the order they are defined in the library code.

###### Node
`network.node()`

Get a node from the network given its ID. Unlike most other functions and methods in Caesium, this method does not use a `config` object because it only has one parameter, `id`. This is the ID of the node you want to retrieve from the network. Remember that node IDs are local and used to identify the node of a specific network.

The `network.node()` function retrieves a given node from the node list of the network object that it is called on. It uses the native `array.prototype.find` function to find a node with a matching ID from the node list. If no node with the provided ID can be found, an error message is returned: `Node with id [ID] could not be found.`

Example:

```javascript
var node = network.node("7f0e0525-48c9-9de0-63b5-f67b9da29938");
```

###### Connection
`network.connection()`

Get a connection from the network given its ID. Unlike most other functions and methods in Caesium, this method does not use a `config` object because it only has one parameter, `id`. This is the ID of the connection you want to retrieve from the network. Remember that connection IDs are local and used to identify the connection of a specific network.

The `network.connection()` function retrieves a given connection from the connection list of the network object that it is called on. It uses the native `array.prototype.find` function to find a connection with a matching ID from the connection list. If no connection with the provided ID can be found, an error message is returned: `Connection with id [ID] could not be found.`

Example:

```javascript
var connection = network.connection("0b4b7920-a25f-727f-0d85-1b2c03da465b");
```

###### Set Inputs

###### Get Outputs

###### Update

###### Mutate

When `evolve()` is called, a population is generated by duplicating the network a set number of times. Then, each network in the population is randomly mutated using the `mutate()` function according to the provided mutation parameters. All the networks are evaluated using `update()` and the provided update parameters. Each network is given a score based on how closely its outputs matched the training data. The best network is selected and a new population is generated from it. This process can be repeated as many times as is necessary.

Config object parameters:

 - Iterations
   - The number of training epochs to run the neuroevolution process. More iterations will usually produce better results, but will take longer. Each iteration represents one generation of the evolutionary algorithm.
 - Population
   - The number of networks that should be generated for each generation (iteration).
 - Inputs
   - A two-dimensional array representing the input data for the model that will be used as input values when the fitness of each network is evaluated. Each sub-array is one set of training data, and should therefore match the number of inputs of the network.
 - Outputs
   - A two-dimensional array representing the correct output values for the model.
 - Mutate
   - Mutation settings for neuroevolution. The `mutate` function will be run on each network in the population.
 - Log
   - Whether or not to log information during training. Can be useful for debugging.
 - Return
   - What information `evolve()` should return when it has finished executing. "network" will return only the evolved neural network, while "all" will also return information about the training process, including the entire population of networks, the average score of all networks, and how long the training process took.

Returns:

 If `config.return` is set to "network":
 `cs.network`

 If `config.return` is set to "all":
 ```javascript
 {
       "population": [cs.network, cs.network, cs.network ...],
       "network": cs.network,
       "average": 0.214146
 }
 ```

Example:

```javascript
network = network.evolve({
      "iterations": 10,
      "population": 50,
      "inputs": [[1], [2], [3], [4], [5]],
      "outputs": [[1], [4], [9], [16], [25]],
      "mutate": {
            "iterations": 1,
            "nodes": {
                  "Value": {
                        "add": [0, 1],
                        "remove": [0, 1],
                        "limit": 1000,
                        "init": [-1, 1],
                        "value": {
                              "mutation_rate": 0,
                              "mutation_size": 0,
                        }
                  },
                  "Addition": {
                        "add": [0, 1],
                        "remove": [0, 1],
                        "limit": 1000
                  },
                  "Multiplication": {
                        "add": [0, 1],
                        "remove": [0, 1],
                        "limit": 1000
                  }
            },
            "connections": {
                  "add": [0, 10],
                  "remove": [0, 10],
                  "limit": 5000,
                  "init": [-1, 1],
                  "value": {
                        "mutation_rate": 1,
                        "mutation_size": 0.001,
                  }
            }
      },
      "log": true,
      "return": "network"
});
```

##### `export()`

Export all network information as a JSON-formatted string. The string can be saved as a text file, transmitted digitally, or saved for later use. For instance, you may want to train a model and then save it so that it can be used again repeatedly without needing to be re-trained. Model data saved with `export()` can be loaded using `import()`.

`export()` accepts no parameters.

Example:

```javascript
network.export();
```

##### `save()`

Save all network information to the web browser's localStorage. The network can be retrieved and reused even after the page has been reloaded. A network saved with `save()` can be loaded and used using `load()`.

Config object parameters:

 - `name`
   - The key to save the network data at in localStorage.
 - `overwrite`
   - Whether or not to overwrite any data already stored at the provided `name`, if any exists.

Example:

```javascript
network.save({
      "name": "network-1",
      "overwrite": false
});
```

#### Node

#### Connection

## Python

A [Python implementation](https://github.com/generic-github-user/Caesium/issues/2) of Caesium is planned.

## Node.js

A [Node.js implementation](https://github.com/generic-github-user/Caesium/issues/97) of Caesium is planned.

# Credits

This project wouldn't have been possible without lots of great open-source technology that people have been kind enough to share with the world. All sources listed here are also credited in code comments.

## Libraries

### Material Design Lite
*[getmdl.io](https://getmdl.io/)*

### Material Design Icons
*[material.io/tools/icons](https://material.io/tools/icons/?style=baseline)*

## Code Snippets

Smaller functions and pieces of code.

### UUID Generation Function
*[stackoverflow.com/a/105074](https://stackoverflow.com/a/105074)*

```javascript
var uuids = [];
const UUID = function () {
      // Generate a random string of four hexadecimal digits
      function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
      }
      // Generate UUID from substrings
      var id;
      do {
            id = s4() + s4() + "-" + s4() + "-" + s4() + "-" + s4() + "-" + s4() + s4() + s4();
      }
      while (uuids.indexOf(id) !== -1)

      uuids.push(id);
      return id;
}
```

### Range Mapping Function
*[stackoverflow.com/a/23202637](https://stackoverflow.com/a/23202637)*

```javascript
const map = function (num, in_min, in_max, out_min, out_max) {
      return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
```

### Hexadecimal Brightness Function
*[stackoverflow.com/a/13542669](https://stackoverflow.com/a/13542669)*

```javascript
const shade_color = function (color, percent) {
    var f=parseInt(color.slice(1),16),t=percent<0?0:255,p=percent<0?percent*-1:percent,R=f>>16,G=f>>8&0x00FF,B=f&0x0000FF;
    return "#"+(0x1000000+(Math.round((t-R)*p)+R)*0x10000+(Math.round((t-G)*p)+G)*0x100+(Math.round((t-B)*p)+B)).toString(16).slice(1);
}
```

### Finding maximum value in array by property
*[stackoverflow.com/a/4020842](https://stackoverflow.com/a/4020842)*

```javascript
var min = Math.min.apply(Math, this.nodes.map(function(x) { return x.value; }));
var max = Math.max.apply(Math, this.nodes.map(function(x) { return x.value; }));
```

## Demos

A series of demos to show just how cool Caesium is and what it is capable of. Feel free to clone any demo and create a new project out of it.

### [Basic Demo](https://generic-github-user.github.io/Caesium/src/versions/javascript/projects/basic-demo/)
Literally just an HTML page with the Caesium library loaded. Have fun.

[![image](./src/versions/javascript/projects/basic-demo/screenshots/1.PNG)](https://generic-github-user.github.io/Caesium/src/versions/javascript/projects/basic-demo/)

### [Network Visualization](https://generic-github-user.github.io/Caesium/src/versions/javascript/projects/network-visualization/)
Visualize all the nodes and connections in a Caesium network.

### [Curve Fitting](https://generic-github-user.github.io/Caesium/src/versions/javascript/projects/curve-fitting/)
Approximate a polynomial function using neuroevolution.

[![image](./src/versions/javascript/projects/curve-fitting/screenshots/1.PNG)](generic-github-user.github.io/Caesium/src/versions/javascript/projects/curve-fitting/)

[![image](./src/versions/javascript/projects/curve-fitting/screenshots/2.PNG)](generic-github-user.github.io/Caesium/src/versions/javascript/projects/curve-fitting/)

[![image](./src/versions/javascript/projects/curve-fitting/screenshots/3.PNG)](generic-github-user.github.io/Caesium/src/versions/javascript/projects/curve-fitting/)

### [Neuroevolution](https://generic-github-user.github.io/Caesium/src/versions/javascript/projects/neuroevolution/)
Evolve a randomly generated population of neural networks.

[![image](./src/versions/javascript/projects/neuroevolution/screenshots/1.PNG)](https://generic-github-user.github.io/Caesium/src/versions/javascript/projects/neuroevolution/)

### [2D Classification](https://generic-github-user.github.io/Caesium/src/versions/javascript/projects/2d-classification/)
Learn to classify 2D points based on their X and Y coordinates.
WARNING: Flashing colors

## Resources

Media and images used in Caesium.

### Transparent Textures
*[transparenttextures.com](https://www.transparenttextures.com/)*

Used for backgrounds in the JavaScript/web version of Caesium.

#### Brushed alum
*[transparenttextures.com/patterns/brushed-alum.png](https://www.transparenttextures.com/patterns/brushed-alum.png)*

*By [Tim Ward](http://www.mentalwarddesign.com/)*

Used for the network visualization background.

#### Az Subtle
*[transparenttextures.com/patterns/az-subtle.png](https://www.transparenttextures.com/patterns/az-subtle.png)*

*By [Anli.](https://azmind.com/)*

Used for the control panel/sidebar background.

### Logos

#### GitHub Logo
*[github.com/logos](https://github.com/logos)*

## Other

### Eric Meyer’s “Reset CSS” 2.0
*[cssreset.com/scripts/eric-meyer-reset-css](https://cssreset.com/scripts/eric-meyer-reset-css/)*

Used to reset the default CSS rules to make development a lot easier.

### ASCII Text Art Creator
*[www.network-science.de/ascii](http://www.network-science.de/ascii/)*

Used to create the ASCII logo art displayed in the console. See issue #20.
