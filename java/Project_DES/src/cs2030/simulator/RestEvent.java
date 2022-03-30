package cs2030.simulator;

public class RestEvent extends Event {
    private final Server server;

    RestEvent(Double time, Server server) {
        super(time, null, Type.REST);
        this.server = server;
    }

    public Server getServer() {
        return server;
    }

    @Override
    public String toString() {
        return "";
    }
}
