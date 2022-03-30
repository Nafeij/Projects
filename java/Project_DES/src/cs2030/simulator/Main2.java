import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.List;
import java.util.ArrayList;
import cs2030.simulator.Simulator;

class Main2 {
    public static void main(String[] args) throws FileNotFoundException{
        //Scanner sc = new Scanner(System.in);
        Scanner sc = new Scanner(new File("src/cs2030/simulator/test0.txt"));
        List<Double> arrivalTimes = new ArrayList<Double>();
        List<Double> serveTimes = new ArrayList<Double>();
        int numServers = 1;
        int queueLength = 1;
        numServers = sc.nextInt();
        queueLength = sc.nextInt();
        while (sc.hasNextLine()) {
            Scanner scLine = new Scanner(sc.nextLine());
            if (scLine.hasNextDouble()) {
                arrivalTimes.add(scLine.nextDouble());
            }
            if (scLine.hasNextDouble()) {
                serveTimes.add(scLine.nextDouble());
            }
        }
        Simulator s = new Simulator(numServers, queueLength, arrivalTimes, serveTimes);
        s.simulate();
    }
}