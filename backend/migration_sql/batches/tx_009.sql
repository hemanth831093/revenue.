INSERT INTO transactions (id,payment_id,customer_id,customer_name,customer_email,amount,payment_method,status,failure_reason,failure_code,previous_successes,previous_failures,retry_count,created_at) VALUES
(121,'pay_syn_10115','cust_9786','Pooja Mehta','pooja.mehta66@example.com',999.0,'Credit Card','FAILED','card_expired','ERR_CARD_EXPIRED',2,2,0,'2026-09-02 13:04:07.139653'),
(122,'pay_syn_10116','cust_9931','Kavya Nair','kavya.nair34@example.com',999.0,'UPI','FAILED','network_error','ERR_NETWORK_ERROR',5,0,0,'2026-08-31 11:04:07.139808'),
(123,'pay_syn_10117','cust_3031','Ishita Banerjee','ishita.banerjee41@example.com',35000.0,'Credit Card','FAILED','bank_timeout','ERR_BANK_TIMEOUT',4,1,1,'2026-09-02 21:04:07.139979'),
(124,'pay_syn_10118','cust_8460','Simran Gill','simran.gill28@example.com',1499.0,'UPI','FAILED','card_expired','ERR_CARD_EXPIRED',4,2,1,'2026-09-04 01:04:07.140159'),
(125,'pay_syn_10119','cust_3079','Nitin Saxena','nitin.saxena13@example.com',35000.0,'UPI','FAILED','card_expired','ERR_CARD_EXPIRED',4,2,0,'2026-09-03 17:04:07.140345'),
(126,'pay_syn_10120','cust_3038','Kavya Nair','kavya.nair16@example.com',999.0,'Netbanking','FAILED','fraud_flag','ERR_FRAUD_FLAG',3,3,2,'2026-09-01 22:04:07.140509'),
(127,'pay_syn_10121','cust_5702','Shruti Agarwal','shruti.agarwal23@example.com',499.0,'Credit Card','FAILED','fraud_flag','ERR_FRAUD_FLAG',6,2,3,'2026-09-01 05:04:07.140664'),
(128,'pay_syn_10122','cust_5923','Aarav Sharma','aarav.sharma17@example.com',18500.0,'Netbanking','RECOVERED','network_error','ERR_NETWORK_ERROR',5,3,0,'2026-08-30 20:04:07.140830'),
(129,'pay_syn_10123','cust_3215','Ishita Banerjee','ishita.banerjee87@example.com',3500.0,'UPI','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',4,2,3,'2026-09-01 11:04:07.141173'),
(130,'pay_syn_10124','cust_5716','Meera Sen','meera.sen47@example.com',35000.0,'Netbanking','FAILED','bank_timeout','ERR_BANK_TIMEOUT',6,1,3,'2026-09-02 06:04:07.141482'),
(131,'pay_syn_10125','cust_4776','Siddharth Malhotra','siddharth.malhotra62@example.com',7500.0,'Netbanking','FAILED','network_error','ERR_NETWORK_ERROR',2,3,2,'2026-09-01 02:04:07.141665'),
(132,'pay_syn_10126','cust_9811','Kavya Nair','kavya.nair57@example.com',999.0,'Credit Card','RECOVERED','network_error','ERR_NETWORK_ERROR',0,0,3,'2026-09-04 03:04:07.141835'),
(133,'pay_syn_10127','cust_2491','Vikram Singh','vikram.singh81@example.com',7500.0,'Debit Card','FAILED','bank_timeout','ERR_BANK_TIMEOUT',5,3,0,'2026-09-03 03:04:07.142190'),
(134,'pay_syn_10128','cust_4880','Varun Bhatia','varun.bhatia49@example.com',12500.0,'UPI','RECOVERED','fraud_flag','ERR_FRAUD_FLAG',5,3,1,'2026-08-31 03:04:07.142486'),
(135,'pay_syn_10129','cust_5011','Manish Kumar','manish.kumar81@example.com',15000.0,'UPI','FAILED','card_expired','ERR_CARD_EXPIRED',3,0,2,'2026-09-04 12:04:07.142836')
ON CONFLICT (payment_id) DO NOTHING;