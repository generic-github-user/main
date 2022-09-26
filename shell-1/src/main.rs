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
