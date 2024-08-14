package concurrent;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;
import concurrent.ConcurrentChatClientThread;

public class ConcurrentChatClientMain {
    public static void main(String[] args) {
        
        try (Socket socket = new Socket("localhost", 5000)) {

            BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter output = new PrintWriter(socket.getOutputStream(), true);

            Scanner scanner = new Scanner(System.in);
            String userInput;
            String response;
            String clientName = "empty";

            ConcurrentChatClientThread clientThread = new ConcurrentChatClientThread(socket);
            clientThread.start();

            do {

                if(clientName.equals("empty")) {

                    System.out.println("Enter your name: ");
                    userInput = scanner.nextLine();
                    clientName = userInput;
                    output.println(userInput);

                    if (userInput.equals("exit")) {
                        break;
                    }

                }

                else {

                    String message = ( "(" + clientName + ") " + " message: ");
                    System.out.println(message);
                    userInput = scanner.nextLine();
                    output.println(message + " " + userInput);
                    
                    if (userInput.equals("exit")) {
                        break;
                    }
                }
            } while (!userInput.equals("exit"));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
