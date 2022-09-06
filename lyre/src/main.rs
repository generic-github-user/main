use std::fs::File;
use std::io::{BufReader, BufRead, Error};
use std::fmt;
use std::collections::HashMap;

/// Represents a token generated by the lexer during the parsing stage; generally groups several
/// contiguous characters by their type as defined in the CharType enum
struct Token {
    content: String,
    chartype: CharType
}

impl fmt::Display for Token {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.content)
    }
}

impl Token {
    fn new(value: &str) -> Token {
        return Token {
            content: String::from(value),
            chartype: CharType::Unknown
        };
    }
}

#[derive(PartialEq)]
enum CharType {
    Whitespace,
    Alphanumeric,
    Symbol,
    Newline,
    LeftSB,
    RightSB,
    Quote,
    String,
    Unknown,
    None
}

struct Node<'a> {
    // content: Option<Token>,
    content: Vec<Token>,
    // children: Vec<&'a Node<'a>>,
    children: Vec<Node<'a>>,
    parent: Option<&'a Node<'a>>
}

impl<'a> fmt::Display for Node<'a> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}",
            self.content.iter()
            .map(|t| t.to_string())
            .collect::<Vec<String>>()
            .join(""))
    }
}

// fn main () -> Result<Value, Error> {
// fn main () -> Option<Value> {
fn main () -> Result<(), Error> {
//fn main () -> Option<Value> {
    let path = "sample";
    let input = File::open(path)?;
    let buffered = BufReader::new(input);

    let mut root = Node {
        content: vec![],
        children: vec![],
        parent: None
    };
    let mut tokens = Vec::<Token>::new();
    for line in buffered.lines() {
        println!("Parsing line: {}", line.as_ref().unwrap());
        let mut ptype = CharType::None;
        let mut ctype = CharType::None;
        let mut current: String = String::from("");

        for c in line?.chars() {
            if c.is_alphanumeric() { ctype = CharType::Alphanumeric; }
            else if c.is_whitespace() { ctype = CharType::Whitespace; }
            else if c == '[' { ctype = CharType::LeftSB; }
            else if c == ']' { ctype = CharType::RightSB; }
            else if c == '"' { ctype = CharType::Quote; }
            else { ctype = CharType::Symbol; }

            if ctype == ptype {
                current += String::from(c).as_ref();
            } else {
                tokens.push(Token {
                    content: current,
                    chartype: ptype
                });
                current = String::from("");
            }

            ptype = ctype;
        }
        tokens.push(Token { 
            content: String::from(""),
            chartype: CharType::Newline
        });
    }
    println!("Parsed {} tokens", tokens.len());
    // println!("{}", tokens);
    
    // let mut stack = Vec::<&mut Node>::new();
    // let current: Option<&Node> = None;
    let mut current = &mut root;
    // stack.push(&mut root);
    for token in tokens {
        // if token.chartype == CharType::LeftSB {
        match token.chartype {
            CharType::LeftSB => {
                /*let mut nnode = Box::new(
                    Node {
                        content: vec![],
                        children: vec![]
                    }
                );*/
                /*let mut nnode = box Node {
                    content: vec![],
                    children: vec![]
                };*/

                //stack.last().as_mut().unwrap().children.push(nnode);
                //current.unwrap().children.push(nnode);
                //stack.last_mut().unwrap().children.push(&nnode);
                //stack.push(stack.last().unwrap()
                            //.children.last_mut().unwrap());

                let mut nnode = Node {
                    content: vec![],
                    children: vec![],
                    parent: Some(current)
                };
                // current.children.push(&mut nnode);
                current.children.push(nnode);
            }

            CharType::RightSB => {
                //stack.pop();
            }

            CharType::Alphanumeric | CharType::Symbol => {

            }

            CharType::Whitespace => {

            }

            CharType::Newline => {

            }

            CharType::String => {

            }

            CharType::None => {

            }

            CharType::Quote | CharType::Unknown => todo!()
        }
    }

    //Ok(())
    //return Ok(root.evaluate().unwrap());
    root.evaluate();
    Ok(())
}
