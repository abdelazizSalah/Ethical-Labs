#include <stdio.h>
#include <stdint.h>
#include <x86intrin.h>   // for __rdtscp() and _mm_clflush()

uint8_t cache_line_data = 1;  // the variable whose access time we are measuring

// 'cpu_core_id' stores the processor ID from __rdtscp(), required but unused in timing
unsigned int cpu_core_id;

/*
    Function: measure_access_time
    Purpose: Measure the time taken to access a specific memory address.
    Input: target_address - pointer to the memory location to access.
    Returns: elapsed CPU cycles for the memory access.
*/
uint64_t measure_access_time(uint8_t *target_address) {
    uint64_t start_cycles, end_cycles;
    
    start_cycles = __rdtscp(&cpu_core_id);   // record start timestamp
    (void)*target_address;                   // access the memory (read)
    end_cycles = __rdtscp(&cpu_core_id);     // record end timestamp

    return end_cycles - start_cycles;        // return the difference in cycles
}

int main() { 
    // Load data into the cache to simulate a cache hit
    cache_line_data = 2;

    printf("Cache hit access time: %lu cycles\n", measure_access_time(&cache_line_data)); 

    return 0; 
}
