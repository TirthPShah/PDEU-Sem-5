package rpc;

import java.rmi.Naming;
import java.util.Scanner;

public class ArithmeticClient {
    public static void main(String[] args) {
        try {
            Arithmetic arithmetic = (Arithmetic) Naming.lookup("rmi://localhost/ArithmeticService");
            Scanner scanner = new Scanner(System.in);
            while (true) {
                System.out.println("Enter two numbers:");
                int a = scanner.nextInt();
                int b = scanner.nextInt();

                System.out.println("Choose an operation:");
                System.out.println("1. Add");
                System.out.println("2. Subtract");
                System.out.println("3. Multiply");
                System.out.println("4. Divide");
                int choice = scanner.nextInt();

                switch (choice) {
                    case 1:
                        System.out.println("Result: " + arithmetic.add(a, b));
                        break;
                    case 2:
                        System.out.println("Result: " + arithmetic.subtract(a, b));
                        break;
                    case 3:
                        System.out.println("Result: " + arithmetic.multiply(a, b));
                        break;
                    case 4:
                        try {
                            System.out.println("Result: " + arithmetic.divide(a, b));
                        } catch (ArithmeticException e) {
                            System.out.println("Error: " + e.getMessage());
                        }
                        break;
                    default:
                        System.out.println("Invalid choice");
                        break;
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
