/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl.link;

import dnl.node.Node;

/**
 * This class models a centroid connector (no capacity constraint, no density constraint).
 * Centroid connectors are typically used as a buffer zone between sources/sinks and the main network.
 * 
 * @author Michael Levin
 */
public class CentroidConnector extends Link
{
    // store the occupancy: that is the sending flow also.
    private double n;
    
    // this will be the change in occupancy at the next time step
    private double total_y;
    
    public CentroidConnector(int id, Node source, Node dest, double length, double ffspd, double capacityPerLane, int numLanes)
    {
        // these values actually don't matter!
        super(id, source, dest, 1, 60, 100000, 1);
    }
    
    public double getOccupancy()
    {
        return n;
    }
    
    public void step()
    {
        // nothing to do here
    }
    
    public void update()
    {
        // addFlow() and removeFlow() updated total_y; now we need to propagate those changes to the occupancy
        n += total_y;
        
        // zero out total_y for the next time step
        total_y = 0;
    }
    
    public double getSendingFlow()
    {
        // all flow can exit
        return n;
    }
    
    public double getReceivingFlow()
    {
        // no constraint on entering flow
        // I'm using Integer.MAX_VALUE as a stand-in for infinity. Flow will never be that high.
        return Integer.MAX_VALUE;
    }
    
    public void addFlow(double y)
    {
        // add y to the occupancy for the next time step
        total_y += y;
    }
    
    public void removeFlow(double y)
    {
        // remove y from the occupancy for the next time step
        total_y -= y;
    }
}
