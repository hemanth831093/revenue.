# -*- coding: utf-8 -*-
"""
RecoverAI — SQLite → Supabase PostgreSQL Data Migration Script
Exports all rows from SQLite and produces INSERT SQL files for each table.
Run from: backend/
"""
import os
import sys
import json
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "recoverai.db")
OUT_DIR  = os.path.join(os.path.dirname(__file__), "migration_sql")
os.makedirs(OUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

def q(val):
    """Safely quote a value for PostgreSQL INSERT."""
    if val is None:
        return "NULL"
    if isinstance(val, (int, float)):
        return str(val)
    # Escape single quotes
    return "'" + str(val).replace("'", "''") + "'"

# ──────────────────────────────────────────────
# 1. transactions
# ──────────────────────────────────────────────
rows = conn.execute("SELECT * FROM transactions ORDER BY id").fetchall()
print(f"transactions    : {len(rows)} rows")

tx_lines = [
    "-- transactions data\n"
    "INSERT INTO transactions "
    "(id,payment_id,customer_id,customer_name,customer_email,amount,"
    "payment_method,status,failure_reason,failure_code,"
    "previous_successes,previous_failures,retry_count,created_at) VALUES"
]
values = []
for r in rows:
    ts = r["created_at"] if r["created_at"] else datetime.utcnow().isoformat()
    values.append(
        f"({r['id']},{q(r['payment_id'])},{q(r['customer_id'])},"
        f"{q(r['customer_name'])},{q(r['customer_email'])},{r['amount']},"
        f"{q(r['payment_method'])},{q(r['status'])},{q(r['failure_reason'])},"
        f"{q(r['failure_code'])},{r['previous_successes']},{r['previous_failures']},"
        f"{r['retry_count']},{q(ts)})"
    )
tx_sql = "\n".join(tx_lines) + "\n" + ",\n".join(values) + "\nON CONFLICT (payment_id) DO NOTHING;"
with open(os.path.join(OUT_DIR, "01_transactions.sql"), "w", encoding="utf-8") as f:
    f.write(tx_sql)

# ──────────────────────────────────────────────
# 2. risk_scores
# ──────────────────────────────────────────────
rows = conn.execute("SELECT * FROM risk_scores ORDER BY id").fetchall()
print(f"risk_scores     : {len(rows)} rows")

if rows:
    rs_lines = [
        "-- risk_scores data\n"
        "INSERT INTO risk_scores "
        "(id,transaction_id,recovery_probability,priority,risk_factors,model_version,created_at) VALUES"
    ]
    values = []
    for r in rows:
        ts = r["created_at"] if r["created_at"] else datetime.utcnow().isoformat()
        values.append(
            f"({r['id']},{r['transaction_id']},{r['recovery_probability']},"
            f"{q(r['priority'])},{q(r['risk_factors'])},{q(r['model_version'])},{q(ts)})"
        )
    rs_sql = "\n".join(rs_lines) + "\n" + ",\n".join(values) + "\nON CONFLICT DO NOTHING;"
    with open(os.path.join(OUT_DIR, "02_risk_scores.sql"), "w", encoding="utf-8") as f:
        f.write(rs_sql)

# ──────────────────────────────────────────────
# 3. recovery_actions
# ──────────────────────────────────────────────
rows = conn.execute("SELECT * FROM recovery_actions ORDER BY id").fetchall()
print(f"recovery_actions: {len(rows)} rows")

if rows:
    ra_lines = [
        "-- recovery_actions data\n"
        "INSERT INTO recovery_actions "
        "(id,transaction_id,action_type,status,amount_recovered,"
        "razorpay_sim_id,executed_at,response_metadata) VALUES"
    ]
    values = []
    for r in rows:
        ts = r["executed_at"] if r["executed_at"] else datetime.utcnow().isoformat()
        values.append(
            f"({r['id']},{r['transaction_id']},{q(r['action_type'])},"
            f"{q(r['status'])},{r['amount_recovered']},"
            f"{q(r['razorpay_sim_id'])},{q(ts)},{q(r['response_metadata'])})"
        )
    ra_sql = "\n".join(ra_lines) + "\n" + ",\n".join(values) + "\nON CONFLICT DO NOTHING;"
    with open(os.path.join(OUT_DIR, "03_recovery_actions.sql"), "w", encoding="utf-8") as f:
        f.write(ra_sql)

# ──────────────────────────────────────────────
# 4. audit_logs
# ──────────────────────────────────────────────
rows = conn.execute("SELECT * FROM audit_logs ORDER BY id").fetchall()
print(f"audit_logs      : {len(rows)} rows")

if rows:
    al_lines = [
        "-- audit_logs data\n"
        "INSERT INTO audit_logs "
        "(id,transaction_id,decision,reason,action_taken,"
        "execution_result,stopping_rules_applied,created_at) VALUES"
    ]
    values = []
    for r in rows:
        ts = r["created_at"] if r["created_at"] else datetime.utcnow().isoformat()
        values.append(
            f"({r['id']},{r['transaction_id']},{q(r['decision'])},"
            f"{q(r['reason'])},{q(r['action_taken'])},"
            f"{q(r['execution_result'])},{q(r['stopping_rules_applied'])},{q(ts)})"
        )
    al_sql = "\n".join(al_lines) + "\n" + ",\n".join(values) + "\nON CONFLICT DO NOTHING;"
    with open(os.path.join(OUT_DIR, "04_audit_logs.sql"), "w", encoding="utf-8") as f:
        f.write(al_sql)

conn.close()

# ──────────────────────────────────────────────
# 5. Sequence reset (so auto-increment picks up after migration)
# ──────────────────────────────────────────────
seq_sql = """-- Reset sequences so new rows don't collide with migrated IDs
SELECT setval('transactions_id_seq',     (SELECT MAX(id) FROM transactions));
SELECT setval('risk_scores_id_seq',      (SELECT MAX(id) FROM risk_scores));
SELECT setval('recovery_actions_id_seq', (SELECT MAX(id) FROM recovery_actions));
SELECT setval('audit_logs_id_seq',       (SELECT MAX(id) FROM audit_logs));
"""
with open(os.path.join(OUT_DIR, "05_reset_sequences.sql"), "w", encoding="utf-8") as f:
    f.write(seq_sql)

print(f"\nSQL files written to: {OUT_DIR}")
print("Files: 01_transactions.sql, 02_risk_scores.sql, 03_recovery_actions.sql, 04_audit_logs.sql, 05_reset_sequences.sql")
