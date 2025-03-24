import socket
import hashlib
import json
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5000

users = []
merchants = []

def sha256_16(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def handle_registration(data):
    if data["type"] == "register_user":
        print("[BANK] 👤 Registering user...")
        uid = sha256_16(data["name"] + data["mobile"] + data["timestamp"])
        pin_hash = hashlib.sha256(data["pin"].encode()).hexdigest()
        mmid = hashlib.sha256((uid + data["mobile"]).encode()).hexdigest()
        user = {
            "name": data["name"],
            "mobile": data["mobile"],
            "uid": uid,
            "mmid": mmid,
            "pin_hash": pin_hash,
            "balance": float(data["balance"])
        }
        users.append(user)
        print(f"[BANK] ✅ Registered UID={uid}, MMID={mmid}, Balance={user['balance']}")
        return {"status": "success", "uid": uid, "mmid": mmid}

    elif data["type"] == "register_merchant":
        print("[BANK] 🏪 Registering merchant...")
        mid = sha256_16(data["name"] + data["password"] + data["timestamp"])
        pass_hash = hashlib.sha256(data["password"].encode()).hexdigest()
        merchant = {
            "name": data["name"],
            "password_hash": pass_hash,
            "mid": mid,
            "balance": float(data["balance"])
        }
        merchants.append(merchant)
        print(f"[BANK] ✅ Registered MID={mid}, Balance={merchant['balance']}")
        return {"status": "success", "mid": mid}

    return {"status": "error", "message": "Unknown registration type"}

def handle_transaction(data):
    print("\n[BANK] 💸 Transaction Received:")
    print(f"  VMID: {data['vmid']}")
    print(f"  MMID: {data['mmid']}")
    print(f"  Amount: {data['amount']}")
    print(f"  PIN: {'*' * len(data['pin'])}")

    mmid = data["mmid"]
    pin = data["pin"]
    amount = float(data["amount"])

    for user in users:
        if user["mmid"] == mmid:
            print("[BANK] ✅ MMID found.")
            hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
            if hashed_pin != user["pin_hash"]:
                print("[BANK] ❌ Incorrect PIN.")
                return {"status": "fail", "message": "Invalid PIN"}
            if user["balance"] >= amount:
                user["balance"] -= amount
                print(f"[BANK] ✅ Txn approved. New balance: {user['balance']}")
                return {"status": "success", "message": "Transaction approved"}
            else:
                print("[BANK] ❌ Insufficient balance.")
                return {"status": "fail", "message": "Insufficient funds"}
    print("[BANK] ❌ MMID not found.")
    return {"status": "fail", "message": "Invalid MMID"}

def start_bank():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[BANK] 🏦 Listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"\n[BANK] 🔗 Connection from {addr}")
                data = conn.recv(4096)
                if not data:
                    continue
                try:
                    msg = json.loads(data.decode())
                    if msg["type"].startswith("register"):
                        response = handle_registration(msg)
                    elif msg["type"] == "transaction":
                        response = handle_transaction(msg)
                    else:
                        response = {"status": "fail", "message": "Invalid request"}
                    conn.sendall(json.dumps(response).encode())
                except Exception as e:
                    print(f"[BANK] ❌ Error: {e}")
                    conn.sendall(json.dumps({"status": "error", "message": str(e)}).encode())

if __name__ == "__main__":
    start_bank()
