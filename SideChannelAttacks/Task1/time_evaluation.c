#include <stdio.h>
#include <stdint.h>
#include <x86intrin.h>

#define ITERATIONS 100

uint64_t time_eval(uint8_t *addr) {
    // this variable is required by the rdtscp to save the processor ID,
    //  so it is just a dummy parameter we will not use
    unsigned int junk;
    uint64_t start = __rdtscp(&junk);
    junk = *addr; // just to access the value of the data, to measure what is time needed to access it.
    uint64_t end = __rdtscp(&junk);
    return end - start;
}

uint8_t data = 1;

int main() {
    // lets define arrays to store in them the time for each trial
    uint64_t times_cached[ITERATIONS], times_uncached[ITERATIONS];

    for (int i = 0; i < ITERATIONS; i++) {
        // volatile is important here, because without it, the cpu may allow another threads to work
        // which can make use of the cache and change its values.
        // also during the compilation, the compiler tends to enahnce the code, and since the 
        // data here is not used, so it may consider it as constant, and not assign it as variable.
        // but volatile force the compiler to leave it, and read it from the the memory each time. 
        volatile uint8_t *access_pointer = &data;

        // Ensure data is in cache (cached read)
        *access_pointer;
        times_cached[i] = time_eval((uint8_t *)access_pointer);

        // Flush from cache (uncached read)
        _mm_clflush((void *)access_pointer);
        times_uncached[i] = time_eval((uint8_t *)access_pointer);
    }

    FILE *f = fopen("cache_timings.csv", "w");
    fprintf(f, "cached,uncached\n");
    for (int i = 0; i < ITERATIONS; i++) {
        fprintf(f, "%lu,%lu\n", times_cached[i], times_uncached[i]);
    }
    fclose(f);

    printf("processing is done\n");
    return 0;
}

