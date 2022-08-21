#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

bool inrange(int x, int a, int b) {
		return x >= a && x <= b;
}

enum nodetype {
		letter,
		digit,
		whitespace,
		comment,

		integer,
		float_,
		number,
		string_,

		identifier,
		symbol,

		tuple_,
		operator_,
		operation,
		call,
		expression,

		assignment,
		statement,
		block,
		root,
		unmatched
};


//template <class T>
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

		Node (nodetype t, string v) : type(t), value(v) { }
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

int main() {
		vector<Node> context = { Node(root) };
		Node* current = &context[0];
		Node* nn;
		// TODO: create a secondary tree marking "spans" of text (e.g., lines) that
		// may contain parts of different nodes
		
		const vector<string> operators = {
				"+", "-", "*", "/", "%", "**",
				"==", "!+", "<", "<=", ">", ">=",
				"&", "|", "<<", ">>",
				"..", "+-"
		};

		string line;
		ifstream src;
		string cs;

		src.open("example.fn");
		if (src.is_open()) {
				while (getline(src, line)) {
						std::cout << line << '\n';
						for (char& c : line) {
								cs = std::string(1, c);
								nodetype current_type = unmatched;

								if (inrange(c, 'a', 'z')) { current_type = nodetype::letter; }
								else if (inrange(c, '0', '9')) { current_type = nodetype::digit; }
								else if (std::string("\t ").find(c)) { current_type = whitespace; }
								else if (std::find(operators.begin(), operators.end(), cs) != operators.end())
								//else if (std::any_of(operators.begin(), operators.end(), [=](string s){return s==cs;}))
										{ current_type = operator_; }

								if (current -> type == root && (
										current_type == digit)) {
										cout << "Adding node";
										nn = new Node(current_type, cs);

										// TODO: check that we're using pointers to nodes where
										// appropriate rather than passing by value (particularly
										// when modifying them...)

										context.push_back(*nn);
										(current -> subnodes).push_back(*nn);
										current = &context.back();
								}

								if (current_type == comment) {
										current -> text += c;
								}
								else if (current_type == string_) {
										if (c == '"') {
												context.pop_back();
												current = current -> parent;
										}
										else current -> text += c;
								}
								else {
										if (current_type == digit &&
														(current -> type == integer || current -> type == float_)) {
												current -> text += c;
										}

										if (current_type == whitespace && current -> type == whitespace)
												current -> text += c;

										if ((current_type == letter ||
												current_type == digit) &&
												current -> type == identifier) {
												current -> text += c;
										}
								}
						}
				}
		}
		else cout << "could not open file";

		context[0].print();

		return 0;
}
