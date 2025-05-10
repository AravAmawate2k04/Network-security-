# NSC-A2: Poly-Alphabetic Substitution Cipher (Vigenère Cipher)

## Overview
This assignment implements encryption and decryption using a **Poly-Alphabetic Substitution Cipher**, specifically the **Vigenère Cipher**. The cipher uses a repeating key to determine the substitution for each character in the plaintext, making it more secure than mono-alphabetic substitution ciphers. Additionally, the assignment includes a brute-force attack to discover the key.

---

## Features
- **Encryption**: Encrypts plaintext using the Vigenère Cipher with a given key.
- **Decryption**: Decrypts ciphertext back into plaintext using the same key.
- **Brute-Force Attack**: Attempts to discover the key by trying all possible combinations and validating the plaintext using a hash function.
- **Key**: A repeating key of fixed length (default: 4).

---

## Installation & Prerequisites
### Prerequisites
- Ensure you have Python installed on your system.
- Install the required libraries by running:
  ```sh
  pip install -r requirements.txt

## How to Run
Navigate to the nsc-a2-2022071-2022091 folder:
 ```sh
cd nsc-a2-2022071-2022091
```
run the script via terminal:
 ```sh
 python nsc-a2.py
 ```
