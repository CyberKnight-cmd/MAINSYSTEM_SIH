import hashlib
import zlib

class Processor:
    # Placeholder class variable (can be used later if needed)
    mainString = ""

    # Data string: User Id | Hash Code | X co-ord | Y co-ord
    NUM = " 0101011 0255656871 22.22956785 -33.45256587 "

    @classmethod
    def encode(cls):
        """
        Encode the NUM string by converting each character to its ASCII value,
        concatenating those values into a string, compressing the result using zlib,
        and then encoding it in hexadecimal format.
        Additionally, generate a SHA-256 hash of the hex-encoded compressed string.
        """
        # Convert the NUM string into a string of ASCII values
        ascii_string = ''.join(str(ord(char)) for char in cls.NUM)
        
        # Compress the ASCII string using zlib
        compressed_data = zlib.compress(ascii_string.encode())
        
        # Convert the compressed data to hexadecimal
        hex_encoded = compressed_data.hex()
        
        # Generate a SHA-256 hash of the hex-encoded compressed string for verification
        sha256_hash = hashlib.sha256(hex_encoded.encode()).hexdigest()
        
        return hex_encoded, sha256_hash

    @classmethod
    def decode(cls, encoded):
        """
        Decode a given hex-encoded compressed string back into the original NUM string.
        """
        # Convert the hex string back to compressed binary data
        compressed_data = bytes.fromhex(encoded)
        
        # Decompress the data to get the original ASCII string
        decompressed_ascii = zlib.decompress(compressed_data).decode('utf-8')
        
        # Convert the ASCII values back to characters
        decoded_string = ''.join(chr(int(decompressed_ascii[i:i+2])) for i in range(0, len(decompressed_ascii), 2))
        
        return decoded_string

    @classmethod
    def hash_string(cls, input_string):
        """
        Generate a SHA-256 hash of the given input string.
        """
        return hashlib.sha256(input_string.encode()).hexdigest()

    @classmethod
    def verify_hash(cls, original_encoded, original_hash):
        """
        Verify if the hash of the original encoded string matches the provided hash.
        """
        # Generate a new hash from the original encoded string and compare it
        return hashlib.sha256(original_encoded.encode()).hexdigest() == original_hash

def processedString(encodedString):
    """
    Process the decoded string by splitting it into its components.
    The encodedString is first decoded using the Processor class, and then split into parts.
    """
    return Processor.decode(encodedString).split()

# Example Usage:
processor = Processor()

# Encode the data and generate its hash
encoded, generated_hash = processor.encode()
print("Encoded String (Hex with Compression):", encoded)
print("Generated SHA-256 Hash:", generated_hash)

# Decode the encoded string back into the original format
decoded = processor.decode(encoded)
print("Decoded String:", decoded)

# Verify that the hash matches
is_valid = processor.verify_hash(encoded, generated_hash)
print("Hash Verification Result:", is_valid)

# Processed String - Using the method properly
processed = processedString(encoded)
print("Processed String:", processed)
