import asyncio
import random
import json
import hashlib
from datetime import datetime

BANK_IP = '127.0.0.1'
BANK_PORT = 5000
UPI_IP = '127.0.0.1'
UPI_PORT = 6001
VMID = "84c3ae9c51785857"

semaphore = asyncio.Semaphore(250)
results = []  # Will store all transaction results

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

async def register_user(session_id):
    async with semaphore:
        name = f"user{session_id}"
        mobile = f"99999{random.randint(10000, 99999)}"
        pin = "4321"
        balance = round(random.uniform(50, 1000), 2)
        timestamp = datetime.now().isoformat()

        user = {
            "type": "register_user",
            "name": name,
            "mobile": mobile,
            "pin": pin,
            "balance": balance,
            "timestamp": timestamp
        }

        try:
            reader, writer = await asyncio.open_connection(BANK_IP, BANK_PORT)
            writer.write(json.dumps(user).encode())
            await writer.drain()
            data = await reader.read(4096)
            writer.close()
            await writer.wait_closed()
            resp = json.loads(data.decode())
            return {
                "name": name,
                "mobile": mobile,
                "pin": pin,
                "balance": balance,
                "mmid": resp.get("mmid")
            }
        except Exception as e:
            print(f"[REGISTER {name}] ERROR: {e}")
            return None

async def send_transaction(user, fake_pin=False, zero_balance=False):
    async with semaphore:
        pin = user["pin"]
        if fake_pin:
            pin = "0000"
            amount = round(random.uniform(1, user["balance"]), 2)
        elif zero_balance:
            amount = user["balance"] + 100
        else:
            amount = round(random.uniform(1, user["balance"] * 0.8), 2)

        txn = {
            "type": "transaction",
            "vmid": VMID,
            "mmid": user["mmid"],
            "pin": pin,
            "amount": amount
        }

        try:
            reader, writer = await asyncio.open_connection(UPI_IP, UPI_PORT)
            writer.write(json.dumps(txn).encode())
            await writer.drain()
            result = await reader.read(4096)
            writer.close()
            await writer.wait_closed()

            resp = json.loads(result.decode())
            status = resp.get("status", "error").upper()
            message = resp.get("message", "Unknown")

            results.append({
                "user": user["name"],
                "mmid": user["mmid"],
                "amount": amount,
                "result": status,
                "message": message
            })

            print(f"[TXN {user['name']}] → {status}: {message}")
        except Exception as e:
            results.append({
                "user": user["name"],
                "mmid": user["mmid"],
                "amount": amount,
                "result": "ERROR",
                "message": str(e)
            })
            print(f"[TXN {user['name']}] ERROR: {e}")

async def simulate_all(num_users=10000):
    print(f"\n[⚔️] Simulating {num_users} Users...")
    users_raw = await asyncio.gather(*[register_user(i) for i in range(num_users)])
    users = [u for u in users_raw if u]

    tasks = []
    for user in users:
        mode = random.choice(['ok', 'bad_pin', 'low_funds'])
        if mode == 'bad_pin':
            tasks.append(send_transaction(user, fake_pin=True))
        elif mode == 'low_funds':
            tasks.append(send_transaction(user, zero_balance=True))
        else:
            tasks.append(send_transaction(user))

    await asyncio.gather(*tasks)

    # 🧾 Save to JSON file
    with open("simulation_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # 🧮 Final Summary
    success = sum(1 for r in results if r['result'] == 'SUCCESS')
    fail_pin = sum(1 for r in results if 'Wrong PIN' in r['message'])
    fail_funds = sum(1 for r in results if 'Insufficient' in r['message'])
    error_other = len(results) - success - fail_pin - fail_funds

    print(f"\n📊 Simulation Summary:")
    print(f"  ✅ SUCCESS: {success}")
    print(f"  ❌ Wrong PIN: {fail_pin}")
    print(f"  💸 Insufficient Funds: {fail_funds}")
    print(f"  ⚠️ Other Errors: {error_other}")
    print(f"  📁 Full log saved to: simulation_results.json")

if __name__ == "__main__":
    asyncio.run(simulate_all())
import asyncio
import random
import json
import hashlib
from datetime import datetime

BANK_IP = '127.0.0.1'
BANK_PORT = 5000
UPI_IP = '127.0.0.1'
UPI_PORT = 6001
VMID = "a2560038e7942ace"

semaphore = asyncio.Semaphore(250)
results = []  # Will store all transaction results

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

async def register_user(session_id):
    async with semaphore:
        name = f"user{session_id}"
        mobile = f"99999{random.randint(10000, 99999)}"
        pin = "4321"
        balance = round(random.uniform(50, 1000), 2)
        timestamp = datetime.now().isoformat()

        user = {
            "type": "register_user",
            "name": name,
            "mobile": mobile,
            "pin": pin,
            "balance": balance,
            "timestamp": timestamp
        }

        try:
            reader, writer = await asyncio.open_connection(BANK_IP, BANK_PORT)
            writer.write(json.dumps(user).encode())
            await writer.drain()
            data = await reader.read(4096)
            writer.close()
            await writer.wait_closed()
            resp = json.loads(data.decode())
            return {
                "name": name,
                "mobile": mobile,
                "pin": pin,
                "balance": balance,
                "mmid": resp.get("mmid")
            }
        except Exception as e:
            print(f"[REGISTER {name}] ERROR: {e}")
            return None

async def send_transaction(user, fake_pin=False, zero_balance=False):
    async with semaphore:
        pin = user["pin"]
        if fake_pin:
            pin = "0000"
            amount = round(random.uniform(1, user["balance"]), 2)
        elif zero_balance:
            amount = user["balance"] + 100
        else:
            amount = round(random.uniform(1, user["balance"] * 0.8), 2)

        txn = {
            "type": "transaction",
            "vmid": VMID,
            "mmid": user["mmid"],
            "pin": pin,
            "amount": amount
        }

        try:
            reader, writer = await asyncio.open_connection(UPI_IP, UPI_PORT)
            writer.write(json.dumps(txn).encode())
            await writer.drain()
            result = await reader.read(4096)
            writer.close()
            await writer.wait_closed()

            resp = json.loads(result.decode())
            status = resp.get("status", "error").upper()
            message = resp.get("message", "Unknown")

            results.append({
                "user": user["name"],
                "mmid": user["mmid"],
                "amount": amount,
                "result": status,
                "message": message
            })

            print(f"[TXN {user['name']}] → {status}: {message}")
        except Exception as e:
            results.append({
                "user": user["name"],
                "mmid": user["mmid"],
                "amount": amount,
                "result": "ERROR",
                "message": str(e)
            })
            print(f"[TXN {user['name']}] ERROR: {e}")

async def simulate_all(num_users=10000):
    print(f"\n[⚔️] Simulating {num_users} Users...")
    users_raw = await asyncio.gather(*[register_user(i) for i in range(num_users)])
    users = [u for u in users_raw if u]

    tasks = []
    for user in users:
        mode = random.choice(['ok', 'bad_pin', 'low_funds'])
        if mode == 'bad_pin':
            tasks.append(send_transaction(user, fake_pin=True))
        elif mode == 'low_funds':
            tasks.append(send_transaction(user, zero_balance=True))
        else:
            tasks.append(send_transaction(user))

    await asyncio.gather(*tasks)

    # 🧾 Save to JSON file
    with open("simulation_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # 🧮 Final Summary
    success = sum(1 for r in results if r['result'] == 'SUCCESS')
    fail_pin = sum(1 for r in results if 'Wrong PIN' in r['message'])
    fail_funds = sum(1 for r in results if 'Insufficient' in r['message'])
    error_other = len(results) - success - fail_pin - fail_funds

    print(f"\n📊 Simulation Summary:")
    print(f"  ✅ SUCCESS: {success}")
    print(f"  ❌ Wrong PIN: {fail_pin}")
    print(f"  💸 Insufficient Funds: {fail_funds}")
    print(f"  ⚠️ Other Errors: {error_other}")
    print(f"  📁 Full log saved to: simulation_results.json")

if __name__ == "__main__":
    asyncio.run(simulate_all())
