import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000"

def test_ai():
    print("Testing AI API Endpoint...")
    
    # Wait for server to start
    time.sleep(2)
    
    # Test transactions
    tx_ids = [1, 2, 10]
    
    all_pass = True
    
    for tx_id in tx_ids:
        try:
            res = requests.post(f"{BASE_URL}/api/ai/analyze/{tx_id}")
            if res.status_code == 200:
                data = res.json()
                print(f"--- TX {tx_id} PASS ---")
                
                # Check keys
                required_keys = [
                    "transaction_id", "diagnosis", "risk_score", 
                    "recovery_probability", "expected_recovery_value", 
                    "recommended_action", "explanation", "safety_override"
                ]
                missing = [k for k in required_keys if k not in data]
                if missing:
                    print(f"Missing keys: {missing}")
                    all_pass = False
                else:
                    print("All required keys present.")
                    print(f"Recommended action: {data['recommended_action']}")
                    print(f"Safety override: {data['safety_override']}")
            else:
                print(f"--- TX {tx_id} FAIL ({res.status_code}: {res.text}) ---")
                all_pass = False
        except Exception as e:
            print(f"--- TX {tx_id} FAIL (Exception: {e}) ---")
            all_pass = False

    if all_pass:
        print("\nALL AI TESTS PASSED")
    else:
        print("\nSOME AI TESTS FAILED")

if __name__ == "__main__":
    test_ai()
