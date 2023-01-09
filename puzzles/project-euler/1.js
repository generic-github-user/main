const range = require('./../../lib/js/range.js').range;
const rrange = require('./../../lib/js/range.js').rrange;

console.log(rrange(1, 42));
console.log(rrange(0, 20).to_array());
console.log(rrange(1, 20).filter(x => x % 2 === 0).to_array());
console.log(rrange(1, 30).sum());
console.log(rrange(1, 1000).filter(x => x % 3 === 0 || x % 5 === 0).sum());
