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

impl<'a> Node<'a> {
    /// Recursively evaluates an AST node, (possibly) returning a `Value`. Some built-ins that are
    /// delegated to Rust's standard library are handled here, as well as special operators like
    /// the `def` keyword. The plan is to gradually move an increasingly large subset of this
    /// "internal" functionality to lyre-based code; if a full compiler is ever created,
    /// bootstrapping the entire language featureset is also a possibility.

    // fn evaluate(&self) -> Result<Value, Error> {
    fn evaluate(&self) -> Option<Value> {
        let mut symbols: HashMap<String, &Value> = HashMap::new();
        if self.content[0].content == "def" {
            let def = Token::new("def");
            // let val = Error::new();

            match self.children[..] {
                [def, name, value] => {
                    let val = Value {
                        vtype: String::from("auto"),
                        value: &value
                    };
                    symbols.insert(name.to_string(), &val);
                    return Some(val);
                }

                [def, vtype, name, value] => {
                    let val = Value {
                        vtype: vtype.to_string(),
                        value: &value
                    };
                    symbols.insert(name.to_string(), &val);
                    return Some(val);
                }

                _ => todo!()
            }

            // return val;
        }
        // roughly equivalent to the progn special form in Common Lisp (see
        // https://www.gnu.org/software/emacs/manual/html_node/eintr/progn.html for more
        // information) -- evaluates each sub-form, returning the value of the last one
        else if self.content[0].content == "prog" {
            let mut result = None;
            for node in self.children {
                result = node.evaluate();
            }
            return result;
        }
        // if the first symbol isn't a keyword, interpret it as a function name that should be
        // called with the subsequent symbols and forms as arguments
        else {
            let rest = &self.children[1..];
            match self.content[0].content.as_str() {
                "print" => {
                    let value = rest[0].evaluate().unwrap();
                    print!("{}", value);
                    return Some(value);
                },
                "println" => {
                    let value = rest[0].evaluate().unwrap();
                    println!("{}", value);
                    return Some(value);
                },
            }
        }

        return None;
    }
}

struct Value<'a> {
    vtype: String,
    value: &'a Node<'a>
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
