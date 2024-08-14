package concurrent;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.lang.Thread;

public class ConcurrentChatClientThread extends Thread {

    private Socket socket;
    private BufferedReader input;

    public ConcurrentChatClientThread(Socket s) throws IOException {
        this.socket = s;
        this.input = new BufferedReader(new InputStreamReader((socket.getInputStream())));
    }

    @Override
    public void run() {
        
        try {
            while(true) {
                String response = input.readLine();
                System.out.println(response);
            }
        }

        catch (IOException e) {
            e.printStackTrace();
        }

        finally {
            try {
                input.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}   