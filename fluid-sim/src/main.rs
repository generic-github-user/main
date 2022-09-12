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

    let res = 20;

    for _i in 0..100 {
        let mut grid = Array2::<bool>::from_elem((res, res), false);
        for p in points.iter() {
            grid[[
                (p.x.round() as usize).clamp(0, res-1),
                (p.y.round() as usize).clamp(0, res-1)]]= true;
        }
        // for ((x, y), value) in grid.indexed_iter() {
        for row in grid.axis_iter(Axis(0)) {
            println!("{}", row.to_vec().iter()
                     .map(|v| if *v {".".to_string()} else {" ".to_string()})
                     .collect::<Vec<String>>().join(""));
        }

        thread::sleep(Duration::from_millis(100));
    }
}
