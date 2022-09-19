use std::fs::File;
use std::io::{BufReader, Error};
use std::collections::HashMap;

mod token;
mod chartype;
mod node;
mod value;
mod lexer;
mod parser;

use lexer::lex;
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
    let mut symbols = HashMap::new();
    root.evaluate(&mut symbols, true);
    Ok(())
}
