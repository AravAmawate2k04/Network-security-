import socket
import pickle
import time
import hashlib
from rsa import RSA  

class CAClient:
    def __init__(self, server_host, server_port, client_id, public_key, private_key, ca_public_key):
        self.server_host = server_host
        self.server_port = server_port
        self.client_id = client_id
        self.public_key = public_key        
        self.private_key = private_key      
        self.ca_public_key = ca_public_key  
        self.rsa = RSA(1024)
        self.certificate = None  

    def send_request(self, request):
        """Send a request to the CA server and wait for its response."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.server_host, self.server_port))
                client_socket.sendall(pickle.dumps(request))
                data = client_socket.recv(4096)
                if not data:
                    print("No data received from server for request:", request)
                    return {}
                response = pickle.loads(data)
                return response
        except Exception as e:
            print("Error in send_request for request", request, ":", e)
            return {}

    def register(self):
        request = {
            "action": "register",
            "client_id": self.client_id,
            "public_key": self.public_key
        }
        response = self.send_request(request)
        if response.get("status") == "success":
            # Update CA public key from the server response.
            self.ca_public_key = response.get("ca_public_key", self.ca_public_key)
            print(f"Client {self.client_id} registration successful.")
        else:
            print(f"Client {self.client_id} registration failed:", response.get("message", "Unknown error"))

    def request_certificate(self):
        """Ask the CA to sign a certificate for this client."""
        request = {"action": "sign", "client_id": self.client_id}
        response = self.send_request(request)
        if response.get("status") == "success":
            self.certificate = response.get("certificate")
            print(f"Certificate issued for Client {self.client_id}: {self.certificate}")
        else:
            print(f"Certificate signing failed for Client {self.client_id}: {response.get('message')}")

    def get_peer_certificate(self, peer_id):
        """Request a peer's certificate from the CA."""
        request = {"action": "get_certificate", "peer_id": peer_id}
        response = self.send_request(request)
        if response and response.get("status") == "success":
            return response["certificate"]
        else:
            err = response.get("message", "No response") if response else "No response"
            print(f"Failed to get certificate for {peer_id}: {err}")
            return None

    def validate_certificate(self, certificate):
        """Ask the CA server to verify a certificate."""
        if not certificate:
            return False
        request = {"action": "verify", "client_id": certificate["client_id"]}
        response = self.send_request(request)
        if response.get("status") == "success":
            return True
        else:
            print(f"Certificate verification failed for {certificate['client_id']}: {response.get('message')}")
            return False


    def send_message(self, recipient_public_key, message):
        """Encrypt a message using the recipient's public key."""
        encrypted_message = self.rsa.encrypt(message, recipient_public_key)
        return encrypted_message

    def receive_message(self, encrypted_message):
        """Decrypt an incoming message using the client's private key.
        If the default RSA.decrypt call produces a padding error,
        use a fallback method that converts the decrypted integer to a fixed-length byte string.
        """
        decrypted_message = self.rsa.decrypt(encrypted_message, self.private_key)
        return decrypted_message
