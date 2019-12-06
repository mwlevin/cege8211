/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl.node;

import dnl.Params;
import dnl.link.Link;
import java.util.HashMap;
import java.util.TreeMap;

/**
 * This class models a source (origin node): vehicles spawn at this location at predetermined rates.
 * 
 * @author Michael Levin
 */
public class Source extends Node
{
    
    /**
     * This stores the rate of demand as a map between final time and rate of demand.
     * For instance, the entry ([0, 20], 50) means that when the time is between 0 and 20s, 50veh/hr enter at this source.
     */
    private HashMap<Double[], Double> demand_rates;
    
    
    /**
     * See {@link Node} constructor.
     */
    public Source(int id, double longitude, double latitude, double elevation)
    {
        super(id, longitude, latitude, elevation);
        
        demand_rates = new HashMap<>();
    }
    
    public void reset()
    {
        // nothing to do here
    }
    
    /**
     * This is used to add demand to the source. 
     * It is typically called in {@link dnl.ReadNetwork} when constructing the {@link dnl.Network}.
     */
    public void addDemand(double start_time, double end_time, double demand)
    {
        Double[] time = new Double[]{start_time, end_time};
        
        if(demand_rates.containsKey(time))
        {
            demand_rates.put(time, demand_rates.get(time) + demand);
        }
        else
        {
            demand_rates.put(time, demand);
        }
    }
    
    /**
     * This method is called every time step by {@link dnl.Network#nextTimestep()}.
     * Since this is a source node, it adds the exogenous amount of demand to the network - to the appropriate {@link dnl.link.CentroidConnector}. 
     * 
     */
    public void step()
    {
        /**
         * Here we need to add the specified amount of demand to the network.
         * First, calculate the rate at which vehicles enter during the next time step.
         * The time interval is [Params.time, Params.time + Params.dt).
         * If the demand applies for part of the time interval, scale the rate proportionally to the overlap.
         */
        
        double rate = 0.0;
        
        for(Double[] times : demand_rates.keySet())
        {
            double start_time = Math.max(Params.time, times[0]);
            double end_time = Math.min(Params.time + Params.dt, times[1]);
            
            if(end_time >= start_time)
            {
                rate += demand_rates.get(times) * (end_time - start_time) / Params.dt;
            }
        }
        
        // now add demand at the given rate
        double newDemand = rate * Params.dt / 3600.0;
        
        // split it according to turning proportions
        for(Link ds : getOutgoing())
        {
            ds.addFlow(newDemand * getTurningProp(null, ds));
        }
    }
    
    public void update()
    {
        // nothing to do here
    }
        
    
    /**
     * This is actually useful - it stores which downstream link entering vehicles go to!
     * We need a dummy link to serve as the incoming link, since a source does not have incoming links.
     */
    Link dummy = new Link(-1, null, null, 0, 0, 0, 0)
    {
        public void reset(){}
        public void step(){}
        public void update(){}
        public double getSendingFlow(){return 0;}
        public double getReceivingFlow(){return 0;}
        public void addFlow(double y){}
        public void removeFlow(double y){}
        public double getOccupancy(){return 0;}
    };
    
    /**
     * Used to store exogenous turning proportions from input data.
     */
    public void storeTurningProportion(Link i, Link j, double p)
    {
        super.storeTurningProportion(dummy, j, p);
    }
    
    /**
     * @return the proportion of vehicles turning from {@link Link} i to {@link Link} j.
     */
    public double getTurningProp(Link i, Link j)    
    {
        return super.getTurningProp(dummy, j);
    }
}
