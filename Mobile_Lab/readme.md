# Solution: 

## Task2 
1. the secret is: I want to believe
2. we got it using the script **./Mobile_Lab/decryption.py**
3. I generated readable files using jadx
    > jadx -d jadx_out Unpawnable.apk
4. then examining the files, I found that it uses AES as encryption scheme, and the used key is stored there which is: 
    - 8d127684cbc37c17616d806cf50473cc
5. and the secret key is encoded using base64, and encrypted with the key
    - 5UJiFctbmgbDoLXmpL12mkno8HT4Lv8dlat8FxR2GOc=
6. so I wrote the script to decrypt it. 

## Task3: 