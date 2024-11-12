import threading
import time
import queue

# Global variable to count total messages transferred
message_count = 0
message_count_lock = threading.Lock()  # Lock to ensure thread-safe updates

class Process:
    def _init_(self, pid, total_processes):
        self.pid = pid  # Process ID
        self.timestamp = 0  # Logical timestamp
        self.queue = queue.Queue()  # Message queue
        self.request_queue = []  # List of pending requests
        self.total_processes = total_processes
        self.replies_received = 0  # Count of replies received

    def send_message(self, message, target):
        """Simulate sending a message to another process."""
        global message_count
        with message_count_lock:
            message_count += 1  # Increment message count
        
        target.queue.put(message)

    def broadcast_request(self):
        """Broadcast the request for the critical section to all other processes."""
        self.timestamp += 1
        request_message = (self.timestamp, self.pid, "REQUEST")
        print(f"Process {self.pid} broadcasting request at time {self.timestamp}")
        for process in processes:
            if process.pid != self.pid:
                self.send_message(request_message, process)

    def receive_message(self):
        """Handle incoming messages."""
        while True:
            try:
                message = self.queue.get(timeout=1)  # Check for messages
            except queue.Empty:
                continue

            timestamp, sender_pid, msg_type = message
            self.timestamp = max(self.timestamp, timestamp) + 1

            if msg_type == "REQUEST":
                # Handle request: Send REPLY if this process is not interested or has a lower priority
                if (len(self.request_queue) == 0 or 
                   (self.request_queue[0][0] > timestamp or 
                    (self.request_queue[0][0] == timestamp and self.request_queue[0][1] > sender_pid))):
                    reply_message = (self.timestamp, self.pid, "REPLY")
                    print(f"Process {self.pid} sending REPLY to {sender_pid}")
                    self.send_message(reply_message, processes[sender_pid])
                # Otherwise, add the request to the queue
                else:
                    self.request_queue.append((timestamp, sender_pid))

            elif msg_type == "REPLY":
                # Handle reply: Increment the number of replies received
                self.replies_received += 1

            elif msg_type == "RELEASE":
                # Handle release: Remove the request from the queue and send pending replies
                if self.request_queue and self.request_queue[0][1] == sender_pid:
                    self.request_queue.pop(0)
                if self.request_queue:
                    reply_message = (self.timestamp, self.pid, "REPLY")
                    next_process_pid = self.request_queue.pop(0)[1]
                    self.send_message(reply_message, processes[next_process_pid])

    def enter_critical_section(self):
        """Request access to the critical section and wait for replies."""
        self.broadcast_request()

        # Wait until all replies are received
        while self.replies_received < self.total_processes - 1:
            time.sleep(0.1)

        # Enter the critical section
        start_time = time.time()  # Start time measurement
        print(f"Process {self.pid} entering critical section at time {self.timestamp}")
        time.sleep(2)  # Simulate work in the critical section
        end_time = time.time()  # End time measurement

        # Log the time spent in the critical section
        print(f"Process {self.pid} spent {end_time - start_time:.4f} seconds in the critical section.")

        # Release the critical section
        self.release_critical_section()

    def release_critical_section(self):
        """Release the critical section and notify waiting processes."""
        print(f"Process {self.pid} releasing critical section at time {self.timestamp}")
        release_message = (self.timestamp, self.pid, "RELEASE")
        for process in processes:
            if process.pid != self.pid:
                self.send_message(release_message, process)
        self.replies_received = 0  # Reset reply count


# Create processes
num_processes = 3
processes = [Process(i, num_processes) for i in range(num_processes)]

# Start message receiving threads
for process in processes:
    threading.Thread(target=process.receive_message, daemon=True).start()

# Simulate processes requesting the critical section
for process in processes:
    threading.Thread(target=process.enter_critical_section).start()

# Wait for all processes to finish
time.sleep(10)  # Wait to allow all processes to complete execution

# Print the total number of messages transferred
print(f"\nTotal number of messages transferred: {message_count}")