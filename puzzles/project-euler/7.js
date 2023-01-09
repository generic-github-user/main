const range = require('./../../lib/js/range.js').range;
console.log(range(2, 3000).filter(x =>
    range(2, Math.ceil(x**0.5)+1).all(y => x % y != 0 || x === y)).nth(100));
