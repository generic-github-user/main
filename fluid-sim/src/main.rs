use derive_more::{Add, Div};
use rand::Rng;
use std::{thread, time::Duration};
use ndarray::{Array2, Axis};

#[derive(Add, Div)]
struct Point {
    x: f64,
    y: f64
}

impl Point {
    fn new(x: f64, y: f64) -> Point {
        return Point { x, y };
    }
}

fn main() {
    let mut rng = rand::thread_rng();
    let mut points = vec![];
    for _i in 0..100 {
        points.push(Point::new(
            rng.gen_range(0.0..10.0),
            rng.gen_range(0.0..10.0),
        ));
    }
}
