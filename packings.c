#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

int MAX_WIDTH = 10;
int MAX_BLOCKS = 100;
int compute = 0;

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
//
// TODO: polyomino perimeter
// TODO: optimization

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

int get_cell_value(struct polyomino p, struct vector w) {
	int* cell_ptr = get_cell(p, w);
	return cell_ptr == NULL ? 0 : *cell_ptr;
}

void pinfo(struct polyomino p) {
	printf("n: %i, shape: %i by %i \n", p.n, p.matrix.shape[0], p.matrix.shape[1]);
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

int intersect(struct polyomino p1, struct polyomino p2, int dx, int dy) {
	// TODO: revise bounds
	for (int x=0; x<p1.matrix.shape[0]; x++) {
		for (int y=0; y<p1.matrix.shape[1]; y++) {
			if (
				get_cell_value(p1, (struct vector) { x, y }) &&
				get_cell_value(p2, (struct vector) { x+dx, y+dy })
			) {
				return 1;
			}
		}
	}
	return 0;
}

void* find_space(struct vector** source, int n) {
	for (int i=0; i<n; i++) {
		if (source[n] == NULL) {
			return &source[n];
		}
	}
	return NULL;
}

void add_block(struct polyomino p, struct vector w) {
	int* cell_ptr = get_cell(p, w);
	*cell_ptr = 1;
//	p.idx[p.n] = w;
	// TODO***
	struct vector* w_ptr = find_space(p.indices, p.n);
	*w_ptr = w;
	p.n ++;
}
struct edges {
	int** edges;
	int num_edges;
};

int count_adj(struct polyomino p, int x, int y) {
	int adj = (
		get_cell_value(p, (struct vector) { x-1, y })+
		get_cell_value(p, (struct vector) { x+1, y })+
		get_cell_value(p, (struct vector) { x, y-1 })+
		get_cell_value(p, (struct vector) { x, y+1 })
	);
	return adj;
}

int perimeter(struct polyomino p) {
	int P = 0;
//	for (int i=0; i<p.n; i++) {
	for (int x=0; x<p.matrix.shape[0]; x++) {
		for (int y=0; y<p.matrix.shape[1]; y++) {
			int v = get_cell_value(p, (struct vector) { x, y });
			if (v) {
				P += 4 - count_adj(p, x, y);
			}
		}
	}
	return P;
}

struct edges get_edges(struct polyomino p) {
	int** edges = calloc(p.matrix.size, sizeof(int));
	int num_edges = 0;
	// more elegant way to do this?
	for (int x=0; x<p.matrix.shape[0]; x++) {
		for (int y=0; y<p.matrix.shape[1]; y++) {
			struct vector v = { x, y };
			int* cell_ptr = get_cell(p, v);
			//int adj = (
			//	*get_cell(p, (struct vector) { x-1, y })+
			//	*get_cell(p, (struct vector) { x+1, y })+
			//	*get_cell(p, (struct vector) { x, y-1 })+
			//	*get_cell(p, (struct vector) { x, y+1 })
			//);
			int adj = (
				get_cell_value(p, (struct vector) { x-1, y })+
				get_cell_value(p, (struct vector) { x+1, y })+
				get_cell_value(p, (struct vector) { x, y-1 })+
				get_cell_value(p, (struct vector) { x, y+1 })
			);
			// printf("%i adj; ", adj);
			compute ++;
			if (*cell_ptr == 0 && adj > 0) {
				edges[num_edges] = cell_ptr;
				num_edges ++;
			}
		}
	}
	struct edges e = { edges, num_edges };
	return e;

}

int enumerate(struct polyomino p, int n, int i, int limit, int* prev) {
//	printf("Enumerating extensions on p of size %i (running total is %i, limit %i) \n", n, i, limit);
	struct edges e = get_edges(p);
	for (int j=0; j<e.num_edges; j++) {
		if (i > limit) {
			printf("Limit (%i) reached; halting execution \n", limit);
			break;
		}
		if (n == 1) {
			return 1;
			//i = 1;
			//break;
		}
		//if (prev != NULL) {
		//	*prev = 0;
		//}

		*(e.edges[j]) = 1;
//		pprint(p, "n");
		compute ++;
		i += enumerate(p, n-1, 0, limit, e.edges[j]);
		*(e.edges[j]) = 0;
	}
	return i;
}
// Modifies polyomino in place
struct polyomino grow_polyomino(struct polyomino p) {
	//int* edges[p.matrix.size] = {0};
	//int* edges[p.matrix.size];
	
	// ???

	struct edges e = get_edges(p);	
	if (e.num_edges > 0) {
	// if (edges != NULL) {
		int z = rand() % e.num_edges;
		*(e.edges[z]) = 1;
	}
	free(e.edges);
	return p;
}

// TODO: more robust coordinate system (what is a polyomino?)
int equivalent(struct polyomino p1, struct polyomino p2, int dx, int dy) {
	for (int x=0; x<p1.matrix.shape[0]; x++) {
		for (int y=0; y<p1.matrix.shape[1]; y++) {
			compute ++;
			if (
				get_cell_value(p1, (struct vector) { x, y }) !=
				get_cell_value(p2, (struct vector) { x, y })
			) {
				return 0;
			}
		}
	}
	return 1;
}

// Other methods of comparison (more efficient)?
int translation_equivalent(struct polyomino p1, struct polyomino p2) {
	for (int x=-p1.matrix.shape[0]; x<p1.matrix.shape[0]*2; x++) {
		for (int y=-p1.matrix.shape[1]; y<p1.matrix.shape[1]*2; y++) {
			compute ++;
			if (!equivalent(p1, p2, x, y)) {
				return 0;
			}
		}
	}
	return 1;
}
