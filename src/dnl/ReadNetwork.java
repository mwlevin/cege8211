/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl;

import dnl.link.MN;
import dnl.link.CTM;
import dnl.link.CentroidConnector;
import dnl.link.LTM;
import dnl.link.Link;
import dnl.link.PointQueue;
import dnl.link.SpatialQueue;
import dnl.node.Diverge;
import dnl.node.Series;
import dnl.node.Merge;
import dnl.node.Node;
import dnl.node.PedSignal;
import dnl.node.Signal;
import dnl.node.Sink;
import dnl.node.Source;
import dnl.node.StopSign;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.TreeMap;

/**
 * 
 * @author Michael Levin
 */
public class ReadNetwork 
{
    /**
     * These are Node types. They are not case-sensitive.
     * They correspond to the type field in the nodes.txt input file.
     * They are used to identify the Node subclass that is to be constructed.
     */
    public static final String SOURCE = "source";
    public static final String SINK = "sink";
    public static final String SERIES = "series";
    public static final String DIVERGE = "diverge";
    public static final String MERGE = "merge";
    public static final String SIGNAL = "signal";
    public static final String STOP_SIGN = "stop-sign";
    public static final String PED_SIGNAL = "ped-signal";
    
    /**
     * These are Link types. They are not case-sensitive.
     * They are used in the type field in the links.txt input file.
     */
    public static final String CTM = "CTM";
    public static final String LTM = "LTM";
    public static final String CENTROID_CONNECTOR = "centroid-connector";
    public static final String POINT_QUEUE = "point-queue";
    public static final String SPATIAL_QUEUE = "spatial-queue";
    public static final String MN = "mn";
    
    
    
    
    
    private String network_name;
    
    
    private Map<Integer, Node> nodesmap;
    private Map<Integer, Link> linksmap;
    
    /**
     * Constructs a new ReadNetwork
     */
    public ReadNetwork()
    {
        
    }
    
    /**
     * Reads in the network with the given directory.
     * For instance, if given the name "2-link", it will read in the network in the "networks/2-link" folder.
     */
    public Network createNetwork(String name)
    {
        System.out.println("Creating network "+name);
        
        network_name = name;
        
        nodesmap = new TreeMap<>();
        linksmap = new TreeMap<>();
        
        readParams(new File("networks/"+name+"/params.txt"));
        readNodes(new File("networks/"+name+"/nodes.txt"));
        readLinks(new File("networks/"+name+"/links.txt"));
        readSignals(new File("networks/"+name+"/signals.txt"), new File("networks/"+name+"/phases.txt"));
        
        
        readTurningProportions(new File("networks/"+name+"/turning_proportions.txt"));
        readDemand(new File("networks/"+name+"/demand.txt"));
        
        
        List<Node> nodes = new ArrayList<>();
        List<Link> links = new ArrayList<>();
        
        
        for(int i : nodesmap.keySet())
        {
            nodes.add(nodesmap.get(i));
        }
        
        for(int i : linksmap.keySet())
        {
            links.add(linksmap.get(i));
        }
        
        nodesmap = null;
        linksmap = null;
        
        return new Network(name, nodes, links);
    }
    
    public void readParams(File params)
    {
        try
        {
            Scanner filein = new Scanner(params);

            filein.nextLine();

            while(filein.hasNext())
            {
                String next = filein.next();
                double value = filein.nextDouble();

                if(next.equalsIgnoreCase("dt"))
                {
                    Params.dt = (int)value;
                }
                else if(next.equalsIgnoreCase("duration"))
                {
                    Params.DURATION = (int)value;
                }
                else if(next.equalsIgnoreCase("jam_density"))
                {
                    Params.JAM_DENSITY = value;
                }
            }

            filein.close();
        }
        catch(FileNotFoundException ex)
        {
            System.out.println("\tSkipping file \"networks/"+network_name+"/params.txt\"");
        }
    }
    
    /**
     * Constructs a node with the given parameters.
     * Elevation is in ft.
     */
    public Node createNode(int id, String type, double longitude, double latitude, double elevation)
    {
        if(type.equalsIgnoreCase(SOURCE))
        {
            return new Source(id, longitude, latitude, elevation);
        }
        else if(type.equalsIgnoreCase(SINK))
        {
            return new Sink(id, longitude, latitude, elevation);
        }
        else if(type.equalsIgnoreCase(SERIES))
        {
            return new Series(id, longitude, latitude, elevation);
        }
        else if(type.equalsIgnoreCase(DIVERGE))
        {
            return new Diverge(id, longitude, latitude, elevation);
        }
        else if(type.equalsIgnoreCase(MERGE))
        {
            return new Merge(id, longitude, latitude, elevation);
        }
        else if(type.equalsIgnoreCase(SIGNAL))
        {
            return new Signal(id, longitude, latitude, elevation);
        }
        else if(type.equalsIgnoreCase(STOP_SIGN))
        {
            return new StopSign(id, longitude, latitude, elevation);
        }
        else if(type.equalsIgnoreCase(PED_SIGNAL))
        {
            return new PedSignal(id, longitude, latitude, elevation);
        }
        else
        {
            throw new RuntimeException("Node type not recognized: "+type);
        }
    }
    
    
    /**
     * Constructs a link with the given parameters.
     * Capacity is in veh/hr.
     * Free flow speed is in mi/hr.
     * Length is in mi.
     */
    public Link createLink(int id, String type, Node source, Node dest, double length, double ffspeed, double capacity, int numLanes)
    {
        if(type.equalsIgnoreCase(CTM))
        {
            return new CTM(id, source, dest, length, ffspeed, capacity, numLanes);
        }
        else if(type.equalsIgnoreCase(LTM))
        {
            return new LTM(id, source, dest, length, ffspeed, capacity, numLanes);
        }
        else if(type.equalsIgnoreCase(POINT_QUEUE))
        {
            return new PointQueue(id, source, dest, length, ffspeed, capacity, numLanes);
        }
        else if(type.equalsIgnoreCase(SPATIAL_QUEUE))
        {
            return new SpatialQueue(id, source, dest, length, ffspeed, capacity, numLanes);
        }
        else if(type.equalsIgnoreCase(CENTROID_CONNECTOR))
        {
            return new CentroidConnector(id, source, dest, length, ffspeed, capacity, numLanes);
        }
        else if(type.equalsIgnoreCase(MN))
        {
            return new MN(id, source, dest, length, ffspeed, capacity, numLanes);
        }
        else
        {
            throw new RuntimeException("Link type ont recognized: "+type);
        }
    }
    
    /**
     * Reads all nodes from the specified file.
     * Header data is ignored.
     */
    public void readNodes(File file)
    {
        try
        {
            Scanner filein = new Scanner(file);

            while(!filein.hasNextInt() && filein.hasNextLine())
            {
                filein.nextLine();
            }

            while(filein.hasNextInt())
            {
                int id = filein.nextInt();
                String type = filein.next();
                double longitude = filein.nextDouble();
                double latitude = filein.nextDouble();
                double elevation = filein.nextDouble();

                Node node = createNode(id, type, longitude, latitude, elevation);

                nodesmap.put(node.getId(), node);


                if(filein.hasNextLine())
                {
                    filein.nextLine();
                }
            }
            filein.close();
        }
        catch(FileNotFoundException ex)
        {
            throw new RuntimeException("Cannot find file \"networks/"+network_name+"/nodes.txt\"");
        }
    }
    
    
    /**
     * Reads all links from the specified file.
     * Header data is ignored.
     */
    public void readLinks(File file)
    {
        try
        {
            Scanner filein = new Scanner(file);

            while(!filein.hasNextInt() && filein.hasNextLine())
            {
                filein.nextLine();
            }

            while(filein.hasNextInt())
            {
                int id = filein.nextInt();
                String type = filein.next();
                int source_id = filein.nextInt();
                int dest_id = filein.nextInt();
                double length = filein.nextDouble();
                double ffspd = filein.nextDouble();
                double capacityPerLane = filein.nextDouble();
                int numLanes = filein.nextInt();

                Node source = nodesmap.get(source_id);
                Node dest = nodesmap.get(dest_id);

                if(source == null)
                {
                    throw new RuntimeException("Source node not found: "+source_id);
                }

                if(dest == null)
                {
                    throw new RuntimeException("Dest node not found: "+dest_id);
                }

                Link link = createLink(id, type, source, dest, length, ffspd, capacityPerLane, numLanes);

                linksmap.put(link.getId(), link);


                if(filein.hasNextLine())
                {
                    filein.nextLine();
                }
            }
            filein.close();
        }
        catch(FileNotFoundException ex)
        {
            throw new RuntimeException("Cannot find file \"networks/"+network_name+"/links.txt\"");
        }
    }

    /**
     * Reads the demand (incoming vehicles) from the given file
     */
    public void readDemand(File file)
    {
        try
        {
            Scanner filein = new Scanner(file);

            while(!filein.hasNextInt() && filein.hasNextLine())
            {
                filein.nextLine();
            }

            while(filein.hasNextInt())
            {
                int node_id = filein.nextInt();
                double start_time = filein.nextDouble();
                double end_time = filein.nextDouble();
                double rate = filein.nextDouble();

                Node node = nodesmap.get(node_id);

                if(node == null)
                {
                    throw new RuntimeException("Cannot find node "+node_id);
                }

                if(!(node instanceof Source))
                {
                    throw new RuntimeException("Attempting to add demand to non-source node: "+node_id);
                }

                ((Source)node).addDemand(start_time, end_time, rate);
            }
        }
        catch(FileNotFoundException ex)
        {
            throw new RuntimeException("Cannot find file \"networks/"+network_name+"/demand.txt\"");
        }
    }
    
    /** 
     * Reads the turning proportions from the given file.
     */
    public void readTurningProportions(File file)
    {
        try
        {
            Scanner filein = new Scanner(file);

            while(!filein.hasNextInt() && filein.hasNextLine())
            {
                filein.nextLine();
            }

            while(filein.hasNextInt())
            {
                int upstream_id = filein.nextInt();
                int downstream_id = filein.nextInt();
                double proportion = filein.nextDouble();

                Link upstream = linksmap.get(upstream_id);
                Link downstream = linksmap.get(downstream_id);

                if(upstream == null && downstream == null)
                {
                    throw new RuntimeException("Cannot find link pair: upstream: "+upstream_id+" downstream: "+downstream_id);
                }

                if(downstream != null)
                {
                    downstream.getSource().storeTurningProportion(upstream, downstream, proportion);
                }
                else
                {
                    upstream.getDest().storeTurningProportion(upstream, downstream, proportion);
                }

                if(filein.hasNextLine())
                {
                    filein.nextLine();
                }
            }
            filein.close();
        }
        catch(FileNotFoundException ex){
            System.out.println("\tSkipping file \"networks/"+network_name+"/turning_proportions.txt\"");
        }
    }
    
    /**
     * This method reads the signal cycle data for all nodes.
     * Note that signal cycle data will only be stored for nodes that are actual signals. Otherwise, it will be ignored.
     * This method reads two files: first, it looks at signals.txt to calculate the offset. Then, it looks at phases.txt to read signal phases
     */
    public void readSignals(File signals, File phases)
    {
        try
        {
            Scanner filein = new Scanner(signals);

            while(!filein.hasNextInt() && filein.hasNextLine())
            {
                filein.nextLine();
            }

            while(filein.hasNextInt())
            {
                int node_id = filein.nextInt();
                double offset = filein.nextDouble();

                Node node = nodesmap.get(node_id);

                if(node == null)
                {
                    throw new RuntimeException("Cannot find node "+node_id);
                }

                if(node instanceof Signal)
                {
                    ((Signal)node).setOffset(offset);
                }

                if(filein.hasNextLine())
                {
                    filein.nextLine();
                }
            }
            filein.close();
        }
        catch(FileNotFoundException ex)
        {
            System.out.println("\tSkipping file \"networks/"+network_name+"/signals.txt\"");

        }
        
        try
        {
            Scanner filein = new Scanner(phases);

            while(!filein.hasNextInt() && filein.hasNextLine())
            {
                filein.nextLine();
            }

            while(filein.hasNextInt())
            {
                int node_id = filein.nextInt();
                String type = filein.next();
                int sequence = filein.nextInt();
                double all_red = filein.nextDouble();
                double yellow = filein.nextDouble();
                double green = filein.nextDouble();

                int num_moves = filein.nextInt();

                String line = filein.nextLine();

                // String[] containing ids of incoming links
                String[] inc_links = line.substring(line.indexOf('{')+1, line.indexOf('}')).split(",");

                // String[] containing ids of outgoing links
                line = line.substring(line.indexOf('}')+1);
                String[] out_links = line.substring(line.indexOf('{')+1, line.indexOf('}')).split(",");

                // this is a list of protected turning movements
                List<Link[]> protected_turns = new ArrayList<>();

                for(int idx = 0; idx < num_moves; idx++)
                {
                    int i_id = Integer.parseInt(inc_links[idx].trim());
                    int j_id = Integer.parseInt(out_links[idx].trim());

                    Link i = linksmap.get(i_id);
                    Link j = linksmap.get(j_id);

                    if(i == null)
                    {
                        throw new RuntimeException("Cannot find link "+i_id);
                    }

                    if(j == null)
                    {
                        throw new RuntimeException("Cannot find link "+j_id);
                    }

                    protected_turns.add(new Link[]{i, j});
                }

                Node node = nodesmap.get(node_id);

                if(node == null)
                {
                    throw new RuntimeException("Cannot find node "+node_id);
                }

                if(node instanceof Signal)
                {
                    ((Signal)node).addPhase(sequence, green, yellow, all_red, protected_turns);
                }

            }
        }
        catch(FileNotFoundException ex){
            System.out.println("\tSkipping file \"networks/"+network_name+"/phases.txt\"");
        }
    }
    
}
