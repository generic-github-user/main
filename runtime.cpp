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
// definitions, etc.
enum nodetype {
		letter,
		digit,

		integer,
		float_,
		number,
		string_,

		identifier,
		tuple_,
		symbol,
		operator_,
		operation,
		call,
		expression,

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
