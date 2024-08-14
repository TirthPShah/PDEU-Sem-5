package concurrent;

import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class ConcurrentServerMain {
    public static void main(String[] args) {
        ArrayList<ConcurrentServerThread> threadList = new ArrayList<>();

        try(ServerSocket serverSocket = new ServerSocket(5000)) {
            while(true) {
                Socket socket = serverSocket.accept();
                ConcurrentServerThread serverThread = new ConcurrentServerThread(socket, threadList);
                threadList.add(serverThread);
                serverThread.start();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
