# 💳 UPI Simulation System

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Asyncio](https://img.shields.io/badge/asyncio-enabled-green)](https://docs.python.org/3/library/asyncio.html)

A modular Python-based simulation of a **Unified Payments Interface (UPI)** system demonstrating:
- 🔐 Secure user and merchant registration
- 📄 QR-based payment routing
- ⛓️ Blockchain-style transaction ledger
- ⚡ Concurrency-safe, async-driven bank server
- 🧪 Stress-tested with 10,000 simulated users

---

## 🚀 Why this project is impressive

✅ End-to-end architecture with separate components for user, merchant (POS/UPI machine), and bank  
✅ Asyncio-powered bank + threaded UPI machines for realistic concurrency  
✅ Tamper-evident append-only ledger (hash-linked blocks)  
✅ Real-world inspired flow: QR codes, PIN validation, balance management  
✅ Load tested for high concurrency with 10,000 simulated users  

---

## 🛠 Setup Instructions

### 1️⃣ Clone the repo
```bash
git clone https://github.com/abhiniveshmitra/UPI
cd upi-simulation
```

---

### 2️⃣ Start the bank server  
Open **Terminal 1**
```bash
python3 bank_server.py
```
_Listens on port 5000, handles registration and transactions asynchronously._

---

### 3️⃣ Start a UPI machine  
Open **Terminal 2**
```bash
python3 upi_machine.py
```
During setup, enter:
- Merchant Name
- Password
- Starting Balance
- Unique Port (e.g., `6001`)

A QR PNG like `merchantname_qr.png` will be generated.

---

### 4️⃣ Simulate user actions  
Open **Terminal 3**
```bash
python3 user_client.py
```
Options:
- Register User (get MMID)
- Make Payment (paste QR content like `VMID:PORT`)

---

### 5️⃣ (Optional) Stress test with 10,000 users  
Open **Terminal 4**
```bash
python3 simulate_10000_users.py
```
- Saves results to `simulation_results.json`
- Prints summary stats

---

## ⚠️ Limitations

- Data is in-memory → no persistence after restart  
- PINs hashed with SHA256 → for demonstration only (replace with bcrypt/scrypt for production)  
- No TLS → data transmitted in plaintext  
- No nonce/timestamp → vulnerable to replay attacks in real networks  

---

## 💡 Potential Extensions

- Add database persistence (e.g., PostgreSQL, MongoDB)  
- Add TLS encryption for secure communication  
- Include nonce/timestamp to block replay attacks  
- Build a web dashboard to visualize ledger and transactions  

---

## 📂 Example Output

```json
{
  "user": "user123",
  "mmid": "aabbccdd112233",
  "amount": 200,
  "result": "SUCCESS",
  "message": "Transaction successful"
}
```
