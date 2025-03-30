# clientA.py
import socket
import pickle
from rsa import RSA

class CAClientA:
    def __init__(self, ca_host, ca_port, client_id):
        print(f"[DEBUG A] CAClientA.__init__ for client_id='{client_id}'")
        self.ca_host = ca_host
        self.ca_port = ca_port
        self.client_id = client_id
        print(f"[DEBUG A] Generating RSA key pair for {client_id}")
        self.rsa = RSA(1024)
        (pub, priv) = self.rsa.generate_keys()
        self.public_key = pub   # (eA, nA)
        self.private_key = priv # (dA, nA)
        print(f"[DEBUG A] {client_id} public_key = {self.public_key}")
        print(f"[DEBUG A] {client_id} private_key = {self.private_key}")

    def send_request_to_ca(self, request):
        print(f"[DEBUG A] {self.client_id} -> CA: Connecting to {self.ca_host}:{self.ca_port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ca_host, self.ca_port))
            print(f"[DEBUG A] {self.client_id} Connected to CA. Sending request: {request}")
            raw_data = pickle.dumps(request)
            print(f"[DEBUG A] {self.client_id} Pickled request length = {len(raw_data)}. Sending data...")
            s.sendall(raw_data)
            s.shutdown(socket.SHUT_WR)
            print(f"[DEBUG A] {self.client_id} Done sending, waiting for response...")
            data = b""
            while True:
                packet = s.recv(4096)
                if not packet:
                    break
                data += packet
            if data:
                try:
                    response = pickle.loads(data)
                    print(f"[DEBUG A] {self.client_id} <- CA: Received response: {response}")
                    return response
                except Exception as e:
                    print(f"[DEBUG A] {self.client_id} <- CA: Error unpickling: {e}")
                    return None
            else:
                print(f"[DEBUG A] {self.client_id} <- CA: No data received!")
                return None

    def register_with_ca(self):
        print(f"[DEBUG A] {self.client_id} register_with_ca() called.")
        req = {
            "action": "register",
            "client_id": self.client_id,
            "client_public_key": self.public_key
        }
        resp = self.send_request_to_ca(req)
        if resp and resp.get("status") == "success":
            print(f"[{self.client_id}] Registration success: {resp['message']}")
        else:
            print(f"[{self.client_id}] Registration failed: {resp}")

    def get_public_key_of(self, target_client_id):
        print(f"[DEBUG A] {self.client_id} get_public_key_of({target_client_id}) called.")
        req = {
            "action": "get_public_key",
            "target_client_id": target_client_id
        }
        resp = self.send_request_to_ca(req)
        if resp and resp.get("status") == "success":
            print(f"[DEBUG A] {self.client_id} Got public key of {target_client_id}: {resp['public_key']}")
            return resp["public_key"]
        else:
            print(f"[{self.client_id}] Failed to get public key of {target_client_id}. Response: {resp}")
            return None

    def send_message_to_B(self, message, b_public_key):
        print(f"[DEBUG A] {self.client_id} Encrypting message for B: {message}")
        ciphertext = self.rsa.encrypt(message, b_public_key)
        msg_dict = {
            "sender_id": self.client_id,
            "ciphertext": ciphertext
        }
        print(f"[DEBUG A] {self.client_id} Connecting to B on 127.0.0.1:6000...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", 6000))
            raw_data = pickle.dumps(msg_dict)
            print(f"[DEBUG A] {self.client_id} Sending message to B (pickled length: {len(raw_data)})...")
            s.sendall(raw_data)
            # Shutdown the writing side to signal end-of-data.
            s.shutdown(socket.SHUT_WR)
            print(f"[DEBUG A] {self.client_id} Done sending message to B, waiting for ACK...")
            data = b""
            while True:
                packet = s.recv(4096)
                if not packet:
                    break
                data += packet
        if not data:
            print(f"[DEBUG A] {self.client_id} No ACK received from B!")
            return
        response_dict = pickle.loads(data)
        ack_ciphertext = response_dict["ciphertext"]
        print(f"[DEBUG A] {self.client_id} Received ACK ciphertext (length={len(ack_ciphertext)}). Decrypting...")
        ack_plain = self.rsa.decrypt(ack_ciphertext, self.private_key)
        print(f"[{self.client_id}] ACK from B: {ack_plain}")

def main():
    print("[DEBUG A] __name__ == '__main__' in clientA.py - calling main()")
    a_client = CAClientA("127.0.0.1", 5000, "A")
    a_client.register_with_ca()
    b_pub_key = a_client.get_public_key_of("B")
    if b_pub_key is None:
        print("[A] Could not get B's public key, aborting.")
        return
    msgs = ["Hello1", "Hello2", "Hello3"]
    for m in msgs:
        print(f"[A] Sending to B: {m}")
        a_client.send_message_to_B(m, b_pub_key)

if __name__ == "__main__":
    main()
