# clientB.py
import socket
import pickle
from rsa import RSA

class CAClient:
    def __init__(self, ca_host, ca_port, client_id):
        print(f"[DEBUG B] CAClient.__init__ for client_id='{client_id}'")
        self.ca_host = ca_host
        self.ca_port = ca_port
        self.client_id = client_id
        print(f"[DEBUG B] Generating RSA key pair for {client_id}")
        self.rsa = RSA(1024)
        (pub, priv) = self.rsa.generate_keys()
        self.public_key = pub
        self.private_key = priv
        print(f"[DEBUG B] {client_id} public_key = {self.public_key}")
        print(f"[DEBUG B] {client_id} private_key = {self.private_key}")

    def send_request_to_ca(self, request):
        print(f"[DEBUG {self.client_id}] -> CA: Connecting to {self.ca_host}:{self.ca_port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ca_host, self.ca_port))
            print(f"[DEBUG {self.client_id}] Connected to CA. Sending request: {request}")
            raw_data = pickle.dumps(request)
            print(f"[DEBUG {self.client_id}] Pickled request length = {len(raw_data)}. Sending data...")
            s.sendall(raw_data)
            s.shutdown(socket.SHUT_WR)
            print(f"[DEBUG {self.client_id}] Done sending, waiting for response...")
            data = b""
            while True:
                packet = s.recv(4096)
                if not packet:
                    break
                data += packet
            if data:
                try:
                    response = pickle.loads(data)
                    print(f"[DEBUG {self.client_id}] <- CA: Received response: {response}")
                    return response
                except Exception as e:
                    print(f"[DEBUG {self.client_id}] <- CA: Error unpickling: {e}")
                    return None
            else:
                print(f"[DEBUG {self.client_id}] <- CA: No data received!")
                return None

    def register_with_ca(self):
        print(f"[DEBUG B] {self.client_id} register_with_ca() called.")
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
        print(f"[DEBUG B] {self.client_id} get_public_key_of({target_client_id}) called.")
        req = {
            "action": "get_public_key",
            "target_client_id": target_client_id
        }
        resp = self.send_request_to_ca(req)
        if resp and resp.get("status") == "success":
            print(f"[DEBUG B] {self.client_id} Got public key of {target_client_id}: {resp['public_key']}")
            return resp["public_key"]
        else:
            print(f"[{self.client_id}] Failed to get public key of {target_client_id}. Response: {resp}")
            return None

    def start_listening_for_messages(self, host="127.0.0.1", port=6000):
        print(f"[DEBUG B] {self.client_id} start_listening_for_messages on {host}:{port}")
        print(f"[{self.client_id}] Listening for messages on {host}:{port} ...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen(5)
            while True:
                print(f"[DEBUG B] {self.client_id} waiting for inbound connection on {host}:{port}")
                conn, addr = server_socket.accept()
                with conn:
                    print(f"[DEBUG B] {self.client_id} accepted connection from {addr}")
                    data = b""
                    while True:
                        packet = conn.recv(4096)
                        if not packet:
                            break
                        data += packet
                    if not data:
                        print(f"[DEBUG B] {self.client_id} no data received from {addr}, continuing...")
                        continue
                    print(f"[DEBUG B] {self.client_id} received {len(data)} bytes from {addr}")
                    # Expecting a dict: { 'sender_id': ..., 'ciphertext': ... }
                    msg_dict = pickle.loads(data)
                    sender_id = msg_dict["sender_id"]
                    ciphertext = msg_dict["ciphertext"]
                    print(f"[DEBUG B] {self.client_id} decrypting message from {sender_id}...")
                    plaintext = self.rsa.decrypt(ciphertext, self.private_key)
                    print(f"[{self.client_id}] Received from {sender_id}: {plaintext}")
                    # Build ACK:
                    if plaintext == "Hello1":
                        ack_message = "ACK1"
                    elif plaintext == "Hello2":
                        ack_message = "ACK2"
                    elif plaintext == "Hello3":
                        ack_message = "ACK3"
                    else:
                        ack_message = "ACK_UNKNOWN"
                    print(f"[DEBUG B] {self.client_id} preparing ack_message = '{ack_message}'")
                    a_pub_key = self.get_public_key_of(sender_id)
                    if a_pub_key is None:
                        print(f"[DEBUG B] {self.client_id} no public key for {sender_id}, sending empty response")
                        response_cipher = ""
                    else:
                        response_cipher = self.rsa.encrypt(ack_message, a_pub_key)
                        print(f"[DEBUG B] {self.client_id} ack_message encrypted for {sender_id}")
                    response_dict = {
                        "sender_id": self.client_id,
                        "ciphertext": response_cipher
                    }
                    print(f"[DEBUG B] {self.client_id} sending ACK response back to {addr}")
                    conn.sendall(pickle.dumps(response_dict))

def main():
    print("[DEBUG B] __name__ == '__main__' in clientB.py - calling main()")
    b_client = CAClient("127.0.0.1", 5000, "B")
    b_client.register_with_ca()
    b_client.start_listening_for_messages(host="127.0.0.1", port=6000)

if __name__ == "__main__":
    main()
