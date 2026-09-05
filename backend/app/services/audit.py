import json
from datetime import datetime, timezone
from typing import Any
from sqlalchemy.orm import Session
from app.models import AuditLog

def log_audit_event(
    db: Session,
    transaction_id: int,
    decision: str,
    reason: str,
    action_taken: str,
    execution_result: str,
    stopping_rules_applied: Any
) -> AuditLog:
    """Writes an unalterable audit log entry into the database."""
    if isinstance(stopping_rules_applied, (dict, list)):
        rules_json = json.dumps(stopping_rules_applied)
    elif isinstance(stopping_rules_applied, str):
        rules_json = stopping_rules_applied
    else:
        rules_json = json.dumps({})

    audit_entry = AuditLog(
        transaction_id=transaction_id,
        decision=decision,
        reason=reason,
        action_taken=action_taken,
        execution_result=execution_result,
        stopping_rules_applied=rules_json,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db.add(audit_entry)
    db.commit()
    db.refresh(audit_entry)
    return audit_entry
