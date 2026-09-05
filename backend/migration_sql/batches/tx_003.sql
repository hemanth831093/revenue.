INSERT INTO transactions (id,payment_id,customer_id,customer_name,customer_email,amount,payment_method,status,failure_reason,failure_code,previous_successes,previous_failures,retry_count,created_at) VALUES
(31,'pay_syn_10025','cust_9392','Aditya Joshi','aditya.joshi61@example.com',7500.0,'UPI','RECOVERED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',3,2,3,'2026-09-03 03:04:07.114580'),
(32,'pay_syn_10026','cust_7422','Tanya Das','tanya.das81@example.com',2499.0,'Netbanking','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',0,0,2,'2026-09-04 08:04:07.115330'),
(33,'pay_syn_10027','cust_5905','Ananya Verma','ananya.verma84@example.com',12500.0,'Credit Card','RECOVERED','bank_timeout','ERR_BANK_TIMEOUT',1,0,0,'2026-09-01 01:04:07.115643'),
(34,'pay_syn_10028','cust_9713','Deepika Iyer','deepika.iyer25@example.com',15000.0,'Credit Card','RECOVERED','fraud_flag','ERR_FRAUD_FLAG',0,3,2,'2026-08-30 16:04:07.116004'),
(35,'pay_syn_10029','cust_7867','Aditya Joshi','aditya.joshi95@example.com',3500.0,'Debit Card','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',5,2,3,'2026-09-02 23:04:07.116622'),
(36,'pay_syn_10030','cust_2076','Simran Gill','simran.gill19@example.com',15000.0,'Netbanking','FAILED','fraud_flag','ERR_FRAUD_FLAG',0,1,2,'2026-09-03 23:04:07.116950'),
(37,'pay_syn_10031','cust_9202','Manish Kumar','manish.kumar18@example.com',3500.0,'Credit Card','RECOVERED','card_expired','ERR_CARD_EXPIRED',6,2,0,'2026-09-01 02:04:07.117156'),
(38,'pay_syn_10032','cust_2848','Rahul Deshmukh','rahul.deshmukh94@example.com',999.0,'Credit Card','FAILED','card_expired','ERR_CARD_EXPIRED',5,1,2,'2026-09-03 03:04:07.117631'),
(39,'pay_syn_10033','cust_7878','Varun Bhatia','varun.bhatia36@example.com',18500.0,'Debit Card','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',2,3,2,'2026-08-30 20:04:07.117947'),
(40,'pay_syn_10034','cust_7196','Ananya Verma','ananya.verma21@example.com',499.0,'Netbanking','RECOVERED','card_expired','ERR_CARD_EXPIRED',6,1,2,'2026-09-03 19:04:07.118141'),
(41,'pay_syn_10035','cust_6594','Karan Kapoor','karan.kapoor64@example.com',999.0,'UPI','FAILED','bank_timeout','ERR_BANK_TIMEOUT',5,1,0,'2026-08-31 05:04:07.118534'),
(42,'pay_syn_10036','cust_6526','Manish Kumar','manish.kumar84@example.com',1499.0,'Credit Card','RECOVERED','network_error','ERR_NETWORK_ERROR',2,0,2,'2026-09-03 13:04:07.118928'),
(43,'pay_syn_10037','cust_2842','Siddharth Malhotra','siddharth.malhotra95@example.com',7500.0,'Debit Card','FAILED','fraud_flag','ERR_FRAUD_FLAG',5,1,1,'2026-08-31 01:04:07.119690'),
(44,'pay_syn_10038','cust_9220','Neha Reddy','neha.reddy32@example.com',1499.0,'Netbanking','FAILED','bank_timeout','ERR_BANK_TIMEOUT',2,3,1,'2026-09-03 05:04:07.120035'),
(45,'pay_syn_10039','cust_2885','Neha Reddy','neha.reddy99@example.com',9999.0,'Netbanking','FAILED','bank_timeout','ERR_BANK_TIMEOUT',6,3,2,'2026-09-03 00:04:07.120245')
ON CONFLICT (payment_id) DO NOTHING;