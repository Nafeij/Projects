package cs2030.simulator;

class ArrivalEvent extends Event {
    
    ArrivalEvent(Double time, Customer customer) {
        super(time, customer, Type.ARRIVAL);
    }
   
    @Override
    public String toString() {
        return String.format("%s arrives\n", super.toString());
    }
}