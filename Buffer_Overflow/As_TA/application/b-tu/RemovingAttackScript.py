import subprocess

def run_btu_with_custom_password():
    try:
        uid = '1024'
        length = int(input("Enter the desired password length: "))
        
        print(f'input length is {length}')
        password = 'A' * length

        print(f'password length is {len(password)}')
        
        command = ['./build/bin/btu', 'remove', uid, password]

        print(f"Running: {' '.join(command)}\n")
        subprocess.run(command)
        print('-------------------------')
    except ValueError:
        print("Please enter a valid integer.")
    except FileNotFoundError:
        print("Error: btu binary not found. Make sure it's compiled and in the correct path.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    print('hello')
    run_btu_with_custom_password()
    