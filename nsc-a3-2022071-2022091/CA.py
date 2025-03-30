# CA.py
import socket
import pickle
import hashlib
from datetime import datetime, timedelta
from rsa import RSA

class CertificationAuthority:
    def __init__(self, ca_id="MyCA", key_size=1024):
        print("[DEBUG CA] CertificationAuthority.__init__ called")
        self.ca_id = ca_id
        self.rsa = RSA(key_size)
        self.public_key = None   # (eCA, nCA)
        self.private_key = None  # (dCA, nCA)
        self.client_db = {}      # client_id -> public key
        self.certificate_db = {} # client_id -> certificate info

    def initialize_ca(self):
        print("[DEBUG CA] Generating CA's RSA key pair...")
        (e, n), (d, n) = self.rsa.generate_keys()
        self.public_key = (e, n)
        self.private_key = (d, n)
        print(f"[CA] Initialized with public key = {self.public_key}")

    def register_client(self, client_id, client_public_key):
        print(f"[DEBUG CA] register_client: {client_id} -> {client_public_key}")
        self.client_db[client_id] = client_public_key
        issue_time = datetime.now()
        duration_days = 365
        expiry_time = issue_time + timedelta(days=duration_days)
        cert_info = {
            "client_id": client_id,
            "public_key": client_public_key,
            "issue_time": str(issue_time),
            "duration_days": duration_days,
            "expiry_time": str(expiry_time),
            "ca_id": self.ca_id
        }
        cert_str = f"{client_id}|{client_public_key}|{issue_time}|{duration_days}|{self.ca_id}"
        cert_hash = hashlib.sha256(cert_str.encode()).digest()
        cert_hash_int = int.from_bytes(cert_hash, byteorder='big')
        signature_int = pow(cert_hash_int, self.private_key[0], self.private_key[1])
        cert_info["signature"] = str(signature_int)
        self.certificate_db[client_id] = cert_info
        return True

    def get_client_public_key(self, target_client_id):
        pubkey = self.client_db.get(target_client_id, None)
        print(f"[DEBUG CA] get_client_public_key({target_client_id}) => {pubkey}")
        return pubkey

class CAServer:
    def __init__(self, host="127.0.0.1", port=5000):
        print("[DEBUG CA] CAServer.__init__ called")
        self.host = host
        self.port = port
        self.ca = CertificationAuthority()
        self.ca.initialize_ca()

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"[CA Server] Listening on {self.host}:{self.port} ...")
            while True:
                client_conn, addr = server_socket.accept()
                with client_conn:
                    print(f"[CA Server] Connection from {addr}")
                    data = b""
                    while True:
                        packet = client_conn.recv(4096)
                        if not packet:
                            break
                        data += packet
                    if not data:
                        print("[DEBUG CA] No data received, continuing...")
                        continue
                    print(f"[DEBUG CA] Data length from client = {len(data)}")
                    try:
                        request = pickle.loads(data)
                    except Exception as e:
                        print(f"[DEBUG CA] Error unpickling data: {e}")
                        continue
                    print(f"[DEBUG CA] Received request: {request}")
                    response = self.handle_request(request)
                    print(f"[DEBUG CA] Sending response: {response}")
                    client_conn.sendall(pickle.dumps(response))

    def handle_request(self, request):
        action = request.get("action")
        if action == "register":
            client_id = request.get("client_id")
            client_pub_key = request.get("client_public_key")
            if client_id and client_pub_key:
                success = self.ca.register_client(client_id, client_pub_key)
                if success:
                    return {"status": "success", "message": f"Client {client_id} registered with CA."}
            return {"status": "fail", "message": "Registration failed."}
        elif action == "get_public_key":
            target_id = request.get("target_client_id")
            pub_key = self.ca.get_client_public_key(target_id)
            if pub_key:
                return {"status": "success", "public_key": pub_key}
            else:
                return {"status": "fail", "message": f"No such client '{target_id}'."}
        else:
            return {"status": "fail", "message": "Unknown action."}

if __name__ == "__main__":
    server = CAServer(host="127.0.0.1", port=5000)
    server.start_server()
