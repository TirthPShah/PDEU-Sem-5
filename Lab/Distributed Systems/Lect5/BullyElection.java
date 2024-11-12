import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class BullyElection {

    // Define constants and variables for process status and current coordinator
    static final int MAX = 20;
    static int[] pStatus = new int[MAX]; // Array to store the status of each process (0 - dead, 1 - alive)
    static int n; // Number of processes in the system
    static int coordinator; // PID of the current coordinator

    public static void main(String[] args) {
        Random random = new Random();
        
        // Initialize a random number of processes between 5 and 15
        n = random.nextInt(10) + 5;

        // Initialize each process status randomly as alive (1) or dead (0)
        // Set the initial coordinator as the highest alive process
        for (int i = 1; i <= n; i++) {
            pStatus[i] = random.nextInt(2); // Random status (0 or 1)
            if (pStatus[i] == 1) {
                coordinator = i; // Track the highest PID of alive process as coordinator
            }
        }
        display(); // Display initial status of processes and coordinator

        // Create thread pool for simulating process events
        ExecutorService executor = Executors.newFixedThreadPool(3);
        executor.execute(() -> simulateCrashes()); // Thread for simulating process crashes
        executor.execute(() -> simulateActivations()); // Thread for simulating process activations
        executor.execute(() -> periodicElections()); // Thread for periodic elections to check coordinator

        // Shutdown executor after 20 seconds
        try {
            executor.awaitTermination(15, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        executor.shutdown();
    }

    // Simulate random process crashes
    static void simulateCrashes() {
        Random random = new Random();
        while (!Thread.currentThread().isInterrupted()) {
            int crash = random.nextInt(n) + 1; // Select a random process to crash
            if (pStatus[crash] == 1) {
                pStatus[crash] = 0; // Set process to dead
                System.out.println("Process " + crash + " crashed.");
                initiateElection(crash); // Start a new election due to crash
            }
            sleep(3000); // Wait 3 seconds before the next crash
        }
    }

    // Simulate random process activations (recovery from failure)
    static void simulateActivations() {
        Random random = new Random();
        while (!Thread.currentThread().isInterrupted()) {
            int activate = random.nextInt(n) + 1; // Select a random process to activate
            if (pStatus[activate] == 0) {
                pStatus[activate] = 1; // Set process to alive
                System.out.println("Process " + activate + " activated.");
                initiateElection(-1); // Start a new election due to activation
            }
            sleep(5000); // Wait 5 seconds before the next activation
        }
    }

    // Periodically initiate an election to ensure coordinator is still alive
    static void periodicElections() {
        while (!Thread.currentThread().isInterrupted()) {
            initiateElection(-1); // Trigger an election periodically
            sleep(7000); // Wait 7 seconds before the next periodic election
        }
    }

    // Bully election algorithm implementation
    static void initiateElection(int initiator) {
        int newCoordinator = -1; // Variable to store the PID of the new coordinator

        // Check for the highest PID among the alive processes
        for (int i = initiator + 1; i <= n; i++) {
            if (pStatus[i] == 1) { // If process is alive
                newCoordinator = i; // Update potential new coordinator
                System.out.println("Message sent to Process " + i); // Simulate message sending
            }
        }

        // If a new coordinator is found, update the current coordinator
        if (newCoordinator != -1) {
            coordinator = newCoordinator;
            System.out.println("New Coordinator: Process " + coordinator);
        } else {
            System.out.println("No alive processes found!"); // Handle case where no processes are alive
        }
    }

    // Display current process statuses and the current coordinator
    static void display() {
        System.out.print("Processes: ");
        for (int i = 1; i <= n; i++) {
            System.out.print(i + " ");
        }
        System.out.print("\nAlive:     ");
        for (int i = 1; i <= n; i++) {
            System.out.print(pStatus[i] + " ");
        }
        System.out.println("\nCoordinator: Process " + coordinator);
    }

    // Helper method to pause thread execution
    static void sleep(int millis) {
        try {
            Thread.sleep(millis); // Pause thread for specified time
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt(); // Handle thread interruption
        }
    }
}
