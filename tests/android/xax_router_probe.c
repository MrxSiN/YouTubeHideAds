/* Test-only lookup/ownership adapter. The XAX graph performs the BF JNI call. */
#include <jni.h>
extern jobject youtubehideads_xax_router_call(JNIEnv *, jclass, jmethodID, jbyteArray);

JNIEXPORT jbyteArray JNICALL Java_XaxTransportProbe_xaxDispatch
    (JNIEnv *env, jclass ignored, jbyteArray input) {
    (void)ignored;
    if (input == NULL) {
        jclass error = (*env)->FindClass(env, "java/lang/IllegalArgumentException");
        if (error != NULL) {
            (*env)->ThrowNew(env, error, "NULL_TEST_INPUT");
            (*env)->DeleteLocalRef(env, error);
        }
        return NULL;
    }
    jclass router = (*env)->FindClass(env, "org/youtubehideads/bf/dispatch_all");
    if (router == NULL) return NULL;
    jmethodID method = (*env)->GetStaticMethodID(env, router, "run", "([B)[B");
    if (method == NULL) {
        (*env)->DeleteLocalRef(env, router);
        return NULL;
    }
    jobject output = youtubehideads_xax_router_call(env, router, method, input);
    (*env)->DeleteLocalRef(env, router);
    if ((*env)->ExceptionCheck(env)) {
        if (output != NULL) (*env)->DeleteLocalRef(env, output);
        return NULL;
    }
    return (jbyteArray)output;
}
