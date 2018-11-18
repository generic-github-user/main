var network = new cs.network({
      "nodes": {
            "Input": {
                  "num": 1
            },
            "Output": {
                  "num": 1
            },
            "Value": {
                  "num": 3,
                  "init": [-1, 1]
            },
            "Addition": {
                  "num": 3
            },
            "Multiplication": {
                  "num": 3
            },
            // "Tanh": {
            //       "num": 3
            // },
            // "Sine": {
            //       "num": 3
            // },
            // "Cosine": {
            //       "num": 3
            // },
            // "Abs": {
            //       "num": 3
            // }
      },
      "connections": {
            "num": 10,
            "init": [-1, 1]
      }
});