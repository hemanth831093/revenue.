from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.models import Transaction, RiskScore, RecoveryAction, AuditLog
from app.schemas import TransactionRead, TransactionCreate
from app.services.risk_engine import risk_engine

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])

@router.get("")
def list_transactions(
    search: Optional[str] = None,
    status: Optional[str] = None,
    failure_reason: Optional[str] = None,
    priority: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(15, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)

    if search:
        s = f"%{search}%"
        query = query.filter(
            (Transaction.payment_id.ilike(s)) |
            (Transaction.customer_name.ilike(s)) |
            (Transaction.customer_email.ilike(s))
        )

    if status:
        query = query.filter(Transaction.status == status.upper())

    if failure_reason:
        query = query.filter(Transaction.failure_reason == failure_reason)

    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)

    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)

    all_matching = query.order_by(Transaction.id.desc()).all()

    # Calculate Risk Score & Priority on the fly if priority filter is specified or for rich response
    results = []
    for t in all_matching:
        prob, prio, risk_factors = risk_engine.calculate_risk(t)
        
        if priority and prio.upper() != priority.upper():
            continue

        results.append({
            "id": t.id,
            "payment_id": t.payment_id,
            "customer_id": t.customer_id,
            "customer_name": t.customer_name,
            "customer_email": t.customer_email,
            "amount": t.amount,
            "payment_method": t.payment_method,
            "status": t.status,
            "failure_reason": t.failure_reason,
            "failure_code": t.failure_code,
            "previous_successes": t.previous_successes,
            "previous_failures": t.previous_failures,
            "retry_count": t.retry_count,
            "recovery_probability": prob,
            "priority": prio,
            "created_at": t.created_at.isoformat()
        })

    total_items = len(results)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_items = results[start_idx:end_idx]

    return {
        "items": paginated_items,
        "total": total_items,
        "page": page,
        "limit": limit,
        "total_pages": (total_items + limit - 1) // limit if total_items > 0 else 1
    }

@router.get("/{id}")
def get_transaction_detail(id: int, db: Session = Depends(get_db)):
    tx = db.query(Transaction).filter(Transaction.id == id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    prob, priority, risk_factors = risk_engine.calculate_risk(tx)

    actions = db.query(RecoveryAction).filter(RecoveryAction.transaction_id == id).order_by(RecoveryAction.id.desc()).all()
    audits = db.query(AuditLog).filter(AuditLog.transaction_id == id).order_by(AuditLog.id.desc()).all()

    return {
        "id": tx.id,
        "payment_id": tx.payment_id,
        "customer_id": tx.customer_id,
        "customer_name": tx.customer_name,
        "customer_email": tx.customer_email,
        "amount": tx.amount,
        "payment_method": tx.payment_method,
        "status": tx.status,
        "failure_reason": tx.failure_reason,
        "failure_code": tx.failure_code,
        "previous_successes": tx.previous_successes,
        "previous_failures": tx.previous_failures,
        "retry_count": tx.retry_count,
        "recovery_probability": prob,
        "priority": priority,
        "risk_factors": risk_factors,
        "created_at": tx.created_at.isoformat(),
        "recovery_actions": [
            {
                "id": a.id,
                "action_type": a.action_type,
                "status": a.status,
                "amount_recovered": a.amount_recovered,
                "razorpay_sim_id": a.razorpay_sim_id,
                "executed_at": a.executed_at.isoformat()
            } for a in actions
        ],
        "audit_logs": [
            {
                "id": au.id,
                "decision": au.decision,
                "reason": au.reason,
                "action_taken": au.action_taken,
                "execution_result": au.execution_result,
                "stopping_rules_applied": au.stopping_rules_applied,
                "created_at": au.created_at.isoformat()
            } for au in audits
        ]
    }

@router.post("/import")
def batch_import_transactions(items: List[TransactionCreate], db: Session = Depends(get_db)):
    created = []
    for item in items:
        tx = Transaction(**item.dict())
        db.add(tx)
        created.append(tx)
    db.commit()
    return {"message": f"Successfully imported {len(created)} transactions", "count": len(created)}
