/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl.node;

import dnl.Params;
import dnl.link.Link;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * This represents a single signal phase. It stores the green, yellow, and all-red times, as well as a list of permitted turning movements.
 * @author mlevin
 */
public class Phase 
{
    private double red, yellow, green;
    private Map<Link, List<Link>> turns;
    
    
    private double start_time, end_time;
    
    public Phase(double green, double yellow, double red, List<Link[]> turnslist)
    {
        this.red = red;
        this.yellow = yellow;
        this.green = green;
        
        turns = new HashMap<>();
        
        for(Link[] pair : turnslist)
        {
            if(!turns.containsKey(pair[0]))
            {
                turns.put(pair[0], new ArrayList<Link>());
            }
            
            turns.get(pair[0]).add(pair[1]);
        }
    }
    
    /**
     * @return the exogenously specified start time of this phase
     */
    public double getStartTime()
    {
        return start_time;
    }
    
    /**
     * @return the exogenously specified end time of this phase
     */
    public double getEndTime()
    {
        return end_time;
    }
    
    /**
     * Updates the start and end times given the specified start time.
     * The end time is calculated based on the phase duration.
     */
    public void setStartTime(double start)
    {
        start_time = start;
        end_time = start_time + getDuration();
    }
    
    /**
     * @return the duration of this phase, which is the sum of the green, yellow, and all-red time.
     */
    public double getDuration()
    {
        return red+yellow+green;
    }
    
    

    

    /**
     * @return the amount of green time if this phase were to be actuated from time curr_time to end. If the phase duration is too short, then a smaller green time will be returned.
     */
    public double getGreenDuration(double curr_time, double end)
    {
        double end_green = start_time + green + yellow/2;
        
        return Math.max(0, Math.min(end, end_green) - curr_time);
    }
    
    /**
     * @return a map of turning movements permitted during this phase.
     */
    public Map<Link, List<Link>> getTurns()
    {
        return turns;
    }
    
}
