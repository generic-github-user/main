use rand::{thread_rng, Rng, seq::SliceRandom};
use std::fmt;

/// A symbol, the smallest meaningful unit in a language or grammar
//#[derive(FromIterator)]
#[derive(PartialEq, Eq, Copy, Clone)]
struct Symbol<T> {
    value: T
}

impl<T> Symbol<T> {
    /// Convert a string literal into a vector of Symbols
    fn from(string: &str) -> Vec<Symbol<char>> {
        string.chars().map(|c| Symbol { value: c }).collect()
    }
}

impl<T> Symbol<T> where T: Copy {
    /// Create a String containing only this symbol
    fn to_string(&self) -> String<T> {
        String { letters: vec![*self] }
    }
}

impl<T> fmt::Display for Symbol<T> where T: fmt::Display {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}
