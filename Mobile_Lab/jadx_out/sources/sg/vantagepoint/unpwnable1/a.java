package sg.vantagepoint.unpwnable1;

import android.util.Base64;
import android.util.Log;

/* JADX INFO: loaded from: classes.dex */
public class a {
    public static boolean a(String str) {
        byte[] bArrA;
        byte[] bArr = new byte[0];
        try {
            bArrA = sg.vantagepoint.a.a.a(b("8d127684cbc37c17616d806cf50473cc"), Base64.decode("5UJiFctbmgbDoLXmpL12mkno8HT4Lv8dlat8FxR2GOc=", 0));
        } catch (Exception e) {
            Log.d("CodeCheck", "AES error:" + e.getMessage());
            bArrA = bArr;
        }
        return str.equals(new String(bArrA));
    }

    public static byte[] b(String str) {
        '''
        This function converts hex string into array of bytes.
        '''
        // compute the length of the input
        int length = str.length();

        // create a byte array of length / 2 as we will consider hex, and each two consecutive hex represent one byte
        byte[] bArr = new byte[length / 2];

        // iterate on the input and increment by 2 because we need to process every two consecutive hex together.
        for (int i = 0; i < length; i += 2) {
            // analyzing the hex value for every 2 consecutive characters and converting them to byte value. 
            // convert each character to hex, shift 4 to left because we want to make it the MSB, then add to it the second char after converting it to decimal
            bArr[i / 2] = (byte) ((Character.digit(str.charAt(i), 16) << 4) + Character.digit(str.charAt(i + 1), 16));
        }
        return bArr; // 1 byte is 8 bits, and 1 hexchar is 4 bits, that is why we divide the length by 2
    }
}
