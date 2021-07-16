package my.djinnilibrary;

/**
 * Loads the native binary.
 * Instantiate this class once in the static block before using any functionality from this library.
 *
 * ```java
 * public class MainActivity extends Activity {
 *     static {
 *         MyDjinniLibrary()
 *     }
 * }
 * ```
 */
public class MyDjinniLibrary {

    // Used to load the 'MyDjinniLibrary' library on first usage.
    static {
        System.loadLibrary("MyDjinniLibrary");
    }

}