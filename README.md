# Caesium

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

The JavaScript implementation of Caesium. It currently is only meant for use in the browser as a script tag embedded in an HTML file. No Node.js implementation is currently planned.

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

###### Connection

###### Set Inputs

###### Get Outputs

###### Update

###### Mutate

###### Evolve



#### Node

#### Connection

## Python

A Python implementation of Caesium is planned. See issue #2.

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
