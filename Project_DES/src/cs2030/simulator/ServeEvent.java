package cs2030.simulator;

class ServeEvent extends Event {
    private final Server server;
    
    ServeEvent(Double time, Customer customer, Server server) {
        super(time, customer, Type.SERVE);
        this.server = server;
    }
    
    public Server getServer() {
        return server;
    }
   
    @Override
    public String toString() {
        return String.format("%s serves by %s\n", super.toString(), server.toString());
    }
}