# -*- coding: utf-8 -*-
"""
RecoverAI — Supabase PostgreSQL Data Importer
Reads migration_sql/*.sql files and executes them against Supabase.
Uses psycopg2 (already in requirements as psycopg2-binary).

Usage:
  Set SUPABASE_DB_URL in environment or pass as arg.
  python import_to_supabase.py "postgresql://postgres:<password>@db.bcosbegvmailqolpcrrl.supabase.co:5432/postgres"
"""
import os
import sys
import glob

def get_db_url():
    url = os.environ.get("SUPABASE_DB_URL") or (sys.argv[1] if len(sys.argv) > 1 else None)
    if not url:
        print("ERROR: Provide SUPABASE_DB_URL env var or pass URL as first argument.")
        print("  python import_to_supabase.py \"postgresql://postgres:<password>@db.bcosbegvmailqolpcrrl.supabase.co:5432/postgres\"")
        sys.exit(1)
    return url

def main():
    import psycopg2

    db_url = get_db_url()
    sql_dir = os.path.join(os.path.dirname(__file__), "migration_sql")
    sql_files = sorted(glob.glob(os.path.join(sql_dir, "*.sql")))

    if not sql_files:
        print(f"No SQL files found in {sql_dir}")
        sys.exit(1)

    print(f"Connecting to Supabase PostgreSQL...")
    conn = psycopg2.connect(db_url)
    conn.autocommit = False
    cur = conn.cursor()

    for fpath in sql_files:
        fname = os.path.basename(fpath)
        with open(fpath, "r", encoding="utf-8") as f:
            sql = f.read().strip()
        if not sql:
            continue
        print(f"  Executing {fname} ...", end=" ", flush=True)
        try:
            cur.execute(sql)
            conn.commit()
            print("OK")
        except Exception as e:
            conn.rollback()
            print(f"ERROR: {e}")
            # Don't abort — continue with remaining files
            continue

    # Verify row counts
    print("\n=== Supabase Row Count Verification ===")
    for tbl in ["transactions", "risk_scores", "recovery_actions", "audit_logs"]:
        cur.execute(f"SELECT COUNT(*) FROM {tbl}")
        count = cur.fetchone()[0]
        print(f"  {tbl:<22}: {count} rows")

    cur.close()
    conn.close()
    print("\nMigration complete.")

if __name__ == "__main__":
    main()
