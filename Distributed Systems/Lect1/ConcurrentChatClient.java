// import java.io.BufferedReader;
// import java.io.IOException;
// import java.io.InputStreamReader;
// import java.io.PrintWriter;
// import java.net.Socket;
// import java.util.Scanner;

// public class ConcurrentChatClient {

//     public static void main(String[] args) {
//         try {
//             Socket socket = new Socket("localhost", 4444);
//             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
//             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
//             Scanner scanner = new Scanner(System.in);
//             String userInput;
//             String serverResponse;
//             String clientName = "empty";

//             ClientThread clientThread = new ClientThread();
//             clientThread.start();

//             while (true) {
//                 if(clientName.equals("empty")) {
//                     System.out.println("Enter your name: ");
//                     clientName = scanner.nextLine();
//                     out.println(clientName);
//                     if("exit".equalsIgnoreCase(clientName)) {
//                         break;
//                     }
//                 } else {
//                     String message = in.readLine();
//                     userInput = scanner.nextLine();
//                     out.println(userInput);
//                     if ("exit".equalsIgnoreCase(userInput)) {
//                         break;
//                     }
//                 }
//             }
//             System.out.println("Type your messages (type 'exit' to quit):");
//             System.out.print("Client: ");
//         } catch (IOException e) {
//             e.printStackTrace();
//         }
//     }
    
//     public class ClientThread extends Thread {

//     }
// }
