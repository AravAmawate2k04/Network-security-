# NSC-A4: Secure Communication using RSA and Certificates

## Overview
This assignment demonstrates secure communication between two clients using **RSA encryption** and certificates issued by a **Certification Authority (CA)**. The project is divided into two main components:
1. **Backend**: Handles the CA server, client registration, certificate issuance, and validation.
2. **Frontend**: Provides a user interface for interacting with the system.

The project also includes a `utils` folder containing helper scripts for cryptographic operations and other utilities.

---

## Features
- **Certificate Authority (CA)**:
  - Issues certificates to clients.
  - Verifies certificates upon request.
- **Client Communication**:
  - Clients exchange messages securely using RSA encryption.
  - Certificates are used to validate the authenticity of public keys.
- **Frontend**:
  - User-friendly interface for client registration, certificate requests, and secure communication.
- **Backend**:
  - Implements the CA server and handles all cryptographic operations.
- **Utilities**:
  - Helper scripts for RSA key generation, encryption, decryption, and certificate management.

---

---

## Installation & Prerequisites
### Prerequisites
- Ensure you have Python and Node.js installed on your system.
- Install the required Python libraries:
  ```sh
  pip install -r requirements.txt
  ```
- Install the required Node.js dependencies:
 ```sh
 cd backend
 npm install
 ```
## How to Run
Navigate to the nsc-a4-2022071-2022091 folder:
 ```sh
cd nsc-a4-2022071-2022091
```
Before starting enter valid credentails in the nsc-a4-2022071-2022091/utils/email_utils.py.

SENDER_EMAIL    = "your email"        
SENDER_PASSWORD = "your password"  
Navigate to the backend folder:
  ```sh
 npm start
 ```
 Navigate to the frontend in another terminal and run:
 ```sh
  npm start
 ```

