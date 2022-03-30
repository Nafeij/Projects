package cs2030.simulator;

import java.util.Comparator;

class SortByTime implements Comparator<Event> {
    
    private final int oNE = 1;
    
    public int compare(Event a, Event b) {
        if (a.getTime() == b.getTime()) {
            if (a.isType(Type.DONE)) {
                return -oNE;
            } else if (b.isType(Type.DONE)) {
                return oNE;
            } else if (a.isType(Type.SERVE)) {
                return -oNE;
            } else if (b.isType(Type.SERVE)) {
                return oNE;
            }
        }
        return Double.compare(a.getTime(), b.getTime());
    }
}