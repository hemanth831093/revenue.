# -*- coding: utf-8 -*-
"""
Phase 5 Safety Rules - Manual Test Script
Tests all 7 required safety cases without pytest
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app
from app.services.seed_data import seed_database, reset_demo_transactions
from app.database import SessionLocal
from app.models import Transaction

# Seed and reset demo transactions to canonical state
seed_database()
reset_demo_transactions()

client = TestClient(app)

CASES = [
    ("pay_DEMO_UPI_5000",       "RETRY",            "Rs.5000 + bank_timeout + retry_count=0"),
    ("pay_DEMO_HIGH_VALUE",     "HUMAN_ESCALATION", "Rs.25000 + bank_timeout (high value)"),
    ("pay_DEMO_FRAUD_FLAG",     "HUMAN_ESCALATION", "fraud_flag"),
    ("pay_DEMO_EXPIRED_CARD",   "PAYMENT_LINK",     "card_expired"),
    ("pay_DEMO_REMINDER_FUNDS", "REMINDER",         "insufficient_funds"),
    ("pay_DEMO_RETRY_MAX",      "HUMAN_ESCALATION", "retry_count=3"),
]

all_passed = True
print("=" * 60)
print("PHASE 5 -- SAFETY RULES TEST SUITE")
print("=" * 60)

for payment_id, expected_action, label in CASES:
    resp = client.get(f"/api/transactions?search={payment_id}")
    items = resp.json()["items"]
    if not items:
        print(f"[FAIL] {label}: Transaction not found ({payment_id})")
        all_passed = False
        continue
    tx_id = items[0]["id"]
    ai_resp = client.post(f"/api/ai/analyze/{tx_id}")
    assert ai_resp.status_code == 200, f"HTTP error {ai_resp.status_code}: {ai_resp.text}"
    data = ai_resp.json()
    actual = data.get("recommended_action")
    prob = data.get("recovery_probability")
    rules = data.get("stopping_rules_applied", [])
    # insufficient_funds accepts REMINDER or PAYMENT_LINK
    if expected_action == "REMINDER":
        passed = actual in ("REMINDER", "PAYMENT_LINK")
    else:
        passed = actual == expected_action
    if not passed:
        all_passed = False
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {label}")
    print(f"       expected={expected_action}  got={actual}  prob={prob}")
    if rules:
        print(f"       rules_applied={rules}")

# Case 7: network_error + high recovery probability (create fresh test tx if needed)
print()
db = SessionLocal()
existing = db.query(Transaction).filter(Transaction.payment_id == "pay_TEST_NETWORK_HIGH").first()
if existing:
    existing.status = "FAILED"
    existing.retry_count = 0
    existing.previous_successes = 5
    db.commit()
    tx_id = existing.id
else:
    tx = Transaction(
        payment_id="pay_TEST_NETWORK_HIGH",
        customer_id="cust_test_net",
        customer_name="Test Network User",
        customer_email="testnet@example.com",
        amount=3000.0,
        payment_method="UPI",
        status="FAILED",
        failure_reason="network_error",
        failure_code="NET_ERR",
        previous_successes=5,
        previous_failures=0,
        retry_count=0,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    tx_id = tx.id
db.close()

ai_resp = client.post(f"/api/ai/analyze/{tx_id}")
data = ai_resp.json()
actual = data.get("recommended_action")
prob = data.get("recovery_probability")
passed = actual == "RETRY"
if not passed:
    all_passed = False
print(f"[{'PASS' if passed else 'FAIL'}] network_error + high recovery probability")
print(f"       expected=RETRY  got={actual}  prob={prob}")

# Verify AuditLog was created
print()
audit_resp = client.get("/api/audit-logs?search=pay_DEMO_UPI_5000")
audits = audit_resp.json()["items"]
audit_ok = len(audits) > 0
status = "PASS" if audit_ok else "FAIL"
print(f"[{status}] AuditLog created for AI analysis (found {len(audits)} entries)")
if not audit_ok:
    all_passed = False

print()
print("=" * 60)
if all_passed:
    print("ALL PHASE 5 SAFETY TESTS PASSED")
else:
    print("SOME TESTS FAILED -- see above")
print("=" * 60)
