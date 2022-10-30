// extern crate pest;
// #[macro_use]
// extern crate pest_derive;

// use self::AstNode::*;
// use pest::error::Error;
// use pest::Parser;
use pest::pratt_parser;

// #[derive(Parser)]
// #[grammar = "../grammar.pest"]
// pub struct MainParser;

pub enum AstNode {
    Int(i32)
}

fn main() {
    let source = std::fs::read_to_string("stdlib.z").expect("cannot read file");
}
