# -*- coding: utf-8 -*-
"""
Phase 6 — Recovery Simulator Test Suite
Tests all required recovery cases including idempotency and dashboard metrics.
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app
from app.services.seed_data import seed_database, reset_demo_transactions
from app.database import SessionLocal
from app.models import Transaction

# Always reset demo transactions to canonical state before testing
seed_database()
reset_demo_transactions()

client = TestClient(app)
all_passed = True


def check(label, condition, got=None, expected=None):
    global all_passed
    status = "PASS" if condition else "FAIL"
    if not condition:
        all_passed = False
    suffix = f"  expected={expected}  got={got}" if (got is not None or expected is not None) else ""
    print(f"  [{status}] {label}{suffix}")


def get_tx_id(payment_id):
    resp = client.get(f"/api/transactions?search={payment_id}")
    items = resp.json()["items"]
    assert items, f"Transaction {payment_id} not found in DB"
    return items[0]["id"]


def get_dashboard():
    return client.get("/api/dashboard").json()


print("=" * 65)
print("PHASE 6 -- RECOVERY SIMULATOR TEST SUITE")
print("=" * 65)

# ─────────────────────────────────────────────────────────────────
# TEST 1: Rs.5,000 bank_timeout retry_count=0 -> RETRY -> SUCCESS
# ─────────────────────────────────────────────────────────────────
print("\nTEST 1: Rs.5000 bank_timeout + retry_count=0 -> RETRY -> SUCCESS")
reset_demo_transactions()
dash_before = get_dashboard()
recovered_before = dash_before["total_revenue_recovered"]

tx_id = get_tx_id("pay_DEMO_UPI_5000")
resp = client.post(f"/api/recovery/execute/{tx_id}")
check("HTTP 200", resp.status_code == 200, resp.status_code, 200)
d = resp.json()
check("action == RETRY",           d.get("action") == "RETRY",         d.get("action"),           "RETRY")
check("status == SUCCESS",         d.get("status") == "SUCCESS",        d.get("status"),           "SUCCESS")
check("amount_recovered == 5000",  d.get("amount_recovered") == 5000.0, d.get("amount_recovered"), 5000.0)
check("new_status == RECOVERED",   d.get("new_status") == "RECOVERED",  d.get("new_status"),       "RECOVERED")
check("simulation_id present",     bool(d.get("simulation_id")))
check("audit_log_id > 0",          d.get("audit_log_id", 0) > 0)

dash_after = get_dashboard()
recovered_after = dash_after["total_revenue_recovered"]
check("Dashboard recovered revenue increased",
      recovered_after > recovered_before,
      round(recovered_after, 2), f"> {round(recovered_before, 2)}")

# ─────────────────────────────────────────────────────────────────
# TEST 2: retry_count = 3 -> HUMAN_ESCALATION
# ─────────────────────────────────────────────────────────────────
print("\nTEST 2: retry_count=3 -> HUMAN_ESCALATION")
reset_demo_transactions()
tx_id = get_tx_id("pay_DEMO_RETRY_MAX")
resp = client.post(f"/api/recovery/execute/{tx_id}")
check("HTTP 200", resp.status_code == 200, resp.status_code, 200)
d = resp.json()
check("action == HUMAN_ESCALATION", d.get("action") == "HUMAN_ESCALATION", d.get("action"), "HUMAN_ESCALATION")
check("new_status == ESCALATED",    d.get("new_status") == "ESCALATED",    d.get("new_status"),  "ESCALATED")
check("amount_recovered == 0",      d.get("amount_recovered") == 0.0,      d.get("amount_recovered"), 0.0)

# ─────────────────────────────────────────────────────────────────
# TEST 3: amount = Rs.25,000 -> HUMAN_ESCALATION
# ─────────────────────────────────────────────────────────────────
print("\nTEST 3: amount=Rs.25000 -> HUMAN_ESCALATION")
reset_demo_transactions()
tx_id = get_tx_id("pay_DEMO_HIGH_VALUE")
resp = client.post(f"/api/recovery/execute/{tx_id}")
check("HTTP 200", resp.status_code == 200, resp.status_code, 200)
d = resp.json()
check("action == HUMAN_ESCALATION", d.get("action") == "HUMAN_ESCALATION", d.get("action"), "HUMAN_ESCALATION")
check("new_status == ESCALATED",    d.get("new_status") == "ESCALATED",    d.get("new_status"),  "ESCALATED")

# ─────────────────────────────────────────────────────────────────
# TEST 4: fraud_flag -> HUMAN_ESCALATION
# ─────────────────────────────────────────────────────────────────
print("\nTEST 4: fraud_flag -> HUMAN_ESCALATION")
reset_demo_transactions()
tx_id = get_tx_id("pay_DEMO_FRAUD_FLAG")
resp = client.post(f"/api/recovery/execute/{tx_id}")
check("HTTP 200", resp.status_code == 200, resp.status_code, 200)
d = resp.json()
check("action == HUMAN_ESCALATION", d.get("action") == "HUMAN_ESCALATION", d.get("action"), "HUMAN_ESCALATION")
check("new_status == ESCALATED",    d.get("new_status") == "ESCALATED",    d.get("new_status"),  "ESCALATED")

# ─────────────────────────────────────────────────────────────────
# TEST 5: card_expired -> PAYMENT_LINK
# ─────────────────────────────────────────────────────────────────
print("\nTEST 5: card_expired -> PAYMENT_LINK")
reset_demo_transactions()
tx_id = get_tx_id("pay_DEMO_EXPIRED_CARD")
resp = client.post(f"/api/recovery/execute/{tx_id}")
check("HTTP 200", resp.status_code == 200, resp.status_code, 200)
d = resp.json()
check("action == PAYMENT_LINK",    d.get("action") == "PAYMENT_LINK",  d.get("action"),   "PAYMENT_LINK")
check("status == SUCCESS",         d.get("status") == "SUCCESS",       d.get("status"),   "SUCCESS")
check("simulation_id present",     bool(d.get("simulation_id")))
check("new_status == RECOVERED",   d.get("new_status") == "RECOVERED", d.get("new_status"), "RECOVERED")

# ─────────────────────────────────────────────────────────────────
# TEST 6: insufficient_funds -> REMINDER or PAYMENT_LINK
# ─────────────────────────────────────────────────────────────────
print("\nTEST 6: insufficient_funds -> REMINDER or PAYMENT_LINK")
reset_demo_transactions()
tx_id = get_tx_id("pay_DEMO_REMINDER_FUNDS")
resp = client.post(f"/api/recovery/execute/{tx_id}")
check("HTTP 200", resp.status_code == 200, resp.status_code, 200)
d = resp.json()
check("action in (REMINDER, PAYMENT_LINK)",
      d.get("action") in ("REMINDER", "PAYMENT_LINK"),
      d.get("action"), "REMINDER or PAYMENT_LINK")
check("simulation_id present", bool(d.get("simulation_id")))
print(f"  [INFO] Got action={d.get('action')}  status={d.get('status')}  amount_recovered={d.get('amount_recovered')}")

# ─────────────────────────────────────────────────────────────────
# TEST 7: IDEMPOTENCY — execute the same RECOVERED tx twice
#          Revenue must NOT be double-counted
# ─────────────────────────────────────────────────────────────────
print("\nTEST 7: Idempotency — execute RECOVERED tx twice, no double-count")
reset_demo_transactions()

tx_id = get_tx_id("pay_DEMO_UPI_5000")
# First execution
r1 = client.post(f"/api/recovery/execute/{tx_id}").json()
check("First execution SUCCESS",     r1.get("status") == "SUCCESS", r1.get("status"), "SUCCESS")
check("First execution RECOVERED",   r1.get("new_status") == "RECOVERED")

dash_mid = get_dashboard()
recovered_mid = dash_mid["total_revenue_recovered"]

# Second execution — must be idempotent
r2 = client.post(f"/api/recovery/execute/{tx_id}").json()
check("Second execution is ALREADY_RECOVERED",
      r2.get("status") == "ALREADY_RECOVERED",
      r2.get("status"), "ALREADY_RECOVERED")

dash_final = get_dashboard()
recovered_final = dash_final["total_revenue_recovered"]
check("Revenue NOT double-counted after second execution",
      abs(recovered_final - recovered_mid) < 0.01,
      round(recovered_final, 2), round(recovered_mid, 2))

# ─────────────────────────────────────────────────────────────────
# TEST 8: Batch Execute — process multiple transactions safely
# ─────────────────────────────────────────────────────────────────
print("\nTEST 8: Batch Execute — multiple transactions, safety enforced")
reset_demo_transactions()

# Use DEMO_UPI_5000 (RETRY) and DEMO_RETRY_MAX (HUMAN_ESCALATION)
id1 = get_tx_id("pay_DEMO_UPI_5000")
id2 = get_tx_id("pay_DEMO_RETRY_MAX")
batch_resp = client.post("/api/recovery/batch-execute", json=[id1, id2])
check("Batch HTTP 200", batch_resp.status_code == 200, batch_resp.status_code, 200)
bd = batch_resp.json()
check("Batch processed_count == 2", bd.get("processed_count") == 2, bd.get("processed_count"), 2)
r_upi = bd["results"][0]
r_max = bd["results"][1]
check("Batch tx1 -> RETRY/SUCCESS",
      r_upi.get("action") == "RETRY" and r_upi.get("status") == "SUCCESS",
      f"action={r_upi.get('action')} status={r_upi.get('status')}")
check("Batch tx2 -> HUMAN_ESCALATION (safety enforced)",
      r_max.get("action") == "HUMAN_ESCALATION",
      r_max.get("action"), "HUMAN_ESCALATION")

# ─────────────────────────────────────────────────────────────────
# TEST 9: Verify RecoveryAction + AuditLog DB records
# ─────────────────────────────────────────────────────────────────
print("\nTEST 9: DB records — RecoveryAction + AuditLog created")
audit_resp = client.get("/api/audit-logs?search=pay_DEMO_UPI_5000")
audits = audit_resp.json()["items"]
check("AuditLog entries exist for demo tx", len(audits) > 0, len(audits), "> 0")

history_resp = client.get("/api/recovery/history")
check("Recovery history HTTP 200", history_resp.status_code == 200)
history = history_resp.json()
check("Recovery history not empty", len(history) > 0, len(history), "> 0")

# ─────────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────────
print()
print("=" * 65)
if all_passed:
    print("ALL PHASE 6 RECOVERY TESTS PASSED")
else:
    print("SOME TESTS FAILED -- see above")
print("=" * 65)
