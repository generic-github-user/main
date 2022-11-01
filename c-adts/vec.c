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
