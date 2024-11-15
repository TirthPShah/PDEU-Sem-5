Lamport's Logical Clock Simulation

Description

This project simulates a distributed system using Lamport's Logical Clocks to order events in a system with multiple processes. Each process maintains its own logical clock and vector clock, and these clocks are used to ensure events are correctly ordered, even without a global clock. The simulation demonstrates basic concepts of distributed systems and logical clocks through message passing and event logging.

Features

• Lamport's Logical Clock: Implements Lamport's algorithm where clocks are updated based on internal events, send events, and receive events.
• Vector Clocks: Extends the simulation by implementing vector clocks for a more accurate representation of event ordering across processes.
• Event Logging: Logs every event (internal, send, receive) along with the logical clock and vector clock values in a file (LamportLog.txt).
• Process Communication: Simulates communication between processes through a shared buffer acting as a mailbox.
• Random Event Generation: Processes randomly perform internal events, send messages, or receive messages to simulate asynchronous distributed systems.
• Completion Logging: Each process logs its final clock values upon completing a set number of iterations.

Prerequisites

• Java Development Kit (JDK): Ensure JDK is installed on your machine (version 8 or higher).
• IDE or Terminal: You can run this simulation using any Java-supporting IDE or directly from the terminal.

Compilation

To compile the simulation code, navigate to the directory containing the source files and run the following command:

javac LamportLogicalClock.java

Running the Simulation

To start the simulation, execute the following command in your terminal or command prompt:

java LamportLogicalClock

The simulation will run with three processes, each performing a set of random events.

Usage

• Internal Events: Each process can perform internal events, incrementing its logical clock and vector clock.
• Send Events: Processes can send messages to other processes, attaching their current clock values.
• Receive Events: Processes can receive messages, updating their clocks based on the received values.
• Event Logging: All events are logged in LamportLog.txt, providing a detailed record of the simulation.

Request/Response Protocol

• Send Event: When a process sends a message, it increments its logical clock, updates its vector clock, and sends the message with these clocks attached.
• Receive Event: Upon receiving a message, the process updates its clocks by comparing the received clocks with its own, ensuring events are correctly ordered.

Error Handling

• Message Queue Overflow: The simulation handles cases where the message queue might overflow by limiting the buffer size and gracefully managing overflows.
• Interrupted Threads: The simulation includes error handling to manage thread interruptions during sleep or wait states.

Limitations and Future Improvements

• Single-Threaded Processes: Currently, each process runs in its own thread, which limits scalability. Future improvements could include more sophisticated thread management or distributed system simulation across multiple machines.
• Enhanced Logging: The logging could be enhanced with more detailed timestamps and additional context for each event.
• Conflict Resolution: Implementing a scenario with resource conflict resolution using Lamport's clocks could further demonstrate the utility of logical clocks in distributed systems.

Conclusion

This project provides a clear demonstration of Lamport's Logical Clock in a distributed system, showcasing how processes can maintain a consistent event order without a global clock. The extension to vector clocks further illustrates the complexities of distributed computing and the need for accurate event ordering.
