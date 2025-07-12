/*
	@Author: Abdelaziz Neamatallah
	@desc: this file is implemented to solve task2 using the flush and reload method
	@date: 11/7/2025 
*/
#include <emmintrin.h>
#include <x86intrin.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

#define CACHE_HIT_THRESHOLD 250  // measured value
/*

we need the struct to add padding, but we can also get rid of it, and try to make a workaround by reading array elements each 4098 index
datablock [ 4096 * 256 ]
when access datablock[i * 4096]

We did it in this way in order to make the attack work, because if we made it in small size
	the cache line is 64, so it will get many elements of the array in the same time, which will 
	make our attack not feasible. 

	so we want to put one element in one page, so we can distingush between elements coming from the cache, and others.
*/
typedef struct datablock {
    uint8_t lpad[2048];   // Ensures dat is isolated
    uint8_t dat;
    uint8_t rpad[2047];  // Total size = 2048 + 1 + 2047 = 4096 bytes (1 page)
} DataBlock;

DataBlock array[256];


void victim() {
        uint8_t secret = 94;

        // It is helpful to give the victim time for a couple accesses to the data - this way, we
        // are less likely to be affected by cache-displacement strategies, which we really
        // don't want for this simple experiment.
        for (int i = 0; i < 20; i++) {
                uint8_t temp = array[secret].dat;
                array[secret].dat = 0;
                temp = array[secret].dat;
        }
}


void flushSideChannel() {
    for (int i = 255; i > -1; i--) {
        _mm_clflush(&array[i].dat);  // Flush only the dat field
    }
}


uint64_t time_eval(uint8_t *addr) {
    // this variable is required by the rdtscp to save the processor ID, so it is just a dummy parameter we will not use
    unsigned int junk;
    uint64_t start = __rdtscp(&junk);
    junk = *addr; // just to access the value of the data, to measure what is time needed to access it.
    uint64_t end = __rdtscp(&junk);
    return end - start;
}


uint8_t reloadSideChannel() {
        int junk = 0;
        uint64_t timeElapse;
        int best_index = 0;
        uint64_t best_time = UINT64_MAX;

    for (int i = 255; i > -1; i--) {
        volatile uint8_t *data = &array[i].dat;
        timeElapse = time_eval(data);
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

int main(int argc, const char** argv) {
        // Ensure array is initialized
        for (int i = 0; i < 256; i++) {
        array[i].dat = 1;
        }

        flushSideChannel();
        victim();

        uint8_t secret = reloadSideChannel();

        printf("The secret is %d\n", secret);


        return 0;
}

