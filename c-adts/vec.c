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
    unsigned int real_size;
    Type type;
    Array data;
    void** raw;

    Array (*data_) ();
    Option (*vec_expand) (struct Vec* self);
    Option (*vec_push) (struct Vec* self, void*);
    Option (*vec_pop) (struct Vec* self);
    struct Vec* (*vec_empty) (struct Vec* self);
    Result (*swap) (uint, uint);
    struct Vec* (*clone) ();
    struct Vec* (*shuffle) ();
    struct Vec* (*contains) ();
};
typedef struct Vec Vec;


Option vec_expand (Vec* self);
Result vec_swap (uint, uint);
Vec* vec_empty (Vec*);
Vec* vec_clone (Vec*);
Vec* vec_shuffle ();
bool vec_contains (void* value);

vec_iter iter (Vec self);
vec_iter iter ();
Option vec_new (unsigned int init_capacity, Type T) {
    Array buffer = new_array(init_capacity, T);
    return Some(& (Vec) {
        0,
        init_capacity,
        1 << 16,

        0, T,

        buffer,
        buffer.data,

        &vec_data,
        &vec_expand,
        &vec_push,
        &vec_pop,
        &vec_empty,
        &vec_swap,
        &vec_clone,
        &vec_shuffle,
        &vec_contains,
        &iter_
    });
}

// Deallocates the buffer associated with this vector
Option vec_free (Vec self) {
    self.data.free(&self.data);
    self.length = 0;
    self.capacity = 0;
    return None;
}

struct Iterator {
    void* interior;
    Option (*next) ();
    Type T;

    void (*each) ();
};
typedef struct Iterator Iterator;
void each (Iterator iter, void* (*f) (void*));
void each_ (void* (*f) (void*));

Iterator iter_new (void* interior, Option (*next) (), Type T) {
    return (Iterator) {
        interior, next, T,
        &each_
    };
}

Option iter_next (Iterator* iter) {
    // return iter -> interior ->
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

Option map_next (Option value, void* (*f) (void*)) {
    if (is_none(value)) { return None; }
    else { return Some(f(value.value)); }
}
Iterator map (Iterator iter, void* (*f) (void*)) {
    return (Iterator) {
        NULL,
        &map_next,
        iter.T
    };
}

void each (Iterator iter, void* (*f) (void*)) {
    Option next = None;
    while (is_some(next = iter.next(iter.interior)))
        f(next.value);
}

void each_ (void* (*f) (void*)) {
    Iterator* self = (Iterator*) self_;
    each(*self, f);
}

Vec* iter_collect (Iterator iter) {
    Vec* result = (Vec*) vec_new(128, iter.T).value;
    Option next = None;
    while (!is_none(next = iter.next(iter))) {
        vec_push(result, next.value);
    }
    return result;
}

struct range {
    uint a;
    uint b;
    Iterator (*iter) ();
};
typedef struct range range;

typedef struct range_iter {
    uint i;
    range source;
    Option (*next) (struct range_iter*);
} range_iter;

void* allocate_uint (uint x) {
    uint* y = malloc(sizeof(uint));
    *y = x;
    return (void*) y;
}

Option range_next (range_iter* iter) {
    uint current = iter -> i;
    if ((iter -> i ++) < (iter -> source.b))
        return Some(allocate_uint(current));
    else { return None; }
}

Iterator range_iter_new (range R) {
    range_iter* r_iter = malloc(sizeof(range_iter));
    *r_iter = (range_iter) { R.a, R, range_next };
    /* return (Iterator) {
        (void*) r_iter,
        range_next,
        (Type) { 4 }
    }; */
    Iterator outer = iter_new(r_iter, range_next, (Type) { "uint", 4 });
    // TODO: do this automatically in the iterator constructor
    init_self((void*) allocated(&outer, sizeof(Iterator)));
    return outer;
}

Iterator range_iter_new_ () {
    range* self = (range*) self_;
    return range_iter_new(*self);
}

range range_new (uint a, uint b) {
    range new_range = (range) {
        a, b, &range_iter_new_
    };
    init_self((void*) allocated(&new_range, sizeof(range)));
    return new_range;
}
