package concurrent;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;
import java.lang.Thread;

public class ConcurrentServerThread extends Thread {
    
    private Socket socket;
    private ArrayList<ConcurrentServerThread> threadList;
    private PrintWriter output;

    public ConcurrentServerThread(Socket socket, ArrayList<ConcurrentServerThread> threadList) {
        this.socket = socket;
        this.threadList = threadList;
    }

    @Override
    public void run() {
        try {
            
            BufferedReader input = new BufferedReader(new InputStreamReader((socket.getInputStream())));
            output = new PrintWriter(socket.getOutputStream(), true);

            while(true) {
                String outputString = input.readLine();

                if (outputString.equals("exit")) {
                    break;
                }

                printToAllClients(outputString);

                System.out.println("Serer recieved: " + outputString);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void printToAllClients(String outputString) {
        for (ConcurrentServerThread sth : threadList) {
            sth.output.println(outputString);
        }
    }
}
