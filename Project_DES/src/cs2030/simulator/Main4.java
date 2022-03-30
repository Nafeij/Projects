import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import cs2030.simulator.Simulator;

class Main4 {
    public static void main(String[] args) throws FileNotFoundException {
        //Scanner sc = new Scanner(System.in);
        Scanner sc = new Scanner(new File("src/cs2030/simulator/test0.txt"));
        List<Double> arrivalTimes = new ArrayList<Double>();
        List<Double> serveTimes = new ArrayList<Double>();
        List<Double> restTimes = new ArrayList<Double>();
        int numServers = sc.nextInt();
        int numCounters = sc.nextInt();
        int queueLength = sc.nextInt();
        int numCustomers = sc.nextInt();
        while (sc.hasNextLine()) {
            Scanner scLine = new Scanner(sc.nextLine());
            if (numCustomers >= 0) {
                if (scLine.hasNextDouble()) {
                    arrivalTimes.add(scLine.nextDouble());
                }
                if (scLine.hasNextDouble()) {
                    serveTimes.add(scLine.nextDouble());
                }
            } else {
                if (scLine.hasNextDouble()) {
                    restTimes.add(scLine.nextDouble());
                }
            }
            numCustomers--;
        }
        Simulator s = new Simulator(numServers, numCounters, queueLength,
                arrivalTimes, serveTimes, restTimes);
        s.simulate();
    }
}