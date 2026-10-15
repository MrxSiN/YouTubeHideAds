// Read-only device research oracle; never packaged in the module.
import org.luckypray.dexkit.DexKitBridge;
import org.luckypray.dexkit.query.FindMethod;
import org.luckypray.dexkit.query.matchers.MethodMatcher;
import org.luckypray.dexkit.result.MethodData;

public final class DexKitProbe {
    public static void main(String[] args) throws Exception {
        System.load(args[0] + "/libdexkit.so");
        try (DexKitBridge bridge = DexKitBridge.create(args[1])) {
            bridge.setThreadNum(2);
            for (int i = 2; i < args.length; i++) {
                System.out.println("QUERY " + args[i]);
                MethodMatcher matcher = args[i].startsWith("L") && args[i].contains("->")
                    ? MethodMatcher.create(args[i]) : MethodMatcher.create().usingStrings(args[i]);
                if (args[i].equals("DIALOG")) {
                    matcher = MethodMatcher.create().returnType("void").paramTypes(java.util.Arrays.asList("byte[]", null))
                        .addInvoke(MethodMatcher.create().name("show").paramCount(0).returnType("void"));
                }
                for (MethodData m : bridge.findMethod(FindMethod.create().matcher(matcher))) {
                    System.out.println("METHOD " + m.getDescriptor() + " flags=" + m.getModifiers());
                    System.out.println("STRINGS " + m.getUsingStrings());
                    System.out.println("INVOKES " + m.getInvokes());
                    System.out.println("FIELDS " + m.getUsingFields());
                    System.out.println("CLASSFIELDS " + m.getDeclaredClass().getFields());
                    System.out.println("CLASSMETHODS " + m.getDeclaredClass().getMethods());
                }
            }
        }
    }
}
