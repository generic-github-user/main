use std::fmt;
use std::ops::{Add, Sub, Mul, Div};

use super::node::Node;

#[derive(Clone, Debug)]
pub struct Value {
    pub value: String
}

impl std::fmt::Display for Value {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}
