use rand::Rng;
use std::ops;
//use std::ops::{Deref, DerefMut};

extern crate derive_more;
use derive_more::{Add, Mul, Sub, Div};

#[derive(Add, Mul)]
struct Int32(i32);
#[derive(Add, Mul)]
struct Int64(i64);
