INSERT INTO transactions (id,payment_id,customer_id,customer_name,customer_email,amount,payment_method,status,failure_reason,failure_code,previous_successes,previous_failures,retry_count,created_at) VALUES
(46,'pay_syn_10040','cust_2193','Siddharth Malhotra','siddharth.malhotra38@example.com',4999.0,'Credit Card','FAILED','network_error','ERR_NETWORK_ERROR',0,2,2,'2026-09-01 05:04:07.120493'),
(47,'pay_syn_10041','cust_7566','Meera Sen','meera.sen61@example.com',999.0,'Debit Card','FAILED','bank_timeout','ERR_BANK_TIMEOUT',2,1,2,'2026-09-04 11:04:07.120748'),
(48,'pay_syn_10042','cust_5559','Priya Patel','priya.patel86@example.com',7500.0,'Debit Card','FAILED','card_expired','ERR_CARD_EXPIRED',4,0,3,'2026-08-30 20:04:07.120992'),
(49,'pay_syn_10043','cust_4086','Shruti Agarwal','shruti.agarwal34@example.com',499.0,'UPI','FAILED','network_error','ERR_NETWORK_ERROR',6,1,2,'2026-09-02 08:04:07.121231'),
(50,'pay_syn_10044','cust_9542','Rohan Gupta','rohan.gupta95@example.com',4999.0,'Debit Card','FAILED','fraud_flag','ERR_FRAUD_FLAG',0,2,2,'2026-09-01 02:04:07.121434'),
(51,'pay_syn_10045','cust_5296','Amitabh Roy','amitabh.roy51@example.com',1499.0,'Debit Card','RECOVERED','fraud_flag','ERR_FRAUD_FLAG',5,3,1,'2026-09-01 09:04:07.121649'),
(52,'pay_syn_10046','cust_6488','Rahul Deshmukh','rahul.deshmukh61@example.com',3500.0,'UPI','RECOVERED','card_expired','ERR_CARD_EXPIRED',6,2,3,'2026-09-02 07:04:07.122447'),
(53,'pay_syn_10047','cust_6187','Nitin Saxena','nitin.saxena37@example.com',18500.0,'Netbanking','RECOVERED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',4,2,0,'2026-08-31 07:04:07.123108'),
(54,'pay_syn_10048','cust_3840','Nitin Saxena','nitin.saxena49@example.com',499.0,'Credit Card','RECOVERED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',3,0,3,'2026-09-02 10:04:07.123674'),
(55,'pay_syn_10049','cust_7884','Shruti Agarwal','shruti.agarwal34@example.com',7500.0,'Netbanking','FAILED','network_error','ERR_NETWORK_ERROR',5,0,0,'2026-08-31 12:04:07.124181'),
(56,'pay_syn_10050','cust_3440','Amitabh Roy','amitabh.roy38@example.com',12500.0,'Netbanking','FAILED','bank_timeout','ERR_BANK_TIMEOUT',6,0,3,'2026-09-03 22:04:07.124481'),
(57,'pay_syn_10051','cust_6351','Pooja Mehta','pooja.mehta95@example.com',15000.0,'Debit Card','FAILED','network_error','ERR_NETWORK_ERROR',4,3,3,'2026-08-30 21:04:07.124662'),
(58,'pay_syn_10052','cust_5686','Neha Reddy','neha.reddy70@example.com',18500.0,'Debit Card','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',6,3,1,'2026-09-03 04:04:07.124835'),
(59,'pay_syn_10053','cust_7845','Pooja Mehta','pooja.mehta19@example.com',3500.0,'Debit Card','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',4,0,1,'2026-09-03 20:04:07.124999'),
(60,'pay_syn_10054','cust_7684','Siddharth Malhotra','siddharth.malhotra59@example.com',999.0,'Credit Card','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',2,3,3,'2026-09-04 08:04:07.125159')
ON CONFLICT (payment_id) DO NOTHING;