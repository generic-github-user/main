// Generate a random UUID
// Based on https://stackoverflow.com/a/105074
var uuids = [];
cs.UUID = function(type) {
      // Generate a random string of four hexadecimal digits
      function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
                  .toString(16)
                  .substring(1);
      }
      // Generate UUID from substrings
      var id;
      do {
            if (type == "global") {
                  id = s4() + s4() + "-" + s4() + "-" + s4() + "-" + s4() + "-" + s4() + s4() + s4();
            } else if (type == "local") {
                  id = s4() + s4() + "-" + s4() + "-" + s4();
            } else {
                  console.error("UUID type must be either 'global' or 'local'.");
            }
      }
      while (uuids.indexOf(id) !== -1)


      uuids.push(id);
      return id;
}