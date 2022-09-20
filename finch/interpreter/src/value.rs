use std::fmt;
use std::ops::{Add, Sub, Mul, Div};
use num_traits::pow::Pow;

use super::node::Node;

#[derive(Clone, Debug)]
pub struct Value {
    pub vtype: String,
    // value: &'a Node<'a>
    pub value: ValueType
}

macro_rules! value_impl {
    ($trait:ident, $func:ident, $op:tt) => {
        impl $trait for Value {
            type Output = Self;

            fn $func(self, other: Self) -> Self {
                Self {
                    vtype: self.vtype,
                    value: self.value $op other.value
                }
            }
        }
    }
}

value_impl!(Add, add, +);
value_impl!(Sub, sub, -);
value_impl!(Mul, mul, *);
value_impl!(Div, div, /);

impl Pow<Value> for Value {
    type Output = Self;

    fn pow(self, other: Self) -> Self {
        Self {
            vtype: self.vtype,
            value: self.value.pow(other.value)
        }
    }
}

impl Value {
    //fn new(
}

macro_rules! make_stringifier {
    ($($type:ident),*) => {
        {ValueType::$type(value) => value.to_string()}
    }
}

/// Enables the Display and ToString traits for Value structs (used in implementations of `print`
/// and `println`, among other implementation-level functions that necessitate conversion of
/// primitive types to string representations)
impl fmt::Display for Value {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // Unwraps ValueType enums containing actual Rust values
        write!(f, "{}", match self.value.clone() {
            ValueType::i8(value) => value.to_string(),
            ValueType::i16(value) => value.to_string(),
            ValueType::i32(value) => value.to_string(),
            ValueType::i64(value) => value.to_string(),
            ValueType::i128(value) => value.to_string(),
            ValueType::char(value) => value.to_string(),
            ValueType::bool(value) => value.to_string(),
            // make_stringifier!(bool)
            ValueType::string(value) => value,
            _ => {
                println!("{:?}", self);
                todo!()
            }
        })
    }
}

/// Used to represent primitive data types like ints and floats with direct equivalents in Rust's
/// data model; literals from the AST can be parsed directly into variants of this enum. Compound
/// types (lists, arrays, tuples, dictionaries, etc.) are implemented in lyre itself.
#[derive(Debug, Clone)]
pub enum ValueType {
    // Signed integer types
    i8(i8),
    i16(i16),
    i32(i32),
    i64(i64),
    i128(i128),

    // Unsigned integer types
    u8(u8),
    u16(u16),
    u32(u32),
    u64(u64),
    u128(u128),

    // Floating-point number types
    f32(f32),
    f64(f64),

    // Other basic types
    bool(bool),
    char(char),
    string(String),

    Form(Node)
}

macro_rules! valuetype_impl {
    ( $trait:ident, $func:ident, $op:tt ) => {
        impl $trait for ValueType {
            type Output = Self;

            fn $func(self, other: Self) -> Self {
                // ValueType
                match (self, other) {
                    (ValueType::i8(value), ValueType::i8(other))  => ValueType::i8(value $op other),
                    (ValueType::i16(value), ValueType::i16(other))  => ValueType::i16(value $op other),
                    (ValueType::i32(value), ValueType::i32(other))  => ValueType::i32(value $op other),
                    (ValueType::i64(value), ValueType::i64(other))  => ValueType::i64(value $op other),
                    (ValueType::i128(value), ValueType::i128(other))  => ValueType::i128(value $op other),
                    _ => panic!()
                }
            }
        }
    }
}

valuetype_impl!(Add, add, +);
valuetype_impl!(Sub, sub, -);
valuetype_impl!(Mul, mul, *);
valuetype_impl!(Div, div, /);

impl Pow<ValueType> for ValueType {
    type Output = Self;

    fn pow(self, other: Self) -> Self {
        match (self, other) {
            (ValueType::i8(value), ValueType::i8(other))  => ValueType::i8(value.pow(other.try_into().unwrap())),
            (ValueType::i16(value), ValueType::i16(other))  => ValueType::i16(value.pow(other.try_into().unwrap())),
            (ValueType::i32(value), ValueType::i32(other))  => ValueType::i32(value.pow(other.try_into().unwrap())),
            (ValueType::i64(value), ValueType::i64(other))  => ValueType::i64(value.pow(other.try_into().unwrap())),
            (ValueType::i128(value), ValueType::i128(other))  => ValueType::i128(value.pow(other.try_into().unwrap())),
            _ => panic!()
        }
    }
}
