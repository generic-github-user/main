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

impl Node {
    pub fn evaluate(self, symbols: &mut HashMap<String, Value>, verbose: bool) -> Option<Value> {
        return None;
    }
}
