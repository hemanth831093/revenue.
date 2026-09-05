-- Reset sequences so new rows don't collide with migrated IDs
SELECT setval('transactions_id_seq',     (SELECT MAX(id) FROM transactions));
SELECT setval('risk_scores_id_seq',      (SELECT MAX(id) FROM risk_scores));
SELECT setval('recovery_actions_id_seq', (SELECT MAX(id) FROM recovery_actions));
SELECT setval('audit_logs_id_seq',       (SELECT MAX(id) FROM audit_logs));
