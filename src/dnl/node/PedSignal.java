/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl.node;

import dnl.Params;
import dnl.link.Link;

/**
 * This class models 2 links in series, but the links are separated by a traffic light used to provide access to pedestrians.
 * Essentially, the light alternates between green and red, with these times as class parameters.
 * The primary utility of this class is to create a simple signal that can cause congestion waves to form.
 * @author mlevin
 */
public class PedSignal extends Node
{
    // change these to modify the green time and red time.
    // I assume that the time step is less than the cycle length.
    private final double green_time = 32;
    private final double red_time = 15;
    
    
    
    
    // alternate green and red, then cycle back when needed
    private double curr_time;
    private double cycle_length = green_time + red_time;
    
    public PedSignal(int id, double longitude, double latitude, double elevation)
    {
        super(id, longitude, latitude, elevation);
        
        curr_time = 0;
    }
    
    public void reset()
    {
        curr_time = 0;
    }
    
    public void step()
    {
        double green_dt = 0.0;
        
        // assume that time step is less than the cycle length
        double start_time = curr_time;
        double end_time = curr_time + Params.dt;
        
        // check green phase
        double time_rem = Math.min(Math.max(0, green_time - start_time), end_time - start_time);
        green_dt += time_rem;
        start_time += time_rem;
        
        time_rem = Math.min(Math.max(0, cycle_length - start_time), end_time - start_time);
        start_time += time_rem;
        
        time_rem = Math.min(Math.max(0, green_time + cycle_length - start_time), end_time - start_time);
        green_dt += time_rem;
        start_time += time_rem;
        
        curr_time = end_time;
        if(curr_time >= cycle_length)
        {
            curr_time -= cycle_length;
        }

        Link us = getIncoming().get(0);
        Link ds = getOutgoing().get(0);
        
        double y = Math.min(us.getSendingFlow(), ds.getReceivingFlow()) * green_dt;
        
        us.removeFlow(y);
        ds.addFlow(y);
        
    }
    
    public void update()
    {
        
    }
}
