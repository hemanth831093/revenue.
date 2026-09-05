from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Transaction, RiskScore
from app.services.ai_agent import ai_agent
from app.services.audit import log_audit_event
import json

router = APIRouter(prefix="/api/ai", tags=["AI Agent"])

@router.post("/analyze/{transaction_id}")
def analyze_transaction(transaction_id: int, db: Session = Depends(get_db)):
    tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Run AI Analysis (Risk Engine + Diagnosis + Safety Check + Expected Value)
    analysis = ai_agent.analyze_transaction(tx)

    # 1. Persist or update RiskScore record
    existing_risk = db.query(RiskScore).filter(RiskScore.transaction_id == transaction_id).first()
    if existing_risk:
        existing_risk.recovery_probability = analysis["recovery_probability"]
        existing_risk.priority = analysis["priority"]
        existing_risk.risk_factors = json.dumps(analysis.get("risk_factors", []))
        existing_risk.risk_score = analysis.get("risk_score")
        existing_risk.diagnosis = analysis.get("diagnosis")
    else:
        new_risk = RiskScore(
            transaction_id=tx.id,
            recovery_probability=analysis["recovery_probability"],
            priority=analysis["priority"],
            risk_factors=json.dumps(analysis.get("risk_factors", [])),
            model_version="v1.0.0-rf",
            risk_score=analysis.get("risk_score"),
            diagnosis=analysis.get("diagnosis")
        )
        db.add(new_risk)

    # 2. Create unalterable AuditLog entry for this AI diagnosis & recommendation
    log_audit_event(
        db=db,
        transaction_id=tx.id,
        decision=f"DIAGNOSIS_{analysis['recommended_action']}",
        reason=analysis["explanation"],
        action_taken=analysis["recommended_action"],
        execution_result="RECOMMENDED",
        stopping_rules_applied=json.dumps({"safety_override": analysis["safety_override"]})
    )

    db.commit()

    return analysis
