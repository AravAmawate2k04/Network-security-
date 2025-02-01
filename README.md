# Network Security Assignments (CSE350/550) - Jan-May 2025

## Overview
This repository contains the programming assignments for the Network Security (CSE350/550) course. The assignments involve implementing encryption, decryption, and brute-force attack algorithms based on different cryptographic techniques. 

### Completed Assignments:
- **Project 1**: Poly-Alphabetic Substitution Cipher (Vigenère Cipher)
  - Implemented encryption and decryption using a poly-alphabetic substitution cipher.
  - Used a key of length 4 for encryption and decryption.
  - Conducted a brute-force attack to discover the key.
  - Ensured the decrypted text satisfies a recognizable property using a hash function.

### Upcoming Assignments:
- **Project 0**: Mono-Alphabetic Substitution Cipher  
  *To be implemented*
- **Project 2**: Transposition Cipher  
  *To be implemented*
- **Final Assignment**: *To be implemented*

---

## Installation & Usage
### Prerequisites
Ensure you have Python installed along with the required libraries. You can install dependencies using:
```sh
pip install -r requirements.txt
```

### Running the Code
To run Project 1, open the Jupyter Notebook and execute the cells sequentially:
```sh
jupyter notebook code_2022071_2022091.ipynb
```

Alternatively, if you want to run the script via terminal:
```sh
python project1.py
```

---

## Project 1: Details
- **Encryption Algorithm**: Poly-Alphabetic Substitution (Vigenère Cipher)
- **Key Length**: 4
- **Brute-Force Attack**: Attempts all possible keys and validates the plaintext using a hash function.

---

## Contribution
Feel free to fork the repository and contribute. If you find any issues, please open an issue or submit a pull request.

---

## License
This project is under the MIT License.

