package cs2030.simulator;

import java.util.List;
import java.util.Optional;
import java.util.Queue;
import java.util.concurrent.LinkedBlockingQueue;

class SelfCheckout extends Server {
    private static final int zERO = 0;
    private final Queue<Customer> selfCheckCustomers;

    SelfCheckout(int id, Queue<Customer> selfCheckCustomers) {
        super(id, zERO, false);
        this.selfCheckCustomers = selfCheckCustomers;
    }

    @Override
    public Customer serveQueue(Double time) {
        Customer customer = super.serveQueue(time);
        if (customer == null) {
            return checkSelfCheckQueue(time);
        }
        return customer;
    }

    private Customer checkSelfCheckQueue(Double time) {
        if (!selfCheckCustomers.isEmpty()) {
            Customer customer = selfCheckCustomers.poll();
            super.queue(customer, time);
            return customer;
        } else {
            return null;
        }
    }

    @Override
    public String toString() {
        return String.format("self-check %d", super.getId());
    }
}