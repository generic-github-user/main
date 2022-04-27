function clip (x, min, max) {
  return Math.min(Math.max(x, min), max);
};

class ndarray {
      constructor(dimensions) {
            this.dimensions = dimensions;
            this.data = new Array(dimensions[0]).fill(0);
            this.update();
            if (dimensions.length > 1) {
                  this.data = this.data.map(x => new ndarray(dimensions.slice(1)));
            }
      }

      setData(data) {
            // console.log(data);
            this.data = data;
            // this.dimensions = [this.data.length, ...this.data[0].dimensions];
            this.update();
            return this;
      }

      update() {
            this.rank = this.dimensions.length;
            this.size = this.dimensions.reduce((x, y) => x * y, 1);
            return this;
      }

      get(...w) {
            // let result = (w[0] === -1) ? this.data : this.data[w[0]];
            let result = (w[0] === -1) ? this.data : this.data[w[0]];
            if (w.length > 1) {
                  // result = result.map(x => x.get(w.slice(1)));
                  result = result.get(w.slice(1));
            }
            return result;
      }

      slice(a, b) {

      }

      index(s) {
            // null element?
            // console.log(s);
            let axes = s.split(' ');
            let x = axes[0].split(':');
            let a, b;
            [a, b] = x.map(n => parseInt(n)).map(y => clip(y, 0, this.data.length-1));
            let result = [];
            for (let i=a; i<b; ++i) {
                  result.push(this.data[i]);
            }
            if (axes.length > 1) { result = result.map(y => y.index(axes.slice(1).join(' '))); }
            // console.log(result, a, b, this.data.length, x);
            // console.log(x, x.map(parseInt));
            // console.log(result[0]);
            let m = k => (k === undefined) ? [] : k;
            return new ndarray([b-a, ...m(result[0].dimensions)]).setData(result);
      }

      reduce(f, init) {
            let result = init;
            // if ()
            this.forEach((...x) => {
                  // result = f(result, x);
                  result = f(result, this.get(...x));
            });
            return result;
      }
      // reduce axis-by-axis?

      sum() {
            return this.reduce((x, y) => x + y, 0);
      }

      mean() {
            return this.sum() / this.size;
      }
      max() { return this.reduce(Math.max, -Infinity) }

      map(f) {
            if (this.rank === 1) {
                  this.data = this.data.map(f);
            } else {
                  this.data = this.data.map(x => x.map(f));
            }
            return this;
      }

      forEach(f) {
            // function forEachR()
            for (let i=0; i<this.data.length; ++i) {
                  if (this.rank === 1) {
                        f(i);
                  } else {
                        this.data[i].forEach((...b) => f(i, ...b));
                  }
            }
            return this;
      }

      // choose

      convolveFunc(f, r, q) {
            return this.imap((...i) => {
                  let x = this.get(...i);
                  let y = f(this.index(i.map(j => `${j-r}:${j+r+1}`).join(' ')));
                  return (x * (1 - q)) + (y * q);
            })
      }
}
