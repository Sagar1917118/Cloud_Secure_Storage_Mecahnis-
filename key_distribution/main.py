import secrets
from sympy import mod_inverse
from Crypto.Random import get_random_bytes


PRIME = 2**137 - 1 

def generate_128bit_key() -> int:
    """Generate a random 128-bit container key as an integer"""
    return int.from_bytes(get_random_bytes(16), byteorder='big')

def eval_polynomial(coeffs, x, prime):
    """Evaluate a polynomial at x with coefficients under GF(prime)"""
    return sum((coeff * pow(x, power, prime)) for power, coeff in enumerate(coeffs)) % prime

def generate_shares(secret, threshold, total, prime):
    """Create 'total' shares with a threshold using Shamir's Secret Sharing"""
    coeffs = [secret] + [secrets.randbelow(prime) for _ in range(threshold - 1)]
    shares = [(x, eval_polynomial(coeffs, x, prime)) for x in range(1, total + 1)]
    return shares

def lagrange_interpolation(x, x_s, y_s, prime):
    """Perform Lagrange interpolation at x to find the secret"""
    total = 0
    k = len(x_s)
    for i in range(k):
        xi, yi = x_s[i], y_s[i]
        li_num = li_den = 1
        for j in range(k):
            if i == j:
                continue
            xj = x_s[j]
            li_num = (li_num * (x - xj)) % prime
            li_den = (li_den * (xi - xj)) % prime
        li = li_num * mod_inverse(li_den, prime)
        total = (total + yi * li) % prime
    return total

# Step 1: Generate a 128-bit container key
original_key = generate_128bit_key()
print("Original 128-bit Container Key (as integer):")
print(original_key)

# Step 2: Create and print shares
threshold = 3
total_shares = 5
shares = generate_shares(original_key, threshold, total_shares, PRIME)

print("\n Distributed Shares:")
for i, (x, y) in enumerate(shares, 1):
    print(f"Share {i}: (x={x}, y={y})")


selected = shares[:4]
x_s, y_s = zip(*selected)
recovered_key = lagrange_interpolation(0, list(x_s), list(y_s), PRIME)

print("\nRecovered Key from Shares:")
print(recovered_key)

# Step 4: Verify match
print("\nKey Match:", original_key == recovered_key)
