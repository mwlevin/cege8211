/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl.link;

import dnl.Params;
import dnl.node.Node;

/**
 * This represents a link in the network.
 * This is an abstract class: key methods are not implemented, and must be implemented in subclasses. 
 * These depend on the specific flow model.
 * 
 * @author Michael Levin
 */
public abstract class Link implements Comparable<Link>
{
    // id used to reference the link
    private int id;
    
    // stores the upstream and downstream nodes
    private Node source, dest;
    
    // capacity per lane in veh/hr
    private double capacityPerLane;
    
    // number of lanes
    private int numLanes;
    
    // link length in miles
    private double length;
    
    // free flow speed in mi/hr
    private double ffspd; 
    
    // travel time information
    private double avgTT;
    
    // during each DNL, update total entering flow and total time spent occupying the link.
    private double total_entering;
    private double total_time_occ;
    
    
    
    /**
     * Constructs a new {@link Link} with the given parameters.
     * Generally {@link Link}s will be constructed in {@link ReadNetwork}.
     * 
     * Jam density is global and found in {@link Params}
     * Backwards wave speed may or may not be calculated based on these parameters - depends on the flow model.
     * @param id id of this {@link Link}
     * @param source start {@link Node} of this {@link Link}
     * @param dest end {@link Node} of this {@link Link}
     * @param length length in mi
     * @param ffspd free flow speed in mi/hr
     * @param capacityPerLane capacity (per lane) in veh/hr
     * @param numLanes number of lanes
     */
    public Link(int id, Node source, Node dest, double length, double ffspd, double capacityPerLane, int numLanes)
    {
        // store link parameters
        this.id = id;
        this.source = source;
        this.dest = dest;
        this.capacityPerLane = capacityPerLane;
        this.ffspd = ffspd;
        this.length = length;
        this.numLanes = numLanes;
        
        // update incoming/outgoing sets of links in the Node class
        if(source != null)
        {
            source.addLink(this);
        }
        if(dest != null)
        {
            dest.addLink(this);
        }
        
        total_time_occ = 0.0;
        total_entering = 0.0;
    }
    
    /**
     * @return the free flow speed in mi/hr
     */
    public double getFFSpeed()
    {
        return ffspd;
    }
    
    /**
     * @return the free flow travel time in s.
     */
    public double getFFTime()
    {
        return getLength() / getFFSpeed() * 3600.0;
    }
    
    /**
     * @return the travel time when entering at the given time (in s).
     */
    public double getAvgTT()
    {
        return Math.max(avgTT, getFFTime());
    }
    
    
    /**
     * @return the average grade (change in elevation) in percent vertical change in ft per horizontal distance
     */
    public double getAvgGrade()
    {
        return (dest.getElevation() - source.getElevation()) / (getLength() * 5280);
    }
    
    /**
     * @return the length in mi
     */
    public double getLength()
    {
        return length;
    }
    
    /**
     * @return the capacity per lane in veh/hr
     */
    public double getCapacityPerLane()
    {
        return capacityPerLane;
    }
    
    /**
     * @return the total capacity in veh/hr
     */
    public double getCapacity()
    {
        return capacityPerLane * numLanes;
    }
    
    /**
     * @return the number of lanes
     */
    public double getNumLanes()
    {
        return numLanes;
    }
    
    

    /**
     * @return the upstream {@link Node} for this {@link Link}
     */
    public Node getSource()
    {
        return source;
    }
    
    /**
     * @return the downstream {@link Node} for this {@link Link}
     */
    public Node getDest()
    {
        return dest;
    }
    
    
    /**
     * @return the id for this {@link Link}
     */
    public int getId()
    {
        return id;
    }
    
    /**
     * @return the number of vehicles currently on this {@link Link}.
     */
    public abstract double getOccupancy();
    
    /**
     * This is called every time step. 
     * For the {@link Link} class, {@link #step()} should propagate flow along the link.
     */
    public abstract void step();
    
    /**
     * This is called every time step, after {@link #step()} has been called for all {@link Node}s and {@link Link}s.
     * It can be used to finish any updating work that could not occur during {@link #step()}.
     */
    public abstract void update();
    
    /**
     * Adds the given flow (in veh, for a single time step) to the upstream end of the link.
     * This method is called when vehicles enter the link!
     * This is usually called by the {@link Node#step()} method.
     * Subclasses of link need to call {@link #logEnteringFlow()} to update the average travel times.
     */
    public abstract void addFlow(double y);
    
    
    /**
     * This is used to track the total number of vehicles entering this link.
     * The number of vehicles is used to calculate the average travel time.
     * This method is usually called by {@link #addFlow()}.
     * Subclasses of {@link Link} should call this method as part of the {@link #addFlow()} method.
     */
    public void logEnteringFlow(double y)
    {
        total_entering += y;
    }
    
    /**
     * This method is used to calculate the average travel time.
     * It should be called once per time step by the {@link dnl.Network} class.
     */
    public void logOccupancyTime()
    {
        total_time_occ += Params.dt * getOccupancy();
    }
    
    /**
     * This method is used to calculate the total travel time at the end of the dynamic network loading.
     * The result can be accessed by {@link #getAvgTT()}. 
     * This method is called in {@link dnl.Network#simulate()}.
     */
    public void calculateTravelTime()
    {
        if(total_entering > 0)
        {
            avgTT = total_time_occ / total_entering;
        }
        else
        {
            avgTT = getFFTime();
        }
        
        // now reset total_time_occ and total_entering for the next dynamic network loading.
        total_time_occ = 0.0;
        total_entering = 0.0;
    }
    
    
    /**
     * Removes the given flow (in veh, for a single time step) from the downstream end of the link.
     * This method is called when vehicles exit the link! 
     * This is usually called by the {@link Node#step()} method.
     * @param y the flow to be removed
     */
    public abstract void removeFlow(double y);
    
    /**
     * @return the maximum flow that could exit the link in the next time step (in veh)
     */
    public abstract double getSendingFlow();
    
    
    /**
     * @return the maximum flow that could enter the link in the next time step (in veh)
     */
    public abstract double getReceivingFlow();
    
    
    
    
    
    
    
    
    /**
     * Used to sort {@link Link} by id.
     */
    public int compareTo(Link rhs)
    {
        return id - rhs.id;
    }
    
    
    /**
     * Used for hashing. You can ignore it.
     */
    public int hashCode()
    {
        return id;
    }
    
    /**
     * @return the id of this {@link Link}
     */
    public String toString()
    {
        return ""+id;
    }
}
