# JavaScript

The JavaScript implementation of the Caesium library. This is the main version of Caesium. It currently is only meant for use in the browser as a script tag embedded in an HTML file. A [Node.js implementation](https://github.com/generic-github-user/Caesium/issues/97) is planned.

## Usage

Add the following script tag to your HTML code to add the Caesium library to your web page:
```html
<script type="text/javascript" src="https://cdn.jsdelivr.net/gh/generic-github-user/caesium/src/versions/javascript/library/caesium.min.js"></script>
```

Alternatively, download [the full script](https://raw.githubusercontent.com/generic-github-user/Caesium/master/src/versions/javascript/library/caesium.js) and host it within your project. This is highly recommended for any production usage.

## Classes

### Network

The main neural network class. This object contains all of the data and methods necessary to train and use a neural network.

#### Constructor

A new network object can be created using the `new cs.network` constructor.

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

#### Data

##### ID

The unique global ID of a network object, used to identify the networks. The ID of any given network is stored at `network.id`. It should be noted that the network ID is not essential information, as networks can be differentiated as distinct objects because, unlike nodes and connections, they are top-level objects.

##### Nodes

All the nodes that are contained within the structure of the network. Along with connections, these comprise the model architecture. To avoid object reference issues when duplicating entire network objects, each node object is only stored once in the network object and once in the global node list, `cs.all.nodes`. The full list of original connection objects can be found in `network.nodes`.

##### Connections

All the connections that are contained within the structure of the network. Along with nodes, these comprise the model architecture. To avoid object reference issues when duplicating entire network objects, each connections object is only stored once in the network object and once in the global connection list, `cs.all.connections`. The full list of original connection objects can be found in `network.connections`.

#### Methods

Methods are listed in the order they are defined in the library code.

##### `find_node()`

Get a node from the network given its ID. Unlike most other functions and methods in Caesium, this method does not use a `config` object because it only has one parameter, `id`. This is the ID of the node you want to retrieve from the network. Remember that node IDs are local and used to identify the node of a specific network.

The `network.node()` function retrieves a given node from the node list of the network object that it is called on. It uses the native `array.prototype.find` function to find a node with a matching ID from the node list. If no node with the provided ID can be found, an error message is returned: `Node with id [ID] could not be found.`

Example:

```javascript
var node = network.node("7f0e0525-48c9-9de0-63b5-f67b9da29938");
```

##### `find_connection()`

Get a connection from the network given its ID. Unlike most other functions and methods in Caesium, this method does not use a `config` object because it only has one parameter, `id`. This is the ID of the connection you want to retrieve from the network. Remember that connection IDs are local and used to identify the connection of a specific network.

The `network.find_connection()` function retrieves a given connection from the connection list of the network object that it is called on. It uses the native `array.prototype.find` function to find a connection with a matching ID from the connection list. If no connection with the provided ID can be found, an error message is returned: `Connection with id [ID] could not be found.`

Example:

```javascript
var connection = network.connection("0b4b7920-a25f-727f-0d85-1b2c03da465b");
```

##### `set_inputs()`

Set the values of the input nodes for the network so that predictions can be run.

Config object parameters:

 - Inputs
   - An array of inputs for the network

Example:

```javascript
network.set_inputs({
      "inputs": [4, 2, 8, 14, 9.6]
});
```

##### `get_outputs()`

##### `update()`

##### `mutate()`

##### `evolve()`

Optimize the parameters of a network through neuroevolution. Any of the following model parameters can be optimized:

 - Network topology
   - Nodes
   - Connections
 - Connection weights
 - Bias node values

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

### Node

### Connection
