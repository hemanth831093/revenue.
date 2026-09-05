INSERT INTO transactions (id,payment_id,customer_id,customer_name,customer_email,amount,payment_method,status,failure_reason,failure_code,previous_successes,previous_failures,retry_count,created_at) VALUES
(76,'pay_syn_10070','cust_7667','Siddharth Malhotra','siddharth.malhotra61@example.com',18500.0,'Credit Card','FAILED','card_expired','ERR_CARD_EXPIRED',3,2,3,'2026-08-31 16:04:07.128396'),
(77,'pay_syn_10071','cust_4882','Karan Kapoor','karan.kapoor52@example.com',3500.0,'Netbanking','FAILED','card_expired','ERR_CARD_EXPIRED',0,1,2,'2026-09-04 00:04:07.128566'),
(78,'pay_syn_10072','cust_9789','Gaurav Kulkarni','gaurav.kulkarni78@example.com',2499.0,'Credit Card','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',2,2,0,'2026-08-31 05:04:07.128729'),
(79,'pay_syn_10073','cust_3863','Aditya Joshi','aditya.joshi47@example.com',3500.0,'Debit Card','RECOVERED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',4,1,2,'2026-09-04 10:04:07.129255'),
(80,'pay_syn_10074','cust_7713','Karan Kapoor','karan.kapoor47@example.com',999.0,'Credit Card','FAILED','network_error','ERR_NETWORK_ERROR',4,2,3,'2026-09-02 02:04:07.129615'),
(81,'pay_syn_10075','cust_3510','Pooja Mehta','pooja.mehta53@example.com',9999.0,'UPI','RECOVERED','card_expired','ERR_CARD_EXPIRED',0,3,3,'2026-09-04 06:04:07.129901'),
(82,'pay_syn_10076','cust_2439','Ritu Choudhury','ritu.choudhury97@example.com',35000.0,'Credit Card','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',2,0,1,'2026-09-04 00:04:07.130393'),
(83,'pay_syn_10077','cust_6966','Karan Kapoor','karan.kapoor63@example.com',7500.0,'Credit Card','FAILED','fraud_flag','ERR_FRAUD_FLAG',3,2,3,'2026-09-03 00:04:07.130701'),
(84,'pay_syn_10078','cust_2493','Shruti Agarwal','shruti.agarwal89@example.com',18500.0,'UPI','RECOVERED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',5,0,1,'2026-09-03 09:04:07.130887'),
(85,'pay_syn_10079','cust_3282','Karan Kapoor','karan.kapoor19@example.com',9999.0,'UPI','FAILED','network_error','ERR_NETWORK_ERROR',3,2,0,'2026-09-03 10:04:07.131255'),
(86,'pay_syn_10080','cust_7758','Rahul Deshmukh','rahul.deshmukh46@example.com',18500.0,'Netbanking','FAILED','bank_timeout','ERR_BANK_TIMEOUT',2,1,3,'2026-09-04 01:04:07.131555'),
(87,'pay_syn_10081','cust_7305','Karan Kapoor','karan.kapoor38@example.com',1499.0,'Credit Card','RECOVERED','card_expired','ERR_CARD_EXPIRED',1,2,2,'2026-09-02 07:04:07.131728'),
(88,'pay_syn_10082','cust_4491','Pooja Mehta','pooja.mehta98@example.com',12500.0,'Netbanking','FAILED','card_expired','ERR_CARD_EXPIRED',3,0,0,'2026-08-30 22:04:07.132067'),
(89,'pay_syn_10083','cust_6945','Amitabh Roy','amitabh.roy51@example.com',999.0,'Debit Card','FAILED','bank_timeout','ERR_BANK_TIMEOUT',5,0,2,'2026-09-01 14:04:07.132347'),
(90,'pay_syn_10084','cust_5854','Ananya Verma','ananya.verma32@example.com',1499.0,'Netbanking','FAILED','card_expired','ERR_CARD_EXPIRED',3,3,0,'2026-09-02 03:04:07.132515')
ON CONFLICT (payment_id) DO NOTHING;