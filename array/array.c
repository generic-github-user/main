/* Generated from ./array/array.c0 at 05/27/2022 */ 
/* This is a content file generated from a source (.c0) file; you should edit that file instead */ 
#include <stdio.h>
#include <stdlib.h>

// #include "vector.h"
#include "array.h"
#include "../helpers/helpers.h"

// Create a statically typed function that reduces an array to a single value



// Fill an array with a value
array fill_array(array a, int value) {
	for (int i=0; i<a.size; i++) {
		a.data[i] = value;
	}
	return a;
}

// Initialize an array struct
array new_array(int rank, int* shape) {
	// int* size = malloc(sizeof(int));
	int size = 1;
	for(int i=0; i<rank; i++) {
		size *= shape[i];
	}
	//printf("Initalizing array with size %i \n", size);
	int* data = calloc(size, sizeof(int));
	int space = size * sizeof(int);
	array a = { rank, shape, size, data, space, 0, NULL };
	// a.indices = new_array(
	a.indices = new_list(NULL);
	a.labels = calloc(rank, sizeof(char*));

	fill_array(a, 0);
	return a;
};

void free_array(array* a) {
	free(a -> shape);
	free(a -> data);
	// TODO
	free(a -> indices);
	free(a -> labels);
	free(a);
}

array vec_to_array(vector v) {
	int s[1] = {3};
	array output = new_array(1, s);
	//output.data = (int*) {v.x, v.y};
	output.data[0] = v.x;
	output.data[1] = v.y;
	output.data[2] = v.z;
	return output;
}

// Convert a series of indices to a corresponding memory address in the internal representation of the array data
int get_coord(array a, vector z) {
	// ?
	// return z.x * a.shape[1] + z.y;

	array w = vec_to_array(z);
	// TODO: make sure this will still work with very large arrays
	int block_size = 1;
	int q = 0;
	for (int i=0; i<3; i++) {
		q += w.data[i] * block_size;
		block_size *= a.shape[i];
		a.compute ++;
	}
	return q;
}

int array_get(array a, vector z) {
	return a.data[get_coord(a, z)];
}

void array_set(array a, vector z, int value) {
	a.data[get_coord(a, z)] = value;
	if (value != 0) {
		vector* pos = malloc(sizeof(vector));
		*pos = vec(z.x, z.y, z.z);
		list_add(a.indices, (void*) pos);
	}
}


// array array_from(int rank, int* shape, void* values) {


//array array_and(array a1, array a2) {

// void map_array(array a, )

void* reduce_array(array a, void* (F)(void*, void*), void* init) {
	void* output = init;
	for (int i=0; i<a.size; i++) {
		output = F(output, &a.data[i]);
	}
	return output;
}

// void* sum(int a, int b) { return (void*) a + b; }
// int array_sum(array a) { return (int) reduce_array(a, sum, 0); }
/* Imported from ./array/array_reduce.ct at 05/27/2022, 00:14:20 */ 
int array_sum(array a) {
	int output = 0;
	for (int i=0; i<a.size; i++) {
		output = output + a.data[i];
	}
	return output;
}

double array_mean(array a) {
	return (double) array_sum(a) / (double) a.size;
}

int array_min(array* a) {
	int output = a->data[0];
	for (int i=0; i<a->size; i++) {
		if (a->data[i] < output) {
			output = a->data[i];
		}
		a -> compute ++;
	}
	return output;
}

int array_max(array* a) {
	int output = a->data[0];
	for (int i=0; i<a->size; i++) {
		if (a->data[i] > output) {
			output = a->data[i];
		}
		a -> compute ++;
	}
	return output;
}

/* Imported from ./array/array_op.ct at 05/27/2022, 00:14:20 */ 
array array_bsum(array a, array b) {\
	array output = new_array(a.rank, a.shape);\
	for (int i=0; i<a.size; i++) {\
		output.data[i] = a.data[i] + b.data[i];\
	}\
	return output;\
}

/* Imported from ./array/array_op.ct at 05/27/2022, 00:14:20 */ 
array array_bdiff(array a, array b) {\
	array output = new_array(a.rank, a.shape);\
	for (int i=0; i<a.size; i++) {\
		output.data[i] = a.data[i] - b.data[i];\
	}\
	return output;\
}

/* Imported from ./array/array_op.ct at 05/27/2022, 00:14:20 */ 
array array_bprod(array a, array b) {\
	array output = new_array(a.rank, a.shape);\
	for (int i=0; i<a.size; i++) {\
		output.data[i] = a.data[i] * b.data[i];\
	}\
	return output;\
}

/* Imported from ./array/array_op.ct at 05/27/2022, 00:14:20 */ 
array array_bdiv(array a, array b) {\
	array output = new_array(a.rank, a.shape);\
	for (int i=0; i<a.size; i++) {\
		output.data[i] = a.data[i] / b.data[i];\
	}\
	return output;\
}

/* Imported from ./array/array_op.ct at 05/27/2022, 00:14:20 */ 
array array_bmod(array a, array b) {\
	array output = new_array(a.rank, a.shape);\
	for (int i=0; i<a.size; i++) {\
		output.data[i] = a.data[i] % b.data[i];\
	}\
	return output;\
}


array copy_array(array a) {
	array copy = new_array(a.rank, a.shape);
	for (int i=0; i<a.size; i++) {
		copy.data[i] = a.data[i];
	}
	return copy;
}

vector array_to_vec(array a) {
	return vec(a.data[0], a.data[1], a.data[2]);
}

array array_slice(array a, array T, array U, int rank) {
	array shape = array_bdiff(U, T);
	array slice = new_array(rank, shape.data);

	//int* s = malloc(sizeof(int));
	array counta = new_array(1, &rank);
	array countb = copy_array(T);
//	slice_helper(a, slice, T, U, shape, count, 0, rank);
	int i=0;
	//int j=0;
	// are two counters/an inner while-loop needed?
	while (i < rank) {
		if (counta.data[i] < shape.data[i]) {
			counta.data[i] ++; countb.data[i] ++;
			array_set(
				slice,
				array_to_vec(counta),
				array_get(a, array_to_vec(countb))
			);
		} else {
			counta.data[i] = 0;
			countb.data[i] = T.data[i];
			for (int j=0; j<rank; j++) {
				if (counta.data[j] < shape.data[i]) {
					counta.data[j] ++; countb.data[j] ++;
					break;
				}
			}
		}
	}
	return slice;
}

// Fill every index in the specified region with (a copy of) the given value
// Note that j_i must be less than or equal to k_i for all i
void fill_slice(array* a, vector j, vector k, int value) {
	for (int x=j.x; x<k.x; x++) {
		for (int y=j.y; y<k.y; y++) {
			if (k.x < a -> shape[0] && k.y < a -> shape[1]) {
				array_set(*a, vec(x, y, 0), value);
			}
		}
	}
}

void write_array(array a, FILE* fptr, int level) {
	printx(level+1, "Writing array (size %i) to file\n", a.size);
	for (int i=0; i<a.rank; i++) {
		fprintf(fptr, "%s:%i%s", a.labels[i], a.shape[i], i<a.rank-1?",":"\n");
	}
	for (int i=0; i<a.size; i++) {
		fprintf(fptr, "%i,", a.data[i]);
	}
	printx(level+1, "Done\n");
}
