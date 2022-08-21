#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

// Returns true if a <= x <= b and false otherwise (used for concisely
// categorizing ASCII character ranges)
bool inrange(int x, int a, int b) {
		return x >= a && x <= b;
}

// A list of simple AST node types, including literals (e.g., strings and
// numbers), control flow constructs, statements, expressions, identifiers,
// definitions, etc. These roughly correspond to the types specified in the
// Finch grammar(s) from the specification and/or the reference
// implementations.
enum nodetype {
		// Single-character types for the lexer
		letter,
		digit,

		// "Literal" types for primitives (mainly numbers, strings, booleans)
		integer,
		float_,
		number,
		string_,

		// Expression types (or types that will eventually be transformed into an
		// expression; excludes special cases like statements used as expressions).
		// Most of these are composable.
		identifier,
		tuple_,
		symbol,
		operator_,
		operation,
		call,
		expression,

		// Statement types, whose primary purpose (in the language semantics) is to
		// "do something" to the program state, whether globally or within a
		// specific scope
		assignment,
		statement,
		block
};

//template <class T>

// An AST node, which can represent any syntactic construct in the language;
// generally intended to support a tree-like structure that can be recursively
// evaluated, analyzed, and optimized
class Node {
		public:

		string typestring;
		nodetype type;
		//T value;
		char value;

		vector<Node> subnodes;
		Node* parent;

		Node (nodetype t, char v) : type(t), value(v) { }
};
