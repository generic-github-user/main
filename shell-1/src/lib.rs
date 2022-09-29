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
}
