import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.List;
import java.util.ArrayList;
import cs2030.simulator.Simulator;

class Main1 {
    public static void main(String[] args) throws FileNotFoundException {
        // Scanner sc = new Scanner(System.in);
        Scanner sc = new Scanner(new File("src/cs2030/simulator/test0.txt"));
        List<Double> arrivalTimes = new ArrayList<Double>();
        int numServers = 1;
        numServers = sc.nextInt();
        while (sc.hasNextDouble()) {
            arrivalTimes.add(sc.nextDouble());
        }
        Simulator s = new Simulator(numServers, arrivalTimes);
        s.simulate();
    }
}