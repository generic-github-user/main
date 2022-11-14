let range = (a, b) => { return {
    n: a,
    bounds: [a, b],
    next: function () { return (this.n < b ? this.n++ : null) },
    has_next: function () { return this.n < b-1 },
    clone: function () {
        let result = range(...this.bounds);
        result.next = this.next;
        return result;
    },
    find: function (f) {
        // let v = this.n;
        let n;
        let source = this.clone();
        while ((n = source.next()) != null && !f(n));
        // while (v != null && !f(v)) this.next();
        // console.log(this.n);
        return n;
    },
    filter: function (f) {
        // this.next = function () { return this.next().filter(f); };
        let result = this.clone();
        result.next = (function () { return this.find(f); }).bind(this);
        return result;
    },
    map: function (f) {
        let result = this.clone();
        let source = this.clone();
        result.next = (function () {
            let v = source.next();
            return v === null ? v : f(v); }).bind(source);
        return result;
    },
    reduce: function (f, init) {
        let This = this.clone();
        let v = init; let x;
        while ((x = This.next()) != null) v = f(v, x);
        // while (this.has_next()) { v = f(v, this.n); 
        return v;
    },
    sum: function () { return this.reduce((x, y) => x + y, 0) },
    to_array: function () { return this.clone().reduce((a, x) => a.concat([x]), []); },
}};


module.exports.range = range;
