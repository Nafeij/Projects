package cs2030.simulator;

class Customer {
    private final int id;
    private final Double arrivalTime;
    private final Double serviceTime;
    
    Customer(int id, Double arrivalTime, Double serviceTime) {
        this.id = id;
        this.arrivalTime = arrivalTime;
        this.serviceTime = serviceTime;
    }
    
    public double getArrivalTime() {
        return arrivalTime;
    }
    
    public double getServiceTime() {
        return serviceTime;
    }
    
    @Override
    public String toString() {
        return String.format("%d", id);
    }
}