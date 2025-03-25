import hashlib
import time

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

def crack_pin(target_hash, digits=4):
    print(f"\n[🔓] Attempting to crack hashed PIN: {target_hash}")
    start = time.time()
    attempts = 0

    max_pin = 10 ** digits
    for pin_int in range(max_pin):
        pin = str(pin_int).zfill(digits)
        hashed = sha256(pin)
        attempts += 1
        if hashed == target_hash:
            elapsed = time.time() - start
            print(f"\n[⚠️] PIN cracked: {pin}")
            print(f"[⏱️] Time taken: {elapsed:.2f} sec")
            print(f"[🔁] Attempts: {attempts}")
            return pin

    print("\n❌ No match found.")
    return None

def main():
    print("=== Simulated Quantum PIN Cracker ===")
    pin = input("Enter 4-digit PIN to simulate attack: ")
    pin_hash = sha256(pin)
    print(f"[INFO] SHA-256(PIN) = {pin_hash}")
    input("Press Enter to begin attack simulation...")

    crack_pin(pin_hash)

if __name__ == "__main__":
    main()
