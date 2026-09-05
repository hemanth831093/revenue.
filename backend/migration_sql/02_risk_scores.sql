-- risk_scores data
INSERT INTO risk_scores (id,transaction_id,recovery_probability,priority,risk_factors,model_version,created_at) VALUES
(1,1,0.88,'HIGH','["Strong customer track record (4 past successful payments).", "Failure diagnosed as transient bank gateway timeout (High retry success rate)."]','v1.0.0-rf','2026-09-04 16:06:27.625502'),
(2,2,0.02,'LOW','["Failure diagnosed as transient bank gateway timeout (High retry success rate).", "Maximum retry attempts reached (3/3 retries)."]','v1.0.0-rf','2026-09-04 16:06:27.951509'),
(3,3,0.98,'HIGH','["Strong customer track record (5 past successful payments).", "Failure caused by temporary network connectivity glitch.", "High transaction value (\u20b925,000.00 >= \u20b920,000 threshold)."]','v1.0.0-rf','2026-09-04 16:06:28.077500'),
(4,4,0.02,'LOW','["First-time customer transaction with no previous payment history.", "Flagged by risk filters for suspicious velocity; zero autonomous retries allowed."]','v1.0.0-rf','2026-09-04 16:06:28.194458'),
(5,6,0.06,'LOW','["Declined due to insufficient account balance; SMS/WhatsApp reminder recommended."]','v1.0.0-rf','2026-09-04 16:25:29.297811'),
(6,5,0.2,'LOW','["Strong customer track record (3 past successful payments).", "Card instrument expired; requires fresh payment link dispatch."]','v1.0.0-rf','2026-09-04 16:59:37.556804'),
(7,161,0.94,'HIGH','["Strong customer track record (5 past successful payments).", "Failure caused by temporary network connectivity glitch."]','v1.0.0-rf','2026-09-04 16:59:37.639728')
ON CONFLICT DO NOTHING;