INSERT INTO transactions (id,payment_id,customer_id,customer_name,customer_email,amount,payment_method,status,failure_reason,failure_code,previous_successes,previous_failures,retry_count,created_at) VALUES
(91,'pay_syn_10085','cust_4730','Manish Kumar','manish.kumar62@example.com',1499.0,'Debit Card','FAILED','bank_timeout','ERR_BANK_TIMEOUT',5,3,2,'2026-09-01 03:04:07.132685'),
(92,'pay_syn_10086','cust_2300','Deepika Iyer','deepika.iyer80@example.com',4999.0,'Netbanking','FAILED','bank_timeout','ERR_BANK_TIMEOUT',0,3,0,'2026-09-01 03:04:07.132855'),
(93,'pay_syn_10087','cust_5385','Karan Kapoor','karan.kapoor69@example.com',12500.0,'UPI','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',6,3,3,'2026-08-31 14:04:07.133016'),
(94,'pay_syn_10088','cust_4187','Ananya Verma','ananya.verma36@example.com',9999.0,'Credit Card','FAILED','card_expired','ERR_CARD_EXPIRED',3,0,0,'2026-09-01 07:04:07.133172'),
(95,'pay_syn_10089','cust_7814','Varun Bhatia','varun.bhatia40@example.com',12500.0,'Credit Card','RECOVERED','card_expired','ERR_CARD_EXPIRED',3,0,1,'2026-08-31 04:04:07.133325'),
(96,'pay_syn_10090','cust_7306','Pooja Mehta','pooja.mehta25@example.com',22000.0,'Credit Card','FAILED','network_error','ERR_NETWORK_ERROR',5,2,3,'2026-08-31 05:04:07.133674'),
(97,'pay_syn_10091','cust_3996','Sanjay Rao','sanjay.rao70@example.com',1499.0,'Netbanking','FAILED','fraud_flag','ERR_FRAUD_FLAG',4,1,0,'2026-09-03 04:04:07.133974'),
(98,'pay_syn_10092','cust_4784','Simran Gill','simran.gill63@example.com',3500.0,'Debit Card','FAILED','bank_timeout','ERR_BANK_TIMEOUT',6,3,1,'2026-09-02 06:04:07.134145'),
(99,'pay_syn_10093','cust_4827','Karan Kapoor','karan.kapoor71@example.com',35000.0,'Debit Card','FAILED','fraud_flag','ERR_FRAUD_FLAG',3,2,1,'2026-08-31 22:04:07.134313'),
(100,'pay_syn_10094','cust_5137','Siddharth Malhotra','siddharth.malhotra83@example.com',499.0,'Credit Card','FAILED','network_error','ERR_NETWORK_ERROR',3,3,3,'2026-09-01 03:04:07.134489'),
(101,'pay_syn_10095','cust_6057','Ritu Choudhury','ritu.choudhury29@example.com',12500.0,'UPI','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',2,0,3,'2026-09-04 03:04:07.134655'),
(102,'pay_syn_10096','cust_2125','Meera Sen','meera.sen68@example.com',18500.0,'Credit Card','FAILED','network_error','ERR_NETWORK_ERROR',0,3,2,'2026-09-02 20:04:07.134814'),
(103,'pay_syn_10097','cust_5256','Varun Bhatia','varun.bhatia98@example.com',18500.0,'UPI','FAILED','card_expired','ERR_CARD_EXPIRED',3,2,3,'2026-08-31 00:04:07.135041'),
(104,'pay_syn_10098','cust_7058','Karan Kapoor','karan.kapoor14@example.com',18500.0,'UPI','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',2,1,0,'2026-09-02 08:04:07.135229'),
(105,'pay_syn_10099','cust_7766','Priya Patel','priya.patel91@example.com',1499.0,'UPI','FAILED','network_error','ERR_NETWORK_ERROR',0,0,2,'2026-08-31 10:04:07.135460')
ON CONFLICT (payment_id) DO NOTHING;