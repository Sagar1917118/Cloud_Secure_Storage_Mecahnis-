import numpy as np
import random
class InformationDispersalAlgorithm:
    def __init__(self, m, n, prime=257):
        """
        Initialize IDA parameters.
        m: Minimum required fragments to reconstruct data
        n: Total number of generated fragments (n >= m)
        prime: A prime number larger than max byte value (to ensure invertibility)
        """
        self.m = m
        self.n = n
        self.p = prime  # Prime number for modular arithmetic
        self.encoding_matrix = self._generate_vandermonde_matrix()

    def _generate_vandermonde_matrix(self):
        """Generates an (n x m) Vandermonde encoding matrix in modular field Z_p."""
        matrix = np.array([[pow(i, j, self.p) for j in range(self.m)] for i in range(1, self.n + 1)])
        return matrix

    def split_data(self, data):
        """Converts data into integer bytes and splits into m segments."""
        if isinstance(data, str):
            data_bytes = np.frombuffer(data.encode('utf-8'), dtype=np.uint8)
        elif isinstance(data, bytes):
            data_bytes = np.frombuffer(data, dtype=np.uint8)
        else:
            raise TypeError("Input must be a string or bytes")
        # data_bytes = np.frombuffer(data.encode('utf-8'), dtype=np.uint8)  # Convert to bytes
        padding_size = (self.m - len(data_bytes) % self.m) % self.m  # Ensure divisibility
        data_bytes = np.pad(data_bytes, (0, padding_size), mode='constant')  # Zero-padding

        # Reshape into (m x num_blocks)
        data_matrix = data_bytes.reshape(self.m, -1)
        return data_matrix

    def encode(self, data_matrix):
        """Encodes the data using the Vandermonde encoding matrix to generate n fragments."""
        encoded_fragments = (self.encoding_matrix @ data_matrix) % self.p  # Modular multiplication
        return encoded_fragments

    def mod_inv(self, a, p):
        """Returns the modular inverse of a under modulo p using the Extended Euclidean Algorithm."""
        a = a % p  # Ensure a is within field range
        if a == 0:
            raise ValueError("Singular matrix detected (non-invertible element). Try a different prime.")
        
        g, x, _ = self.extended_gcd(a, p)
        if g != 1:
            raise ValueError("No modular inverse exists for this element in Z_p")
        
        return x % p  # Ensure result is positive

    def extended_gcd(self, a, b):
        """Extended Euclidean Algorithm to compute gcd(a, b) and modular inverse."""
        if a == 0:
            return b, 0, 1
        g, x1, y1 = self.extended_gcd(b % a, a)
        return g, y1 - (b // a) * x1, x1

    def modular_inverse_matrix(self, matrix):
        """Computes the modular inverse of a square matrix in Z_p using Gaussian elimination."""
        size = matrix.shape[0]
        augmented = np.hstack((matrix, np.eye(size, dtype=int)))  # Augment with identity matrix
        augmented = augmented % self.p  # Ensure modulo p

        # Gaussian elimination to convert to reduced row echelon form
        for i in range(size):
            # Find a row with a nonzero pivot if needed
            if augmented[i, i] == 0:
                for j in range(i + 1, size):
                    if augmented[j, i] != 0:
                        augmented[[i, j]] = augmented[[j, i]]  # Swap rows
                        break
                else:
                    raise ValueError("Singular matrix detected, no modular inverse exists.")

            # Make diagonal element 1
            inv = self.mod_inv(augmented[i, i], self.p)
            augmented[i] = (augmented[i] * inv) % self.p

            # Make all other column entries 0
            for j in range(size):
                if i != j:
                    factor = augmented[j, i]
                    augmented[j] = (augmented[j] - factor * augmented[i]) % self.p

        return augmented[:, size:]  # Extract right half (inverse matrix)

    def decode(self, received_fragments, fragment_indices):
        """Reconstructs original data from any m valid fragments."""
        decoding_matrix = self.encoding_matrix[fragment_indices, :]  # Select relevant rows
        inverse_matrix = self.modular_inverse_matrix(decoding_matrix[:self.m, :])  # Modular inverse

        # Solve system using modular multiplication
        original_matrix = (inverse_matrix @ received_fragments[:self.m, :]) % self.p  
        return original_matrix.astype(np.uint8).flatten().tobytes().decode('utf-8', errors='ignore')

    def disperse(self, data):
        """Full pipeline: Split, Encode, and return encoded fragments."""
        data_matrix = self.split_data(data)
        encoded_fragments = self.encode(data_matrix)
        return encoded_fragments

    def reconstruct(self, encoded_fragments ):
        """Reconstruct the original data from received fragments."""
        l=len(encoded_fragments)
        fragment_indices = sorted(random.sample(range(l), 3))
        received_fragments = encoded_fragments[fragment_indices, :]
        return self.decode(received_fragments, fragment_indices)

# ---- Example Usage ----

# Initialize IDA with m=3, n=5 (m=minimum required fragments, n=total distributed)
# IDA = InformationDispersalAlgorithm(m=2, n=5)



# # Step 1: Disperse the data
# encoded_fragments = ida.disperse(data)


# # Step 2: Simulate data loss (use only 3 out of 5 fragments for reconstruction)
# chosen_indices = sorted(random.sample(range(5), 2))  # Randomly select 3 indices
# received_fragments = encoded_fragments[chosen_indices, :]

# # Step 3: Reconstruct the original data
# recovered_data = ida.reconstruct(received_fragments, chosen_indices)

# print("Original Data: ", data)
# print("Encoded fragements",encoded_fragments)
# print("Recovered Data:", recovered_data)
