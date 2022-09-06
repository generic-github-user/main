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

/// Allows printing of Tokens and conversion from Tokens to Strings
impl fmt::Display for Token {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.content)
    }
}

impl Token {
    /// Convenience constructor for Token instances
    fn new(value: &str) -> Token {
        return Token {
            content: String::from(value),
            chartype: CharType::Unknown
        };
    }
}

/// Represents a category of token processed by the lexer; used in the very first stage of the
/// parsing pipeline, which happens in parallel with token aggregation
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

/// An AST node (more accurately, a [sub]tree); generally, these nodes will either be a sequence of
/// tokens or other nodes, but not both
struct Node {
    /// The symbol corresponding to this node, if it is a leaf node
    content: Vec<Token>,

    /// Sub-nodes forming the tree rooted at this node
    // children: Vec<&'a Node<'a>>,
    children: Vec<Node>,
}

impl<'a> Node {
    fn get(&'a mut self, path: Vec<usize>) -> &'a mut Node {
        let mut result = self;
        for i in path {
            result = &mut result.children[i];
        }
        return result;
    }
}

impl<'a> fmt::Display for Node {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}",
            self.content.iter()
            .map(|t| t.to_string())
            .collect::<Vec<String>>()
            .join(""))
    }
}

fn main () -> Result<(), Error> {
    let path = "sample";
    let input = File::open(path)?;
    let buffered = BufReader::new(input);

    let mut root = Node {
        content: vec![],
        children: vec![],
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
    
    let mut stack = Vec::<usize>::new();
    for token in tokens {
        // if token.chartype == CharType::LeftSB {
        match token.chartype {
            CharType::LeftSB => {
                let mut nnode = Node {
                    content: vec![],
                    children: vec![],
                };

                let mut current = root.get(stack.clone());
                stack.push(current.children.len());
                current.children.push(nnode);
            }

            CharType::RightSB => {
                stack.pop();
            }

            CharType::Alphanumeric | CharType::Symbol => {
                let mut current = root.get(stack.clone());
                let nnode = Node {
                    content: vec![token],
                    children: vec![]
                };
                current.children.push(nnode);
                *stack.last_mut().unwrap() += 1;
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
    //root.evaluate();
    Ok(())
}
