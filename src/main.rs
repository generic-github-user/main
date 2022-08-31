use rand::Rng;
use std::ops;
//use std::ops::{Deref, DerefMut};

extern crate derive_more;
use derive_more::{Add, Mul, Sub, Div};

#[derive(Add, Mul)]
struct Int32(i32);
#[derive(Add, Mul)]
struct Int64(i64);

//#[derive(Add, Mul, Sub, Div)]
//enum Number {
//    Int32(i32),
//    Int64(i64)
//}

//impl ops::Add for Number {
//    type Output = Number;
//    fn add(


#[derive(PartialEq, PartialOrd, Clone, Debug)]
struct Variable (char);

//#[derive(Clone)]
//struct Vec<Variable> (Variable);

#[derive(Clone, Debug)]
struct Term {
    cf: i64,
    vars: Vec<Variable>,
    exps: Vec<i64>
}

//impl Add for Term {
//    fn add(self, other)
//

// Based on https://stackoverflow.com/a/54603724
pub fn vec_add<T>(v1: &[T], v2: &[T]) -> Vec<T>
    where
        T: std::ops::Add<Output = T> + Copy,
{
    v1.iter().zip(v2).map(|(&i1, &i2)| i1 + i2).collect()
}


impl ops::Mul for Term {
    type Output = Term;
    fn mul(self, other: Term) -> Term {
        Term {
            cf: self.cf * other.cf,
            vars: self.vars.clone(),
//            exps: self.exps + other.exps
            exps: vec_add(&self.exps, &other.exps)
        }
    }
}


// can we just store in an enum and define for all members (term, number, etc.)?
// trait Derivative 

enum Expression {
    Number(i64),
    Variable,
    Term,
    Operator
}

struct Function<T, V> {
    name: String,
    f: fn(T, T) -> V
}

struct Operator<'a, T, V> {
    func: &'a Function<T, V>,
//    terms: Vec<Expression>,
    terms: Vec<Term>
}

impl<'a, T, V> Operator<'a, T, V> {
    fn new(f: &'a Function<T, V>, t: Vec<Term>) -> Operator<'a, T, V> {
        return Operator { func: f, terms: t };
    }

    fn simplify(&self) -> Operator<T, V> {
        let mut result = Operator::new(self.func, vec![]);
        'outer: for term in self.terms.iter() {
            for r in &mut result.terms.iter_mut() {
                if term.vars == r.vars && term.exps == r.exps {
                    r.cf += term.cf;
                }
                break 'outer;
            }
            result.terms.push(term.clone());
        }
        return result;
    }
}

impl<'a, T, V> ops::Mul for Operator<'a, T, V> {
    type Output = Operator<'a, T, V>;
    fn mul(&self, other: i64) -> Operator<'a, T, V> {
        self.clone()
    }
}
