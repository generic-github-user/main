// use std::fs::File;
use std::fs;
use std::io::{BufReader, Error};
use std::collections::HashMap;

mod token;
mod chartype;
mod node;
mod value;
mod lexer;
mod parser;
mod source;

use lexer::lex;
use parser::parse;

use node::Language;

fn main () -> Result<(), Error> {
    let path = "sample.ly";
    // let input = File::open(path).expect("Could not read source file");
    // let buffered = BufReader::new(input);
    // input.read_to_string(&mut source);

    let source: String = fs::read_to_string(path).expect("Could not read source file");
    let tokens = lex(source, false).unwrap();
    let root = parse(tokens, false);

    println!("{}", root.transpile(Language::C, false));

    //Ok(())
    //return Ok(root.evaluate().unwrap());
    root.print(0);
    let mut symbols = HashMap::new();
    root.evaluate(&mut symbols, false);
    Ok(())
}
