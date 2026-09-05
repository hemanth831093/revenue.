import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("Testing DB Connection Stability & Endpoints...")
    
    endpoints = [
        ("GET", "/health"),
        ("GET", "/api/dashboard"),
        ("GET", "/api/transactions?limit=10"),
    ]

    for iteration in range(1, 11):
        print(f"\n--- Iteration {iteration}/10 ---")
        try:
            for method, path in endpoints:
                res = requests.request(method, f"{BASE_URL}{path}")
                assert res.status_code == 200, f"{method} {path} failed with {res.status_code}"
            
            # For POST requests, we need a valid transaction ID. 
            # We fetch one from the transactions list we just got.
            tx_res = requests.get(f"{BASE_URL}/api/transactions?limit=10").json()
            tx_id = tx_res["items"][0]["id"]
            
            ai_res = requests.post(f"{BASE_URL}/api/ai/analyze/{tx_id}")
            assert ai_res.status_code == 200, f"AI analyze failed with {ai_res.status_code}"
            
            # Execute recovery (using RETRY)
            exec_res = requests.post(f"{BASE_URL}/api/recovery/execute/{tx_id}", json={"action_type": "RETRY"})
            assert exec_res.status_code == 200, f"Recovery execute failed with {exec_res.status_code}"
            
            print("Iteration passed successfully.")
            time.sleep(0.5)
        except Exception as e:
            print(f"Iteration {iteration} FAILED: {e}")
            sys.exit(1)
            
    print("\nALL STABILITY TESTS PASSED.")

if __name__ == "__main__":
    run_tests()
