const encode = function(input, charset, length) {
      var output = [];
      for (var i = 0; i < length; i++) {
            output.push(charset.indexOf(input[i]));
      }
      return output;
}

const decode = function(input, charset) {
      var output = "";
      for (var i = 0; i < input.length; i++) {
            var character = charset[input[i]];
            if (!character) {
                  character = "";
            }
            output += character;
      }
      return output;
}