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
