INSERT INTO transactions (id,payment_id,customer_id,customer_name,customer_email,amount,payment_method,status,failure_reason,failure_code,previous_successes,previous_failures,retry_count,created_at) VALUES
(136,'pay_syn_10130','cust_7756','Neha Reddy','neha.reddy44@example.com',4999.0,'Debit Card','RECOVERED','card_expired','ERR_CARD_EXPIRED',6,1,3,'2026-09-04 07:04:07.143152'),
(137,'pay_syn_10131','cust_9961','Gaurav Kulkarni','gaurav.kulkarni91@example.com',22000.0,'UPI','FAILED','bank_timeout','ERR_BANK_TIMEOUT',3,3,3,'2026-09-02 20:04:07.143517'),
(138,'pay_syn_10132','cust_4552','Neha Reddy','neha.reddy57@example.com',15000.0,'Debit Card','RECOVERED','fraud_flag','ERR_FRAUD_FLAG',0,1,1,'2026-08-31 15:04:07.143792'),
(139,'pay_syn_10133','cust_2668','Ananya Verma','ananya.verma96@example.com',18500.0,'Debit Card','FAILED','network_error','ERR_NETWORK_ERROR',4,3,3,'2026-09-03 05:04:07.144167'),
(140,'pay_syn_10134','cust_2932','Aditya Joshi','aditya.joshi75@example.com',999.0,'Debit Card','FAILED','network_error','ERR_NETWORK_ERROR',5,3,2,'2026-09-04 10:04:07.144480'),
(141,'pay_syn_10135','cust_6909','Siddharth Malhotra','siddharth.malhotra60@example.com',2499.0,'UPI','FAILED','bank_timeout','ERR_BANK_TIMEOUT',1,1,2,'2026-09-03 02:04:07.144665'),
(142,'pay_syn_10136','cust_2063','Ishita Banerjee','ishita.banerjee25@example.com',1499.0,'Netbanking','RECOVERED','network_error','ERR_NETWORK_ERROR',4,1,2,'2026-09-04 06:04:07.144845'),
(143,'pay_syn_10137','cust_5573','Gaurav Kulkarni','gaurav.kulkarni15@example.com',999.0,'UPI','FAILED','network_error','ERR_NETWORK_ERROR',4,3,3,'2026-08-31 21:04:07.145218'),
(144,'pay_syn_10138','cust_4371','Ritu Choudhury','ritu.choudhury63@example.com',499.0,'UPI','FAILED','network_error','ERR_NETWORK_ERROR',1,3,2,'2026-09-04 04:04:07.145514'),
(145,'pay_syn_10139','cust_3993','Amitabh Roy','amitabh.roy23@example.com',7500.0,'Netbanking','FAILED','fraud_flag','ERR_FRAUD_FLAG',3,2,2,'2026-09-03 11:04:07.145691'),
(146,'pay_syn_10140','cust_2625','Ishita Banerjee','ishita.banerjee31@example.com',12500.0,'UPI','RECOVERED','fraud_flag','ERR_FRAUD_FLAG',6,2,2,'2026-08-31 18:04:07.145863'),
(147,'pay_syn_10141','cust_2842','Vikram Singh','vikram.singh40@example.com',2499.0,'Credit Card','RECOVERED','card_expired','ERR_CARD_EXPIRED',1,0,1,'2026-08-31 13:04:07.146208'),
(148,'pay_syn_10142','cust_8180','Sanjay Rao','sanjay.rao69@example.com',18500.0,'Netbanking','FAILED','fraud_flag','ERR_FRAUD_FLAG',4,2,2,'2026-09-03 20:04:07.146677'),
(149,'pay_syn_10143','cust_5841','Pooja Mehta','pooja.mehta18@example.com',35000.0,'Netbanking','FAILED','card_expired','ERR_CARD_EXPIRED',0,2,0,'2026-09-03 00:04:07.146955'),
(150,'pay_syn_10144','cust_2308','Pooja Mehta','pooja.mehta67@example.com',3500.0,'UPI','RECOVERED','card_expired','ERR_CARD_EXPIRED',6,0,3,'2026-09-02 04:04:07.147125')
ON CONFLICT (payment_id) DO NOTHING;