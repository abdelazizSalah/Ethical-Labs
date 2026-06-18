import subprocess

def run_btu_with_custom_password():
    try:
        length = int(input("Enter the desired password length: "))
        if length <= 0:
            print("Password length must be a positive integer.")
            return
        print(f'input length is {length}')
        password = 'A' * length
        firstName = 'B' * length
        LastName = 'C' * length

        print(f'password length is {len(password)}')
        
        command = ['./build/bin/btu', 'add', firstName, LastName, '1234', password]

        print(f"Running: {' '.join(command)}\n")
        subprocess.run(command)
        print('-------------------------')
        subprocess.run(['./build/bin/btu', 'print'])

        print('-------------------------')
        subprocess.run(['./build/bin/btu', 'remove', '1234', password])
        

        print('-------------------------')
        print('after deletion')
        subprocess.run(['./build/bin/btu', 'print'])
    except ValueError:
        print("Please enter a valid integer.")
    except FileNotFoundError:
        print("Error: btu binary not found. Make sure it's compiled and in the correct path.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    print('hello')
    run_btu_with_custom_password()
