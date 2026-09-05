INSERT INTO recovery_actions (id,transaction_id,action_type,status,amount_recovered,razorpay_sim_id,executed_at,response_metadata) VALUES
(16,71,'PAYMENT_LINK','SUCCESS',7500.0,'retry_sim_67091','2026-09-02 04:19:07.127255','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(17,79,'PAYMENT_LINK','SUCCESS',3500.0,'retry_sim_17146','2026-09-04 10:19:07.129255','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(18,81,'RETRY','SUCCESS',9999.0,'retry_sim_85631','2026-09-04 06:19:07.129901','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(19,84,'RETRY','SUCCESS',18500.0,'retry_sim_32782','2026-09-03 09:19:07.130887','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(20,87,'PAYMENT_LINK','SUCCESS',1499.0,'retry_sim_26299','2026-09-02 07:19:07.131728','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(21,95,'PAYMENT_LINK','SUCCESS',12500.0,'retry_sim_24871','2026-08-31 04:19:07.133325','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(22,112,'PAYMENT_LINK','SUCCESS',18500.0,'retry_sim_67779','2026-08-31 11:19:07.137570','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(23,128,'PAYMENT_LINK','SUCCESS',18500.0,'retry_sim_20589','2026-08-30 20:19:07.140830','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(24,132,'PAYMENT_LINK','SUCCESS',999.0,'retry_sim_58843','2026-09-04 03:19:07.141835','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(25,134,'RETRY','SUCCESS',12500.0,'retry_sim_24184','2026-08-31 03:19:07.142486','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(26,136,'PAYMENT_LINK','SUCCESS',4999.0,'retry_sim_28595','2026-09-04 07:19:07.143152','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(27,138,'PAYMENT_LINK','SUCCESS',15000.0,'retry_sim_90981','2026-08-31 15:19:07.143792','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(28,142,'PAYMENT_LINK','SUCCESS',1499.0,'retry_sim_62044','2026-09-04 06:19:07.144845','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(29,146,'RETRY','SUCCESS',12500.0,'retry_sim_94599','2026-08-31 18:19:07.145863','{"gateway": "Razorpay_Sandbox", "status": "captured"}'),
(30,147,'PAYMENT_LINK','SUCCESS',2499.0,'retry_sim_92306','2026-08-31 13:19:07.146208','{"gateway": "Razorpay_Sandbox", "status": "captured"}')
ON CONFLICT DO NOTHING;