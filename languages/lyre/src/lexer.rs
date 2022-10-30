use std::fs::File;
use std::io::{BufReader, BufRead, Error};

use super::token::Token;
use super::chartype::CharType;

pub fn lex(source: String, verbose: bool) -> Result<Vec<Token>, Error> {
    // This section has a simple lexer that splits lyre source code into tokens, groups of
    // consecutive characters with similar syntactic purposes

    // A list of tokens parsed from the input program's source code
    let mut tokens = Vec::<Token>::new();
    for line in source.lines() {
        if verbose { println!("Parsing line: {}", line); }

        // Stores the type of the previous character
        let mut ptype = CharType::None;
        // Stores the type of the current character
        let mut ctype = CharType::None;
        // The text content of the current token; incrementally grown as new characters are
        // consumed
        let mut current: String = String::from("");

        // Iterate over characters in line
        for c in line.chars() {
            // Categorize characters by syntactic type (refer to the CharType enum for information
            // about specific types)
            // if c.is_alphanumeric() { ctype = CharType::Alphanumeric; }
            if c.is_digit(10) { ctype = CharType::Digit; }
            else if c.is_alphabetic() { ctype = CharType::Letter; }
            else if c == '\n' { ctype = CharType::Newline; }
            else if c.is_whitespace() { ctype = CharType::Whitespace; }
            else if c == '[' { ctype = CharType::LeftSB; }
            else if c == ']' { ctype = CharType::RightSB; }
            else if c == '"' && ptype != CharType::String { ctype = CharType::String; }
            else { ctype = CharType::Symbol; }

            if ptype == CharType::String && c != '"' {
                ctype = CharType::String;
            }
            if verbose { println!("Lexing character {} as {:?}", c, ctype); }

            // If the character type is unchanged from the previous step, append it to the current
            // token string ...
            if ctype == ptype && ctype != CharType::LeftSB && ctype != CharType::RightSB {
                current += String::from(c).as_ref();
            }
            // ... otherwise, start a new token and store the current one
            else {
                if ptype != CharType::None {
                    let ntoken = Token {
                        content: if ptype == CharType::String { String::from(&current[1..]) }
                                 else { current },
                        chartype: ptype
                    };
                    if verbose { println!("Finished token {:?}", ntoken); }
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
        if verbose { println!("Finished token {:?}", ntoken); }
        tokens.push(ntoken);

        // Insert newline character after parsing line
        tokens.push(Token { 
            content: String::from(""),
            chartype: CharType::Newline
        });
    }
    if verbose { println!("Parsed {} tokens", tokens.len()); }
    // println!("{}", tokens);
    Ok(tokens)
}
