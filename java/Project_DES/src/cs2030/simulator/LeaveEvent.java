package cs2030.simulator;

class LeaveEvent extends Event {
    
    LeaveEvent(Double time, Customer customer) {
        super(time, customer, Type.LEAVE);
    }
   
    @Override
    public String toString() {
        return String.format("%s leaves\n", super.toString());
    }
}