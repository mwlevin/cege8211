/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl.link;

import dnl.Params;
import dnl.node.Node;

/**
 * This class models a centroid connector (no capacity constraint, no density constraint).
 * Centroid connectors are typically used as a buffer zone between sources/sinks and the main network.
 * 
 * @author Michael Levin
 */
public class CentroidConnector extends Link
{
    // fill this in: add instance variables here
    
    public CentroidConnector(int id, Node source, Node dest, double length, double ffspd, double capacityPerLane, int numLanes)
    {
        // these values actually don't matter!
        super(id, source, dest, 1, 60, 100000, 1);
    }
    
    public void reset()
    {
        // fill this in
    }
    
    public double getOccupancy()
    {
        // fill this in
        return 0.0;
    }
    
    public void step()
    {
        // nothing to do here
    }
    
    public void update()
    {
        // fill this in
    }
    
    public double getSendingFlow()
    {
        // fill this in
        return 0.0;
    }
    
    /**
     * @return the free flow travel time in s.
     */
    public double getFFTime()
    {
        return Params.dt;
    }
    
    /**
     * @return the capacity per lane in veh/hr
     */
    public double getCapacityPerLane()
    {
        return Double.MAX_VALUE;
    }
    
    /**
     * @return the total capacity in veh/hr
     */
    public double getCapacity()
    {
        return Double.MAX_VALUE;
    }
    
    public double getReceivingFlow()
    {
        // fill this in
        // Integer.MAX_VALUE can be used as a stand-in for infinity. Flow will never be that high.
        return 0.0;
    }
    
    public void addFlow(double y)
    {
        // fill this in
        
        // keep this line: it records entering flow for travel time calculations
        logEnteringFlow(y);
    }
    
    public void removeFlow(double y)
    {
        // fill this in
    }
}
