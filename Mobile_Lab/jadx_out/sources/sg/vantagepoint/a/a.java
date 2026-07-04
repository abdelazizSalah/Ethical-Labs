package sg.vantagepoint.a;

import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import javax.crypto.Cipher;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.SecretKeySpec;

/* JADX INFO: loaded from: classes.dex */
public class a {
    public static byte[] a(byte[] bArr, byte[] bArr2) throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException {
        '''
            This function is doing AES decryption
            bArr is the AES key
            bArr2 is the data
            it returns the decrypted data as plaintext
        '''
        
        // Creating a key object from bArr in AES algorithm using ECB mode with PKCS7 padding method
        SecretKeySpec secretKeySpec = new SecretKeySpec(bArr, "AES/ECB/PKCS7Padding");

        // Creating AES cipher object
        Cipher cipher = Cipher.getInstance("AES");

        // 2 means decrypt mode
        cipher.init(2, secretKeySpec);

        // doFinal performs the decryption
        return cipher.doFinal(bArr2);
    }
}
