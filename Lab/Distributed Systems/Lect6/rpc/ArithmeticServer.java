package rpc;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class ArithmeticServer extends UnicastRemoteObject implements Arithmetic {

    protected ArithmeticServer() throws RemoteException {
        super();
    }

    @Override
    public int add(int a, int b) throws RemoteException {
        return a + b;
    }

    @Override
    public int subtract(int a, int b) throws RemoteException {
        return a - b;
    }

    @Override
    public int multiply(int a, int b) throws RemoteException {
        return a * b;
    }

    @Override
    public float divide(int a, int b) throws RemoteException {
        if (b == 0) {
            throw new ArithmeticException("Cannot divide by zero!");
        }
        return (float) a / b;
    }

    public static void main(String[] args) {
        try {
            ArithmeticServer server = new ArithmeticServer();
            java.rmi.Naming.rebind("ArithmeticService", server);
            System.out.println("Server is running...");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
