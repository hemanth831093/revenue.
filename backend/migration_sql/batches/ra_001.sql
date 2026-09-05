INSERT INTO recovery_actions (id,transaction_id,action_type,status,amount_recovered,razorpay_sim_id,executed_at,response_metadata) VALUES
(1,7,'PAYMENT_LINK','SUCCESS',2499.0,'retry_sim_13905','2026-09-04 11:19:07.101453','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(2,16,'PAYMENT_LINK','SUCCESS',3500.0,'retry_sim_86484','2026-08-30 21:19:07.109516','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(3,17,'PAYMENT_LINK','SUCCESS',9999.0,'retry_sim_30969','2026-09-01 07:19:07.110027','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(4,24,'PAYMENT_LINK','SUCCESS',9999.0,'retry_sim_87110','2026-09-04 13:19:07.112937','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(5,31,'RETRY','SUCCESS',7500.0,'retry_sim_65444','2026-09-03 03:19:07.114580','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(6,33,'PAYMENT_LINK','SUCCESS',12500.0,'retry_sim_40828','2026-09-01 01:19:07.115643','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(7,34,'PAYMENT_LINK','SUCCESS',15000.0,'retry_sim_44179','2026-08-30 16:19:07.116004','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(8,37,'PAYMENT_LINK','SUCCESS',3500.0,'retry_sim_82692','2026-09-01 02:19:07.117156','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(9,40,'PAYMENT_LINK','SUCCESS',499.0,'retry_sim_67912','2026-09-03 19:19:07.118141','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(10,42,'PAYMENT_LINK','SUCCESS',1499.0,'retry_sim_99399','2026-09-03 13:19:07.118928','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(11,51,'PAYMENT_LINK','SUCCESS',1499.0,'retry_sim_84593','2026-09-01 09:19:07.121649','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(12,52,'RETRY','SUCCESS',3500.0,'retry_sim_67954','2026-09-02 07:19:07.122447','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(13,53,'PAYMENT_LINK','SUCCESS',18500.0,'retry_sim_40784','2026-08-31 07:19:07.123108','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(14,54,'PAYMENT_LINK','SUCCESS',499.0,'retry_sim_92544','2026-09-02 10:19:07.123674','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(15,68,'RETRY','SUCCESS',3500.0,'retry_sim_35995','2026-09-02 13:19:07.126447','{"gateway": "Razorpay_Sandbox", "status": "captured"}')
ON CONFLICT DO NOTHING;