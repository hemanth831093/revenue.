# RecoverAI --- Navigation Specification

## Application Navigation

``` text
Login
  |
  v
Dashboard
  |
  +--> Transactions
  |       |
  |       +--> Transaction Details
  |
  +--> AI Recovery
  |       |
  |       +--> Recovery Result
  |
  +--> Analytics
  |
  +--> Audit Logs
  |
  +--> Settings
```

## 1. Dashboard

Route: `/dashboard`

Purpose: - Show revenue at risk - Show recovered revenue - Show failed
payments - Show recovery rate - Show recent AI actions

Primary CTA: **Review High-Priority Payments**

## 2. Transactions

Route: `/transactions`

Features: - Search - Status filter - Risk filter - Amount filter - Sort
by recovery probability

Clicking a row opens Transaction Details.

## 3. Transaction Details

Route: `/transactions/:id`

Sections: - Payment information - Failure reason - Customer/payment
history - AI risk score - AI diagnosis - Recommended action - Execute
action - Action history

## 4. AI Recovery

Route: `/recovery`

Shows high-priority failed payments.

Columns: - Payment ID - Amount - Recovery probability - Diagnosis -
Recommended action - Execute button

## 5. Analytics

Route: `/analytics`

Charts: - Revenue at risk vs recovered - Recovery by failure reason -
Recovery by action - Daily recovery trend

## 6. Audit Logs

Route: `/audit-logs`

Shows: - Timestamp - Transaction - AI decision - Reason - Action -
Result

## 7. Settings

Route: `/settings`

Demo settings: - Recovery rules - Maximum retries - Human escalation
threshold - Test-mode configuration

## UX Rule

The user should reach any important recovery case in no more than three
clicks from Dashboard.
