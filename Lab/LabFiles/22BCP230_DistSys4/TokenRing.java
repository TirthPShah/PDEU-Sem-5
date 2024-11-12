import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

class TokenRingNode implements Runnable {
    private final int nodeId;
    private final int n; // Total number of nodes
    private final TokenRingManager manager;
    private static final Random random = new Random();

    public TokenRingNode(int nodeId, int n, TokenRingManager manager) {
        this.nodeId = nodeId;
        this.n = n;
        this.manager = manager;
    }

    @Override
    public void run() {
        while (true) {
            // Wait until this node gets the token
            if (manager.getCurrentToken() == nodeId) {
                try {
                    System.out.println("Node " + nodeId + " has the token.");

                    // Enter critical section
                    enterCriticalSection();

                    // Simulate some work inside the critical section
                    Thread.sleep(random.nextInt(3000) + 1000); // 1-4 seconds delay

                    System.out.println("Node " + nodeId + " is leaving the critical section.");
                    
                    // Pass the token to the next node in the ring
                    int nextNode = (nodeId + 1) % n;
                    manager.setCurrentToken(nextNode);
                    System.out.println("Token passed to Node " + nextNode + "\n");

                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    System.out.println("Node " + nodeId + " interrupted.");
                }
            }

            // Introduce a short delay to prevent busy-waiting
            try {
                TimeUnit.MILLISECONDS.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    private void enterCriticalSection() {
        System.out.println("Node " + nodeId + " entering the critical section.");
    }
}

class TokenRingManager {
    private volatile int currentToken; // Stores the current token holder

    public TokenRingManager(int initialTokenHolder) {
        this.currentToken = initialTokenHolder;
    }

    public synchronized int getCurrentToken() {
        return currentToken;
    }

    public synchronized void setCurrentToken(int nextTokenHolder) {
        this.currentToken = nextTokenHolder;
    }
}

public class TokenRing {
    public static void main(String[] args) {
        int n = 5; // Number of nodes
        ExecutorService executor = Executors.newFixedThreadPool(n);

        // Initialize the token manager with the first token holder (Node 0)
        TokenRingManager manager = new TokenRingManager(0);

        // Start all nodes as threads
        for (int i = 0; i < n; i++) {
            executor.execute(new TokenRingNode(i, n, manager));
        }

        // Shutdown executor gracefully after simulation (optional)
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            executor.shutdown();
            try {
                if (!executor.awaitTermination(5, TimeUnit.SECONDS)) {
                    executor.shutdownNow();
                }
            } catch (InterruptedException e) {
                executor.shutdownNow();
            }
            System.out.println("Simulation ended.");
        }));
    }
}
