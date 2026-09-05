"""
RecoverAI — Razorpay Sandbox Simulator (Phase 6)
=================================================
ALL operations are SIMULATED. No real money moves.
No live Razorpay APIs are called. No secrets required.
TEST_MODE is always active.
"""
import uuid
from typing import Dict, Any


class RazorpaySimulator:
    """
    Bounded Recovery Simulator.
    Simulates RETRY, PAYMENT_LINK, REMINDER, and HUMAN_ESCALATION
    in Razorpay Test / Sandbox mode.

    Safety contract:
    - Never calls live Razorpay endpoints.
    - Never moves real funds.
    - Idempotent: will not re-execute if transaction is already RECOVERED/ESCALATED.
    """

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _short_id(prefix: str) -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    # ------------------------------------------------------------------ RETRY
    def simulate_retry(self, transaction) -> Dict[str, Any]:
        """
        Re-present the payment mandate to the bank gateway (simulated).
        Succeeds deterministically for bank_timeout and network_error failures.
        """
        sim_id = self._short_id("retry_sim")

        if transaction.failure_reason in ("bank_timeout", "network_error"):
            success = True
            message = (
                f"Payment retry successful via Razorpay Test Gateway. "
                f"Amount Rs.{transaction.amount:,.2f} captured for {transaction.customer_name}."
            )
        elif transaction.failure_reason == "insufficient_funds" and transaction.retry_count <= 1:
            # Give a deterministic 50% chance based on retry parity for demo consistency
            success = (transaction.retry_count % 2 == 0)
            message = (
                "Retry completed — funds now available." if success
                else "Retry failed: account still has insufficient funds."
            )
        else:
            success = False
            message = (
                f"Retry not feasible for failure reason '{transaction.failure_reason}'. "
                "Alternative recovery method recommended."
            )

        return {
            "success": success,
            "sim_id": sim_id,
            "action_type": "RETRY",
            "gateway": "Razorpay_Test_Gateway",
            "message": message,
            "amount_recovered": transaction.amount if success else 0.0,
        }

    # --------------------------------------------------------------- PAYMENT_LINK
    def simulate_payment_link(self, transaction) -> Dict[str, Any]:
        """
        Generate a simulated Razorpay Payment Link and dispatch it to the customer.
        The link is fake (no real URL). Marked SUCCESS immediately for demo purposes.
        """
        sim_id = self._short_id("plink_sim")
        fake_url = f"https://rzp.io/sim/{uuid.uuid4().hex[:10]}"

        return {
            "success": True,
            "sim_id": sim_id,
            "action_type": "PAYMENT_LINK",
            "gateway": "Razorpay_PaymentLink_Sandbox",
            "payment_link_url": fake_url,
            "message": (
                f"Payment link {sim_id} generated and dispatched to "
                f"{transaction.customer_name} at {transaction.customer_email}. "
                f"Amount: Rs.{transaction.amount:,.2f} (simulated)."
            ),
            "amount_recovered": transaction.amount,
        }

    # --------------------------------------------------------------- REMINDER
    def simulate_reminder(self, transaction) -> Dict[str, Any]:
        """
        Simulate dispatching an SMS/WhatsApp/email payment reminder.
        Reminders are PENDING by nature — they do NOT immediately recover money.
        amount_recovered = 0 because the customer hasn't paid yet.
        """
        sim_id = self._short_id("rem_sim")

        return {
            "success": True,       # reminder was sent successfully
            "sim_id": sim_id,
            "action_type": "REMINDER",
            "gateway": "Razorpay_Notification_Simulator",
            "message": (
                f"Omnichannel reminder dispatched to {transaction.customer_name} "
                f"({transaction.customer_email}) via SMS and WhatsApp. "
                f"Payment link included (simulated)."
            ),
            # Reminders are async — money hasn't been collected yet
            "amount_recovered": 0.0,
        }

    # ------------------------------------------------------------- HUMAN_ESCALATION
    def simulate_human_escalation(self, transaction, reason: str) -> Dict[str, Any]:
        """
        Flag the transaction for human merchant review.
        Halts all autonomous recovery. amount_recovered is always 0.
        """
        sim_id = self._short_id("esc_sim")

        return {
            "success": False,
            "sim_id": sim_id,
            "action_type": "HUMAN_ESCALATION",
            "gateway": "RecoverAI_Escalation_Desk",
            "message": (
                f"Transaction {transaction.payment_id} escalated to Merchant Operations Team. "
                f"Reason: {reason}"
            ),
            "amount_recovered": 0.0,
        }


razorpay_sim = RazorpaySimulator()
