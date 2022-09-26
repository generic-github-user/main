use std::io;
use std::io::Write;
use std::time::SystemTime;
use chrono::{DateTime, Utc};

mod lexer;
mod parser;
mod token;
mod node;
mod chartype;
mod value;

use lexer::lex;
use parser::parse;
use node::Node;

fn main() {
    let mut input = String::new();
    // let now = SystemTime::now();
    let now = Utc::now();
    println!("shell-1 | {}", now);
    loop {
        print!("~ ");
        io::stdout().flush();
        input.clear();
        io::stdin().read_line(&mut input).unwrap();

        let tokens = lex(input.clone(), false).unwrap();
        println!("{:?}", tokens);

        let tree: Node = parse(tokens, false);
        println!("{:?}", tree);

        println!("{}", tree.evaluate().unwrap());
    }
}
