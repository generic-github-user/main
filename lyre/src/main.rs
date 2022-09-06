use std::fs::File;
use std::io::{BufReader, BufRead, Error};
use std::fmt;
use std::collections::HashMap;

/// Represents a token generated by the lexer during the parsing stage; generally groups several
/// contiguous characters by their type as defined in the CharType enum
#[derive(PartialEq, Debug, Clone)]
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
#[derive(PartialEq, Debug, Clone)]
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

/// General Node struct methods
impl<'a> Node {
    /// Takes a list of indices and returns the final node in the path they describe (in which each
    /// index corresponds to a child node/subnode in the next level of the tree)
    fn get(&'a mut self, path: Vec<usize>) -> &'a mut Node {
        let mut result = self;
        for i in path.clone() {
            if i >= result.children.len() {
                eprintln!("{:?}", path.clone());
                // self.print(0);
            }
            result = &mut result.children[i];
        }
        return result;
    }

    fn print(&self, level: u8) -> () {
        print!("{}", "  ".repeat(level as usize));
        let ntype = if !self.content.is_empty() { self.content[0].chartype.clone() }
                    else { CharType::None };
        print!("<{:?}> {}\n", ntype, self);
        for c in self.children.iter() {
            c.print(level+1);
        }
    }
}

/// Enables the Display and ToString traits for Node structs
impl<'a> fmt::Display for Node {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}",
            self.content.iter()
            .map(|t| t.to_string())
            .collect::<Vec<String>>()
            .join(" "))
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

/// Used to represent primitive data types like ints and floats with direct equivalents in Rust's
/// data model; literals from the AST can be parsed directly into variants of this enum. Compound
/// types (lists, arrays, tuples, dictionaries, etc.) are implemented in lyre itself.
#[derive(Debug)]
enum ValueType {
    // Signed integer types
    i8(i8),
    i16(i16),
    i32(i32),
    i64(i64),
    i128(i128),

    // Unsigned integer types
    u8(u8),
    u16(u16),
    u32(u32),
    u64(u64),
    u128(u128),

    // Floating-point number types
    f32(f32),
    f64(f64),

    // Other basic types
    bool(bool),
    char(char)
}

fn lex(buffer: BufReader<File>) -> Result<Vec<Token>, Error> {
    // This section has a simple lexer that splits lyre source code into tokens, groups of
    // consecutive characters with similar syntactic purposes

    // A list of tokens parsed from the input program's source code
    let mut tokens = Vec::<Token>::new();
    for line in buffer.lines() {
        println!("Parsing line: {}", line.as_ref().unwrap());
        // Stores the type of the previous character
        let mut ptype = CharType::None;
        // Stores the type of the current character
        let mut ctype = CharType::None;
        // The text content of the current token; incrementally grown as new characters are
        // consumed
        let mut current: String = String::from("");

        // Iterate over characters in line
        for c in line?.chars() {
            // Categorize characters by syntactic type (refer to the CharType enum for information
            // about specific types)
            if c.is_alphanumeric() { ctype = CharType::Alphanumeric; }
            else if c == '\n' { ctype = CharType::Newline; }
            else if c.is_whitespace() { ctype = CharType::Whitespace; }
            else if c == '[' { ctype = CharType::LeftSB; }
            else if c == ']' { ctype = CharType::RightSB; }
            else if c == '"' && ptype != CharType::String { ctype = CharType::String; }
            else { ctype = CharType::Symbol; }

            if ptype == CharType::String && c != '"' {
                ctype = CharType::String;
            }
            println!("Lexing character {} as {:?}", c, ctype);

            // If the character type is unchanged from the previous step, append it to the current
            // token string ...
            if ctype == ptype && ctype != CharType::LeftSB && ctype != CharType::RightSB {
                current += String::from(c).as_ref();
            }
            // ... otherwise, start a new token and store the current one
            else {
                if ptype != CharType::None {
                    let ntoken = Token {
                        content: current,
                        chartype: ptype
                    };
                    println!("Finished token {:?}", ntoken);
                    tokens.push(ntoken);
                }
                current = String::from(c);
            }

            ptype = ctype;
        }

        let ntoken = Token {
            content: current,
            chartype: ptype
        };
        println!("Finished token {:?}", ntoken);
        tokens.push(ntoken);

        // Insert newline character after parsing line
        tokens.push(Token { 
            content: String::from(""),
            chartype: CharType::Newline
        });
    }
    println!("Parsed {} tokens", tokens.len());
    // println!("{}", tokens);
    Ok(tokens)
}

fn main () -> Result<(), Error> {
    let path = "sample";
    let input = File::open(path)?;
    let buffered = BufReader::new(input);

    let mut root = Node {
        content: vec![],
        children: vec![],
    };
    let tokens = lex(buffered).unwrap();
    
    // a list of indices representing a path through the abstract syntax tree generated by the
    // parser; used to keep track of the current parsing context
    let mut stack = Vec::<usize>::new();
    // stack.push(0);
    let mut indentlevel: usize = 0;
    let mut ptoken: Option<Token> = None;

    for token in tokens {
        // if token.chartype == CharType::LeftSB {
        match token.chartype {
            // A left bracket ([) opens a new form ...
            CharType::LeftSB => {
                let nnode = Node {
                    content: vec![],
                    children: vec![],
                };

                let current = root.get(stack.clone());
                // stack.push(current.children.len());
                stack.push(current.children.len());
                current.children.push(nnode);
            }

            // ... and a right bracket (]) closes it
            CharType::RightSB => {
                stack.pop();
            }

            // An identifier or expression within a form
            CharType::Alphanumeric | CharType::Symbol | CharType::String => {
                let current = root.get(stack.clone());
                let nnode = Node {
                    content: vec![token.clone()],
                    children: vec![]
                };
                current.children.push(nnode);

                // we're adding a new bottom-level node (leaf) to the parent of the last node in
                // the current path
                //if stack.len() == 0 {
                    //stack.push(0);
                //} else {
                   //*stack.last_mut().unwrap() += 1;
                //}
            }

            // Whitespace between tokens/forms or at the beginning of a line (i.e., indentation
            // used to denote sub-forms)
            CharType::Whitespace => {
                if ptoken.is_some() && ptoken.unwrap().chartype == CharType::Newline {
                    if token.content.len() > indentlevel {
                        let nnode = Node {
                            content: vec![],
                            children: vec![],
                        };

                        let current = root.get(stack.clone());
                        stack.push(current.children.len());
                        current.children.push(nnode);
                    } else if token.content.len() == indentlevel {
                        let current = root.get(stack.clone());
                        let nnode = Node {
                            content: vec![token.clone()],
                            children: vec![]
                        };
                        current.children.push(nnode);
                    } else {
                        assert!(token.content.len() < indentlevel);
                        // let current = root.get();
                        // stack.truncate
                        for i in 0..(indentlevel - token.content.len()) {
                            stack.pop();
                        }
                    }

                    indentlevel = token.content.len();
                }
            }

            CharType::Newline => {

            }

            CharType::None => {

            }

            CharType::Quote | CharType::Unknown => {

            }
        }

        ptoken = Some(token.clone());
    }

    //Ok(())
    //return Ok(root.evaluate().unwrap());
    //root.evaluate();

    root.print(0);
    Ok(())
}
