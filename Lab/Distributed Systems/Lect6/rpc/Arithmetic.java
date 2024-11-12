package rpc;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface Arithmetic extends Remote {
    int add(int a, int b) throws RemoteException;
    int subtract(int a, int b) throws RemoteException;
    int multiply(int a, int b) throws RemoteException;
    float divide(int a, int b) throws RemoteException;
}
