#include <stdlib.h>
#include <stdio.h>

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
