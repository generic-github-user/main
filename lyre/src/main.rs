use std::fs::File;
use std::io::{BufReader, BufRead, Error};
use std::fmt;


// use token::Token;
// use crate::token;

mod token;
use token::Token;

mod chartype;
use chartype::CharType;

mod node;
use node::{Node, NodeType};

mod value;
use value::Value;

mod lexer;
use lexer::lex;

mod parser;
use parser::parse;

fn main () -> Result<(), Error> {
    let path = "sample.ly";
    let input = File::open(path)?;
    let buffered = BufReader::new(input);

    let tokens = lex(buffered, false).unwrap();
    let root = parse(tokens, false);

    //Ok(())
    //return Ok(root.evaluate().unwrap());
    root.print(0);
    root.evaluate(false);
    Ok(())
}
