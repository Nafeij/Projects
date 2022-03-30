package cs2030.simulator;

class WaitEvent extends Event {
    private final Server server;
    
    WaitEvent(Double time, Customer customer, Server server) {
        super(time, customer, Type.WAIT);
        this.server = server;
    }
    
    public Server getServer() {
        return server;
    }
   
    @Override
    public String toString() {
        return String.format("%s waits at %s\n", super.toString(), server.toString());
    }
}