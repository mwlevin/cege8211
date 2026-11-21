/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl.node;

import dnl.Params;
import dnl.link.Link;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * This class is used to model a traffic signal. 
 * There can be any number of incoming and outgoing links.
 * During construction, {@link Signal.addPhase()} and {@link Signal.setOffset()} will be called to store signal cycle information.
 * {@link Signal.addPhase()} adds a phase to the signal cycle; {@link Signal.setOffset()} sets the start time of the cycle (relative to 0).
 * 
 * @author Michael Levin
 */
public class Signal extends Node
{
    private List<Phase> phases;
    private double offset;
    
    private int curr_phase;
    private double cycle_length;
    
    // this is the time in the cycle. It resets to 0 whenever the cycle duration is exceeded.
    private double curr_time;
    
    public Signal(int id, double longitude, double latitude, double elevation)
    {
        super(id, longitude, latitude, elevation);
        
        phases = new ArrayList<>();
        
        curr_phase = -1;
        
    }
    
    
    public void reset()
    {
        // fill this in
    }
    
    /**
     * Use a diverge node to model outgoing flow for each approach.
     */
    public void step()
    {
        // fill this in
    }
    
    
    
    
    public void update()
    {
        // fill this in
    }
    
    /**
     * @return the length of the cycle, in s.
     */
    public double getCycleLength()
    {
        return cycle_length;
    }
    
    
    
    /**
     * This updates the offset of the signal cycle (in s). For instance, if the offset is 21s, then phase 1 starts at t=21s. 
     * Note that the signal cycle repeats, so there will always be a phase active at t=0. Depending on the offset, it may not be the first phase!
     */
    public void setOffset(double offset)
    {
        this.offset = offset;
    }
    
    /**
     * This adds the specified phase to this signal. Recall that a signal cycle consists of a list of phases.
     * Sequence is the order that this phase occurs in a fixed cycle, starting from 1.
     * Green, yellow, and all-red time are in seconds. 
     * Protected_turns is a list of pairs of links - one incoming, one outgoing.
     * For instance, if (i,j) is in protected_turns, then this phase allows movement from i to j
     */
    public void addPhase(int sequence, double green, double yellow, double all_red, List<Link[]> protected_turns)
    {
        Phase phase;
        phases.add(sequence-1, phase = new Phase(green, yellow, all_red, protected_turns));
        cycle_length += phase.getDuration();
    }
}
