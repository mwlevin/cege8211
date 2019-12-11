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
    public static int dt = 6;

    /**
     * This is the current time in the network. It is updated when {@link Network#nextTimestep()} is called.
     */
    public static int time = 0;
    
    
    /**
     * this is the end time of the simulation, in s. The maximum number of time steps is {@link #DURATION}/{@link #dt}.
     */
    public static int DURATION = 7200;
    

    /**
     * The exogenous jam density, which is calculated based on {@link #VEHICLE_LENGTH}.
     */
    public static double JAM_DENSITY = 264.0;
}
