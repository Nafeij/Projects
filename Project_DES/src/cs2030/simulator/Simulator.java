package cs2030.simulator;

import java.util.List;
import java.util.PriorityQueue;
import java.util.ArrayList;
import java.util.Queue;
import java.util.concurrent.LinkedBlockingQueue;

public class Simulator {
    private final PriorityQueue<Event> events = new PriorityQueue<Event>(new SortByTime());
    private final ArrayList<Server> servers = new ArrayList<Server>();
    private final ArrayList<Double> rests = new ArrayList<Double>();
    private final Queue<Customer> selfCheckCustomers;
    private final int queueSize = 1;
    private final int oNE = 1;
    private final int zERO = 0;
    private final Double dONE = 1.0;
    private final int numServers;
    private final boolean selfCheckFlag;

    /**
     * Initializes the discrete event simulaton.
     */
    public Simulator(int numServers, List<Double> arrivalTimes) {
        this.numServers = numServers;
        for (int i = oNE; i <= numServers; i++) {
            servers.add(new Server(i,queueSize, true));
        }
        int i = oNE;
        for (Double arrivalTime : arrivalTimes) {
            events.add(new ArrivalEvent(arrivalTime, new Customer(i++,arrivalTime,dONE)));
        }
        rests.add(0.0);
        selfCheckCustomers = new LinkedBlockingQueue<Customer>(oNE);
        selfCheckFlag = false;
    }

    /**
     * Initializes the discrete event simulaton with variable queue length and service time.
     */
    public Simulator(int numServers, int maxQLen,
                     List<Double> arrivalTimes, List<Double> serviceTimes) {
        this.numServers = numServers;
        for (int i = oNE; i <= numServers; i++) {
            servers.add(new Server(i,maxQLen, true));
        }
        for (int i = zERO; i < arrivalTimes.size(); i++) {
            events.add(
                    new ArrivalEvent(arrivalTimes.get(i),
                            new Customer(i + oNE,arrivalTimes.get(i),serviceTimes.get(i)
                            )));
        }
        rests.add(0.0);
        selfCheckCustomers = new LinkedBlockingQueue<Customer>(oNE);
        selfCheckFlag = false;
    }

    /**
     * Initializes the simulaton with variable queue length, service time and rest times.
     */
    public Simulator(int numServers, int maxQLen,
                     List<Double> arrivalTimes, List<Double> serviceTimes, List<Double> restTimes) {
        this.numServers = numServers;
        for (int i = oNE; i <= numServers; i++) {
            servers.add(new Server(i,maxQLen, true));
        }
        for (int i = zERO; i < arrivalTimes.size(); i++) {
            events.add(
                    new ArrivalEvent(arrivalTimes.get(i),
                            new Customer(i + oNE,arrivalTimes.get(i),serviceTimes.get(i)
                            )));
        }
        for (int i = zERO; i < restTimes.size(); i++) {
            rests.add(restTimes.get(i));
        }
        selfCheckCustomers = new LinkedBlockingQueue<Customer>(oNE);
        selfCheckFlag = false;
    }

    /**
     * Initializes the simulaton with queue length, self-checkouts service time and rest times.
     */
    public Simulator(int numServers, int numCounters,int maxQLen,
                     List<Double> arrivalTimes, List<Double> serviceTimes, List<Double> restTimes) {
        int j = oNE;
        this.numServers = numServers;
        while (j <= numServers) {
            servers.add(new Server(j,maxQLen, true));
            j++;
        }
        selfCheckCustomers = new LinkedBlockingQueue<Customer>(maxQLen);
        for (int i = oNE; i <= numCounters; i++) {
            servers.add(new SelfCheckout(j, selfCheckCustomers));
            j++;
        }
        for (int i = zERO; i < arrivalTimes.size(); i++) {
            events.add(
                    new ArrivalEvent(arrivalTimes.get(i),
                            new Customer(i + oNE,arrivalTimes.get(i),serviceTimes.get(i)
                            )));
        }
        for (int i = zERO; i < restTimes.size(); i++) {
            rests.add(restTimes.get(i));
        }
        selfCheckFlag = (numCounters > 0);
    }

    /**
     * Runs the discrete event simulaton.
     */
    public void simulate() {
        Double time;
        Customer customer;
        Server server;
        int statNumServed = 0;
        Double statTotalWait = 0.0;
        int statNumLeft = 0;
        int restIndex = 0;
        while (!events.isEmpty()) {
            Event event = events.poll();
            System.out.print(event);
            customer = event.getCustomer();
            time = event.getTime();
            if (event.isType(Type.ARRIVAL)) {
                event = null;
                for (Server serv : servers) {
                    if (serv.canServe(customer, time)) {
                        event = new ServeEvent(time, customer, serv);
                        events.add(event);
                        break;
                    }
                }
                if (event == null) {
                    for (Server serv : servers) {
                        if (serv.queue(customer, time)) {
                            event = new WaitEvent(time, customer, serv);
                            events.add(event);
                            break;
                        }
                    }
                    if (event == null) {
                        if (selfCheckFlag && selfCheckCustomers.offer(customer)) {
                            event = new WaitEvent(time, customer, servers.get(numServers));
                            events.add(event);
                        } else {
                            events.add(new LeaveEvent(time, customer));
                            statNumLeft++;
                        }
                    }
                }
            } else if (event.isType(Type.SERVE)) {
                server = ((ServeEvent) event).getServer();
                events.add(new DoneEvent(time + customer.getServiceTime(), customer, server));
                statTotalWait += time - customer.getArrivalTime();
                statNumServed++;
            } else if (event.isType(Type.DONE)) {
                server = ((DoneEvent) event).getServer();
                if (server.canRest()) {
                    if (rests.get(restIndex) <= 0.0) {
                        customer = server.serveQueue(time);
                        if (customer != null) {
                            events.add(new ServeEvent(time, customer, server));
                        }
                    } else {
                        events.add(new RestEvent(
                                time + rests.get(restIndex),
                                server));
                        //System.out.println(server.toString() +
                        // " resting for " + rests.get(restIndex));
                    }
                    restIndex++;
                } else {
                    customer = server.serveQueue(time);
                    if (customer != null) {
                        events.add(new ServeEvent(time, customer, server));
                    }
                }
            } else if (event.isType(Type.REST)) {
                server = ((RestEvent) event).getServer();
                customer = server.serveQueue(time);
                if (customer != null) {
                    events.add(new ServeEvent(time, customer, server));
                }
            }
            if (restIndex >= rests.size()) {
                restIndex = 0;
            }
        }
        String stats = String.format("[%.3f %d %d]",
                statTotalWait / statNumServed, statNumServed, statNumLeft);
        System.out.println(stats);
    }
}