import random
import json
from datetime import datetime, timedelta
from app.database import Base, engine, SessionLocal
from app.models import Transaction, RiskScore, RecoveryAction, AuditLog

NAMES = [
    "Aarav Sharma", "Ananya Verma", "Rohan Gupta", "Priya Patel", "Vikram Singh",
    "Neha Reddy", "Aditya Joshi", "Siddharth Malhotra", "Kavya Nair", "Rahul Deshmukh",
    "Ishita Banerjee", "Manish Kumar", "Deepika Iyer", "Amitabh Roy", "Pooja Mehta",
    "Sanjay Rao", "Meera Sen", "Karan Kapoor", "Shruti Agarwal", "Varun Bhatia",
    "Ritu Choudhury", "Nitin Saxena", "Tanya Das", "Gaurav Kulkarni", "Simran Gill"
]

FAILURE_REASONS = [
    "bank_timeout",
    "insufficient_funds",
    "card_expired",
    "network_error",
    "fraud_flag"
]

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Netbanking"]

DEMO_CASES_CANONICAL = [
    {
        "payment_id": "pay_DEMO_UPI_5000",
        "status": "FAILED",
        "failure_reason": "bank_timeout",
        "failure_code": "BANK_GATEWAY_TIMEOUT",
        "previous_successes": 4,
        "previous_failures": 0,
        "retry_count": 0,
    },
    {
        "payment_id": "pay_DEMO_RETRY_MAX",
        "status": "FAILED",
        "failure_reason": "bank_timeout",
        "failure_code": "MAX_ATTEMPTS_EXCEEDED",
        "previous_successes": 1,
        "previous_failures": 3,
        "retry_count": 3,
    },
    {
        "payment_id": "pay_DEMO_HIGH_VALUE",
        "status": "FAILED",
        "failure_reason": "network_error",
        "failure_code": "HIGH_VALUE_TIMEOUT",
        "previous_successes": 5,
        "previous_failures": 0,
        "retry_count": 1,
    },
    {
        "payment_id": "pay_DEMO_FRAUD_FLAG",
        "status": "FAILED",
        "failure_reason": "fraud_flag",
        "failure_code": "SUSPICIOUS_VELOCITY",
        "previous_successes": 0,
        "previous_failures": 2,
        "retry_count": 1,
    },
    {
        "payment_id": "pay_DEMO_EXPIRED_CARD",
        "status": "FAILED",
        "failure_reason": "card_expired",
        "failure_code": "EXPIRED_INSTRUMENT",
        "previous_successes": 3,
        "previous_failures": 0,
        "retry_count": 0,
    },
    {
        "payment_id": "pay_DEMO_REMINDER_FUNDS",
        "status": "FAILED",
        "failure_reason": "insufficient_funds",
        "failure_code": "DECLINED_INSUFFICIENT_FUNDS",
        "previous_successes": 2,
        "previous_failures": 1,
        "retry_count": 1,
    },
]


def reset_demo_transactions():
    """Reset only the 6 canonical demo transactions to their original test values.
    Called after each test run so safety rule tests are always reproducible."""
    db = SessionLocal()
    try:
        for canonical in DEMO_CASES_CANONICAL:
            tx = db.query(Transaction).filter(
                Transaction.payment_id == canonical["payment_id"]
            ).first()
            if tx:
                tx.status = canonical["status"]
                tx.failure_reason = canonical["failure_reason"]
                tx.failure_code = canonical["failure_code"]
                tx.previous_successes = canonical["previous_successes"]
                tx.previous_failures = canonical["previous_failures"]
                tx.retry_count = canonical["retry_count"]
        db.commit()
        print("Demo transactions reset to canonical test state.")
    finally:
        db.close()


def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Check if data already exists — reset demo cases and skip bulk seed
    if db.query(Transaction).count() >= 150:
        print("Database already contains >= 150 transactions. Skipping seed.")
        db.close()
        reset_demo_transactions()
        return

    # Clear old data if partial
    db.query(AuditLog).delete()
    db.query(RecoveryAction).delete()
    db.query(RiskScore).delete()
    db.query(Transaction).delete()
    db.commit()

    print("Generating 160 realistic synthetic payment transactions...")
    random.seed(42)

    transactions = []
    
    # 1. SPECIFIC DEMO CASES to guarantee 100% reliable hackathon presentation
    demo_cases = [
        # Demo Case 1: ₹5,000 UPI temporary bank timeout (High recovery prob ~87%, RETRY)
        {
            "payment_id": "pay_DEMO_UPI_5000",
            "customer_id": "cust_1001",
            "customer_name": "Aarav Sharma",
            "customer_email": "aarav.sharma@example.com",
            "amount": 5000.0,
            "payment_method": "UPI",
            "status": "FAILED",
            "failure_reason": "bank_timeout",
            "failure_code": "BANK_GATEWAY_TIMEOUT",
            "previous_successes": 4,
            "previous_failures": 0,
            "retry_count": 0,
            "created_at": datetime.utcnow() - timedelta(minutes=25)
        },
        # Demo Case 2: Max Retries Exceeded (retry_count = 3 -> HUMAN_ESCALATION)
        {
            "payment_id": "pay_DEMO_RETRY_MAX",
            "customer_id": "cust_1002",
            "customer_name": "Rohan Gupta",
            "customer_email": "rohan.gupta@example.com",
            "amount": 4200.0,
            "payment_method": "Credit Card",
            "status": "FAILED",
            "failure_reason": "bank_timeout",
            "failure_code": "MAX_ATTEMPTS_EXCEEDED",
            "previous_successes": 1,
            "previous_failures": 3,
            "retry_count": 3,
            "created_at": datetime.utcnow() - timedelta(hours=2)
        },
        # Demo Case 3: High Value Transaction (₹25,000 >= ₹20,000 threshold -> HUMAN_ESCALATION)
        {
            "payment_id": "pay_DEMO_HIGH_VALUE",
            "customer_id": "cust_1003",
            "customer_name": "Priya Patel",
            "customer_email": "priya.patel@example.com",
            "amount": 25000.0,
            "payment_method": "Netbanking",
            "status": "FAILED",
            "failure_reason": "network_error",
            "failure_code": "HIGH_VALUE_TIMEOUT",
            "previous_successes": 5,
            "previous_failures": 0,
            "retry_count": 1,
            "created_at": datetime.utcnow() - timedelta(hours=1)
        },
        # Demo Case 4: Fraud Flag Transaction (fraud_flag -> HUMAN_ESCALATION)
        {
            "payment_id": "pay_DEMO_FRAUD_FLAG",
            "customer_id": "cust_1004",
            "customer_name": "Vikram Singh",
            "customer_email": "vikram.singh@example.com",
            "amount": 8500.0,
            "payment_method": "Credit Card",
            "status": "FAILED",
            "failure_reason": "fraud_flag",
            "failure_code": "SUSPICIOUS_VELOCITY",
            "previous_successes": 0,
            "previous_failures": 2,
            "retry_count": 1,
            "created_at": datetime.utcnow() - timedelta(hours=4)
        },
        # Demo Case 5: Customer Needs Alternative Payment Link (card_expired -> PAYMENT_LINK)
        {
            "payment_id": "pay_DEMO_EXPIRED_CARD",
            "customer_id": "cust_1005",
            "customer_name": "Ananya Verma",
            "customer_email": "ananya.verma@example.com",
            "amount": 3500.0,
            "payment_method": "Credit Card",
            "status": "FAILED",
            "failure_reason": "card_expired",
            "failure_code": "EXPIRED_INSTRUMENT",
            "previous_successes": 3,
            "previous_failures": 0,
            "retry_count": 0,
            "created_at": datetime.utcnow() - timedelta(hours=3)
        },
        # Demo Case 6: Customer Needs Reminder (insufficient_funds -> REMINDER)
        {
            "payment_id": "pay_DEMO_REMINDER_FUNDS",
            "customer_id": "cust_1006",
            "customer_name": "Neha Reddy",
            "customer_email": "neha.reddy@example.com",
            "amount": 1800.0,
            "payment_method": "UPI",
            "status": "FAILED",
            "failure_reason": "insufficient_funds",
            "failure_code": "DECLINED_INSUFFICIENT_FUNDS",
            "previous_successes": 2,
            "previous_failures": 1,
            "retry_count": 1,
            "created_at": datetime.utcnow() - timedelta(hours=5)
        }
    ]

    for item in demo_cases:
        t = Transaction(**item)
        db.add(t)
        db.flush()

    # 2. GENERATE 154 RANDOMIZED REALISTIC TRANSACTIONS
    amounts_pool = [499.0, 999.0, 1499.0, 2499.0, 3500.0, 4999.0, 7500.0, 9999.0, 12500.0, 15000.0, 18500.0, 22000.0, 35000.0]
    
    for i in range(1, 155):
        name = random.choice(NAMES)
        email = name.lower().replace(" ", ".") + f"{random.randint(10,99)}@example.com"
        cust_id = f"cust_{random.randint(2000, 9999)}"
        pay_id = f"pay_syn_{10000 + i}"
        method = random.choice(PAYMENT_METHODS)
        reason = random.choice(FAILURE_REASONS)
        amount = random.choice(amounts_pool)
        
        # Decide initial status: ~20% already RECOVERED to show baseline dashboard metrics
        is_recovered = random.random() < 0.22
        status = "RECOVERED" if is_recovered else "FAILED"
        
        prev_succ = random.randint(0, 6)
        prev_fail = random.randint(0, 3)
        retry_ct = random.randint(0, 3)
        
        hours_ago = random.randint(1, 120)
        created_dt = datetime.utcnow() - timedelta(hours=hours_ago)
        
        t = Transaction(
            payment_id=pay_id,
            customer_id=cust_id,
            customer_name=name,
            customer_email=email,
            amount=amount,
            payment_method=method,
            status=status,
            failure_reason=reason,
            failure_code=f"ERR_{reason.upper()}",
            previous_successes=prev_succ,
            previous_failures=prev_fail,
            retry_count=retry_ct,
            created_at=created_dt
        )
        db.add(t)
        db.flush()

        # If recovered, generate baseline recovery action and audit log
        if is_recovered:
            rec_act = RecoveryAction(
                transaction_id=t.id,
                action_type="RETRY" if method == "UPI" else "PAYMENT_LINK",
                status="SUCCESS",
                amount_recovered=amount,
                razorpay_sim_id=f"retry_sim_{random.randint(10000, 99999)}",
                executed_at=created_dt + timedelta(minutes=15),
                response_metadata=json.dumps({"gateway": "Razorpay_Sandbox", "status": "captured"})
            )
            db.add(rec_act)
            db.flush()

            audit = AuditLog(
                transaction_id=t.id,
                decision="RECOVERED_AUTOMATICALLY",
                reason=f"Baseline recovery executed for {reason} payment error.",
                action_taken=rec_act.action_type,
                execution_result="SUCCESS",
                stopping_rules_applied=json.dumps({"max_retries_checked": True, "threshold_checked": True}),
                created_at=rec_act.executed_at
            )
            db.add(audit)

    db.commit()
    count = db.query(Transaction).count()
    print(f"Database seeded successfully with {count} total transactions!")
    db.close()

if __name__ == "__main__":
    seed_database()
