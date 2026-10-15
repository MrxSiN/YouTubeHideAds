// BUILD-ONLY TEST HARNESS. Not shipped to Android; no application feature policies.
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.reflect.InvocationTargetException;
import java.util.HexFormat;

public final class Runner {
    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        for (String line; (line = in.readLine()) != null;) {
            if (line.equals("END")) break;
            String[] fields = line.split(" ", 2);
            try {
                Class<?> type = Class.forName("org.youtubehideads.bf." + fields[0]);
                byte[] result = (byte[])type.getMethod("run", byte[].class)
                        .invoke(null, (Object)HexFormat.of().parseHex(fields[1]));
                System.out.println("OK " + HexFormat.of().formatHex(result));
            } catch (InvocationTargetException e) {
                System.out.println("ERR " + e.getCause().getMessage());
            }
        }
    }
}
