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

