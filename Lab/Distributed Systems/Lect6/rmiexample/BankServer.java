// BankServer.java
package rmiexample;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.HashMap;
import java.util.Map;

public class BankServer extends UnicastRemoteObject implements Bank {
    private Map<Integer, BankAccount> accounts;
    private int nextAccountId;

    public BankServer() throws RemoteException {
        accounts = new HashMap<>();
        nextAccountId = 1; // Start account IDs from 1
    }

    @Override
    public synchronized int createAccount(String accountHolderName) throws RemoteException {
        BankAccount newAccount = new BankAccount(accountHolderName);
        accounts.put(nextAccountId, newAccount);
        return nextAccountId++;
    }

    @Override
    public synchronized double getBalance(int accountId) throws RemoteException {
        BankAccount account = accounts.get(accountId);
        if (account != null) {
            return account.getBalance();
        }
        throw new RemoteException("Account not found");
    }

    @Override
    public synchronized void deposit(int accountId, double amount) throws RemoteException {
        BankAccount account = accounts.get(accountId);
        if (account != null) {
            account.deposit(amount);
        } else {
            throw new RemoteException("Account not found");
        }
    }

    @Override
    public synchronized boolean withdraw(int accountId, double amount) throws RemoteException {
        BankAccount account = accounts.get(accountId);
        if (account != null) {
            return account.withdraw(amount);
        }
        throw new RemoteException("Account not found");
    }
    
    public static void main(String[] args) {
        try {
            BankServer server = new BankServer();
            java.rmi.registry.LocateRegistry.createRegistry(1099);
            java.rmi.Naming.rebind("BankServer", server);
            System.out.println("Bank Server is running...");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
