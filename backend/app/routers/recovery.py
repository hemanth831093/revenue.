"""
RecoverAI — Recovery Execution Router (Phase 6)
================================================
POST /api/recovery/execute/{transaction_id}
POST /api/recovery/batch-execute
GET  /api/recovery/history

All executions are fully simulated (TEST_MODE).
Safety rules always override any caller-supplied action.
Idempotency: already-RECOVERED or already-ESCALATED transactions
are not re-processed — returns the cached outcome instead.
"""
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timezone
import json

from app.database import get_db
from app.models import Transaction, RecoveryAction
from app.services.ai_agent import ai_agent
from app.services.razorpay_sim import razorpay_sim
from app.services.audit import log_audit_event

router = APIRouter(prefix="/api/recovery", tags=["Recovery Actions"])


def _utcnow():
    """Timezone-naive UTC datetime (SQLite compatible)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _execute_recovery(tx: Transaction, action_type: Optional[str], db: Session) -> dict:
    """
    Core recovery execution logic — shared by single and batch endpoints.

    Idempotency contract:
    - RECOVERED transactions: return cached outcome without re-running.
    - ESCALATED transactions: return cached outcome without re-running.
    - IN_PROGRESS / FAILED: proceed with execution.
    """
    # ── IDEMPOTENCY GUARD ────────────────────────────────────────────────────
    if tx.status == "RECOVERED":
        last_action = (
            db.query(RecoveryAction)
            .filter(RecoveryAction.transaction_id == tx.id, RecoveryAction.status == "SUCCESS")
            .order_by(RecoveryAction.id.desc())
            .first()
        )
        return {
            "transaction_id": tx.id,
            "action": last_action.action_type if last_action else "RETRY",
            "status": "ALREADY_RECOVERED",
            "success": True,
            "message": f"Transaction {tx.payment_id} is already RECOVERED. No duplicate execution performed.",
            "action_id": last_action.id if last_action else 0,
            "action_type": last_action.action_type if last_action else "RETRY",
            "simulated_gateway_id": last_action.razorpay_sim_id if last_action else "N/A",
            "amount_recovered": last_action.amount_recovered if last_action else tx.amount,
            "new_status": "RECOVERED",
            "audit_log_id": 0,
        }

    if tx.status == "ESCALATED":
        return {
            "transaction_id": tx.id,
            "action": "HUMAN_ESCALATION",
            "status": "ALREADY_ESCALATED",
            "success": False,
            "message": f"Transaction {tx.payment_id} is already ESCALATED. Awaiting human review.",
            "action_id": 0,
            "action_type": "HUMAN_ESCALATION",
            "simulated_gateway_id": "N/A",
            "amount_recovered": 0.0,
            "new_status": "ESCALATED",
            "audit_log_id": 0,
        }

    # ── AI ANALYSIS + SAFETY CHECK ───────────────────────────────────────────
    analysis = ai_agent.analyze_transaction(tx)
    target_action = action_type or analysis["recommended_action"]

    # Safety rules ALWAYS override caller-supplied action
    safety_checks = analysis.get("safety_checks", {})
    max_retries_triggered = (
        safety_checks.get("retry_limit_passed") is False
        or safety_checks.get("max_retries_rule", {}).get("triggered", False)
    )
    high_value_triggered = (
        safety_checks.get("amount_threshold_passed") is False
        or safety_checks.get("high_value_rule", {}).get("triggered", False)
    )
    fraud_flag_triggered = (
        safety_checks.get("fraud_check_passed") is False
        or safety_checks.get("fraud_flag_rule", {}).get("triggered", False)
    )
    
    safety_override = False
    if target_action != "HUMAN_ESCALATION" and (max_retries_triggered or high_value_triggered or fraud_flag_triggered):
        target_action = "HUMAN_ESCALATION"
        safety_override = True

    explanation = (
        analysis.get("reason")
        or analysis.get("diagnosis_explanation")
        or "Autonomous AI recovery decision"
    )

    # ── SIMULATOR EXECUTION ──────────────────────────────────────────────────
    if target_action == "RETRY":
        tx.retry_count += 1
        sim_result = razorpay_sim.simulate_retry(tx)
    elif target_action == "PAYMENT_LINK":
        sim_result = razorpay_sim.simulate_payment_link(tx)
    elif target_action == "REMINDER":
        sim_result = razorpay_sim.simulate_reminder(tx)
    else:
        target_action = "HUMAN_ESCALATION"
        sim_result = razorpay_sim.simulate_human_escalation(tx, explanation)

    # ── TRANSACTION STATUS UPDATE ────────────────────────────────────────────
    if sim_result["success"] and target_action in ("RETRY", "PAYMENT_LINK"):
        # RETRY and PAYMENT_LINK that succeed → RECOVERED
        tx.status = "RECOVERED"
        rec_status = "SUCCESS"
        new_status = "RECOVERED"
        amount_rec = sim_result["amount_recovered"]
    elif target_action == "REMINDER" and sim_result["success"]:
        # Reminder sent — transaction stays FAILED (async, customer hasn't paid yet)
        rec_status = "PENDING"
        new_status = tx.status          # unchanged
        amount_rec = 0.0
    elif target_action == "HUMAN_ESCALATION":
        tx.status = "ESCALATED"
        rec_status = "ESCALATED"
        new_status = "ESCALATED"
        amount_rec = 0.0
    else:
        rec_status = "FAILED"
        new_status = tx.status          # unchanged
        amount_rec = 0.0

    # ── PERSIST RECOVERY ACTION ──────────────────────────────────────────────
    rec_action = RecoveryAction(
        transaction_id=tx.id,
        action_type=target_action,
        status=rec_status,
        attempt_number=tx.retry_count if target_action == "RETRY" else 1,
        amount_recovered=amount_rec,
        razorpay_sim_id=sim_result["sim_id"],
        executed_at=_utcnow(),
        response_metadata=json.dumps(sim_result),
    )
    db.add(rec_action)
    db.flush()

    # ── AUDIT LOG ────────────────────────────────────────────────────────────
    audit_entry = log_audit_event(
        db=db,
        transaction_id=tx.id,
        decision=f"EXECUTE_{target_action}",
        reason=explanation,
        action_taken=target_action,
        execution_result=rec_status,
        stopping_rules_applied=safety_checks,
    )

    db.commit()

    return {
        # Spec-aligned fields
        "transaction_id": tx.id,
        "action": target_action,
        "status": rec_status,
        "attempt_number": tx.retry_count if target_action == "RETRY" else 1,
        "amount_recovered": amount_rec,
        "message": sim_result["message"],
        "safety_override": safety_override,
        "simulation_id": sim_result["sim_id"],
        # Extended fields for frontend
        "success": sim_result["success"],
        "action_id": rec_action.id,
        "action_type": target_action,
        "simulated_gateway_id": sim_result["sim_id"],
        "new_status": new_status,
        "audit_log_id": audit_entry.id,
    }


# ── ENDPOINTS ────────────────────────────────────────────────────────────────

@router.post("/execute/{transaction_id}")
def execute_recovery_action(
    transaction_id: int,
    action_type: Optional[str] = Body(None, embed=True),
    db: Session = Depends(get_db),
):
    """
    Execute a bounded, simulated recovery action for a single transaction.
    Safety rules always override the caller-supplied action_type.
    Idempotent: re-executing on an already-RECOVERED transaction is a no-op.
    """
    tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return _execute_recovery(tx, action_type, db)


@router.post("/batch-execute")
def batch_execute_recovery(
    transaction_ids: List[int] = Body(...),
    db: Session = Depends(get_db),
):
    """
    Execute recovery actions for multiple transactions in one call.
    Safety rules are enforced individually for each transaction.
    Batch NEVER bypasses safety rules.
    """
    results = []
    for tid in transaction_ids:
        try:
            tx = db.query(Transaction).filter(Transaction.id == tid).first()
            if not tx:
                results.append({
                    "transaction_id": tid,
                    "success": False,
                    "message": f"Transaction {tid} not found",
                })
                continue
            res = _execute_recovery(tx, action_type=None, db=db)
            results.append(res)
        except Exception as exc:
            results.append({
                "transaction_id": tid,
                "success": False,
                "message": str(exc),
            })

    return {"processed_count": len(results), "results": results}


@router.get("/history")
def recovery_history(db: Session = Depends(get_db)):
    """Return the last 50 recovery action records."""
    actions = (
        db.query(RecoveryAction)
        .order_by(RecoveryAction.id.desc())
        .limit(50)
        .all()
    )
    history = []
    for a in actions:
        tx = db.query(Transaction).filter(Transaction.id == a.transaction_id).first()
        history.append({
            "id": a.id,
            "transaction_id": a.transaction_id,
            "payment_id": tx.payment_id if tx else "N/A",
            "customer_name": tx.customer_name if tx else "Customer",
            "action_type": a.action_type,
            "status": a.status,
            "amount_recovered": a.amount_recovered,
            "razorpay_sim_id": a.razorpay_sim_id,
            "executed_at": a.executed_at.isoformat(),
        })
    return history
