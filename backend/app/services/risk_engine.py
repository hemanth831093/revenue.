import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from typing import Dict, Any, List, Tuple

class RiskEngine:
    def __init__(self):
        self.model = None
        self._train_baseline_model()

    def _train_baseline_model(self):
        """Train a lightweight explainable Scikit-Learn RandomForest classifier on synthetic payment feature patterns."""
        np.random.seed(42)
        n_samples = 1000

        # Features: amount, prev_succ, prev_fail, retry_ct, reason_code (0-4), method_code (0-3)
        amounts = np.random.uniform(200, 30000, n_samples)
        prev_succ = np.random.randint(0, 8, n_samples)
        prev_fail = np.random.randint(0, 5, n_samples)
        retry_ct = np.random.randint(0, 4, n_samples)
        reason_codes = np.random.choice([0, 1, 2, 3, 4], n_samples) # 0:bank_timeout, 1:insufficient_funds, 2:card_expired, 3:network_error, 4:fraud_flag
        method_codes = np.random.choice([0, 1, 2, 3], n_samples) # 0:UPI, 1:Credit Card, 2:Debit Card, 3:Netbanking

        # Synthetic recovery likelihood probability calculation formula
        prob = (
            0.40
            + (prev_succ * 0.08)
            - (prev_fail * 0.12)
            - (retry_ct * 0.15)
            + np.where(reason_codes == 0, 0.30, 0) # bank_timeout -> high recovery
            + np.where(reason_codes == 3, 0.25, 0) # network_error -> high recovery
            - np.where(reason_codes == 1, 0.15, 0) # insufficient_funds -> medium
            - np.where(reason_codes == 2, 0.20, 0) # card_expired -> lower retry
            - np.where(reason_codes == 4, 0.80, 0) # fraud_flag -> 0 recovery
            + np.where(method_codes == 0, 0.10, 0) # UPI recovers faster
        )
        prob = np.clip(prob, 0.05, 0.95)
        labels = (prob >= 0.50).astype(int)

        X = pd.DataFrame({
            "amount": amounts,
            "prev_succ": prev_succ,
            "prev_fail": prev_fail,
            "retry_ct": retry_ct,
            "reason_code": reason_codes,
            "method_code": method_codes
        })

        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.model.fit(X, labels)

    def calculate_risk(self, transaction) -> Tuple[float, str, List[str]]:
        """
        Calculates recovery probability (0.00 to 1.00), priority tag (HIGH, MEDIUM, LOW),
        and human-readable explainable risk factors.
        """
        reason_map = {
            "bank_timeout": 0,
            "insufficient_funds": 1,
            "card_expired": 2,
            "network_error": 3,
            "fraud_flag": 4
        }
        method_map = {
            "UPI": 0,
            "Credit Card": 1,
            "Debit Card": 2,
            "Netbanking": 3
        }

        reason_code = reason_map.get(transaction.failure_reason, 0)
        method_code = method_map.get(transaction.payment_method, 0)

        feature_df = pd.DataFrame([{
            "amount": transaction.amount,
            "prev_succ": transaction.previous_successes,
            "prev_fail": transaction.previous_failures,
            "retry_ct": transaction.retry_count,
            "reason_code": reason_code,
            "method_code": method_code
        }])

        # Predict probability of recovery using ML model
        raw_prob = float(self.model.predict_proba(feature_df)[0][1])

        # Adjust for deterministic edge-cases to guarantee exact transparent outcomes for demo
        if transaction.failure_reason == "fraud_flag":
            raw_prob = 0.02
        elif transaction.failure_reason == "bank_timeout" and transaction.previous_successes >= 2 and transaction.retry_count == 0:
            raw_prob = max(raw_prob, 0.87)
        elif transaction.failure_reason == "network_error" and transaction.previous_successes >= 1 and transaction.retry_count == 0:
            raw_prob = max(raw_prob, 0.85)

        prob = round(raw_prob, 2)

        # Priority tag
        if prob >= 0.70:
            priority = "HIGH"
        elif prob >= 0.40:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        # Formulate explainable risk factors
        risk_factors = []
        if transaction.previous_successes >= 3:
            risk_factors.append(f"Strong customer track record ({transaction.previous_successes} past successful payments).")
        elif transaction.previous_successes == 0:
            risk_factors.append("First-time customer transaction with no previous payment history.")

        if transaction.failure_reason == "bank_timeout":
            risk_factors.append("Failure diagnosed as transient bank gateway timeout (High retry success rate).")
        elif transaction.failure_reason == "network_error":
            risk_factors.append("Failure caused by temporary network connectivity glitch.")
        elif transaction.failure_reason == "card_expired":
            risk_factors.append("Card instrument expired; requires fresh payment link dispatch.")
        elif transaction.failure_reason == "insufficient_funds":
            risk_factors.append("Declined due to insufficient account balance; SMS/WhatsApp reminder recommended.")
        elif transaction.failure_reason == "fraud_flag":
            risk_factors.append("Flagged by risk filters for suspicious velocity; zero autonomous retries allowed.")

        if transaction.retry_count >= 3:
            risk_factors.append(f"Maximum retry attempts reached ({transaction.retry_count}/3 retries).")
        
        if transaction.amount >= 20000.0:
            risk_factors.append(f"High transaction value (₹{transaction.amount:,.2f} >= ₹20,000 threshold).")

        return prob, priority, risk_factors

risk_engine = RiskEngine()
