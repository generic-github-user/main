#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

bool inrange(int x, int a, int b) {
		return x >= a && x <= b;
}

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
class Node {
		public:

		string typestring;
		nodetype type;
		//T value;
		char value;

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
		vector<Node> context;
		Node* current;

		string line;
		ifstream src;
		src.open("example.fn");
		if (src.is_open()) {
				while (getline(src, line)) {
						std::cout << line;
						for (char c : line) {
								nodetype current_type;
								if (inrange(c, 'a', 'z')) { current_type = nodetype::letter; }
								if (inrange(c, '0', '9')) { current_type = nodetype::digit; }
						}
				}
		}
		else cout << "could not open file";
		return 0;
}
