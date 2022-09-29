/// Represents a category of token processed by the lexer; used in the very first stage of the
/// parsing pipeline, which happens in parallel with token aggregation
#[derive(PartialEq, Eq, Debug, Clone)]
pub enum CharType {
    Whitespace,
    Alphanumeric,
    Symbol,
    Newline,
    Quote,
    String,
    Letter,
    Digit,
    Unknown,
    None
}
