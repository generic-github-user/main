console.log(decode(
      cs.apply(
            network.evaluate({
                  "input": encode("5+5=", charset, chars),
                  "update": {
                        "iterations": 1,
                        "limit": {
                              "min": -10e3,
                              "max": 10e3
                        }
                  }
            }),
            Math.round
      ),
      charset
));
console.log(decode(
      cs.apply(
            network.evaluate({
                  "input": encode("5+5=", charset, chars),
                  "update": {
                        "iterations": 50,
                        "limit": {
                              "min": -10e3,
                              "max": 10e3
                        }
                  }
            }),
            Math.round
      ),
      charset
));