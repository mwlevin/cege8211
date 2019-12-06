/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl.node;

import dnl.link.Link;

/**
 * This class models behavior at a sink (at a destination node): all vehicles reaching the sink are removed from the network.
 * 
 * @author Michael Levin
 */
public class Sink extends Node
{
    
    private double exiting;
    
    public Sink(int id, double longitude, double latitude, double elevation)
    {
        super(id, longitude, latitude, elevation);
    }
    
    public void step()
    {
        exiting = 0;
        // all vehicles reaching the sink are removed.
        for(Link us : getIncoming())
        {
            double y = us.getSendingFlow();
            exiting += y;
            us.removeFlow(y);
        }
    }
    
    public void update()
    {
        // nothing to do here
    }
    
    public double getNumExiting()
    {
        return exiting;
    }
    
    
    public void storeTurningProportion(Link i, Link j, double p)
    {
        // removed due to uselessness
    }
    
    public double getTurningProp(Link i, Link j)    
    {
        // all vehicles exit when reaching the sink
        return 1;
    }
}
