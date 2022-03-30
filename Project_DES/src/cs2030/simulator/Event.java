package cs2030.simulator;

class Event {
    private final Double time;
    private final Customer customer;
    private final Type type;
    
    Event(Double time, Customer customer, Type type) {
        this.time = time;
        this.customer = customer;
        this.type = type;
    }
    
    public double getTime() {
        return time;
    }
    
    public Customer getCustomer() {
        return customer;
    }
    
    public boolean isType(Type type) {
        return this.type == type;
    }
    
    @Override
    public String toString() {
        return String.format("%.3f %s", time, customer.toString());
    }
}