import random

def is_prime(p):
    # Function to check if a number is prime
    if p < 2:
        return False
    for i in range(2, int(p**0.5) + 1):
        if p % i == 0:
            return False
    return True

def find_primitive_root(p):
    # Function to find a primitive root modulo p
    primitive_roots = []
    for g in range(2, p):
        powers = set()
        for i in range(1, p):
            powers.add(pow(g, i, p))
        if len(powers) == p - 1:
            primitive_roots.append(g)
    return primitive_roots

def generate_private_key(p):
    # Generate a random private key in the range [1, p-1]
    return random.randint(1, p - 1)

def generate_public_key(g, private_key, p):
    # Calculate the public key based on private key and primitive root
    return pow(g, private_key, p)

def generate_secret_key(public_key, private_key, p):
    # Calculate the shared secret key
    return pow(public_key, private_key, p)

def main():
    print("Diffie-Hellman Key Exchange")
    
    while True:
        p_input = input("Enter a prime number (p): ")
        if p_input.isdigit():
            p = int(p_input)
            if is_prime(p):
                break
            else:
                print("p is not a prime number. Please try again.")
        else:
            print("Invalid input. Please enter a positive integer.")
    
    primitive_roots = find_primitive_root(p)
    
    if not primitive_roots:
        print("No primitive roots found for the given prime number.")
        return
    
    g = random.choice(primitive_roots)
    
    print(f"Selected prime number (p): {p}")
    print(f"Primitive root modulo p (g): {g}")
    
    private_key_A = generate_private_key(p)
    private_key_B = generate_private_key(p)
    
    public_key_A = generate_public_key(g, private_key_A, p)
    public_key_B = generate_public_key(g, private_key_B, p)
    
    secret_key_A = generate_secret_key(public_key_B, private_key_A, p)
    secret_key_B = generate_secret_key(public_key_A, private_key_B, p)
    
    print("\nKey Exchange:")
    print(f"Private key for Alice: {private_key_A}")
    print(f"Private key for Bob: {private_key_B}")
    
    print(f"Public key for Alice: {public_key_A}")
    print(f"Public key for Bob: {public_key_B}")
    
    print(f"Shared secret key for Alice: {secret_key_A}")
    print(f"Shared secret key for Bob: {secret_key_B}")
    
    if secret_key_A == secret_key_B:
        print("\nShared secret keys match. Secure communication can now take place.")
    else:
        print("\nShared secret keys do not match. Key exchange failed.")

if __name__ == "__main__":
    main()
