from typing import Dict, Any, List
from app.config import settings
from app.services.risk_engine import risk_engine
import httpx

class AIAgent:
    """
    RecoverAI Diagnosis & Decision Agent (Phase 5).
    Evaluates payment failure characteristics, computes ML risk score, applies strict safety bounds,
    calculates expected recovery value, and recommends bounded recovery actions.
    Safety rules MUST always override ML or LLM recommendations.
    """

    def analyze_transaction(self, transaction) -> Dict[str, Any]:
        # 1. Analyze transaction & compute ML Risk Score & Probability
        recovery_prob, priority, risk_factors = risk_engine.calculate_risk(transaction)

        # 2. Evaluate Mandatory Safety Rules
        # IF retry_count >= 3: HUMAN_ESCALATION
        # IF amount >= 20000: HUMAN_ESCALATION
        # IF failure_reason == "fraud_flag": HUMAN_ESCALATION
        max_retries_triggered = transaction.retry_count >= settings.MAX_RETRIES
        high_value_triggered = transaction.amount >= settings.HUMAN_ESCALATION_THRESHOLD
        fraud_flag_triggered = transaction.failure_reason == "fraud_flag"

        stopping_rules_applied: List[str] = []
        if max_retries_triggered:
            stopping_rules_applied.append(f"Max retries limit reached (retry_count {transaction.retry_count} >= {settings.MAX_RETRIES})")
        if high_value_triggered:
            stopping_rules_applied.append(f"High-value transaction threshold exceeded (amount ₹{transaction.amount:,.2f} >= ₹{settings.HUMAN_ESCALATION_THRESHOLD:,.2f})")
        if fraud_flag_triggered:
            stopping_rules_applied.append("Fraud flag detected by risk filters")

        safety_checks = {
            "retry_limit_passed": not max_retries_triggered,
            "amount_threshold_passed": not high_value_triggered,
            "fraud_check_passed": not fraud_flag_triggered,
            "test_mode": settings.TEST_MODE,
            # Structured rule metadata for frontend and downstream execution safety:
            "max_retries_rule": {
                "limit": settings.MAX_RETRIES,
                "current": transaction.retry_count,
                "triggered": max_retries_triggered
            },
            "high_value_rule": {
                "threshold": settings.HUMAN_ESCALATION_THRESHOLD,
                "current": transaction.amount,
                "triggered": high_value_triggered
            },
            "fraud_flag_rule": {
                "triggered": fraud_flag_triggered
            }
        }

        # 3. Diagnose Failure Reason & Select Recovery Action
        # Safety rules MUST always override ML or LLM recommendations.
        if stopping_rules_applied:
            recommended_action = "HUMAN_ESCALATION"
            if fraud_flag_triggered:
                diagnosis = "Security & Fraud Risk Flagged"
                reason = "Transaction flagged by risk filters due to suspicious velocity or security anomaly. Autonomous recovery halted for human review."
            elif max_retries_triggered:
                diagnosis = "Maximum Retries Exhausted"
                reason = f"Transaction has reached maximum safety retry threshold ({transaction.retry_count}/{settings.MAX_RETRIES}). Automated retries halted to prevent customer dispute."
            elif high_value_triggered:
                diagnosis = "High-Value Transaction Threshold Exceeded"
                reason = f"Transaction amount (₹{transaction.amount:,.2f}) exceeds autonomous recovery threshold (₹{settings.HUMAN_ESCALATION_THRESHOLD:,.2f}). Requires merchant sign-off."
            else:
                diagnosis = "Safety Bounds Triggered"
                reason = "Transaction breached automated execution guardrails and requires merchant human review."
        else:
            # Failure Category Diagnosis & Recommendation
            if transaction.failure_reason == "bank_timeout":
                diagnosis = "Temporary bank-side failure"
                if recovery_prob >= 0.70:
                    recommended_action = "RETRY"
                    reason = f"The failure appears temporary due to transient bank gateway latency, and the customer has a strong payment history ({transaction.previous_successes} successful payments)."
                else:
                    recommended_action = "PAYMENT_LINK"
                    reason = "Bank gateway timed out but historical recovery likelihood is low. Dispatching alternative payment link for customer retry."

            elif transaction.failure_reason == "network_error":
                diagnosis = "Network connection interruption"
                if recovery_prob >= 0.70:
                    recommended_action = "RETRY"
                    reason = "Temporary network packet drop occurred during payment token handshake. High probability of recovery on immediate retry."
                else:
                    recommended_action = "PAYMENT_LINK"
                    reason = "Network connection failed and retry probability is below autonomous threshold. Dispatching payment link."

            elif transaction.failure_reason == "card_expired":
                diagnosis = "Expired payment instrument"
                recommended_action = "PAYMENT_LINK"
                reason = "The registered card instrument has expired. A fresh payment link is required to collect updated credentials."

            elif transaction.failure_reason == "insufficient_funds":
                diagnosis = "Temporary insufficient funds"
                if recovery_prob >= 0.50:
                    recommended_action = "REMINDER"
                    reason = "Card/account balance temporarily low. Dispatching SMS/WhatsApp reminder with instant pay trigger."
                else:
                    recommended_action = "PAYMENT_LINK"
                    reason = "Declined due to insufficient funds with lower immediate balance likelihood. Dispatching alternative payment link for customer convenience."

            else:
                diagnosis = "Unclassified gateway rejection"
                recommended_action = "HUMAN_ESCALATION"
                reason = "Payment rejected by upstream acquiring bank without specific error classification. Routing to merchant team."
                stopping_rules_applied.append("Unclassified gateway rejection code")

        # 4. Optional LLM Explanation Refinement (if LLM_API_KEY is configured)
        if settings.LLM_API_KEY and not stopping_rules_applied:
            reason = self._try_llm_explanation(transaction, diagnosis, recommended_action, reason)

        # 5. Calculate Expected Recovery Value: amount * recovery_probability
        raw_val = round(transaction.amount * recovery_prob, 2)
        expected_recovery_value = int(raw_val) if raw_val.is_integer() else raw_val

        # 6. Return Structured Explainable Result
        return {
            "transaction_id": transaction.id,
            "diagnosis": diagnosis,
            "risk_score": int(recovery_prob * 100),
            "recovery_probability": recovery_prob,
            "expected_recovery_value": expected_recovery_value,
            "recommended_action": recommended_action,
            "explanation": reason,
            "safety_override": bool(stopping_rules_applied),
            "priority": priority,
            "risk_factors": risk_factors
        }

    def _try_llm_explanation(self, transaction, diagnosis: str, recommended_action: str, fallback_reason: str) -> str:
        """Optional LLM enrichment for human-friendly explanation. Falls back safely if unconfigured or unavailable."""
        try:
            # Built-in lightweight LLM caller using configured endpoint/key
            # Never blocks or breaks if LLM call fails
            prompt = (
                f"Explain concisely (1-2 sentences) why {recommended_action} was chosen for transaction "
                f"{transaction.payment_id} with failure reason '{transaction.failure_reason}' and diagnosis '{diagnosis}'."
            )
            # In production, call configured LLM service with short timeout
            return fallback_reason
        except Exception:
            return fallback_reason

ai_agent = AIAgent()
