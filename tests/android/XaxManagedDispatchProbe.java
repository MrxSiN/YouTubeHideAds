// Test-only ART oracle. No native library or conventional feature implementation.
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Arrays;

public final class XaxManagedDispatchProbe {
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
        if (args.length != 1) throw new IllegalArgumentException("XAX class name required");
        Method dispatch = Class.forName(args[0]).getMethod("entry", byte[].class);
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in, "US-ASCII"));
        int count = 0;
        for (String line; (line = reader.readLine()) != null;) {
            String[] fields = line.split(" ");
            if (fields.length != 3 || !fields[0].equals("dispatch_all"))
                throw new IllegalArgumentException("bad routed vector");
            byte[] input = hex(fields[1]);
            byte[] original = input.clone();
            byte[] actual = (byte[])dispatch.invoke(null, (Object)input);
            if (!Arrays.equals(actual, hex(fields[2])) || !Arrays.equals(input, original))
                throw new AssertionError("XAX/BF mismatch at vector " + count);
            count++;
        }
        if (count == 0) throw new AssertionError("no BF vectors");
        for (byte[] invalid : new byte[][] {new byte[0], {0}, {(byte)255}}) {
            if (((byte[])dispatch.invoke(null, (Object)invalid)).length != 0)
                throw new AssertionError("invalid selector produced an action");
        }
        try {
            dispatch.invoke(null, new Object[]{null});
            throw new AssertionError("null input accepted");
        } catch (InvocationTargetException expected) {
            if (!(expected.getCause() instanceof NullPointerException)) throw expected;
        }
        // A failed invocation must not poison subsequent calls.
        byte[] pass = (byte[])dispatch.invoke(null, (Object)new byte[]{1, 0, 0, 0, 0});
        if (!Arrays.equals(pass, new byte[]{0})) throw new AssertionError("failure recovery");
        System.out.println("PASS managed_xax_bf=" + count + " invalid=4 recovery=1 native_libraries=0");
    }
}
