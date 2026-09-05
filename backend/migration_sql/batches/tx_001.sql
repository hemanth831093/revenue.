INSERT INTO transactions (id,payment_id,customer_id,customer_name,customer_email,amount,payment_method,status,failure_reason,failure_code,previous_successes,previous_failures,retry_count,created_at) VALUES
(1,'pay_DEMO_UPI_5000','cust_1001','Aarav Sharma','aarav.sharma@example.com',5000.0,'UPI','RECOVERED','bank_timeout','BANK_GATEWAY_TIMEOUT',4,0,1,'2026-09-04 15:39:07.096197'),
(2,'pay_DEMO_RETRY_MAX','cust_1002','Rohan Gupta','rohan.gupta@example.com',4200.0,'Credit Card','FAILED','bank_timeout','MAX_ATTEMPTS_EXCEEDED',1,3,3,'2026-09-04 14:04:07.096232'),
(3,'pay_DEMO_HIGH_VALUE','cust_1003','Priya Patel','priya.patel@example.com',25000.0,'Netbanking','FAILED','network_error','HIGH_VALUE_TIMEOUT',5,0,1,'2026-09-04 15:04:07.096244'),
(4,'pay_DEMO_FRAUD_FLAG','cust_1004','Vikram Singh','vikram.singh@example.com',8500.0,'Credit Card','FAILED','fraud_flag','SUSPICIOUS_VELOCITY',0,2,1,'2026-09-04 12:04:07.096252'),
(5,'pay_DEMO_EXPIRED_CARD','cust_1005','Ananya Verma','ananya.verma@example.com',3500.0,'Credit Card','FAILED','card_expired','EXPIRED_INSTRUMENT',3,0,0,'2026-09-04 13:04:07.096260'),
(6,'pay_DEMO_REMINDER_FUNDS','cust_1006','Neha Reddy','neha.reddy@example.com',1800.0,'UPI','FAILED','insufficient_funds','DECLINED_INSUFFICIENT_FUNDS',2,1,1,'2026-09-04 11:04:07.096268'),
(7,'pay_syn_10001','cust_2204','Ritu Choudhury','ritu.choudhury24@example.com',2499.0,'Debit Card','RECOVERED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',0,0,3,'2026-09-04 11:04:07.101453'),
(8,'pay_syn_10002','cust_3905','Rohan Gupta','rohan.gupta37@example.com',2499.0,'UPI','FAILED','fraud_flag','ERR_FRAUD_FLAG',5,3,1,'2026-09-02 06:04:07.106175'),
(9,'pay_syn_10003','cust_8630','Shruti Agarwal','shruti.agarwal45@example.com',22000.0,'UPI','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',2,1,1,'2026-08-31 14:04:07.107394'),
(10,'pay_syn_10004','cust_2759','Ishita Banerjee','ishita.banerjee23@example.com',4999.0,'Netbanking','FAILED','bank_timeout','ERR_BANK_TIMEOUT',4,2,0,'2026-08-31 18:04:07.107667'),
(11,'pay_syn_10005','cust_3022','Pooja Mehta','pooja.mehta78@example.com',12500.0,'Netbanking','FAILED','bank_timeout','ERR_BANK_TIMEOUT',5,2,1,'2026-08-31 21:04:07.107899'),
(12,'pay_syn_10006','cust_7417','Rohan Gupta','rohan.gupta15@example.com',999.0,'Credit Card','FAILED','card_expired','ERR_CARD_EXPIRED',6,0,3,'2026-09-03 04:04:07.108525'),
(13,'pay_syn_10007','cust_8833','Pooja Mehta','pooja.mehta91@example.com',4999.0,'Debit Card','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',5,2,0,'2026-09-01 10:04:07.108722'),
(14,'pay_syn_10008','cust_6375','Ritu Choudhury','ritu.choudhury31@example.com',9999.0,'Credit Card','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',5,1,2,'2026-08-31 04:04:07.108927'),
(15,'pay_syn_10009','cust_3876','Simran Gill','simran.gill17@example.com',7500.0,'UPI','FAILED','card_expired','ERR_CARD_EXPIRED',1,2,1,'2026-09-01 04:04:07.109260')
ON CONFLICT (payment_id) DO NOTHING;