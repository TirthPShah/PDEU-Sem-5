import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;
import java.util.Random;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.TimeUnit;

// Message class now includes vectorClockOfSender for vector clocks
class Message {
    private int senderId;
    private int receiverId;
    private int timeStamp; // For Lamport clock
    private int[] vectorClockOfSender; // For Vector clock

    // Constructor for Message with vector clock
    public Message(int senderId, int receiverId, int timeStamp, int[] vectorClockOfSender) {
        this.senderId = senderId;
        this.receiverId = receiverId;
        this.timeStamp = timeStamp;
        this.vectorClockOfSender = Arrays.copyOf(vectorClockOfSender, vectorClockOfSender.length);
    }

    public int getSenderId() {
        return senderId;
    }

    public int getReceiverId() {
        return receiverId;
    }

    public int getTimeStamp() {
        return timeStamp;
    }

    public int[] getVectorClockOfSender() {
        return vectorClockOfSender;
    }

    @Override
    public String toString() {
        return "Message from Process " + senderId + " to Process " + receiverId + " at Time " + timeStamp +
               ", Vector Clock: " + Arrays.toString(vectorClockOfSender);
    }
}

// SharedBuffer acts as the mailbox for each process
class SharedBuffer {
    private int ownerId;
    private BlockingQueue<Message> messageQueue;

    public SharedBuffer(int ownerId, int maxSize) {
        this.ownerId = ownerId;
        this.messageQueue = new ArrayBlockingQueue<>(maxSize);
    }

    // Adds a message to the buffer
    public void addMessage(Message message) {
        try {
            messageQueue.put(message);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            e.printStackTrace();
        }
    }

    // Retrieves a message from the buffer, or returns null if none is available
    public Message retrieveMessage() {
        try {
            return messageQueue.poll(100, TimeUnit.MILLISECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            e.printStackTrace();
        }
        return null;
    }

    public int getOwnerId() {
        return ownerId;
    }

    public int getQueueSize() {
        return messageQueue.size();
    }

    // Logs events to the "LamportLog.txt" file
    private void logEvent(String event) {
        try (PrintWriter out = new PrintWriter(new FileWriter("LamportLog.txt", true))) {
            out.println(event + "\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

// The ProcessThread class represents each process in the distributed system
class ProcessThread implements Runnable {
    private int ownerId; // ID of the process
    private SharedBuffer sharedBuffer; // The mailbox for this process
    private int logicalClock; // The Lamport logical clock for this process
    private int[] vectorClock; // Vector clock for this process
    private Random rand; // Random generator for event types and delays
    private int iterations; // Number of iterations the process will perform

    public ProcessThread(int ownerId, SharedBuffer sharedBuffer, int iterations, int numProcesses) {
        this.ownerId = ownerId;
        this.sharedBuffer = sharedBuffer;
        this.logicalClock = 0;
        this.vectorClock = new int[numProcesses]; // Initialize vector clock
        this.rand = new Random();
        this.iterations = iterations;
    }

    @Override
    public void run() {
        for (int i = 0; i < iterations; i++) {
            // Randomly choose an event type: internal, send, or receive
            int eventType = rand.nextInt(3);
            switch (eventType) {
                case 0:
                    performInternalEvent();
                    break;
                case 1:
                    performSendEvent();
                    break;
                case 2:
                    performReceiveEvent();
                    break;
            }

            // Random rest time between 100 and 1000 milliseconds
            int restTime = rand.nextInt(900) + 100;
            try {
                Thread.sleep(restTime);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                e.printStackTrace();
            }
        }

        // Log final clock values after iterations complete
        logEvent("Thread " + ownerId + " completed their iterations. Final Clock Value: " + logicalClock +
                 ", Vector Clock: " + Arrays.toString(vectorClock));
    }

    // Handles an internal event: increments the logical and vector clocks
    private void performInternalEvent() {
        logicalClock++;
        vectorClock[ownerId]++; // Increment vector clock at the index of this process
        logEvent("Process " + ownerId + " performed internal event at time " + logicalClock +
                 ", Vector Clock: " + Arrays.toString(vectorClock));
    }

    // Handles sending a message: increments the clocks and sends a message to another process
    private void performSendEvent() {
        logicalClock++;
        vectorClock[ownerId]++;

        // Randomly choose a receiver, ensuring it is not the same as the sender
        int receiverId = rand.nextInt(3);
        if (receiverId == ownerId) receiverId = (receiverId + 1) % 3;

        // Create and log the message
        Message message = new Message(ownerId, receiverId, logicalClock, vectorClock);
        logEvent("Process " + ownerId + " sent " + message);
        LamportLogicalClock.getBuffer(receiverId).addMessage(message);
    }

    // Handles receiving a message: updates clocks based on the received message
    private void performReceiveEvent() {
        Message message = sharedBuffer.retrieveMessage();
        if (message != null) {
            // Update vector clock using element-wise maximum
            for (int i = 0; i < vectorClock.length; i++) {
                vectorClock[i] = Math.max(vectorClock[i], message.getVectorClockOfSender()[i]);
            }
            logicalClock = Math.max(logicalClock, message.getTimeStamp()) + 1;
            vectorClock[ownerId]++;
            logEvent("Process " + ownerId + " received " + message + ". Updated clock: " + logicalClock +
                     ", Vector Clock: " + Arrays.toString(vectorClock));
        } else {
            logEvent("Process " + ownerId + "'s mailbox is empty or no message received.");
        }
    }

    // Logs events to the "LamportLog.txt" file
    private void logEvent(String event) {
        try (PrintWriter out = new PrintWriter(new FileWriter("LamportLog.txt", true))) {
            out.println(event + "\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Returns the current value of the logical clock
    public int getClockValue() {
        return logicalClock;
    }

    // Returns the current state of the vector clock
    public int[] getVectorClock() {
        return vectorClock;
    }
}

public class LamportLogicalClock {
    private static SharedBuffer[] buffers;

    public static void main(String[] args) {
        int numProcesses = 3;
        buffers = new SharedBuffer[numProcesses];
        ProcessThread[] processThreads = new ProcessThread[numProcesses];
        Thread[] threads = new Thread[numProcesses];

        try (PrintWriter out = new PrintWriter(new FileWriter("LamportLog.txt"))) {
            String currentTime = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());
            out.println("Simulation started at: " + currentTime + "\n");
        } catch (IOException e) {
            e.printStackTrace();
        }

        int iterations = 10;
        for (int i = 0; i < numProcesses; i++) {
            buffers[i] = new SharedBuffer(i, 10);
            processThreads[i] = new ProcessThread(i, buffers[i], iterations, numProcesses);
            threads[i] = new Thread(processThreads[i]);
        }

        for (int i = 0; i < numProcesses; i++) {
            threads[i].start();
        }

        for (int i = 0; i < numProcesses; i++) {
            try {
                threads[i].join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        for (int i = 0; i < numProcesses; i++) {
            System.out.println("\nProcess " + i + " final clock value: " + processThreads[i].getClockValue() +
                               ", Vector Clock: " + Arrays.toString(processThreads[i].getVectorClock()) + "\n");
        }
    }

    public static SharedBuffer getBuffer(int processId) {
        return buffers[processId];
    }
}