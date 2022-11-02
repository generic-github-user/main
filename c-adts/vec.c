#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

typedef unsigned int bool;
typedef unsigned int uint;
typedef char* String;

struct Type {
    char* name;
    unsigned int size;
};
typedef struct Type Type;
Type type_new (char* name, uint size);

Type type_new (char* name, uint size) {
    return (Type) { name, size };
}

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
Result Ok (const void* value);
Result Error (const Exception* ex);
void* unwrap_ (Result self);
void* unwrap ();

Result Ok (const void* value) {
    return (Result) { value, NULL, 1, 0 };
}
Result Error (const Exception* ex) {
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

struct Option {
    void* value;
    bool is_some;
    bool (*is_none) (struct Option self);
    bool (*is_none_) ();
    uint (*unwrap_uint) (struct Option self);
};
typedef struct Option Option;
bool is_some (Option self) {
    return self.is_some;
}
bool is_none (Option self);
bool is_none_ ();
Option Some (void* value);
uint unwrap_uint (Option self);

// will eventually return a Result<Option::Some<T>> (some restructuring of OOP
// type interface is needed before then)
Option Some (void* value) {
    Option* thing = malloc(sizeof(Option));
    init_self((void*) thing);
    *thing = ((Option) {
        value, 1,
        &is_none,
        &is_none_,
        &unwrap_uint
    });
    return *thing;
}
uint unwrap_uint (Option self) {
    // awful
    init_self((void*) &self);
    if (self.is_none_())
        raise(exception("Attempted to unwrap a None variant of an Option"));
    return *((uint*) self.value);
}

Option None;
Option none () {
    init_self((void*) &None);
    return None;
}
bool is_none (Option self) {
    return !self.is_some;
}
bool is_none_ () {
    return is_none(*((Option*) self_));
}
Option None = { NULL, 0, is_none, is_none_, unwrap_uint };

// (void* (*h) (void*)) cursed_compose () { }

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

// void print (unsigned int x) {
void* print (const void* x) {
    printf("%d\n", *((uint*) x));
    return NULL;
}

static uint verbose = 1;
void test (bool condition) {
    if (!condition) {
        raise(exception("Test failed (condition evaluated to false)"));
    } else if (verbose) {
        printf("Test passed\n");
    }
}

uint incr (uint x) { return x + 1; }
uint add (uint x, uint y) { return x + y; }
int main () {
    srand(time(NULL));

    /*
    Option value = None;
    Iterator source = range_iter_new(range_new(0, 10));
    // while (!is_none(source.next(source)))
    while (!is_none(value = range_next(source.interior)))
        printf("%d ", *((uint*) value.value));
    printf("\n");
    */

    // while ((value = source.interior.next()).is_some())
        // printf("%d ", value.unwrap_uint());

    each(range_iter_new(range_new(0, 10)), &print);
    printf("\n");
    range_new(0, 5).iter().each(print);
    // Range.new()

    test(none().is_none_());
    test(!none().is_some);
    test(!Some(1).is_none_());
    test(Some(42).is_some);

    // test(range_iter_new(range_new(0, 3)).sum() == 6);
}

// TODO:
// - unsafe(r) version of C in which generics and polymorphism are (more)
// viable (in a direct fashion)
// - simple textual preprocessor
