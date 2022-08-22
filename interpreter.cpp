#include <map>
#include <unordered_map>

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
		assignment, statement, block, root, declaration,
		unmatched
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

		// if there is a better way to do this, I am not aware of it
		virtual Node op();

		virtual string name();

		virtual vector<Node*> args();
		virtual vector<Node*> body();

		virtual vector<Node*> params();
};

void interpret(Node* ast, std::unordered_map<string, Object*> names) {

//class vNode { };
//template <class T>
class Object {
		int cvalue;
		Object* type;
		int size;

		public:

		Object (int v) : cvalue(v) { }
};
		switch (ast -> type) {
		}
}
