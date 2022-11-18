#include <stdio.h>

int d(int x) {
    int sum = 0;
    printf("%6d : ", x);
    // while (x > 1) {
        for (int i=1; i<x; i++) {
            if (x % i == 0) {
                // x /= i;
                sum += i;
                printf(" %d", i);
            }
        }
    // }
    printf(" ~ %d\n", sum);
    return sum;
}

int main() {
    int n = 10000;
    // int test[n];
    int S = 0;
    for (int i=1; i<n; i++) {
        int di = d(i);
        if (di < n && i != di && i == d(di)) {
            printf("amicable pair: %d, %d\n", i, di);
            S += i;
        }
    }
    printf("%d\n", S);
}

