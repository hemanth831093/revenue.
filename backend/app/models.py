from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(String(64), unique=True, index=True, nullable=False)
    customer_id = Column(String(64), index=True, nullable=False)
    customer_name = Column(String(128), nullable=False)
    customer_email = Column(String(128), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(32), nullable=False) # UPI, Credit Card, Debit Card, Netbanking
    status = Column(String(32), default="FAILED", index=True) # FAILED, RECOVERED, IN_PROGRESS, ESCALATED
    failure_reason = Column(String(64), nullable=False) # bank_timeout, insufficient_funds, card_expired, network_error, fraud_flag
    failure_code = Column(String(32), nullable=True)
    previous_successes = Column(Integer, default=0)
    previous_failures = Column(Integer, default=0)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    risk_scores = relationship("RiskScore", back_populates="transaction", cascade="all, delete-orphan")
    recovery_actions = relationship("RecoveryAction", back_populates="transaction", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="transaction", cascade="all, delete-orphan")

class RiskScore(Base):
    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    recovery_probability = Column(Float, nullable=False)
    priority = Column(String(16), nullable=False) # HIGH, MEDIUM, LOW
    risk_factors = Column(Text, nullable=True) # JSON string
    model_version = Column(String(32), default="v1.0.0-rf")
    risk_score = Column(Float, nullable=True)
    diagnosis = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    transaction = relationship("Transaction", back_populates="risk_scores")

class RecoveryAction(Base):
    __tablename__ = "recovery_actions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    action_type = Column(String(32), nullable=False) # RETRY, PAYMENT_LINK, REMINDER, HUMAN_ESCALATION
    status = Column(String(32), default="PENDING") # PENDING, SUCCESS, FAILED, ESCALATED
    attempt_number = Column(Integer, default=1)
    amount_recovered = Column(Float, default=0.0)
    razorpay_sim_id = Column(String(64), nullable=True)
    executed_at = Column(DateTime, default=datetime.utcnow)
    response_metadata = Column(Text, nullable=True) # JSON string

    transaction = relationship("Transaction", back_populates="recovery_actions")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    decision = Column(String(64), nullable=False)
    reason = Column(Text, nullable=False)
    action_taken = Column(String(32), nullable=False)
    execution_result = Column(String(32), nullable=False)
    stopping_rules_applied = Column(Text, nullable=True) # JSON string of rules evaluated
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    transaction = relationship("Transaction", back_populates="audit_logs")
