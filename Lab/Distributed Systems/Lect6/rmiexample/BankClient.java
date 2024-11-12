// BankClient.java
package rmiexample;

import java.rmi.Naming;
import java.util.Scanner;

public class BankClient {
    public static void main(String[] args) {
        try {
            Bank bank = (Bank) Naming.lookup("rmi://localhost/BankServer");
            Scanner scanner = new Scanner(System.in);
            int accountId;
            double amount;

            while (true) {
                System.out.println("1. Create Account");
                System.out.println("2. Check Balance");
                System.out.println("3. Deposit");
                System.out.println("4. Withdraw");
                System.out.println("5. Exit");
                System.out.print("Choose an option: ");
                int option = scanner.nextInt();

                switch (option) {
                    case 1:
                        System.out.print("Enter account holder name: ");
                        String name = scanner.next();
                        accountId = bank.createAccount(name);
                        System.out.println("Account created with ID: " + accountId);
                        break;
                    case 2:
                        System.out.print("Enter account ID: ");
                        accountId = scanner.nextInt();
                        double balance = bank.getBalance(accountId);
                        System.out.println("Current balance: " + balance);
                        break;
                    case 3:
                        System.out.print("Enter account ID: ");
                        accountId = scanner.nextInt();
                        System.out.print("Enter amount to deposit: ");
                        amount = scanner.nextDouble();
                        bank.deposit(accountId, amount);
                        System.out.println("Deposited: " + amount);
                        break;
                    case 4:
                        System.out.print("Enter account ID: ");
                        accountId = scanner.nextInt();
                        System.out.print("Enter amount to withdraw: ");
                        amount = scanner.nextDouble();
                        boolean success = bank.withdraw(accountId, amount);
                        if (success) {
                            System.out.println("Withdrawn: " + amount);
                        } else {
                            System.out.println("Insufficient funds.");
                        }
                        break;
                    case 5:
                        scanner.close();
                        System.exit(0);
                        break;
                    default:
                        System.out.println("Invalid option.");
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
