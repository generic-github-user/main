let mDown = false;
let mx, my;
function getPos(canvas, event) {
      let rect = canvas.getBoundingClientRect();
      let x = event.clientX - rect.left;
      let y = event.clientY - rect.top;
      [mx, my] = [x, y];
  }

  let canvas = document.querySelector("canvas");

canvas.addEventListener("mousemove", e => {
      getPos(canvas, e);
      if (mDown) {
            grid.set(1, ...[mx, my].map(z => Math.floor(z / w)));
      }
});
  canvas.addEventListener("mousedown", function(e)
  {
      getPos(canvas, e);
      mDown = true;
  });
  canvas.addEventListener("mouseup", e => {
        getPos(canvas, e);
        mDown = false;
 });

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

      set(v, ...w) {
            if (w.length > 1) {
                  this.data[w[0]].set(v, ...w.slice(1));
            } else {
                  this.data[w[0]] = v;
            }
            return this;
      }

      slice(a, b) {

      }

      index(s) {
            // null element?
            let axes = s.split(' ');
            let x = axes[0].split(':');
            let a, b;
            [a, b] = x.map(n => parseInt(n)).map(y => clip(y, 0, this.data.length-1));
            let result = [];
            for (let i=a; i<b; ++i) {
                  result.push(this.data[i]);
            }
            if (axes.length > 1) { result = result.map(y => y.index(axes.slice(1).join(' '))); }
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

      sum() { return this.reduce((x, y) => x + y, 0); }
      mean() { return this.sum() / this.size; }
      max() { return this.reduce(Math.max, -Infinity) }

      map(f) {
            if (this.rank === 1) {
                  this.data = this.data.map(f);
            } else {
                  this.data = this.data.map(x => x.map(f));
            }
            return this;
      }

      imap(f) {
            // could also use while loop with increments, etc.
            // function imapR(g, i)
            // if (this.rank === 1) {
            //       return this.data.map(f);
            // }

            let result = new Array(this.data.length);
            for (let i=0; i<this.data.length; ++i) {
                  if (this.rank === 1) {
                        result[i] = f(i);
                  } else {
                        result[i] = this.data[i].imap((...b) => f(i, ...b));
                  }
            }
            return new ndarray(this.dimensions).setData(result);
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

// Class.method?

let ctx = canvas.getContext("2d");
let grid = new ndarray([50, 50]).map(x => Math.random());
let objects = [];
let w = 10;
function update() {
        ctx.canvas.width  = window.innerWidth;
        ctx.canvas.height = window.innerHeight;
      grid.forEach((x, y) => {
            ctx.fillStyle = `hsl(0, 100%, ${(1-grid.get(x, y)) * 100}%)`;
            ctx.fillRect(x*w, y*w, w, w);
      });
      grid = grid.convolveFunc(x => x.mean(), 1, 0.05);
}
setInterval(update, 100)
