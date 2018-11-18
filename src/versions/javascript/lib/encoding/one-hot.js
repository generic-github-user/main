// Converting a string to and from a one-hot encoded binary vector

// Accepts a string and returns an array of 1s and 0s
function encodeString(input, charset, length) {
      // Define output as a variable containing an empty array
      var output = [];
      // Convert input string to array of all characters in input
      input = input.split("");
      // Loop through each character of the input string
      for (var i = 0; i < length; i++) {
            // Loop through each possible character
            charset.forEach(
                  char => {
                        // Check for a match between the current input character and the current character from the list; if there is a match, add a 1 to the output array
                        if (input[i] == char) {
                              output.push(1);
                        }
                        // If there is no match, add a 0 to the output array
                        else {
                              output.push(0);
                        }
                  }
            )
      }
      // Return output array
      return output;
}

// Accepts an array of 1s and 0s as an input and returns a string
function decodeString(input, charset) {
      // Define output as a variable containing an empty string
      var output = "";
      // Loop through each character of the input string
      for (var i = 0; i < input.length; i++) {
            // Check value of current element of input array
            if (input[i] == 1) {
                  output += charset[i % charset.length];
            }
      }
      // Return output string
      return output;
}