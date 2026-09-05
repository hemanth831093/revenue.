# -*- coding: utf-8 -*-
"""
Generates numbered small-batch SQL files (15 rows each) for MCP execute_sql migration.
Run from: backend/
"""
import os, sqlite3

DB_PATH  = os.path.join(os.path.dirname(__file__), "recoverai.db")
OUT_DIR  = os.path.join(os.path.dirname(__file__), "migration_sql", "batches")
os.makedirs(OUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

def q(val):
    if val is None: return "NULL"
    if isinstance(val, (int, float)): return str(val)
    return "'" + str(val).replace("'", "''") + "'"

BATCH = 15

# ── transactions ──────────────────────────────────────────────────────
rows = conn.execute("SELECT * FROM transactions ORDER BY id").fetchall()
hdr  = ("INSERT INTO transactions "
        "(id,payment_id,customer_id,customer_name,customer_email,amount,"
        "payment_method,status,failure_reason,failure_code,"
        "previous_successes,previous_failures,retry_count,created_at) VALUES")

files = []
for bi, start in enumerate(range(0, len(rows), BATCH)):
    chunk = rows[start:start+BATCH]
    vals  = []
    for r in chunk:
        ts = r["created_at"] or "2026-09-01 00:00:00"
        vals.append(
            f"({r['id']},{q(r['payment_id'])},{q(r['customer_id'])},"
            f"{q(r['customer_name'])},{q(r['customer_email'])},{r['amount']},"
            f"{q(r['payment_method'])},{q(r['status'])},{q(r['failure_reason'])},"
            f"{q(r['failure_code'])},{r['previous_successes']},{r['previous_failures']},"
            f"{r['retry_count']},{q(ts)})"
        )
    sql = hdr + "\n" + ",\n".join(vals) + "\nON CONFLICT (payment_id) DO NOTHING;"
    fname = os.path.join(OUT_DIR, f"tx_{bi+1:03d}.sql")
    with open(fname, "w", encoding="utf-8") as f: f.write(sql)
    files.append(fname)
print(f"transactions    : {len(rows)} rows -> {len(files)} batch files")

# ── risk_scores ───────────────────────────────────────────────────────
rows = conn.execute("SELECT * FROM risk_scores ORDER BY id").fetchall()
if rows:
    hdr2 = ("INSERT INTO risk_scores "
            "(id,transaction_id,recovery_probability,priority,"
            "risk_factors,model_version,created_at) VALUES")
    for bi, start in enumerate(range(0, len(rows), BATCH)):
        chunk = rows[start:start+BATCH]
        vals  = []
        for r in chunk:
            ts = r["created_at"] or "2026-09-01 00:00:00"
            vals.append(
                f"({r['id']},{r['transaction_id']},{r['recovery_probability']},"
                f"{q(r['priority'])},{q(r['risk_factors'])},{q(r['model_version'])},{q(ts)})"
            )
        sql = hdr2 + "\n" + ",\n".join(vals) + "\nON CONFLICT DO NOTHING;"
        with open(os.path.join(OUT_DIR, f"rs_{bi+1:03d}.sql"), "w", encoding="utf-8") as f:
            f.write(sql)
    print(f"risk_scores     : {len(rows)} rows -> {bi+1} batch files")

# ── recovery_actions ──────────────────────────────────────────────────
rows = conn.execute("SELECT * FROM recovery_actions ORDER BY id").fetchall()
if rows:
    hdr3 = ("INSERT INTO recovery_actions "
            "(id,transaction_id,action_type,status,amount_recovered,"
            "razorpay_sim_id,executed_at,response_metadata) VALUES")
    for bi, start in enumerate(range(0, len(rows), BATCH)):
        chunk = rows[start:start+BATCH]
        vals  = []
        for r in chunk:
            ts = r["executed_at"] or "2026-09-01 00:00:00"
            vals.append(
                f"({r['id']},{r['transaction_id']},{q(r['action_type'])},"
                f"{q(r['status'])},{r['amount_recovered']},"
                f"{q(r['razorpay_sim_id'])},{q(ts)},{q(r['response_metadata'])})"
            )
        sql = hdr3 + "\n" + ",\n".join(vals) + "\nON CONFLICT DO NOTHING;"
        with open(os.path.join(OUT_DIR, f"ra_{bi+1:03d}.sql"), "w", encoding="utf-8") as f:
            f.write(sql)
    print(f"recovery_actions: {len(rows)} rows -> {bi+1} batch files")

# ── audit_logs ────────────────────────────────────────────────────────
rows = conn.execute("SELECT * FROM audit_logs ORDER BY id").fetchall()
if rows:
    hdr4 = ("INSERT INTO audit_logs "
            "(id,transaction_id,decision,reason,action_taken,"
            "execution_result,stopping_rules_applied,created_at) VALUES")
    for bi, start in enumerate(range(0, len(rows), BATCH)):
        chunk = rows[start:start+BATCH]
        vals  = []
        for r in chunk:
            ts = r["created_at"] or "2026-09-01 00:00:00"
            vals.append(
                f"({r['id']},{r['transaction_id']},{q(r['decision'])},"
                f"{q(r['reason'])},{q(r['action_taken'])},"
                f"{q(r['execution_result'])},{q(r['stopping_rules_applied'])},{q(ts)})"
            )
        sql = hdr4 + "\n" + ",\n".join(vals) + "\nON CONFLICT DO NOTHING;"
        with open(os.path.join(OUT_DIR, f"al_{bi+1:03d}.sql"), "w", encoding="utf-8") as f:
            f.write(sql)
    print(f"audit_logs      : {len(rows)} rows -> {bi+1} batch files")

conn.close()

# Print all files sorted
all_files = sorted(os.listdir(OUT_DIR))
print(f"\nTotal batch files: {len(all_files)}")
for fn in all_files:
    size = os.path.getsize(os.path.join(OUT_DIR, fn))
    print(f"  {fn}  ({size} bytes)")
