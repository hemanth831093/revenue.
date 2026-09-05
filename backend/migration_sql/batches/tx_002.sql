INSERT INTO transactions (id,payment_id,customer_id,customer_name,customer_email,amount,payment_method,status,failure_reason,failure_code,previous_successes,previous_failures,retry_count,created_at) VALUES
(16,'pay_syn_10010','cust_9247','Sanjay Rao','sanjay.rao60@example.com',3500.0,'Netbanking','RECOVERED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',5,2,3,'2026-08-30 21:04:07.109516'),
(17,'pay_syn_10011','cust_3796','Deepika Iyer','deepika.iyer56@example.com',9999.0,'Credit Card','RECOVERED','fraud_flag','ERR_FRAUD_FLAG',0,0,1,'2026-09-01 07:04:07.110027'),
(18,'pay_syn_10012','cust_6885','Nitin Saxena','nitin.saxena64@example.com',7500.0,'UPI','FAILED','network_error','ERR_NETWORK_ERROR',3,2,0,'2026-09-01 00:04:07.110838'),
(19,'pay_syn_10013','cust_7584','Gaurav Kulkarni','gaurav.kulkarni24@example.com',999.0,'Debit Card','FAILED','card_expired','ERR_CARD_EXPIRED',1,3,0,'2026-08-31 19:04:07.111505'),
(20,'pay_syn_10014','cust_9961','Gaurav Kulkarni','gaurav.kulkarni43@example.com',999.0,'Credit Card','FAILED','fraud_flag','ERR_FRAUD_FLAG',2,1,1,'2026-09-02 16:04:07.111907'),
(21,'pay_syn_10015','cust_6418','Simran Gill','simran.gill30@example.com',4999.0,'UPI','FAILED','fraud_flag','ERR_FRAUD_FLAG',0,2,2,'2026-09-03 09:04:07.112294'),
(22,'pay_syn_10016','cust_9192','Ananya Verma','ananya.verma40@example.com',22000.0,'UPI','FAILED','bank_timeout','ERR_BANK_TIMEOUT',0,1,1,'2026-09-01 03:04:07.112510'),
(23,'pay_syn_10017','cust_3352','Sanjay Rao','sanjay.rao80@example.com',15000.0,'Debit Card','FAILED','fraud_flag','ERR_FRAUD_FLAG',1,1,2,'2026-09-02 12:04:07.112697'),
(24,'pay_syn_10018','cust_5059','Nitin Saxena','nitin.saxena93@example.com',9999.0,'Netbanking','RECOVERED','fraud_flag','ERR_FRAUD_FLAG',1,0,2,'2026-09-04 13:04:07.112937'),
(25,'pay_syn_10019','cust_6820','Karan Kapoor','karan.kapoor39@example.com',999.0,'Credit Card','FAILED','bank_timeout','ERR_BANK_TIMEOUT',0,1,0,'2026-08-30 20:04:07.113341'),
(26,'pay_syn_10020','cust_2580','Ananya Verma','ananya.verma52@example.com',18500.0,'Credit Card','FAILED','card_expired','ERR_CARD_EXPIRED',4,1,3,'2026-09-03 08:04:07.113668'),
(27,'pay_syn_10021','cust_3559','Sanjay Rao','sanjay.rao62@example.com',18500.0,'UPI','FAILED','bank_timeout','ERR_BANK_TIMEOUT',3,3,3,'2026-08-31 01:04:07.113837'),
(28,'pay_syn_10022','cust_7516','Gaurav Kulkarni','gaurav.kulkarni16@example.com',7500.0,'UPI','FAILED','bank_timeout','ERR_BANK_TIMEOUT',6,0,1,'2026-09-03 15:04:07.114071'),
(29,'pay_syn_10023','cust_5675','Aditya Joshi','aditya.joshi78@example.com',1499.0,'Credit Card','FAILED','network_error','ERR_NETWORK_ERROR',1,0,3,'2026-08-31 08:04:07.114249'),
(30,'pay_syn_10024','cust_2414','Karan Kapoor','karan.kapoor22@example.com',35000.0,'UPI','FAILED','bank_timeout','ERR_BANK_TIMEOUT',1,3,3,'2026-09-02 02:04:07.114418')
ON CONFLICT (payment_id) DO NOTHING;