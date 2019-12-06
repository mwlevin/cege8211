/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl.link;

import dnl.Params;
import dnl.node.Node;

/**
 *
 * @author mlevin
 */
public class MN  extends Link
{

    public MN(int id, Node source, Node dest, double length, double ffspd, double capacityPerLane, int numLanes)
    {
        super(id, source, dest, length, ffspd, capacityPerLane, numLanes);
    }
    
    
    public double getOccupancy()
    {
        // fill this in
        return 0.0;
    }
    
    public void step()
    {
        // fill this in
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
    
    public double getReceivingFlow()
    {
        // fill this in
        return 0.0;
    }
    
    public void addFlow(double y)
    {
        // fill this in
    }
    
    public void removeFlow(double y)
    {
        // fill this in
    }
    
}
