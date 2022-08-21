#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

const vector<string> operators = {
		"+", "-", "*", "/", "%", "**",
		"==", "!+", "<", "<=", ">", ">=",
		"&", "|", "<<", ">>",
		"..", "+-"
};
const string symbols = "()[]<>{}!@#$%^&*`~,.;:-_=+";

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

		token,
		whitespace,
		comment,

		// "Literal" types for primitives (mainly numbers, strings, booleans)
		integer,
		float_,
		number,
		string_,

		// Expression types (or types that will eventually be transformed into an
		// expression; excludes special cases like statements used as expressions).
		// Most of these are composable.
		identifier,
		symbol,

		tuple_,
		operator_,
		operation,
		call,
		expression,

		// Statement types, whose primary purpose (in the language semantics) is to
		// "do something" to the program state, whether globally or within a
		// specific scope
		assignment,
		statement,
		block,
		root,
		unmatched
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
		//char value;
		string value;
		string text;

		string file;
		int line;
		int column;

		vector<Node> subnodes;
		Node* parent;

		Node (nodetype t, string v, Node* p) : type(t), value(v), parent(p) { }
		Node (nodetype t) : type(t) { }

		bool is_expression () {
				return (type == integer || type == float_ ||
								type == string_ || type == operation);
		}

		void print () {
				cout << text;
				for (Node n : subnodes) n.print();
		}
};

void lexchar(Node* base, Node* prev, char c) {
		// overview of lexing rules:
		// - if in a comment, absorb the character
		// - if the immediate context is a numeric type, subsequent digits are
		// assumed to be part of it
		// - a similar rule is observed for chunks of whitespace
		// - identifiers need to start with a non-digit to differentiate them
		// from numbers or coefficient notation

		string cs = std::string(1, c);
		Node* nn;
		nodetype current_type = unmatched;

		// determine primary category of current character
		if (inrange(c, 'a', 'z')) { current_type = nodetype::letter; }
		else if (inrange(c, '0', '9')) { current_type = nodetype::digit; }
		else if (std::string("\t ").find(c)) { current_type = whitespace; }
		else if (symbols.find(c)) { current_type = symbol; }

		if (prev -> type == current_type) {
				prev -> text += c;
		} else {
				nn = new Node(current_type, cs, base);
				base -> subnodes.push_back(*nn);
		}
}

// Process a single character, assumed to be immediately after the char that
// was most recently integrated into the parse tree (ignoring newlines)
void parsetoken (vector<Node>* context, Node* t) {
		Node* nn;
		Node* current = &(*context).back();

		// TODO: check that we're using pointers to nodes where
		// appropriate rather than passing by value (particularly
		// when modifying them...)

		// opening a new tuple form adds another context layer...
		if (t->value == "(") {
				cout << "Opened tuple\n";
				cout << "Adding node\n";
				nn = new Node(tuple_, "", current);
				context -> push_back(*nn);
				(current -> subnodes).push_back(*nn);
				current = &(context -> back());
		}
		// ...and closing it removes one
		if (t->value == ")") {
				cout << "Closed tuple\n";
				context -> pop_back();
				current = current -> parent;
		}

}

int main() {
		Node astroot = Node(root);
		astroot.subnodes.push_back(Node(token, "", &astroot));
		vector<Node> context = { astroot };
		// TODO: create a secondary tree marking "spans" of text (e.g., lines) that
		// may contain parts of different nodes

		string line;
		ifstream src;

		src.open("example.fn");
		if (src.is_open()) {
				while (getline(src, line)) {
						std::cout << line << '\n';
						for (char& c : line) if (c)
								lexchar(&context[0], &context[0].subnodes.back(), c);
				}
				for (Node& n : context[0].subnodes) parsetoken(&context, &n);
		}
		else cout << "could not open file";

		context[0].print();

		return 0;
}
