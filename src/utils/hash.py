import hashlib

def get_file_hash(filename) -> str:
    hash_sha256 = hashlib.sha256()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

if __name__ == "__main__":
    path = rf"S:\_GITHUB\Side-Projects\256bit_hash\example_file.txt"
    hash_value = get_file_hash(path)
    print(f"SHA-256: {hash_value}")