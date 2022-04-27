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
      map(f) {
            if (this.rank === 1) {
                  this.data = this.data.map(f);
            } else {
                  this.data = this.data.map(x => x.map(f));
            }
            return this;
      }
}
