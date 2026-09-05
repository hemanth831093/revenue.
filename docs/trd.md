# RecoverAI --- Technical Requirements Document

## 1. Architecture

RecoverAI uses a React frontend, FastAPI backend, PostgreSQL/Supabase
database, ML risk scoring, and an LLM-powered decision/explanation
layer.

``` text
React Dashboard
      |
      v
FastAPI Backend
      |
      +--> Transaction Service
      +--> Risk Scoring Service
      +--> AI Diagnosis/Decision Service
      +--> Recovery Action Service
      +--> Audit Service
      |
      v
Supabase PostgreSQL
```

## 2. Functional Requirements

### FR-01 Transaction ingestion

The system shall accept synthetic/test payment records.

### FR-02 Risk scoring

The system shall calculate recovery probability and priority.

### FR-03 Diagnosis

The system shall classify a failed payment into a reason category.

### FR-04 Agent decision

The system shall select a bounded recovery action.

### FR-05 Execution

The system shall execute a test/simulated action and store the result.

### FR-06 Metrics

The system shall calculate revenue at risk, recovered revenue, and
recovery rate.

### FR-07 Audit

The system shall store every AI decision and recovery result.

## 3. Non-Functional Requirements

-   API response target: under 2 seconds for normal dashboard requests.
-   Reliable validation of transaction input.
-   No API secrets in frontend source code.
-   Authentication and authorization for production deployment.
-   Idempotent recovery actions.
-   Clear error messages.
-   Logs for failed backend/AI operations.

## 4. AI Requirements

Input features may include: - Payment amount - Payment method - Failure
category - Previous successful payments - Previous failures - Number of
retries - Customer/transaction history - Time since failure

Output:

``` json
{
  "recovery_probability": 0.87,
  "priority": "HIGH",
  "diagnosis": "temporary_bank_failure",
  "recommended_action": "RETRY",
  "reason": "Previous payments succeeded and the current failure appears temporary."
}
```

## 5. Database

### transactions

id, payment_id, amount, payment_method, status, failure_reason,
customer_id, created_at

### risk_scores

id, transaction_id, recovery_probability, priority, model_version,
created_at

### recovery_actions

id, transaction_id, action, status, amount_recovered, executed_at

### audit_logs

id, transaction_id, decision, reason, result, created_at

## 6. API Endpoints

-   `GET /api/dashboard`
-   `GET /api/transactions`
-   `GET /api/transactions/{id}`
-   `POST /api/transactions/import`
-   `POST /api/ai/analyze/{id}`
-   `POST /api/recovery/execute/{id}`
-   `GET /api/recovery/history`
-   `GET /api/audit-logs`

## 7. Error Handling

If an action fails, the system records the failure, does not endlessly
retry, and escalates according to stopping rules.
