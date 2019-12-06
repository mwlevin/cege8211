/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl;

import java.io.File;
import java.io.IOException;

/**
 * This is the Main class. This class contains the entry point for running the project, method main(String[]). 
 * 
 * 
 * @author Michael Levin
 */
public class Main {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException
    {
        //ReadNetwork read = new ReadNetwork();
        //Network network = read.createNetwork("signal1");
        //network.simulate();
        
        Autograde.createSolutions(new File("HW6.txt"));
        System.out.println(Autograde.gradeHW(new File("HW6.txt")));
        
    }
    
}
