# RecoverAI --- Implementation Plan

## Phase 1 --- Project Setup

1.  Create React + TypeScript frontend.
2.  Create FastAPI backend.
3.  Configure Supabase/PostgreSQL.
4.  Add environment variables.
5.  Create Git repository.

## Phase 2 --- Database

Create: - transactions - risk_scores - recovery_actions - audit_logs

Seed the database with 100--500 synthetic transactions.

## Phase 3 --- Backend APIs

Implement: - Transaction listing - Transaction details - Dashboard
metrics - Batch import - Recovery history - Audit logs

## Phase 4 --- Risk Engine

Start with a simple explainable scoring model.

Example features: - Amount - Failure type - Previous success count -
Previous failure count - Retry count

Train/test a lightweight classifier if time permits. Otherwise use a
transparent scoring model for the MVP and clearly label it as a
baseline.

## Phase 5 --- AI Agent

Implement this pipeline:

``` text
Transaction
   ↓
Risk Score
   ↓
Diagnosis
   ↓
Expected Recovery Value
   ↓
Action Selection
   ↓
Safety Check
   ↓
Recovery Execution
   ↓
Audit Log
```

## Phase 6 --- Recovery Simulator / Razorpay Test Mode

Implement safe demo actions: - Retry simulation - Recovery payment-link
simulation - Merchant escalation

Use Razorpay test/sandbox APIs where appropriate. Never expose secret
keys in frontend code.

## Phase 7 --- Frontend

Build: 1. Dashboard 2. Transactions 3. Transaction Details 4. AI
Recovery 5. Analytics 6. Audit Logs

## Phase 8 --- Metrics

Run a fixed batch and report: - Revenue at risk - Attempts - Successful
recoveries - Recovered revenue - Recovery rate - Exception/escalation
count

## Phase 9 --- Testing

Test: - Successful payment - Temporary failure - Repeated failure -
Low-value transaction - High-value transaction - Recovery action
failure - Duplicate recovery request

## Phase 10 --- Demo Preparation

Prepare one clear story:

``` text
Failed payment
→ AI detects risk
→ AI explains reason
→ Agent chooses action
→ Action succeeds
→ ₹ recovered
→ Audit trail updated
```

## Tomorrow Submission Priority

P0: Working end-to-end recovery flow P0: Dashboard metrics P0: AI
decision + explanation P0: Audit trail P1: ML model P1: Analytics P2:
Extra recovery channels
