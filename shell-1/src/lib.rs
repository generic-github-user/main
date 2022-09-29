mod lexer;
mod parser;
mod token;
mod node;
mod chartype;
mod value;

#[cfg(test)]
mod tests {
    use super::parser::parse;
    use super::lexer::lex;
    use super::token::Token;
    use super::chartype::CharType;
    use super::node::{Node, NodeType};
    use super::value::Value;

    #[test]
    fn lex_empty() {
        let result = lex("".to_string(), false);
        assert_eq!(result.unwrap(), vec![]);
    }

    #[test]
    fn lex_token() {
        let result = lex("echo".to_string(), false);
        assert_eq!(result.unwrap(), vec![Token {
            content: "echo".to_string(),
            chartype: CharType::String
        }]);
    }

    #[test]
    fn lex_args() {
        let result = lex("echo Hello world".to_string(), false);
        assert_eq!(result.unwrap(), vec![
            Token {
                content: "echo".to_string(),
                chartype: CharType::String
            },
            Token {
                content: " ".to_string(),
                chartype: CharType::Whitespace
            },
            Token {
                content: "Hello".to_string(),
                chartype: CharType::String
            },
            Token {
                content: " ".to_string(),
                chartype: CharType::Whitespace
            },
            Token {
                content: "world".to_string(),
                chartype: CharType::String
            }
        ]);
    }

    #[test]
    fn parse_empty() {
        let result = parse(vec![], false);
        assert_eq!(result, Node {
            content: None,
            children: vec![],
            nodetype: NodeType::Program
        });
    }

    #[test]
    fn eval_empty() {
        let result = Node {
            content: None,
            children: vec![],
            nodetype: NodeType::Program
        }.evaluate();
        assert_eq!(result.unwrap(), Value { value: String::new() });
    }

    #[test]
    fn eval_reverse() {
        let result = Node {
            content: None,
            children: vec![
                Node {
                    content: Some(Token { content: "reverse".to_string(),
                                     chartype: CharType::String }),
                    children: vec![],
                    nodetype: NodeType::String
                },
                Node {
                    content: Some(Token { content: "12345".to_string(),
                                     chartype: CharType::String }),
                    children: vec![],
                    nodetype: NodeType::String
                }
            ],
            nodetype: NodeType::Program
        }.evaluate();
        assert_eq!(result.unwrap(), Value { value: "54321".to_string() });
    }
}
