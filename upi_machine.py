import socket
import json
import hashlib
import qrcode
from datetime import datetime
import threading

BANK_IP = "127.0.0.1"
BANK_PORT = 5000

def speck_fake_encrypt(mid):
    return hashlib.sha256(mid.encode()).hexdigest()[:16]

def generate_qr(vmid, port, merchant_name):
    qr_data = f"{vmid}:{port}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    filename = f"{merchant_name}_qr.png"
    img.save(filename)
    print(f"[UPI] ✅ QR saved as {filename} with data: {qr_data}")

def send_to_bank(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((BANK_IP, BANK_PORT))
            s.sendall(json.dumps(data).encode())
            response = s.recv(4096)
            return json.loads(response.decode())
    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_user(conn):
    try:
        data = conn.recv(4096)
        tx = json.loads(data.decode())
        print(f"[UPI] 📥 Received from User: {tx}")
        result = send_to_bank(tx)
        conn.sendall(json.dumps(result).encode())
        print("[UPI] 📤 Sent result to User")
    except Exception as e:
        conn.sendall(json.dumps({"status": "error", "message": str(e)}).encode())

def start_listener(port):
    print(f"[UPI] 🧿 Listening on port {port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", port))
        s.listen()
        while True:
            conn, _ = s.accept()
            threading.Thread(target=handle_user, args=(conn,)).start()

def main():
    print("\n=== UPI Machine: Merchant Setup ===")
    name = input("Merchant Name: ")
    password = input("Password: ")
    balance = input("Balance: ")
    port = int(input("Choose a unique UPI port (e.g. 6001, 6002...): "))
    timestamp = datetime.now().isoformat()

    # Register merchant
    data = {
        "type": "register_merchant",
        "name": name,
        "password": password,
        "balance": balance,
        "timestamp": timestamp
    }

    response = send_to_bank(data)
    if response["status"] == "success":
        mid = response["mid"]
        vmid = speck_fake_encrypt(mid)
        generate_qr(vmid, port, name)
        start_listener(port)
    else:
        print("[UPI] ❌ Registration failed:", response.get("message", "Unknown error"))

if __name__ == "__main__":
    main()
