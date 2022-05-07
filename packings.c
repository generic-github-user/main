#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

int MAX_WIDTH = 10;
int MAX_BLOCKS = 100;

// Based on code from https://stackoverflow.com/a/3219471
#define RED     "\x1b[31m"
#define GREEN   "\x1b[32m"
#define YELLOW  "\x1b[33m"
#define BLUE    "\x1b[34m"
#define MAGENTA "\x1b[35m"
#define CYAN    "\x1b[36m"
#define RESET   "\x1b[0m"

// char COLOR_ORDER = { RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA };
// TODO: implement arrayview
// TODO: object representing all combinations/configurations of some objects?
// TODO: add memoization
// TODO: define mappings from one polyomino to another (and transformations, etc.)
// TODO: Polyomino naming
// TODO: bounding box sizes
// TODO: perimeter/edge shapes of polyominoes (convext)
// TODO: polyomino sets

struct vector {
	int x, y, z;
};

struct array {
	int rank;
	int* shape;
	int size;
	int* data;
};


struct array fill_array(struct array a, int value) {
	for (int i=0; i<a.size; i++) {
		a.data[i] = value;
	}
	return a;
}
