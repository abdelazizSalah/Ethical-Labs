import csv

cached = []
uncached = []

with open("cache_timings.csv", newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header
    for row in reader:
        cached.append(int(row[0]))
        uncached.append(int(row[1]))

print(f"Cached min/avg/max: {min(cached)}/{sum(cached)//len(cached)}/{max(cached)} cycles")
print(f"Uncached min/avg/max: {min(uncached)}/{sum(uncached)//len(uncached)}/{max(uncached)} cycles")

~                                                                                                                                       
~                                                                                                                                       
~              