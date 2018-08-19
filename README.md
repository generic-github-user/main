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

## JavaScript

### Classes

#### Node

##### Data

###### Input

###### Output

###### Value

##### Operation

###### Addition

###### Multiplication

#### Network

## Python

A Python implementation of Caesium is planned. See issue #2.

# Credits

This project wouldn't have been possible without lots of great open-source technology that people have been kind enough to share with the world.

## Libraries

### Material Design Lite
*[getmdl.io](https://getmdl.io/)*

### Material Design Icons
*[material.io/tools/icons](https://material.io/tools/icons/?style=baseline)*

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
