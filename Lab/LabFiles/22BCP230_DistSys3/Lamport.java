import java.util.*;

class Message {
    int senderId;
    int receiverId;
    int timestamp;
}

class PersonalSharedBoundedBuffer {
    
    Queue<Message> buffer;
    int size;
    int ownerId;


    PersonalSharedBoundedBuffer(int size, int ownerId) {
        this.size = size;
        buffer = new LinkedList<>();
        this.ownerId = ownerId;
    }

    synchronized void send(Message message) {
        while(buffer.size() == size) {
            try {
                wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        buffer.add(message);
        notifyAll();
    }

    synchronized Message receive() {

        while (true) {

            while(buffer.isEmpty()) {
                try {
                    wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            while(!buffer.isEmpty() && buffer.peek().senderId == ownerId) {
                buffer.poll();
            }

            if(buffer.isEmpty()) {
                continue;
            }

            Message message = buffer.poll();
            notifyAll();
            return message;

        }
    }

}