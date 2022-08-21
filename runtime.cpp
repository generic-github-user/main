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

void parsechar (vector<Node>* context, char c) {
		string cs = std::string(1, c);
		Node* nn;
		nodetype current_type = unmatched;
		Node* current = &(*context)[0];

		if (inrange(c, 'a', 'z')) { current_type = nodetype::letter; }
		else if (inrange(c, '0', '9')) { current_type = nodetype::digit; }
		else if (std::string("\t ").find(c)) { current_type = whitespace; }
		else if (std::find(operators.begin(), operators.end(), cs) != operators.end())
		//else if (std::any_of(operators.begin(), operators.end(), [=](string s){return s==cs;}))
				{ current_type = operator_; }

		if (current -> type == root && (
				current_type == digit)) {
				cout << "Adding node\n";
				nn = new Node(current_type, cs, current);

				// TODO: check that we're using pointers to nodes where
				// appropriate rather than passing by value (particularly
				// when modifying them...)

				context -> push_back(*nn);
				(current -> subnodes).push_back(*nn);
				current = &(context -> back());
		}

		if (current_type == comment) {
				current -> text += c;
		}
		else if (current_type == string_) {
				if (c == '"') {
						context -> pop_back();
						current = current -> parent;
				}
				else current -> text += c;
		}
		else {
				if (c == '(') {
						cout << "Opened tuple\n";
						nn = new Node(tuple_, cs, current);
						context -> push_back(*nn);
						(current -> subnodes).push_back(*nn);
						current = &(context -> back());
				}
				if (c == ')') {
						cout << "Closed tuple\n";
						context -> pop_back();
						current = current -> parent;
				}

				if (current_type == digit &&
								(current -> type == integer || current -> type == float_)) {
						current -> text += c;
				}

				if (current_type == whitespace && current -> type == whitespace) {
						current -> text += c;
				}

				if ((current_type == letter ||
						current_type == digit) &&
						current -> type == identifier) {
						current -> text += c;
				}
		}
}

int main() {
		vector<Node> context = { Node(root) };
		// TODO: create a secondary tree marking "spans" of text (e.g., lines) that
		// may contain parts of different nodes

		string line;
		ifstream src;

		src.open("example.fn");
		if (src.is_open()) {
				while (getline(src, line)) {
						std::cout << line << '\n';
						for (char& c : line) parsechar(&context, c);
				}
		}
		else cout << "could not open file";

		context[0].print();

		return 0;
}
