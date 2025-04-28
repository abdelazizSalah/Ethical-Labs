import random
import string

def generate_random_file(length):
    chars = string.ascii_letters + string.digits + string.punctuation
    random_text = ''.join(random.choices(chars, k=length))
    
    with open("prefix2.txt", "w") as f:
        f.write(random_text)

# Example: Ask the user for input length
if __name__ == "__main__":
    n = int(input("Enter number of characters to generatee: "))
    generate_random_file(n)
    print(f"Generated {n} random characters in prefix2.txt\n ")
