#include <stdlib.h>
#include <stdio.h>

struct Exception {
    char* message;
};
typedef struct Exception Exception;
Exception exception (char* message);

Exception exception (char* message) {
    return (Exception) {
        message
    };
}

void raise (Exception E);
void raise (Exception E) {
    printf("%s\n", E.message);
}

typedef unsigned int bool;
struct Option {
    void* value;
    bool is_some;
    bool (*is_none) (struct Option self);
};
typedef struct Option Option;
Option None = { NULL, 0 };
bool is_none (Option self) {
    return !self.is_some;
}
Option Some (void* value) {
    return (Option) {
        value, 1, &is_none
    };
}

struct Type {
    char* name;
    unsigned int size;
};
typedef struct Type Type;
typedef unsigned int uint;

struct Array {
    unsigned int size;
    unsigned int real_size;
    Option (*free) (struct Array* self);
    Option (*cast) (struct Array* self, Type Q);
    void** data;
    Type T;
};
typedef struct Array Array;

Option array_free (Array* self) {
    free(self -> data);
    self -> size = 0;
    return None;
}

Option array_cast (Array* self, Type Q);
Array new_array (unsigned int size, Type T) {
    return (Array) {
        size,
        size * T.size,
        &array_free,
        &array_cast,
        malloc(size * T.size),
        T
    };
}

Array* new_allocated_array (unsigned int size, Type T) {
    Array* result = malloc(sizeof(Array));
    *result = new_array(size, T);
    return result;
}

Option array_cast (Array* self, Type Q) {
    Array* result = new_allocated_array(self -> size, Q);
    result -> data = self -> data;
    return Some(result);
}

struct Vec {
    unsigned int length;
    unsigned int capacity;
    unsigned int max_capacity;
    Array data;
    Option (*vec_expand) (struct Vec* self);
};
typedef struct Vec Vec;


Option vec_expand (Vec* self);
Option vec_new (unsigned int init_capacity, Type T) {
    return Some(& (Vec) {
        0,
        init_capacity,
        1 << 16,
        new_array(init_capacity, T),
        &vec_expand
    });
}

// Deallocates the buffer associated with this vector
Option vec_free (Vec self) {
    self.data.free(&self.data);
    self.length = 0;
    self.capacity = 0;
    return None;
}
struct vec_iter {
    Vec source;
    unsigned int index;
    Option (*next) ();
};
typedef struct vec_iter vec_iter;

Option vec_iter_next (vec_iter self) {
    if (self.index < self.source.length) {
        uint i = self.index ++;
        return Some(self.source.data.data[i]);
    } else {
        return None;
    }
}

vec_iter iter (Vec self) {
    return (vec_iter) {
        self,
        0,
        &vec_iter_next
    };
}
