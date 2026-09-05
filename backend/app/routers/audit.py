from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
import json

from app.database import get_db
from app.models import AuditLog, Transaction

router = APIRouter(prefix="/api/audit-logs", tags=["Audit Logs"])

@router.get("")
def get_audit_logs(
    search: Optional[str] = None,
    action_type: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(AuditLog)

    if action_type:
        query = query.filter(AuditLog.action_taken == action_type.upper())

    logs = query.order_by(AuditLog.id.desc()).all()

    results = []
    for l in logs:
        tx = db.query(Transaction).filter(Transaction.id == l.transaction_id).first()
        
        # Filter by search string if provided
        if search:
            s = search.lower()
            pay_id = (tx.payment_id.lower() if tx else "")
            c_name = (tx.customer_name.lower() if tx else "")
            if s not in pay_id and s not in c_name and s not in l.decision.lower() and s not in l.reason.lower():
                continue

        results.append({
            "id": l.id,
            "transaction_id": l.transaction_id,
            "payment_id": tx.payment_id if tx else "N/A",
            "customer_name": tx.customer_name if tx else "N/A",
            "amount": tx.amount if tx else 0.0,
            "decision": l.decision,
            "reason": l.reason,
            "action_taken": l.action_taken,
            "execution_result": l.execution_result,
            "stopping_rules_applied": json.loads(l.stopping_rules_applied) if l.stopping_rules_applied else {},
            "created_at": l.created_at.isoformat()
        })

    total = len(results)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated = results[start_idx:end_idx]

    return {
        "items": paginated,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit if total > 0 else 1
    }
