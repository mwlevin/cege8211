/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl.node;

import dnl.link.Link;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * This represents a node in the network.
 * This is an abstract class: key methods are not implemented, and must be implemented in subclasses. 
 * These depend on the specific intersection model.
 * 
 * @author Michael Levin
 */
public abstract class Node implements Comparable<Node>
{
    // id used to reference the node
    private int id;
    
    /**
     * Stores turning proportions between links. 
     * Turning proportions specify the route assignment.
     */
    private Map<Link, Map<Link, Double>> turning_prop;
    
    /**
     * Stores sets of incoming and outgoing links
     */
    private List<Link> incoming, outgoing;
    
    
    /**
     * Elevation, in ft
     */
    private double elevation;
    
    // latitude and longitude
    private double latitude, longitude;
    
    /**
     * Constructs the {@link Node} with the given id, latitude, longitude, and elevation.
     * The incoming and outgoing sets of {@link Link}s will be updated automatically as {@link Link}s are constructed.
     * 
     * @param id the id of this {@link Node}
     * @param longitude the longitude portion of the location
     * @param latitude the latitude portion of the location
     * @param elevation the elevation (in ft)
     */
    public Node(int id, double longitude, double latitude, double elevation)
    {
        // store node parameters
        this.id = id;
        this.elevation = elevation;
        this.latitude = latitude;
        this.longitude = longitude;
        
        
        // construct incoming and outgoing sets. They will be populated as links are constructed.
        incoming = new ArrayList<>();
        outgoing = new ArrayList<>();
        
        turning_prop = new HashMap<>();
    }
    
    /**
     * Resets this {@link Node} to start a new dynamic network loading
     */
    public abstract void reset();
    
    
    /**
     * @return the elevation (in ft)
     */
    public double getElevation()
    {
        return elevation;
    }
    
    /**
     * @return the latitude.
     */
    public double getLatitude()
    {
        return latitude;
    }
    
    /**
     * @return the longitude.
     */
    public double getLongitude()
    {
        return longitude;
    }
    
    /**
     * Used when constructing the {@link Node}: adjusts the turning proportion from {@link Link} i to {@link Link} j.
     * Turning proportions must add to 1 for all incoming {@link Link}s.
     */
    public void storeTurningProportion(Link i, Link j, double p)
    {
        if(!turning_prop.containsKey(i))
        {
            turning_prop.put(i, new HashMap<>());
        }
        turning_prop.get(i).put(j, p);
    }
    
    
    /**
     * @return the Map of turning proportions
     */
    public Map<Link, Map<Link, Double>> getTurningProportions()
    {
        return turning_prop;
    }
    
    
    /**
     * Deletes all stored turning proportions. 
     * This method is used for DTA.
     */
    public void clearTurningProportions()
    {
        turning_prop.clear();
    }
    
    
    /**
     * @return the proportion of flow leaving {@link Link} i turning onto {@link Link} j. The value is between 0 and 1.
     */
    public double getTurningProp(Link i, Link j)    
    {
        if(getOutgoing().size() <= 1)
        {
            return 1;
        }
        if(turning_prop.containsKey(i) && turning_prop.get(i).containsKey(j))
        {
            return turning_prop.get(i).get(j);
        }
        else
        {
            return 0.0;
        }
    }
    
    /**
     * @return the set of incoming {@link Link}s
     */
    public List<Link> getIncoming()
    {
        return incoming;
    }
    
    /**
     * @return the set of outgoing {@link Link}s
     */
    public List<Link> getOutgoing()
    {
        return outgoing;
    }
    
    /**
     * Adds the {@link Link} to the incoming or outgoing sets of links, as appropriate
     */
    public void addLink(Link l)
    {
        if(l.getSource() == this)
        {
            outgoing.add(l);
        }
        else if(l.getDest() == this)
        {
            incoming.add(l);
        }
    }
    
    /**
     * @return the id for this {@link Node}
     */
    public int getId()
    {
        return id;
    }
    
    /**
     * This is called every time step. 
     * For the {@link Node} class, {@link #step()} should move flow between incoming and outgoing {@link Link}s.
     */
    public abstract void step();
    
    /**
     * This is called every time step, after {@link #step()} has been called for all {@link Node}s and {@link Link}s.
     * It can be used to finish any updating work that could not occur during {@link #step()}.
     * DO NOT use this to update the internal state of {@link Link}s. This is used to update the state of this {@link Node}.
     */
    public abstract void update();
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    /**
     * Used to sort {@link Node}s by id.
     */
    public int compareTo(Node rhs)
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
     * Returns the id of the {@link Node}
     */
    public String toString()
    {
        return ""+id;
    }
    
    
    // used by shortest path
    public Link pred;
    public double cost;
}
