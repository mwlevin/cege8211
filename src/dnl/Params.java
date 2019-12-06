/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl;

/**
 * This class stores important global parameters that are useful across the entire project.
 * 
 * @author Michael Levin
 */
public class Params 
{
    /**
     * This is the time step, in seconds
     */
    public static final int dt = 6;

    /**
     * This is the current time in the network. It is updated when {@link Network.newTimestep()} is called.
     */
    public static int time = 0;
    
    
    /**
     * this is the end time of the simulation, in s. The maximum number of time steps is {@link Params.DURATION}/{@link Params.dt}.
     */
    public static final int DURATION = 7200;
    
    /**
     * The exogenous vehicle length, in ft. Assume 20ft per vehicle.
     */
    public static final double VEHICLE_LENGTH = 20;
    
    /**
     * The exogenous jam density, which is calculated based on {@link Params.VEHICLE_LENGTH}.
     */
    public static final double JAM_DENSITY = 5280.0/VEHICLE_LENGTH;
}
