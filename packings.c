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
// TODO: add equivalence pre-checks
// TODO: quicker ways of counting than enumerating all polyominoes?
// TODO: database indices
// TODO: polyomino grammars

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

struct array new_array(int rank, int* shape) {
	// int rank = sizeof(shape);
	// int* size = malloc(sizeof(int));
	int size = 1;
	for(int i=0; i<rank; i++) {
		size *= shape[i];
	}
	printf("Initalizing array with size %i \n", size);
	//int data[size] = {0};
	//int data[size];
	int* data = calloc(size, sizeof(int));
	struct array a = { rank, shape, size, data };
	fill_array(a, 0);
	return a;
};

//struct array array_and(struct array a1, struct array a2) {

// struct array map_array(struct array a

struct polyomino {
	int n;
	int* indices;
	struct array matrix;
};

struct polyomino new_polyomino(int n, int x, int y) {
	// use array of pointers?
	//int idx[MAX_BLOCKS * 2] = {0};
	//int idx[MAX_BLOCKS * 2];

	// do we need to typecast this?
	int* idx = calloc(MAX_BLOCKS * 2, sizeof(int));
	//int shape[2] = { MAX_WIDTH, MAX_WIDTH };
	int* shape = calloc(2, sizeof(int));
	//shape = { MAX_WIDTH, MAX_WIDTH };
	shape[0] = x;
	shape[1] = y;

	printf("Creating polyomino (max width: %i, max height: %i) \n", shape[0], shape[1]);
	// malloc?
	struct array matrix = new_array(2, shape);
	struct polyomino p = { n, idx, matrix };
	return p;
}
// TODO: use bit arrays

int bound(int* x, int a, int b) {
	if (*x < a) { *x = a; }
	if (*x > b) { *x = b; }
}

int* get_cell(struct polyomino p, struct vector w) {
	//bound(&w.x, 0, p.matrix.shape[0]);
	//bound(&w.y, 0, p.matrix.shape[1]);
	if (w.x < 0 || w.x > p.matrix.shape[0]-1) { return NULL; }
	if (w.y < 0 || w.y > p.matrix.shape[1]-1) { return NULL; }
	return &p.matrix.data[w.x * p.matrix.shape[1] + w.y];
}

void pprint(struct polyomino p, char color[]) {
	for (int x=0; x<p.matrix.shape[0]; x++) {
		for (int y=0; y<p.matrix.shape[1]; y++) {
			if (color == "n") {
				//char C[] = COLOR_ORDER[(int) 
				printf((*get_cell(p, (struct vector) { x, y })) == 1 ? ("**") : "  ");
				compute ++;
			}
		}
		printf("\n");
	}
}

void afree(struct array a) {
	free(a.shape);
	free(a.data);
}

void pfree(struct polyomino p) {
	afree(p.matrix);
	free(p.indices);
}
