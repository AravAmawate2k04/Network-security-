import socket
import pickle
import hashlib
from rsa import RSA  
import time

# Certification Authority: stores client public keys and issues certificates.
class CertificationAuthority:
    def __init__(self):
        self.rsa = RSA(1024)
        self.ca_public_key, self.ca_private_key = self.rsa.generate_keys()
        self.client_public_keys = {}  
        self.certificates = {}        

    def register_client(self, client_id, client_public_key):
        """Register a client by storing its public key."""
        self.client_public_keys[client_id] = client_public_key
        print(f"[CA] Registered client {client_id} with public key: {client_public_key}")
        return "Client registered successfully."

    def sign_certificate(self, client_id, duration=600):
        if client_id not in self.client_public_keys:
            return None, "Client not registered"

        public_key = self.client_public_keys[client_id]
        issue_time = int(time.time())
        certificate_data = f"ClientID: {client_id}, PublicKey: {public_key}, IssueTime: {issue_time}, Duration: {duration}"
        certificate_hash = hashlib.sha256(certificate_data.encode()).digest()
        hash_int = int.from_bytes(certificate_hash, byteorder='big')
        encrypted_signature = self.rsa.encrypt(str(hash_int), self.ca_public_key)

        certificate = {
            "client_id": client_id,
            "public_key": public_key,
            "issue_time": issue_time,
            "duration": duration,
            "signature": encrypted_signature
        }
        self.certificates[client_id] = certificate
        print(f"[CA] Issued certificate for client {client_id}: {certificate}")
        return certificate, "Certificate Issued"

    def verify_certificate(self, client_id):
        if client_id not in self.certificates:
            return False, "Certificate not found!"

        certificate = self.certificates[client_id]
        current_time = int(time.time())
        if current_time > (certificate["issue_time"] + certificate["duration"]):
            return False, "Certificate Expired!"

        certificate_data = (
            f"ClientID: {certificate['client_id']}, PublicKey: {certificate['public_key']}, "
            f"IssueTime: {certificate['issue_time']}, Duration: {certificate['duration']}"
        )
        expected_hash = hashlib.sha256(certificate_data.encode()).digest()

        try:
            decrypted_hash_str = self.rsa.decrypt(certificate["signature"], self.ca_private_key)
            decrypted_hash = int(decrypted_hash_str).to_bytes(32, byteorder='big')
            if decrypted_hash == expected_hash:
                return True, "Certificate is Valid."
            else:
                return False, "Invalid Certificate Signature!"
        except Exception as e:
            return False, f"Decryption Failed: {str(e)}"

# CA Server: handles requests from clients.
class CAServer:
    def __init__(self, host="127.0.0.1", port=50051):
        self.host = host
        self.port = port
        self.ca = CertificationAuthority()

    def start(self):
        """Start the CA server to listen for client requests."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                # Allow reuse of the socket address.
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_socket.bind((self.host, self.port))
                server_socket.listen(5)
                print(f"\n[CA Server] Running at {self.host}:{self.port}...\n")
                while True:
                    client_socket, address = server_socket.accept()
                    print("[CA Server] Connected to", address)
                    with client_socket:
                        request = pickle.loads(client_socket.recv(4096))
                        response = self.handle_request(request)
                        client_socket.sendall(pickle.dumps(response))
        except Exception as e:
            print("Server encountered an error:", e)

    def handle_request(self, request):
        action = request.get("action")
        if action == "register":
            client_id = request["client_id"]
            client_public_key = request.get("public_key")
            message = self.ca.register_client(client_id, client_public_key)
            return {
                "status": "success",
                "message": message,
                "ca_public_key": self.ca.ca_public_key 
            }
        elif action == "sign":
            client_id = request["client_id"]
            certificate, message = self.ca.sign_certificate(client_id)
            if certificate:
                return {"status": "success", "certificate": certificate}
            else:
                return {"status": "failed", "message": message}
        elif action == "get_certificate":
            peer_id = request.get("peer_id")
            if peer_id in self.ca.certificates:
                return {"status": "success", "certificate": self.ca.certificates[peer_id]}
            else:
                return {"status": "failed", "message": "Certificate not found"}
        elif action == "verify":
            client_id = request.get("client_id")
            valid, message = self.ca.verify_certificate(client_id)
            if valid:
                return {"status": "success", "message": message}
            else:
                return {"status": "failed", "message": message}
        else:
            return {"status": "error", "message": "Invalid request"}


if __name__ == "__main__":
    ca_server = CAServer()
    ca_server.start()
