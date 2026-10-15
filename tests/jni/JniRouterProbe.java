// TEST HARNESS ONLY — not bundled in an Android APK or generated as app logic.
// Calls compiled Brainfuck through a genuine native JNI round trip.
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLClassLoader;
import java.nio.file.Path;
import java.util.HexFormat;

public final class JniRouterProbe {
    static { System.loadLibrary("bfr_jni_probe"); }
    private static native byte[] callRouter(byte[] input);
    private static native byte[] callRouterWithLoader(ClassLoader loader, byte[] input);
    private static native byte[] callRouterWithValidatedLoader(ClassLoader loader, byte[] input);
    private static native boolean systemLoaderSeesRouter();

    public static void main(String[] args) throws Exception {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        HexFormat hex = HexFormat.of();
        // One isolated loader, one delegating child, and a deliberately hostile
        // ClassLoader. All are test-only; they own zero application features.
        URL[] urls = args.length == 0 ? new URL[0] :
                new URL[] { Path.of(args[0]).toUri().toURL() };
        try (URLClassLoader isolated = new URLClassLoader(urls, null);
             URLClassLoader parent = new URLClassLoader(urls, null);
             URLClassLoader delegatingChild = new URLClassLoader(new URL[0], parent)) {
            ClassLoader spoof = new ClassLoader(null) {
                @Override public Class<?> loadClass(String name) throws ClassNotFoundException {
                    if (name.equals("org.youtubehideads.bf.dispatch_all")) return String.class;
                    return super.loadClass(name);
                }
            };
            for (String line; (line = reader.readLine()) != null; ) {
                if (line.equals("END")) break;
                try {
                    if (line.equals("SYSTEM_CLASS_VISIBILITY")) {
                        System.out.println("VISIBLE " + systemLoaderSeesRouter());
                        continue;
                    }
                    boolean viaLoader = line.startsWith("LOAD:") ||
                            line.startsWith("LOAD_UNCHECKED:") || line.startsWith("LOAD_PARENT:") ||
                            line.startsWith("LOAD_SPOOF:") || line.startsWith("LOAD_NULL_LOADER:");
                    boolean unchecked = line.startsWith("LOAD_UNCHECKED:");
                    ClassLoader requested = line.startsWith("LOAD_PARENT:") ? delegatingChild :
                            line.startsWith("LOAD_SPOOF:") ? spoof :
                            line.startsWith("LOAD_NULL_LOADER:") ? null : isolated;
                    if (viaLoader) line = line.substring(line.indexOf(':') + 1);
                    byte[] raw = line.equals("NULL") ? null : hex.parseHex(line);
                    byte[] result = viaLoader ?
                            (unchecked ? callRouterWithLoader(requested, raw) :
                                    callRouterWithValidatedLoader(requested, raw)) : callRouter(raw);
                    if (result == null) throw new AssertionError("JNI returned null without an exception");
                    System.out.println("OK " + hex.formatHex(result));
                } catch (Throwable ex) {
                    System.out.println("ERR " + ex.getClass().getName() + ":" + ex.getMessage());
                }
            }
        }
    }
}
