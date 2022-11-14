const range = require('./../../lib/js/range.js').range;
let R = range(1, 101);
console.log(R.map(x => x ** 2).to_array());
// console.log(R.map(x => x.toString()).sum());
console.log(R.sum() ** 2 - R.map(x => x ** 2).sum());
