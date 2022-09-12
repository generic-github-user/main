use std::fs::File;
use std::io::{BufReader, BufRead, Error};
use std::fmt;
use std::collections::HashMap;

use std::ops::{Add, Sub, Mul, Div};

// use token::Token;
// use crate::token;

mod token;
use token::Token;

mod chartype;
use chartype::CharType;

mod node;
use node::{Node, NodeType};


struct Value {
    vtype: String,
    // value: &'a Node<'a>
    value: ValueType
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
            _ => todo!()
        })
    }
}

/// Used to represent primitive data types like ints and floats with direct equivalents in Rust's
/// data model; literals from the AST can be parsed directly into variants of this enum. Compound
/// types (lists, arrays, tuples, dictionaries, etc.) are implemented in lyre itself.
#[derive(Debug, Clone)]
enum ValueType {
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



fn lex(buffer: BufReader<File>) -> Result<Vec<Token>, Error> {
    // This section has a simple lexer that splits lyre source code into tokens, groups of
    // consecutive characters with similar syntactic purposes

    // A list of tokens parsed from the input program's source code
    let mut tokens = Vec::<Token>::new();
    for line in buffer.lines() {
        println!("Parsing line: {}", line.as_ref().unwrap());
        // Stores the type of the previous character
        let mut ptype = CharType::None;
        // Stores the type of the current character
        let mut ctype = CharType::None;
        // The text content of the current token; incrementally grown as new characters are
        // consumed
        let mut current: String = String::from("");

        // Iterate over characters in line
        for c in line?.chars() {
            // Categorize characters by syntactic type (refer to the CharType enum for information
            // about specific types)
            // if c.is_alphanumeric() { ctype = CharType::Alphanumeric; }
            if c.is_digit(10) { ctype = CharType::Digit; }
            else if c.is_alphabetic() { ctype = CharType::Letter; }
            else if c == '\n' { ctype = CharType::Newline; }
            else if c.is_whitespace() { ctype = CharType::Whitespace; }
            else if c == '[' { ctype = CharType::LeftSB; }
            else if c == ']' { ctype = CharType::RightSB; }
            else if c == '"' && ptype != CharType::String { ctype = CharType::String; }
            else { ctype = CharType::Symbol; }

            if ptype == CharType::String && c != '"' {
                ctype = CharType::String;
            }
            println!("Lexing character {} as {:?}", c, ctype);

            // If the character type is unchanged from the previous step, append it to the current
            // token string ...
            if ctype == ptype && ctype != CharType::LeftSB && ctype != CharType::RightSB {
                current += String::from(c).as_ref();
            }
            // ... otherwise, start a new token and store the current one
            else {
                if ptype != CharType::None {
                    let ntoken = Token {
                        content: if ptype == CharType::String { String::from(&current[1..]) }
                                 else { current },
                        chartype: ptype
                    };
                    println!("Finished token {:?}", ntoken);
                    tokens.push(ntoken);
                }
                current = String::from(c);
            }

            ptype = ctype;
        }

        let ntoken = Token {
            content: current,
            chartype: ptype
        };
        println!("Finished token {:?}", ntoken);
        tokens.push(ntoken);

        // Insert newline character after parsing line
        tokens.push(Token { 
            content: String::from(""),
            chartype: CharType::Newline
        });
    }
    println!("Parsed {} tokens", tokens.len());
    // println!("{}", tokens);
    Ok(tokens)
}

fn main () -> Result<(), Error> {
    let path = "sample.ly";
    let input = File::open(path)?;
    let buffered = BufReader::new(input);

    let mut root = Node {
        content: None,
        children: vec![],
        nodetype: NodeType::Program
    };
    let tokens = lex(buffered).unwrap();
    
    // a list of indices representing a path through the abstract syntax tree generated by the
    // parser; used to keep track of the current parsing context
    let mut stack = Vec::<usize>::new();
    // stack.push(0);
    let mut indentlevel: usize = 0;
    let mut ptoken: Option<Token> = None;

    for token in tokens {
        // if token.chartype == CharType::LeftSB {
        match token.chartype {
            // A left bracket ([) opens a new form ...
            CharType::LeftSB => {
                let nnode = Node {
                    content: None,
                    children: vec![],
                    nodetype: NodeType::Form
                };

                let current = root.get(stack.clone());
                // stack.push(current.children.len());
                stack.push(current.children.len());
                current.children.push(nnode);
            }

            // ... and a right bracket (]) closes it
            CharType::RightSB => {
                stack.pop();
            }

            // An identifier or expression within a form
            CharType::Letter | CharType::Symbol
                | CharType::String | CharType::Digit => {

                let current = root.get(stack.clone());
                let nnode = Node {
                    content: Some(token.clone()),
                    children: vec![],
                    nodetype: match token.chartype {
                        CharType::Letter | CharType::Symbol => NodeType::Token,
                        CharType::String => NodeType::String,
                        CharType::Digit => NodeType::Integer,
                        _ => unreachable!()
                    }
                };
                current.children.push(nnode);

                // we're adding a new bottom-level node (leaf) to the parent of the last node in
                // the current path
                //if stack.len() == 0 {
                    //stack.push(0);
                //} else {
                   //*stack.last_mut().unwrap() += 1;
                //}
            }

            // Whitespace between tokens/forms or at the beginning of a line (i.e., indentation
            // used to denote sub-forms)
            CharType::Whitespace => {
                if ptoken.is_some() && ptoken.unwrap().chartype == CharType::Newline {
                    if token.content.len() > indentlevel {
                        // TODO: abstract this out into a function
                        let nnode = Node {
                            content: None,
                            children: vec![],
                            nodetype: NodeType::Form
                        };

                        let current = root.get(stack.clone());
                        stack.push(current.children.len());
                        current.children.push(nnode);
                    } else if token.content.len() == indentlevel {
                        // TODO: abstract this out into a function
                        let current = root.get(stack.clone());
                        let nnode = Node {
                            content: Some(token.clone()),
                            children: vec![],
                            nodetype: NodeType::Whitespace
                        };
                        current.children.push(nnode);
                    } else {
                        assert!(token.content.len() < indentlevel);
                        // let current = root.get();
                        // stack.truncate
                        for i in 0..(indentlevel - token.content.len()) {
                            stack.pop();
                        }
                    }

                    indentlevel = token.content.len();
                }
            }

            CharType::Newline => {

            }

            CharType::None => {

            }

            CharType::Quote | CharType::Unknown => {

            }

            CharType::Alphanumeric => unreachable!()
        }

        ptoken = Some(token.clone());
    }

    //Ok(())
    //return Ok(root.evaluate().unwrap());
    root.print(0);
    root.evaluate(false);
    Ok(())
}
