INSERT INTO transactions (id,payment_id,customer_id,customer_name,customer_email,amount,payment_method,status,failure_reason,failure_code,previous_successes,previous_failures,retry_count,created_at) VALUES
(106,'pay_syn_10100','cust_4936','Ananya Verma','ananya.verma47@example.com',1499.0,'Debit Card','FAILED','network_error','ERR_NETWORK_ERROR',3,1,1,'2026-09-03 17:04:07.135649'),
(107,'pay_syn_10101','cust_9133','Rohan Gupta','rohan.gupta88@example.com',18500.0,'Netbanking','FAILED','fraud_flag','ERR_FRAUD_FLAG',4,1,1,'2026-09-02 04:04:07.136243'),
(108,'pay_syn_10102','cust_5764','Ritu Choudhury','ritu.choudhury42@example.com',35000.0,'Debit Card','FAILED','bank_timeout','ERR_BANK_TIMEOUT',2,1,0,'2026-09-02 07:04:07.136623'),
(109,'pay_syn_10103','cust_4450','Manish Kumar','manish.kumar85@example.com',9999.0,'Netbanking','FAILED','card_expired','ERR_CARD_EXPIRED',1,3,3,'2026-09-04 02:04:07.136884'),
(110,'pay_syn_10104','cust_6685','Siddharth Malhotra','siddharth.malhotra58@example.com',3500.0,'Debit Card','FAILED','fraud_flag','ERR_FRAUD_FLAG',2,0,3,'2026-09-03 04:04:07.137147'),
(111,'pay_syn_10105','cust_9086','Aarav Sharma','aarav.sharma82@example.com',22000.0,'UPI','FAILED','fraud_flag','ERR_FRAUD_FLAG',2,1,2,'2026-09-03 11:04:07.137370'),
(112,'pay_syn_10106','cust_7086','Ritu Choudhury','ritu.choudhury34@example.com',18500.0,'Debit Card','RECOVERED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',5,0,2,'2026-08-31 11:04:07.137570'),
(113,'pay_syn_10107','cust_4988','Ananya Verma','ananya.verma84@example.com',3500.0,'Credit Card','FAILED','bank_timeout','ERR_BANK_TIMEOUT',3,1,1,'2026-09-03 23:04:07.138030'),
(114,'pay_syn_10108','cust_6348','Karan Kapoor','karan.kapoor56@example.com',3500.0,'Debit Card','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',3,2,2,'2026-08-31 09:04:07.138455'),
(115,'pay_syn_10109','cust_9888','Priya Patel','priya.patel69@example.com',35000.0,'UPI','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',6,3,2,'2026-09-04 04:04:07.138656'),
(116,'pay_syn_10110','cust_4166','Deepika Iyer','deepika.iyer11@example.com',4999.0,'UPI','FAILED','network_error','ERR_NETWORK_ERROR',5,2,3,'2026-08-31 06:04:07.138831'),
(117,'pay_syn_10111','cust_2887','Ritu Choudhury','ritu.choudhury57@example.com',499.0,'Credit Card','FAILED','network_error','ERR_NETWORK_ERROR',4,2,1,'2026-09-01 05:04:07.138992'),
(118,'pay_syn_10112','cust_8749','Rohan Gupta','rohan.gupta91@example.com',18500.0,'Netbanking','FAILED','card_expired','ERR_CARD_EXPIRED',1,0,0,'2026-09-03 01:04:07.139170'),
(119,'pay_syn_10113','cust_2796','Sanjay Rao','sanjay.rao24@example.com',1499.0,'Credit Card','FAILED','fraud_flag','ERR_FRAUD_FLAG',2,3,1,'2026-08-30 22:04:07.139337'),
(120,'pay_syn_10114','cust_2811','Amitabh Roy','amitabh.roy93@example.com',7500.0,'Netbanking','FAILED','fraud_flag','ERR_FRAUD_FLAG',2,0,2,'2026-09-03 12:04:07.139496')
ON CONFLICT (payment_id) DO NOTHING;