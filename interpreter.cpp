#include <map>
#include <string>
#include <vector>

#include <stdlib.h>

#define FMT_HEADER_ONLY
#include "include/fmt/core.h"
#include "include/fmt/format.h"

using namespace std;

enum nodetype {
		letter, digit,
		token, whitespace, comment,
		integer, float_, number, string_,
		identifier, symbol,
		tuple_, operator_, operation, call, expression,
		assignment, statement, block, root, unmatched
};

class Node {
		public:

		string typestring;
		nodetype type;
		string value;
		string text;

		string file;
		int line;
		int column;

		vector<Node> subnodes;
		Node* parent;

		Node (nodetype t, string v, Node* p);
		Node (nodetype t);

		Node* add(nodetype t, string v);
		bool is_expression ();
		void print (int depth=0);
};

void interpret(Node* ast, std::unordered_map<string, Object*> names) {
		switch (ast -> type) {
		}
}
