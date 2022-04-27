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
}
