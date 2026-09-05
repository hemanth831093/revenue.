import time
import requests

BASE_URL = "http://127.0.0.1:8000"

def get_tx(transactions, reason, max_retries=0):
    for t in transactions:
        if t["failure_reason"] == reason and t["retry_count"] == max_retries:
            return t
    return None

def test_recovery():
    print("Fetching transactions from API...")
    res = requests.get(f"{BASE_URL}/api/transactions?limit=100")
    if res.status_code != 200:
        print("Failed to fetch transactions")
        return
        
    transactions = res.json()["items"]
    
    # 1. Find a TX for RETRY SUCCESS (bank_timeout)
    tx_bank = get_tx(transactions, "bank_timeout", 0)
    
    # 2. Find a TX for RETRY FAILURE (insufficient_funds with retry_count=0)
    tx_insufficient = get_tx(transactions, "insufficient_funds", 0)
    
    # 3. Find a TX for HUMAN_ESCALATION (fraud_flag)
    tx_escalate = get_tx(transactions, "fraud_flag")
    
    # 4. Find a TX for PAYMENT_LINK (card_expired)
    tx_card = get_tx(transactions, "card_expired", 0)
    
    tests = [
        {"desc": "RETRY SUCCESS", "id": tx_bank["id"], "expected_action": "RETRY", "expected_success": True},
        {"desc": "RETRY FAILURE", "id": tx_insufficient["id"], "force_action": "RETRY", "expected_action": "RETRY", "expected_success": False},
        {"desc": "HUMAN_ESCALATION", "id": tx_escalate["id"], "expected_action": "HUMAN_ESCALATION", "expected_success": False},
        {"desc": "PAYMENT_LINK", "id": tx_card["id"], "expected_action": "PAYMENT_LINK", "expected_success": True}
    ]
    
    all_pass = True
    
    for t in tests:
        print(f"\nTesting {t['desc']} (TX {t['id']})")
        payload = {}
        if "force_action" in t:
            payload["action_type"] = t["force_action"]
            
        res = requests.post(f"{BASE_URL}/api/recovery/execute/{t['id']}", json=payload)
        
        if res.status_code != 200:
            print(f"FAILED: HTTP {res.status_code}")
            print(res.text)
            all_pass = False
            continue
            
        data = res.json()
        print(f"Result Action: {data['action']}, Status: {data['status']}, Success: {data['success']}")
        
        # Verify attempt_number exists
        if "attempt_number" not in data:
            print("FAILED: Missing attempt_number")
            all_pass = False
            
        if "safety_override" not in data:
            print("FAILED: Missing safety_override")
            all_pass = False
            
        if data['action'] != t['expected_action'] and not data.get("safety_override"):
            print(f"FAILED: Expected action {t['expected_action']}, got {data['action']}")
            all_pass = False
            
    if all_pass:
        print("\nALL RECOVERY TESTS PASSED")
    else:
        print("\nSOME RECOVERY TESTS FAILED")

if __name__ == "__main__":
    test_recovery()
