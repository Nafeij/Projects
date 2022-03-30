package cs2030.simulator;

class DoneEvent extends Event {
    private final Server server;
    
    DoneEvent(Double time, Customer customer, Server server) {
        super(time, customer, Type.DONE);
        this.server = server;
    }
    
    public Server getServer() {
        return server;
    }
   
    @Override
    public String toString() {
        return String.format("%s done serving by %s\n", super.toString(), server.toString());
    }
}