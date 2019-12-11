/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl;

import dnl.link.Link;
import dnl.node.Node;
import dnl.node.Sink;
import dnl.node.Source;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Scanner;
import java.util.Set;

/**
 * This class represents and stores the entire network, including the sets of {@link Node}s and {@link Link}s.
 * Generally, this will be the go-to class for dealing with the network as a whole.
 * The easiest way to construct a new {@link Network} is to create an instance of {@link ReadNetwork}, then call {@link ReadNetwork#createNetwork(String)} with the name of the network folder.
 * To calculate the state of the network at the next timestep, call {@link #nextTimestep()}.
 * There are also methods to get the sets of {@link Node}s and {@link Link}s, and the specific {@link Node} or {@link Link} with a given id.
 * 
 * @author Michael Levin
 */
public class Network 
{
    
    private List<Link> links;
    private List<Node> nodes;
    
    private String name;
    
    /**
     * Constructs the {@link Network} with the given {@link Node} and {@link Link}.
     * In general, the easiest way to construct a {@link Network} will be to create a new {@link ReadNetwork} instance, then call {@link ReadNetwork#createNetwork(String)} with the name of the network folder.
     */
    public Network(String name, List<Node> nodes, List<Link> links)
    {
        this.nodes = nodes;
        this.links = links;
        this.name = name;
    }
    
    /**
     * @return the name of the network
     */
    public String getName()
    {
        return name;
    }
    
    /** 
     * @return the set of all {@link Node}s
     */
    public List<Node> getNodes()
    {
        return nodes;
    }
    
    /**
     * @return the set of all {@link Link}s
     */
    public List<Link> getLinks()
    {
        return links;
    }
    
    
    /**
     * Finds the {@link Node} with the given id. If none exists, returns null.
     */
    public Node getNode(int id)
    {
        for(Node n : nodes)
        {
            if(n.getId() == id)
            {
                return n;
            }
        }
        return null;
    }
    
    
    
    /**
     * Finds the {@link Link} with the given id. If none exists, returns null.
     */
    public Link getLink(int id)
    {
        for(Link l : links)
        {
            if(l.getId() == id)
            {
                return l;
            }
        }
        return null;
    }
    
    
    /**
     * This method uses {@link Network#simulate()} but records the exiting vehicles from each sink node for autograding.
     */
    public double autograde(File solutions) throws IOException
    {
        Scanner filein = new Scanner(solutions);
        
        List<Sink> solOrder = new ArrayList<>();
        
        filein.next();
        
        while(filein.hasNextInt())
        {
            solOrder.add((Sink)getNode(filein.nextInt()));
        }
        
        filein.nextLine();
        
        Params.time = 0;
        
        int count = 0;
        int correct = 0;
        
        try
        {
            while(Params.time <= Params.DURATION)
            {
                nextTimestep();
                
                if(filein.nextInt() != Params.time-Params.dt)
                {
                    throw new RuntimeException("Time mismatch");
                }

                for(Sink s : solOrder)
                {
                    double solution = filein.nextDouble();
                    double exiting = s.getNumExiting();

                    if(solution > 0.1 || exiting > 0.1)
                    {
                        if(Math.abs(solution - exiting) <= 0.01)
                        {
                            correct++;
                        }
                        count++;
                    }
                }
                
                
            }
        }
        catch(NoSuchElementException ex)
        {
            ex.printStackTrace(System.err);
        }
        
        filein.close();
        
        return ((double)correct)/count;
    }
    
    
    public void printAutograde(File output) throws IOException
    {
        PrintStream fileout = new PrintStream(new FileOutputStream(output), true);
        
        fileout.print("time");
        
        List<Sink> sinks = new ArrayList<>();
        
        for(Node n : nodes)
        {
            if(n instanceof Sink)
            {
                sinks.add((Sink)n);
            }
        }
        
        
        for(Sink n : sinks)
        {
            fileout.print("\t"+n.getId());
        }
        fileout.println("\t end");
        
        Params.time = 0;
        
        while(Params.time <= Params.DURATION)
        {
            nextTimestep();
            
            fileout.print(Params.time-Params.dt);
            
            for(Sink n : sinks)
            {
                fileout.print("\t"+n.getNumExiting());
            }
            fileout.println();
        }
        
        fileout.close();

        // calculate the average travel time for each link
        for(Link l : links)
        {
            l.calculateTravelTime();
        }
    }
    
    /**
     * This method resets the network to prepare for the next dynamic network loading.
     */
    public void reset()
    {
        Params.time = 0;
        
        for(Node n : nodes)
        {
            n.reset();
        }
        
        for(Link l : links)
        {
            l.reset();
        }
    }
    
    /**
     * @return the {@link Link} between the given {@link Node}s, or null if none exists.
     */
    public Link getLink(Node i, Node j)
    {
        for(Link l : i.getOutgoing())
        {
            if(l.getDest() == j)
            {
                return l;
            }
        }
        return null;
    }
    
    
    /**
     * This method simulates traffic flow from the current time to {@link Params#DURATION}. 
     * It calls {@link Network#nextTimestep()} for each time step.
     */
    public void simulate()
    {
        while(Params.time <= Params.DURATION)
        {
            nextTimestep();
        }
        
        // calculate the average travel time for each link
        for(Link l : links)
        {
            l.calculateTravelTime();
        }
    }
    
    
    
    
    /**
     * This method calculates the state of the network at the next time step. 
     * First, it calls {@link Link#step()} and {@link Node#step()} on all {@link Node}s and {@link Link}s.
     * Then, it calls {@link Link#update()} and {@link Node#update()} on all {@link Node}s and {@link Link}s.
     * {@link Node}s and {@link Link}s should implement step() and update() according to their specific traffic flow behavior.
     */
    public void nextTimestep()
    {
        // calculate flow to move during the next time step
        for(Link l : links)
        {
            l.step();
        }
        
        // calculate flow to move during the next time step
        for(Node n : nodes)
        {
            n.step();
        }
        
        // actually move flow for the next time step
        for(Link l : links)
        {
            l.update();
        }
        
        // actually move flow for the next time step
        for(Node n : nodes)
        {
            n.update();
        }
        
        // Used to calculate average travel time. 
        for(Link l : links)
        {
            l.logOccupancyTime();
        }
        
        
        // update the current time
        Params.time += Params.dt;
        
    }
    
    
    
    /**
     * Runs one-to-all shortest path rooted at the specified destination node.
     * This method sets the {@link Node} shortest path labels, {@link Node#cost} and {@link Node#pred}.
     */
    public void dijkstras(Node dest)
    {
        // fill this in
    }
   
    
    
    /**
     * After running {@link Network#dijkstras()}, this method is used to find the shortest path between an origin and a destination.
     */
    public Path trace(Node origin, Node dest)
    {
        // fill this in
        return null;
    }
    
    /**
     * This method calls {@link #dijkstras(Node)} then {@link #trace(Node, Node)} to find the shortest path between two {@link Node}s.
     */
    public Path shortestPath(Node origin, Node dest)
    {
        dijkstras(dest);
        return trace(origin, dest);
    }

    /**
     * Assumption: only one destination node exists in this network.
     * @param num_iterations the number of iterations
     */
    public void msa(int num_iterations)
    {
        // delete turning proportions
        for(Node n : nodes)
        {
            n.clearTurningProportions();
        }
        
        // find destination node
        Sink dest = null;
        for(Node n : nodes)
        {
            if(n instanceof Sink)
            {
                if(dest != null)
                {
                    throw new RuntimeException("DNL is not equipped to handle multiple destinations.");
                }
                dest = (Sink)n;
            }
        }
        
        System.out.println("Iteration\tGap");
        
        for(int iteration = 1; iteration <= num_iterations; iteration++)
        {
            double lambda = 1.0/iteration;
            
            double gap = msa_iteration(lambda, dest);
            
            System.out.println(iteration+"\t"+gap);
        }
    }
    
    public double msa_iteration(double lambda, Sink dest)
    {
        // Find all-or-nothing assignment.
        
        // Take lambda-weighted convex combination of all-or-nothing assignment and current assignment.
        // This involves adjusting the turning proportions at each node. 
        
        
        
        
        
        
        
        
        
        simulate();
        reset();
        
        return calculateGap(dest);
    }
    
    public double calculateGap(Sink dest)
    {
        // fill this in
        return 0.0;
    }
    
    /**
     * @return the shortest path TSTT possible if travel times are equal to the current shortest paths.
     */
    public double getSPTT(Sink dest)
    {
        // fill this in
        return 0.0;
    }
    
    public double getTSTT()
    {
        double output = 0.0;
        
        for(Link l : links)
        {
            output += l.getTotalTT();
        }
        
        return output;
    }
}
