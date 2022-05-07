#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

int MAX_WIDTH = 10;
int MAX_BLOCKS = 100;


struct vector {
	int x, y, z;
};

struct array {
	int rank;
	int* shape;
	int size;
	int* data;
};

