# NSC-A3: RSA-based Public-key Certification Authority (CA)

## Overview
This assignment implements a **Public-key Certification Authority (CA)** using the **RSA algorithm**. The CA is responsible for issuing and verifying certificates for clients, enabling secure communication. The project demonstrates the use of public-key cryptography for authentication and trust establishment.

---

## Features
- **Client Registration**: Registers clients with their public keys.
- **Certificate Issuance**: Issues certificates signed with the CA's private key.
- **Certificate Verification**: Verifies certificates upon request.
- **RSA Encryption**: Uses RSA (1024-bit keys) for secure communication.

---

## Installation & Prerequisites
### Prerequisites
- Ensure you have Python installed on your system.
- Install the required libraries by running:
  ```sh
  pip install -r requirements.txt

## How to Run
Navigate to the nsc-a3-2022071-2022091 folder:
 ```sh
cd nsc-a3-2022071-2022091
```
Start the CA server:

 ```sh
python CA.py
 ```
Run the client communication script to interact with the CA:
 ```sh
python Code_2022071_2022091/code_2022071_2022091.ipynb
 ```
