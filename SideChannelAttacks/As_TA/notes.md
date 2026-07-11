1. What is the meaning of side-channel attacks?
   -  It means that we do not break the security mechanism directly, instead we observe the indirect information (side effects) produced while a system is operating to infer secret data.
   -  i.e instead of stealing the secret directly by accessing the memory, we observe how the computer behaves in different states and try to infer the secret based on these differences. 
   -  In other words if we considered a binary system, usually the system will do operations when the current bit is 1, which are different from the operations done when the bit is 0. So based on these different operations we can infer what is the value of the bit without looking at it directly.
   -  And there can be different kind of observations such as time, electromagnitic radiations, energy, etc... 
2. What is the difference between registers, cache, RAM, and Harddisk? (In terms of speed access and size)
   - Speed comparision -> registers, cache, RAM, hard
   - Size comparision -> hard, RAM, cache, registers.
3. What is the meaning of cache-hit and cache-miss? Why can not we always have cache-hit? 
   - Cache-hit means that we have found the data we are looking for in the cache, cache miss means that we didn't found it.
   - We can not always have cache hit because there is a tradeoff between the size of the cache and the speed, usually the cache is not big enough to hold all the data, so can not always found the data we are looking for in the cache.
4.  What does flushing the cache mean? How can we ensure that the variable we want is inside the cache?
    - It means forcing the CPU to remove the data from the cache.
    - We can ensure that by reading or writing the variable of interest. i.e x = 4 then we measure the speed of accessing x. 
5.   What is the meaning of CPU cycles?
    - CPU cycle is the basic time used by the CPU to perform work or do instructions. 
    - In each cycle, the CPU perform part of instructions, some instructions can be performed in one cycle, and some complex instructions can take multiple cycles to be done. 
    - CPU cycles are computed using this equation:
      - Cycles = Time * clock frequency
        - Time is the time taken to perform one cycle
        - Frequency is the CPU speed,  Cycles per second
        - Cycles = number of CPU clock ticks.
6. Explain FLUSH+RELOAD technique
   1. We should flush the entire array from the cache memory to ensure that no part exist in the cache.
   2. Call the victim function, which will access one element from the array, which will cause the array to be cached.    
   3. Reload the entire array and measure the time taken to load each element. 
   4. The secret is the element with the lowest access time.
7. Why do we need to have 4096 bytes in the datablock, not only 1 byte for the secret?
   - Because the  cache line is 64 bytes, so it will get many elements of the array in the same time and this will make our attack infeasible. So we want to have single character in each cache page.
8. What is prefetching?
   - It is a performance optimization in which the CPU predicts which data or instruction will be needed next and loads them into the cache before the program actually request them 
9. What is speculative-execution?
   - It is an optimization method  in which processor guesses the outcome of a branch and begins executing instructions before it knows whether the guess is correct or not. 
   - The main purpose is to avoid setting the CPU idle.
10. What is the difference between prefetching and speculative-execution then?
    - Both are CPU optimizations.
    - But they are optimizing different things.
    - Prefetching
      - Prefetching predicts which data we will need.
      - Loads the data into the cache early
      - Never changes the program states
      - The main goal is to reduce memory access latency
    - Speculative-execution
      - Predicts which instruction wil be executed
      - Execute instructions before knowing which should run
      - Can change the cache and register values
      - The main goal is to reduce the branch latency
11. How can speculative-execution be used in making a side-channel attack?
    - The microarchitectural states are not always reverted, so the items that are loaded in the cache will still be there. 
    - So attacker can make use of this information and check if it was in the cache or not. 
12. What is the secret in task4, is it X or the size?
    1.  It is x.
13. Why do Spectre attack works?
    1.  It is mentioned in the PDF already, but students should state, because modern CPUs generally do not flush the cache after performing the wrong prediction.
