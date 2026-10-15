/*
 * TEST HARNESS ONLY — NEVER linked or packaged with the Android module.
 * Exercises JNI loader isolation, exact defining-loader provenance, and the
 * actual Brainfuck AOT router. There is no application feature rule in C.
 */
#include <jni.h>
#include <string.h>

static void reject(JNIEnv *env, const char *reason) {
    /* Never replace an unrelated pending JNI exception. */
    if ((*env)->ExceptionCheck(env)) return;
    jclass error = (*env)->FindClass(env, "java/lang/SecurityException");
    if (error != NULL && !(*env)->ExceptionCheck(env)) {
        (*env)->ThrowNew(env, error, reason);
    }
    if (error != NULL) (*env)->DeleteLocalRef(env, error);
}

static jbyteArray run_resolved(JNIEnv *env, jclass router, jbyteArray input) {
    jmethodID run = (*env)->GetStaticMethodID(env, router, "run", "([B)[B");
    if (run == NULL || (*env)->ExceptionCheck(env)) return NULL;
    jvalue values[1];
    values[0].l = input;
    jobject result = (*env)->CallStaticObjectMethodA(env, router, run, values);
    if ((*env)->ExceptionCheck(env)) return NULL;
    return (jbyteArray)result;
}

JNIEXPORT jboolean JNICALL Java_JniRouterProbe_systemLoaderSeesRouter
    (JNIEnv *env, jclass ignored) {
    (void)ignored;
    jclass router = (*env)->FindClass(env, "org/youtubehideads/bf/dispatch_all");
    if (router == NULL) {
        /* Only this test diagnostic clears its expected class-not-found error. */
        if ((*env)->ExceptionCheck(env)) (*env)->ExceptionClear(env);
        return JNI_FALSE;
    }
    (*env)->DeleteLocalRef(env, router);
    return JNI_TRUE;
}

JNIEXPORT jbyteArray JNICALL Java_JniRouterProbe_callRouter
    (JNIEnv *env, jclass ignored, jbyteArray input) {
    (void)ignored;
    if (input == NULL) {
        jclass error = (*env)->FindClass(env, "java/lang/IllegalArgumentException");
        if (error != NULL) {
            (*env)->ThrowNew(env, error, "NULL_BRAINFUCK_INPUT");
            (*env)->DeleteLocalRef(env, error);
        }
        return NULL;
    }
    jclass router = (*env)->FindClass(env, "org/youtubehideads/bf/dispatch_all");
    if (router == NULL || (*env)->ExceptionCheck(env)) return NULL;
    jbyteArray result = run_resolved(env, router, input);
    (*env)->DeleteLocalRef(env, router);
    return result;
}

/*
 * Exact defining-loader check: ClassLoader.loadClass may delegate to a parent,
 * or be overridden to return a different Class entirely. In neither case may
 * a same-spelled method be treated as the module's verified Brainfuck code.
 */
static int verify_router_provenance(JNIEnv *env, jclass router, jobject loader) {
    static const char expected[] = "org.youtubehideads.bf.dispatch_all";
    int accepted = 0;
    jclass classClass = NULL;
    jstring binaryName = NULL;
    jobject definingLoader = NULL;
    const char *name = NULL;

    classClass = (*env)->GetObjectClass(env, router);
    if (classClass == NULL || (*env)->ExceptionCheck(env)) goto cleanup;
    jmethodID getName = (*env)->GetMethodID(env, classClass, "getName", "()Ljava/lang/String;");
    if (getName == NULL || (*env)->ExceptionCheck(env)) goto cleanup;
    jmethodID getClassLoader = (*env)->GetMethodID(env, classClass, "getClassLoader", "()Ljava/lang/ClassLoader;");
    if (getClassLoader == NULL || (*env)->ExceptionCheck(env)) goto cleanup;
    binaryName = (jstring)(*env)->CallObjectMethodA(env, router, getName, NULL);
    if (binaryName == NULL || (*env)->ExceptionCheck(env)) goto cleanup;
    name = (*env)->GetStringUTFChars(env, binaryName, NULL);
    if (name == NULL || (*env)->ExceptionCheck(env)) goto cleanup;
    int validName = strcmp(name, expected) == 0;
    (*env)->ReleaseStringUTFChars(env, binaryName, name);
    name = NULL;
    if (!validName) {
        reject(env, "ROUTER_CLASS_NAME_MISMATCH");
        goto cleanup;
    }
    definingLoader = (*env)->CallObjectMethodA(env, router, getClassLoader, NULL);
    if ((*env)->ExceptionCheck(env)) goto cleanup;
    if (!(*env)->IsSameObject(env, definingLoader, loader)) {
        reject(env, "ROUTER_LOADER_PROVENANCE_MISMATCH");
        goto cleanup;
    }
    accepted = 1;
cleanup:
    if (name != NULL) (*env)->ReleaseStringUTFChars(env, binaryName, name);
    if (definingLoader != NULL) (*env)->DeleteLocalRef(env, definingLoader);
    if (binaryName != NULL) (*env)->DeleteLocalRef(env, binaryName);
    if (classClass != NULL) (*env)->DeleteLocalRef(env, classClass);
    return accepted;
}

static jbyteArray with_loader(JNIEnv *env, jobject loader, jbyteArray input, int verify) {
    jbyteArray result = NULL;
    jclass loaderClass = NULL;
    jstring binaryName = NULL;
    jclass router = NULL;
    if (loader == NULL || input == NULL) {
        jclass error = (*env)->FindClass(env, "java/lang/IllegalArgumentException");
        if (error != NULL) {
            (*env)->ThrowNew(env, error, loader == NULL ?
                "NULL_MODULE_CLASS_LOADER" : "NULL_BRAINFUCK_INPUT");
            (*env)->DeleteLocalRef(env, error);
        }
        return NULL;
    }
    loaderClass = (*env)->GetObjectClass(env, loader);
    if (loaderClass == NULL || (*env)->ExceptionCheck(env)) goto cleanup;
    jmethodID loadClass = (*env)->GetMethodID(env, loaderClass,
        "loadClass", "(Ljava/lang/String;)Ljava/lang/Class;");
    if (loadClass == NULL || (*env)->ExceptionCheck(env)) goto cleanup;
    binaryName = (*env)->NewStringUTF(env, "org.youtubehideads.bf.dispatch_all");
    if (binaryName == NULL || (*env)->ExceptionCheck(env)) goto cleanup;
    jvalue args[1];
    args[0].l = binaryName;
    router = (jclass)(*env)->CallObjectMethodA(env, loader, loadClass, args);
    if (router == NULL || (*env)->ExceptionCheck(env)) goto cleanup;
    if (verify && !verify_router_provenance(env, router, loader)) goto cleanup;
    result = run_resolved(env, router, input);
cleanup:
    if (router != NULL) (*env)->DeleteLocalRef(env, router);
    if (binaryName != NULL) (*env)->DeleteLocalRef(env, binaryName);
    if (loaderClass != NULL) (*env)->DeleteLocalRef(env, loaderClass);
    return result;
}

JNIEXPORT jbyteArray JNICALL Java_JniRouterProbe_callRouterWithLoader
    (JNIEnv *env, jclass ignored, jobject loader, jbyteArray input) {
    (void)ignored;
    return with_loader(env, loader, input, 0);  /* pre-existing test oracle */
}

JNIEXPORT jbyteArray JNICALL Java_JniRouterProbe_callRouterWithValidatedLoader
    (JNIEnv *env, jclass ignored, jobject loader, jbyteArray input) {
    (void)ignored;
    return with_loader(env, loader, input, 1);
}
