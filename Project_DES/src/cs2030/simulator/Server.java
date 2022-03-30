package cs2030.simulator;

import java.util.Queue;
import java.util.concurrent.LinkedBlockingQueue;

class Server {
    private final int id;
    private final Queue<Customer> waitingCustomers;
    private final boolean rests;

    Server(int id, int size, boolean rests) {
        this.id = id;
        this.waitingCustomers = new LinkedBlockingQueue<Customer>(size + 1);
        this.rests = rests;
    }
    
    public boolean canServe(Customer customer, Double time) {
        boolean empty = waitingCustomers.isEmpty();
        if (empty) {
            waitingCustomers.add(customer);
        } 
        return empty;
    }

    public boolean canRest() {
        return rests;
    }
    
    public boolean queue(Customer customer, Double time) {
        return waitingCustomers.offer(customer);
    }
    
    public Customer serveQueue(Double time) {
        waitingCustomers.remove();
        if (!waitingCustomers.isEmpty()) {
            return waitingCustomers.peek();
        } else {
            return null;
        }
    }

    public int getId() {
        return id;
    }

    @Override
    public String toString() {
        return String.format("server %d", id);
    }
}