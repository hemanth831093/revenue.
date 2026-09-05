from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Transaction, RecoveryAction, AuditLog
from app.services.risk_engine import risk_engine

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    total_txs = db.query(Transaction).all()
    
    total_count = len(total_txs)
    failed_count = sum(1 for t in total_txs if t.status == "FAILED")
    recovered_count = sum(1 for t in total_txs if t.status == "RECOVERED")
    escalated_count = sum(1 for t in total_txs if t.status == "ESCALATED")

    revenue_at_risk = sum(t.amount for t in total_txs if t.status == "FAILED")
    recovered_revenue = sum(t.amount for t in total_txs if t.status == "RECOVERED")
    
    total_attempted_revenue = revenue_at_risk + recovered_revenue
    recovery_rate = round((recovered_revenue / total_attempted_revenue * 100), 1) if total_attempted_revenue > 0 else 0.0

    # Calculate high priority count using RiskEngine
    high_priority_count = 0
    for t in total_txs:
        if t.status == "FAILED":
            prob, priority, _ = risk_engine.calculate_risk(t)
            if priority == "HIGH":
                high_priority_count += 1

    # Recent Audit & Recovery Actions
    recent_audits = db.query(AuditLog).order_by(AuditLog.id.desc()).limit(8).all()
    recent_actions_feed = []
    for a in recent_audits:
        tx = db.query(Transaction).filter(Transaction.id == a.transaction_id).first()
        recent_actions_feed.append({
            "id": a.id,
            "transaction_id": a.transaction_id,
            "payment_id": tx.payment_id if tx else "N/A",
            "customer_name": tx.customer_name if tx else "Customer",
            "amount": tx.amount if tx else 0.0,
            "action_taken": a.action_taken,
            "execution_result": a.execution_result,
            "created_at": a.created_at.isoformat()
        })

    # Failure Reason Distribution Chart Data
    reason_counts = {}
    for t in total_txs:
        r = t.failure_reason
        reason_counts[r] = reason_counts.get(r, 0) + 1

    chart_reason_data = [
        {"reason": reason.replace("_", " ").title(), "count": count}
        for reason, count in reason_counts.items()
    ]

    # Revenue Chart Data
    chart_revenue_data = [
        {"category": "Revenue at Risk", "amount": round(revenue_at_risk, 2)},
        {"category": "Recovered Revenue", "amount": round(recovered_revenue, 2)}
    ]

    return {
        "total_revenue_at_risk": round(revenue_at_risk, 2),
        "total_revenue_recovered": round(recovered_revenue, 2),
        "failed_payments_count": failed_count,
        "recovered_payments_count": recovered_count,
        "escalated_payments_count": escalated_count,
        "recovery_rate": recovery_rate,
        "high_priority_count": high_priority_count,
        "recent_actions": recent_actions_feed,
        "chart_revenue_data": chart_revenue_data,
        "chart_reason_data": chart_reason_data
    }
