INSERT INTO transactions (id,payment_id,customer_id,customer_name,customer_email,amount,payment_method,status,failure_reason,failure_code,previous_successes,previous_failures,retry_count,created_at) VALUES
(151,'pay_syn_10145','cust_5684','Karan Kapoor','karan.kapoor15@example.com',15000.0,'Credit Card','FAILED','card_expired','ERR_CARD_EXPIRED',1,0,3,'2026-09-04 02:04:07.147483'),
(152,'pay_syn_10146','cust_6133','Ishita Banerjee','ishita.banerjee20@example.com',2499.0,'Credit Card','FAILED','bank_timeout','ERR_BANK_TIMEOUT',3,1,2,'2026-09-02 16:04:07.147763'),
(153,'pay_syn_10147','cust_5348','Rahul Deshmukh','rahul.deshmukh59@example.com',499.0,'Debit Card','FAILED','fraud_flag','ERR_FRAUD_FLAG',5,2,0,'2026-09-02 21:04:07.147935'),
(154,'pay_syn_10148','cust_7557','Priya Patel','priya.patel81@example.com',3500.0,'Netbanking','FAILED','card_expired','ERR_CARD_EXPIRED',5,1,2,'2026-09-04 05:04:07.148096'),
(155,'pay_syn_10149','cust_3158','Shruti Agarwal','shruti.agarwal94@example.com',18500.0,'Debit Card','FAILED','card_expired','ERR_CARD_EXPIRED',3,1,0,'2026-09-03 00:04:07.148253'),
(156,'pay_syn_10150','cust_7271','Karan Kapoor','karan.kapoor58@example.com',18500.0,'Debit Card','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',5,0,3,'2026-09-01 22:04:07.148422'),
(157,'pay_syn_10151','cust_4970','Manish Kumar','manish.kumar12@example.com',2499.0,'Debit Card','FAILED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',6,3,1,'2026-09-03 11:04:07.148589'),
(158,'pay_syn_10152','cust_2632','Vikram Singh','vikram.singh29@example.com',12500.0,'Debit Card','FAILED','bank_timeout','ERR_BANK_TIMEOUT',6,0,2,'2026-08-30 23:04:07.148745'),
(159,'pay_syn_10153','cust_3073','Simran Gill','simran.gill89@example.com',1499.0,'Netbanking','RECOVERED','insufficient_funds','ERR_INSUFFICIENT_FUNDS',5,1,3,'2026-09-04 10:04:07.148898'),
(160,'pay_syn_10154','cust_7894','Manish Kumar','manish.kumar96@example.com',15000.0,'Credit Card','FAILED','network_error','ERR_NETWORK_ERROR',5,3,1,'2026-09-01 19:04:07.149234'),
(161,'pay_TEST_NETWORK_HIGH','cust_test_net','Test Network User','testnet@example.com',3000.0,'UPI','FAILED','network_error','NET_ERR',5,0,0,'2026-09-04 16:59:37.625292')
ON CONFLICT (payment_id) DO NOTHING;