Multi-Client Chat Application
Description
The Multi-Client Chat Application is a Java-based project that facilitates real-time communication between multiple clients over a network. The server handles multiple client connections concurrently, allowing clients to send and receive messages in a whole server chat setting. This application supports basic chat functionalities such as broadcasting messages to all clients, sending private messages, and managing client connections and disconnections.
Features
• Whole Server Chat: All connected clients can participate in a chat where messages are broadcasted to everyone.
• Private Messaging: Clients can send direct messages to specific users by addressing them with their call sign.
• Client List Command: Clients can retrieve a list of all active users in the chat.
• Multi-Threaded Server: The server handles multiple clients simultaneously using a thread pool.
• Timeout Handling: Clients that remain inactive for a specified period are automatically disconnected.
• Graceful Disconnection: Clients can gracefully exit the chat using the @exit command, notifying the server and other clients.
Prerequisites
• Java Development Kit (JDK): Ensure you have JDK installed on your machine (version 8 or higher).
• Network: Both the server and clients should be able to communicate over a common network (e.g., localhost for testing, or over a LAN/WAN).
Compilation
To compile the server and client code, navigate to the directory containing the source files and run the following commands:
javac ChatServer.java
javac ChatClient.java

Running the Application
Starting the Server
To start the server, execute the following command in your terminal or command prompt:
java ChatServer

The server will start listening for client connections on port 4221.
Starting a Client
To start a client, open a new terminal or command prompt and execute the following command:
java ChatClient

The client will prompt you to enter a call sign before connecting to the server. Once connected, you can start sending and receiving messages.
Usage
• Sending Messages: Simply type your message and press Enter to send it to all connected clients.
• Private Messaging: To send a direct message to a specific client, type @<CallSign> <Message> and press Enter.
• Broadcasting Messages: To send a message to all clients, type @broadcast <Message> and press Enter.
• Listing Clients: To see a list of all connected clients, type @list and press Enter.
• Exiting the Chat: Type @exit and press Enter to disconnect from the server. This command also stops the server after the client disconnects.
Request/Response Protocol
Client to Server
• Message Format:
◦ Broadcast: @broadcast <Message> sends the message to all clients.
◦ Private: @<CallSign> <Message> sends the message only to the specified client.
◦ List Clients: @list retrieves the list of all active clients.
◦ Exit: @exit disconnects the client and shuts down the server.
Server to Client
• Broadcast Message: The server broadcasts each message it receives to all connected clients.
• Private Message: The server relays private messages to the intended recipient only.
• Client Connection/Disconnection Notification: The server notifies all clients when a new client joins or leaves the chat.
• Timeout Disconnection: If a client remains inactive for a specified time, the server automatically disconnects them and notifies others.
Test Scenarios
• Basic Whole Server Chat
◦ Objective: Verify that multiple clients can participate in a chat where all messages are broadcasted to everyone.
◦ Steps:
▪ Start the server.
▪ Start multiple clients and connect them to the server.
▪ Send messages from each client and verify that all clients receive them.
• Private Messaging
◦ Objective: Demonstrate the ability to send private messages between clients.
◦ Steps:
▪ Start the server.
▪ Start multiple clients and connect them to the server.
▪ Send a private message from one client to another using the @CallSign <Message> format.
▪ Verify that only the intended recipient receives the message.
• Listing Clients
◦ Objective: Test the functionality of listing all connected clients.
◦ Steps:
▪ Start the server.
▪ Start multiple clients and connect them to the server.
▪ Use the @list command from any client to retrieve the list of connected clients.
• Graceful Disconnection
◦ Objective: Ensure that clients can gracefully disconnect using the @exit command.
◦ Steps:
▪ Start the server.
▪ Start multiple clients and connect them to the server.
▪ Use the @exit command from one client and verify that the client disconnects, notifying others.
▪ The server should also shut down after the client disconnects.
• Timeout Handling
◦ Objective: Verify that clients are automatically disconnected after being inactive for a specified period.
◦ Steps:
▪ Start the server.
▪ Start multiple clients and connect them to the server.
▪ Ensure that one of the clients remains inactive for the timeout period.
▪ Verify that the inactive client is disconnected, and other clients are notified of the disconnection.
▪ 
Error Handling
• Connection Failures: If a client fails to connect to the server, an error message is displayed, and the client terminates.
• Abrupt Disconnection: The server gracefully handles abrupt disconnections, ensuring other clients are notified.
• Message Sending Errors: If a message fails to send, the client attempts to close the connection gracefully.
Limitations and Future Improvements
• Scalability: The current implementation is designed for a small number of clients. Scaling to handle more clients may require optimizations such as load balancing.
• Security: Messages are sent in plain text, making the communication vulnerable to interception. Future versions could implement encryption for secure communication.
• GUI Interface: Currently, the client is console-based. A graphical user interface (GUI) could be developed for a more user-friendly experience.
• Advanced Features: Future improvements could include implementing chat rooms, message history, and file-sharing capabilities.
