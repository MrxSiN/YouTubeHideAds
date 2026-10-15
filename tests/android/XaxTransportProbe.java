// Test-only ART/JNI oracle. Feature decisions come only from compiled BF classes.
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.reflect.Method;
import java.util.Arrays;

public final class XaxTransportProbe {
    private static native byte[] xaxDispatch(byte[] input);

    private static byte[] hex(String text) {
        if (text.equals("-")) return new byte[0];
        if ((text.length() & 1) != 0) throw new IllegalArgumentException("odd hex length");
        byte[] result = new byte[text.length() / 2];
        for (int i = 0; i < result.length; i++) {
            int high = Character.digit(text.charAt(2 * i), 16);
            int low = Character.digit(text.charAt(2 * i + 1), 16);
            if (high < 0 || low < 0) throw new IllegalArgumentException("invalid hex");
            result[i] = (byte)((high << 4) | low);
        }
        return result;
    }

    public static void main(String[] args) throws Exception {
        System.loadLibrary("xaxprobe");
        Class<?> type = Class.forName("org.youtubehideads.bridge.BinaryTransport");
        Object transport = type.getConstructor().newInstance();
        Method roundTrip = type.getMethod("roundTrip", byte[].class);
        int transportCases = 0;
        for (int length = 0; length <= 256; length++) {
            byte[] input = new byte[length];
            for (int i = 0; i < length; i++) input[i] = (byte)(255 - i);
            byte[] before = input.clone();
            Object output = roundTrip.invoke(transport, (Object)input);
            if (output != input || !Arrays.equals(input, before))
                throw new AssertionError("XAX borrowed-array identity/content mismatch");
            transportCases++;
        }
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in, "US-ASCII"));
        int count = 0;
        int xaxCalls = 0;
        for (String line; (line = reader.readLine()) != null;) {
            String[] fields = line.split(" ");
            if (fields.length != 3) throw new IllegalArgumentException("bad test vector");
            Method run = Class.forName("org.youtubehideads.bf." + fields[0])
                    .getMethod("run", byte[].class);
            byte[] output = (byte[])run.invoke(null, (Object)hex(fields[1]));
            byte[] echoed = (byte[])roundTrip.invoke(transport, (Object)output);
            if (echoed != output || !Arrays.equals(echoed, hex(fields[2])))
                throw new AssertionError("ART/BF/XAX mismatch at " + fields[0] + " vector " + count);
            if (fields[0].equals("dispatch_all")) {
                byte[] nativeOutput = xaxDispatch(hex(fields[1]));
                if (!Arrays.equals(nativeOutput, hex(fields[2])))
                    throw new AssertionError("XAX to BF mismatch at vector " + count);
                xaxCalls++;
            }
            count++;
        }
        if (count == 0) throw new AssertionError("no BF vectors");
        if (xaxDispatch(new byte[]{0}).length != 0 || xaxDispatch(new byte[]{(byte)255}).length != 0)
            throw new AssertionError("invalid BF selector produced output");
        try {
            xaxDispatch(null);
            throw new AssertionError("null input accepted");
        } catch (IllegalArgumentException expected) { }
        System.out.println("PASS transport=" + transportCases + " bf=" + count + " xax_calls=" + xaxCalls);
    }
}
