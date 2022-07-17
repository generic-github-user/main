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

/// A concrete string formed from any number of symbols
#[derive(PartialEq, Eq, Clone)]
struct String<T> {
    letters: Vec<Symbol<T>>
}

impl<T> String<T> where T: fmt::Display {
    /// Convert a string literal into a String
    fn from(string: &str) -> String<char> {
        String { letters: string.chars().map(|c| Symbol { value: c }).collect() }
    }

    fn new() -> String<T> {
        String { letters: Vec::new() }
    }

    fn print(&self) -> () {
        println!("{}", self);
    }
}

/// Display a String based on the enclosed Symbols' fmt::Display implementation
impl<T> fmt::Display for String<T> where T: fmt::Display {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        //write!(f, "{}", self.letters.join(""))
        for L in &self.letters {
            write!(f, "{}", L)?;
        }
        Ok(())
    }
}

#[derive(Clone)]
struct Rule<T> {
    input: String<T>,
    output: String<T>
}

impl<'a, T> Rule<T> {
    /// Initialize a new rule using `String`s corresponding to that rule's input and output
    fn new(input: String<T>, output: String<T>) -> Rule<T> {
        Rule { input, output }
    }

    /// Create a rule using individual symbols
    fn sym(input: Symbol<T>, output: Symbol<T>) -> Rule<T> where T: Copy{
        Rule { input: input.to_string(), output: output.to_string() }
    }

    /// Create a rule from raw strings (string literals)
    fn raw(input: &str, output: &str) -> Rule<char> {
        Rule { input: String::<char>::from(input), output: String::<char>::from(output) }
    }

    //fn sym(input: Symbol<T>, output: Symbol<T>) -> Rule<'a, T> where T: Copy {
    //    let A = &input.to_string();
    //    let B = &output.to_string();
    //    Rule { input: A, output: B }
    //}
}
