# Secure Communication System with RSA and Certificate Authority

This repository implements a comprehensive secure communication system using RSA encryption and certificates issued by a Certification Authority (CA). The system includes backend and frontend components designed for secure certificate issuance, user authentication, and encrypted communication.

## Features

### Updated Features

#### Database Connectivity:
- Utilizes **MongoDB** via `pymongo`.
- Stores user details in the `certificate_db.users` collection for authentication and certificate issuance.

#### Secure Communication:
- Implements RSA encryption with public/private key management.
- Keys are stored in PEM format (`public_key.pem`, `private_key.pem`).

#### Authentication:
- OTP-based signup and login system.
- Password hashing through **bcrypt**.
- Includes modules for secure email delivery (`email_utils`).

#### Certificate Generation:
- Generates degree certificates and grade reports as PDFs using **ReportLab**.
- Embeds RSA signatures for verification.

#### Time Synchronization:
- Fetches UTC time from NTP servers (`pool.ntp.org`, `time.google.com`, `time.cloudflare.com`).

#### PDF Utilities:
- Adds signatures to PDFs.
- Uses **PyPDF2** for PDF manipulation.

#### API Interface:
- Provides CLI-based operations via JSON input (`api.py`).

### Folder Structure
- **Backend**:
  - Implements CA server logic and handles cryptographic operations.
  - Includes utilities for RSA encryption, database management, and email delivery.
- **Frontend**:
  - Provides an intuitive user interface for interaction.
  - Built using **React** and communicates with backend APIs.

## Prerequisites
### Backend:
- Node.js v16+
- Python 3.x
- MongoDB instance running locally or remotely.

### Frontend:
- Node.js v16+
- React setup tools (`npm`).

## Installation
### Backend:
1. Navigate to the backend directory:
   ```bash
   cd nsc-a4-2022071-2022091/backend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the server:
   ```bash
   npm start
   ```

### Frontend:
1. Navigate to the frontend directory:
   ```bash
   cd nsc-a4-2022071-2022091/frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

## Usage
1. **Sign Up**:
   - Register with personal and academic information.
   - Verify OTP sent via email.

2. **Login**:
   - Authenticate using credentials and OTP.

3. **Generate and Download Certificates**:
   - Generate official degree certificates and grade reports with embedded RSA signatures.

## Technical Highlights
- **Cryptography**:
  - RSA key management and signing.
  - Secure storage of keys in PEM format.

- **API Integration**:
  - Python utilities for cryptographic operations.
  - RESTful API endpoints for user actions.

- **Security**:
  - OTP-based authentication.
  - Password hashing via **bcrypt**.

- **PDF Generation**:
  - Dynamic creation of certificates and reports using **ReportLab**.
  - PDF manipulation with **PyPDF2**.

## License
This project is licensed under the MIT License.
