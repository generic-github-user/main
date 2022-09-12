use std::fmt;
use std::collections::HashMap;

use super::token::Token;
// use super::nodetype::NodeType;
use super::chartype::CharType;
use super::value::{Value, ValueType};

use num_traits::Pow;

/// An AST node (more accurately, a [sub]tree); generally, these nodes will either be a sequence of
/// tokens or other nodes, but not both
#[derive(Debug, Clone)]
pub struct Node {
    /// The symbol corresponding to this node, if it is a leaf node
    pub content: Option<Token>,

    /// Sub-nodes forming the tree rooted at this node
    // children: Vec<&'a Node<'a>>,
    pub children: Vec<Node>,

    pub nodetype: NodeType
}

/// General Node struct methods
impl<'a> Node {
    /// Takes a list of indices and returns the final node in the path they describe (in which each
    /// index corresponds to a child node/subnode in the next level of the tree)
    pub fn get(&'a mut self, path: Vec<usize>) -> &'a mut Node {
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

    pub fn print(&self, level: u8) -> () {
        print!("{}", "  ".repeat(level as usize));
        let ntype = self.nodetype.clone();
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

#[derive(PartialEq, Debug, Clone)]
pub enum NodeType {
    Form,
    Token,
    Program,
    String,
    Integer,
    Whitespace,
    None
}

macro_rules! op_match {
    ($op:tt, $r:ident, $v:ident, $s:ident) => {
        {
            let A = $r[0].evaluate($s, $v).unwrap();
            let B = $r[1].evaluate($s, $v).unwrap();
            if $v { println!("{} {}", A, B); }
            return Some(A $op B);
        }
    }
}


/// Provides the implementation(s) for methods on the `Node` type, most notably `Node.evaluate`
impl Node {
    /// Recursively evaluates an AST node, (possibly) returning a `Value`. Some built-ins that are
    /// delegated to Rust's standard library are handled here, as well as special operators like
    /// the `def` keyword. The plan is to gradually move an increasingly large subset of this
    /// "internal" functionality to lyre-based code; if a full compiler is ever created,
    /// bootstrapping the entire language featureset is also a possibility.

    // fn evaluate(&self) -> Result<Value, Error> {
    pub fn evaluate(&self, symbols: &mut HashMap<String, Value>, verbose: bool) -> Option<Value> {
        if verbose {
            println!("{}", "Evaluating node:");
            self.print(1);
        }

        // let mut symbols: HashMap<String, &Value> = HashMap::new();
        // let mut symbols = symbols.clone();

        // Matches a literal node, generally a single token that represents a value; the
        // interpreter can use these nodes directly for computations, which is generally done with
        // primitive types that correspond directly to simple data types in Rust (strings,
        // integers, floats, etc. -- see ValueType for the full list).
        //
        // This block converts string literals into `Value`s in which `vtype == "string"` and
        // `value` is of the enum type `ValueType::string`
        if self.content.is_some() && self.content.clone().unwrap().chartype == CharType::String {
            assert!(self.children.is_empty());
            if verbose { println!("{}", "Evaluating node that represents a value: string literal"); }
            return Some(Value {
                vtype: String::from("string"),
                value: ValueType::string(
                    self.content.clone().unwrap().content)
            });
        }
        else if self.content.is_some() && self.nodetype == NodeType::Integer {
            assert!(self.children.is_empty());
            if verbose { println!("{}", "Evaluating node that represents a value: integer literal"); }
            return Some(Value {
                vtype: String::from("int"),
                value: ValueType::i64(
                    self.content.clone().unwrap().content
                    .parse().unwrap())
            });
        }

        // handles the `def` keyword, which sets its first argument (i.e., in the current
        // namespace) to a form consisting of all subsequent arguments
        else if !self.children.is_empty() && self.children[0].clone().content == Some(Token::new("def", CharType::Letter)) {
            if verbose { println!("{}", "Evaluating function, class, or type definition (def keyword)"); }

            let def = Token::new("def", CharType::Letter);
            // let val = Error::new();

            match &self.children[..] {
                [def, name, value] => {
                    if verbose { println!("{}", "Matched untyped definition, will attempt to infer type"); }
                    let val = Value {
                        vtype: String::from("auto"),
                        value: ValueType::Form(value.clone())
                    };
                    symbols.insert(name.to_string(), val.clone());
                    return Some(val.clone());
                }

                [def, vtype, name, value] => {
                    if verbose { println!("{}", "Matched typed definition"); }
                    let val = Value {
                        vtype: vtype.to_string(),
                        value: ValueType::Form(value.clone())
                    };
                    symbols.insert(name.to_string(), val.clone());
                    return Some(val.clone());
                }

                _ => todo!()
            }

            // return val;
        }

        // if the first symbol isn't a keyword, interpret it as a function name that should be
        // called with the subsequent symbols and forms as arguments
        else if !self.children.is_empty() && self.children[0].content.is_some() {
        // else if !self.children.is_empty() {
            if verbose { println!("{}", "Found generic form, interpreting as function call"); }

            let rest = &self.children[1..];
            if verbose { println!("Operands are {:?}", rest); }
            match self.children[0].clone().content.unwrap().to_string().as_str() {
                "print" => {
                    if verbose { println!("{}", "Executing internal call (implementation-level)"); }
                    let value = rest[0].evaluate(symbols, verbose).unwrap();
                    print!("{}", value);
                    return Some(value);
                },

                "println" => {
                    if verbose { println!("{}", "Executing internal call (implementation-level)"); }
                    let value = rest[0].evaluate(symbols, verbose).unwrap();
                    println!("{}", value);
                    return Some(value);
                },

                // "add" | "+" => Value::new(rest[1].evaluate().unwrap() + rest[2].evaluate().unwrap()),
                "add" | "+" => op_match!(+, rest, verbose, symbols),
                "sub" | "-" => op_match!(-, rest, verbose, symbols),
                "mul" | "*" => op_match!(*, rest, verbose, symbols),
                "div" | "/" => op_match!(/, rest, verbose, symbols),
                "pow" | "**" => {
                    let A = rest[0].evaluate(symbols, verbose).unwrap();
                    let B = rest[1].evaluate(symbols, verbose).unwrap();
                    if verbose { println!("{} {}", A, B); }
                    return Some(A.pow(B));
                }

                "set" => {
                    let name = rest[0].to_string();
                    if verbose { println!("Setting name {} (in current scope)", name); }
                    let value = rest[1].evaluate(symbols, verbose).unwrap();
                    symbols.insert(name, value.clone());
                    return Some(value);
                }

                "get" => {
                    let name = rest[0].to_string();
                    if verbose { println!("Getting name {} (in current scope)", name); }
                    return match symbols.get(&String::from(name)) {
                        // Some(value) => Some((*value.clone()).clone()),
                        Some(value) => Some(value.clone()),
                        None => panic!("undefined")
                    };
                }

                name => {
                    let target = symbols.get(&String::from(name));
                    // if target.type != "function"
                    match target {
                        // Some(tval) => tval.value.evaluate()
                        Some(tval) => {
                            match tval.value.clone() {
                                ValueType::Form(body) => {
                                    return body.evaluate(symbols, verbose);
                                },
                                _ => panic!("Cannot execute a non-Form type as a function; aborting")
                            }
                        },
                        None => panic!("undefined")
                    }
                }

                _ => todo!(),
                // _ => None
            };
        }

        else if self.children.is_empty() && self.content.is_some() {
            let name = self.to_string();
            if verbose { println!("Getting name {} (in current scope)", name); }
            return match symbols.get(&String::from(name)) {
                // Some(value) => Some((*value.clone()).clone()),
                Some(value) => Some(value.clone()),
                None => panic!("undefined")
            };
        }

        // roughly equivalent to the progn special form in Common Lisp (see
        // https://www.gnu.org/software/emacs/manual/html_node/eintr/progn.html for more
        // information) -- evaluates each sub-form, returning the value of the last one (somewhat
        // similarly to Rust's block return value semantics, though they are not directly
        // applicable here because of the additional layer of abstraction)
        else if (!self.children.is_empty() &&
            self.children[0].clone().content == Some(Token::new("prog", CharType::Letter)))
            || (self.content.is_none() && !self.children.is_empty()) {

            if verbose { println!("{}", "Evaluating as prog form or statement list"); }

            let mut result = None;
            for node in self.children.iter() {
                result = node.evaluate(symbols, verbose);
            }
            return result;
        }

        // any other types of expressions should cause a panic
        else {
            println!("Could not evaluate node (no pattern matched)");
            self.print(1);
            panic!();
        }

        return None;
    }
}
