INSERT INTO transactions (id,payment_id,customer_id,customer_name,customer_email,amount,payment_method,status,failure_reason,failure_code,previous_successes,previous_failures,retry_count,created_at) VALUES
(61,'pay_syn_10055','cust_5190','Aditya Joshi','aditya.joshi63@example.com',7500.0,'UPI','FAILED','fraud_flag','ERR_FRAUD_FLAG',2,2,3,'2026-08-31 02:04:07.125314'),
(62,'pay_syn_10056','cust_8123','Amitabh Roy','amitabh.roy78@example.com',2499.0,'Credit Card','FAILED','network_error','ERR_NETWORK_ERROR',3,0,3,'2026-09-02 20:04:07.125488'),
(63,'pay_syn_10057','cust_8538','Nitin Saxena','nitin.saxena96@example.com',9999.0,'Netbanking','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',4,0,3,'2026-09-01 12:04:07.125663'),
(64,'pay_syn_10058','cust_2222','Shruti Agarwal','shruti.agarwal94@example.com',1499.0,'UPI','FAILED','network_error','ERR_NETWORK_ERROR',1,0,2,'2026-09-02 15:04:07.125825'),
(65,'pay_syn_10059','cust_5724','Ishita Banerjee','ishita.banerjee37@example.com',35000.0,'Debit Card','FAILED','card_expired','ERR_CARD_EXPIRED',2,3,2,'2026-08-31 05:04:07.125981'),
(66,'pay_syn_10060','cust_2158','Rohan Gupta','rohan.gupta70@example.com',2499.0,'UPI','FAILED','card_expired','ERR_CARD_EXPIRED',6,0,0,'2026-09-03 08:04:07.126132'),
(67,'pay_syn_10061','cust_7089','Aditya Joshi','aditya.joshi12@example.com',1499.0,'Credit Card','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',0,1,3,'2026-08-31 22:04:07.126281'),
(68,'pay_syn_10062','cust_3374','Kavya Nair','kavya.nair57@example.com',3500.0,'UPI','RECOVERED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',0,2,3,'2026-09-02 13:04:07.126447'),
(69,'pay_syn_10063','cust_7657','Rohan Gupta','rohan.gupta85@example.com',22000.0,'Credit Card','FAILED','bank_timeout','ERR_BANK_TIMEOUT',6,0,0,'2026-09-02 19:04:07.126787'),
(70,'pay_syn_10064','cust_7419','Karan Kapoor','karan.kapoor64@example.com',12500.0,'Debit Card','FAILED','bank_timeout','ERR_BANK_TIMEOUT',0,3,3,'2026-09-04 02:04:07.127084'),
(71,'pay_syn_10065','cust_7206','Amitabh Roy','amitabh.roy56@example.com',7500.0,'Netbanking','RECOVERED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',4,2,3,'2026-09-02 04:04:07.127255'),
(72,'pay_syn_10066','cust_4198','Gaurav Kulkarni','gaurav.kulkarni85@example.com',999.0,'Debit Card','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',3,1,3,'2026-09-01 15:04:07.127611'),
(73,'pay_syn_10067','cust_5104','Varun Bhatia','varun.bhatia95@example.com',9999.0,'Debit Card','FAILED','bank_timeout','ERR_BANK_TIMEOUT',1,3,1,'2026-09-02 18:04:07.127900'),
(74,'pay_syn_10068','cust_4290','Kavya Nair','kavya.nair53@example.com',499.0,'Debit Card','FAILED','fraud_flag','ERR_FRAUD_FLAG',1,0,1,'2026-08-31 19:04:07.128069'),
(75,'pay_syn_10069','cust_6548','Amitabh Roy','amitabh.roy72@example.com',18500.0,'Credit Card','FAILED','network_error','ERR_NETWORK_ERROR',3,0,0,'2026-09-03 02:04:07.128236')
ON CONFLICT (payment_id) DO NOTHING;