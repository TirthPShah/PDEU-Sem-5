Single-Client Server Chat Application
Description
The Single-Client Server Chat Application is a Java-based project that demonstrates basic client-server communication. The server echoes messages received from the client and can also independently send messages to the client. Additionally, both the client and the server are capable of gracefully shutting down when the client sends an exit() command.
Features
• Echo Messaging: The server echoes back any message sent by the client, demonstrating basic request-response communication.
• Server-Initiated Messaging: The server can send messages to the client independently, without waiting for a client prompt.
• Graceful Shutdown: When the client sends the exit() command, both the client and the server shut down in a controlled manner.
Prerequisites
• Java Development Kit (JDK): Ensure JDK is installed on your machine (version 8 or higher).
• Network: The client and server should be able to communicate over a common network (localhost is sufficient for testing).

Compilation
To compile the server and client code, navigate to the directory containing the source files and run the following commands:

javac EchoServer.java
javac EchoClient.java

Running the Application
Starting the Server
To start the server, execute the following command in your terminal or command prompt:

java EchoServer

The server will start listening for client connections on port 5000.
Starting the Client
To start the client, open a new terminal or command prompt and execute the following command:
java EchoClient

The client will attempt to connect to the server at localhost on port 5000. Upon successful connection, a confirmation message will be displayed.
Usage
• Sending Messages: Type your message and press Enter to send it to the server. The server will echo the message back.
• Receiving Server Messages: The server can send messages to the client at any time, which will be displayed in the client terminal.
• Exiting the Chat: Type exit() and press Enter to gracefully disconnect from the server. Both the client and server will shut down.
Request/Response Protocol
Client to Server
• Message Format: Messages are sent as plain text and are echoed back by the server.
• Command Format: Sending exit() signals the server to stop and initiates the client's shutdown.
Server to Client
• Echoed Messages: The server echoes every message it receives from the client.
• Server-Initiated Messages: The server can send unsolicited messages to the client, which are displayed in the client terminal.
Test Scenarios
1 Client-Initiated Messaging (Echo)
◦ Objective: Verify that the server echoes messages sent by the client.
◦ Steps:
• Start the server.
• Start the client and send a message.
• Verify that the message is echoed back by the server.
1 Server-Initiated Messaging
◦ Objective: Demonstrate that the server can send a message to the client without first receiving one.
◦ Steps:
• Start the server.
• Start the client.
• Have the server send a message to the client.
• Verify that the client displays the server's message.
1 Graceful Shutdown (exit() Command)
◦ Objective: Test the shutdown process when the client sends the exit() command.
◦ Steps:
• Start the server.
• Start the client.
• Send the exit() command from the client.
• Verify that both the client and server shut down gracefully.
Error Handling
• Connection Failures: If the client fails to connect to the server, an error message is displayed, and the client terminates.
• Abrupt Disconnection: The server gracefully handles a client disconnecting abruptly (e.g., by closing the terminal), ensuring the server can still be restarted without issues.
Limitations and Future Improvements
• Single Client: The current implementation only supports a single client. Extending this to multiple clients would require handling concurrency with threads or other parallelization techniques.
• Security: The communication is in plain text and could be intercepted. Future versions could implement encryption for secure communication.
• GUI Interface: Currently, the client is console-based. A graphical user interface (GUI) could be developed for a more user-friendly experience.
