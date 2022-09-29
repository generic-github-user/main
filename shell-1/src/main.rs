use std::io;
use std::io::Write;
use std::env::args;
use std::time::SystemTime;
use chrono::{DateTime, Utc};
use clap::Parser;

mod lexer;
mod parser;
mod token;
mod node;
mod chartype;
mod value;

use lexer::lex;
use parser::parse;
use node::Node;

// mod lib;
// use lib::test;

#[derive(Parser, Debug)]
#[clap(version, about)]
struct Args {
    #[clap(short, long, value_parser, default_value="")]
    path: String,

    // #[clap(short, long, default_value_t=false)]
    #[clap(short, long, action)]
    debug: bool
}

fn main() {
    let mut input = String::new();
    // let now = SystemTime::now();
    let now = Utc::now();
    let args = Args::parse();
    println!("{:#?}", args);
    println!("shell-1 | {}", now);
    loop {
        print!("~ ");
        io::stdout().flush();
        input.clear();
        io::stdin().read_line(&mut input).unwrap();

        let tokens = lex(input.clone(), false).unwrap();
        if args.debug {
            println!("{:#?}", tokens);
        }

        let tree: Node = parse(tokens, false);
        if args.debug {
            println!("{:#?}", tree);
        }

        println!("{}", tree.evaluate().unwrap());
    }
}
