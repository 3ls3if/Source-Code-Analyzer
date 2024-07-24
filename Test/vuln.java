    import java.sql.Connection;
    import java.sql.DriverManager;
    import java.io.File;
    import javax.crypto.Cipher;
    import java.util.Random;

    public class Test {
        public static void main(String[] args) {
            // Unsafe code snippets
            File file = new File("test.txt");
            Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/mydb", "user", "pass");
            Cipher cipher = Cipher.getInstance("DES");
            Random rand = new Random();
            System.out.println("Hello World");
        }
    }
