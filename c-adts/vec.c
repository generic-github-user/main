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

struct Result {
    void* value;
    Exception* error;
    bool is_ok;
    bool is_err;
};
typedef struct Result Result;
Result Ok (void* value);
Result Error (Exception* ex);
void* unwrap_ (Result self);
void* unwrap ();

Result Ok (void* value) {
    return (Result) { value, NULL, 1, 0 };
}
Result Error (Exception* ex) {
    return (Result) { NULL, ex, 1, 0 };
}

void* unwrap_ (Result self) {
    if (self.is_err)
        raise(exception("Attempted to unwrap an Error variant of a Result"));
    else
        return self.value;
}
void* unwrap () {
    Result self = *((Result*) self_);
    return unwrap_(self);
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

Option vec_expand (Vec* self) {
    uint new_capacity = self -> capacity + 128;
    self -> data.data = realloc(self -> data.data, new_capacity);
    self -> capacity = new_capacity;
    return Some(self);
}

Option vec_push (Vec* self, void* value) {
    if ((self -> capacity) - (self -> length) < 16) {
        Option result = self -> vec_expand(self);
        if (is_none(result)) { return None; }
    }
    self -> data.data[self -> length ++] = value;
    return Some(self);
}

Option vec_pop (Vec self) {
    if (self.length > 0) {
        return Some(self.data.data[-- self.length]);
    }
    else {
        return None;
    }
}

Vec* vec_empty (Vec* self) {
    self -> length = 0;
    self -> capacity = 0;
    return self;
}

Option vec_remove (Vec self, unsigned int i) {
    void* value = self.data.data[i];
    for (uint j = i; j < self.length; j++) {
        self.data.data[j] = self.data.data[j + 1];
    }
    self.length --;
    return Some(value);
}
