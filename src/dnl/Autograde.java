/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl;

import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.util.Scanner;

/**
 *
 * @author mlevin
 */
public class Autograde 
{
    public static void main(String[] args) throws IOException
    {
        gradeHW(new File("HW2.txt"));
    }
    
    /**
     * Grades the test cases listed in the following file. 
     * Each line of the file contains the name of a test case, e.g. hw1 corresponds to the "networks/hw1/" network.
     * Returns a number between 0 and 1 indicating the percent correct. Each test cases is weighted equally.
     */
    public static double gradeHW(File testCases) throws IOException
    {
        System.setOut(new PrintStream(new File("log.txt")));
        
        
        int total = 0;
        double correct = 0;
        
        
        // used to trigger running msa() first before running dynamic network loading
        boolean dta = false;
        int num_iter = 0;
        
        Scanner filein = new Scanner(testCases);
        
        System.err.println("Grading "+testCases+" tests\n");
        System.err.println("-------");
        
        while(filein.hasNext())
        {
            String name = filein.next();
            
            if(name.equalsIgnoreCase("dta"))
            {
                dta = true;
                num_iter = filein.nextInt();
                continue;
            }
            
            String description = "";
            if(filein.hasNextLine())
            {
                description = filein.nextLine().trim();
            }
            
            if(description.length() == 0)
            {
                description = name;
            }
            
            double output;
            
            if(dta)
            {
                output = gradeNetworkDTA(name, num_iter);
            }
            else
            {
                output = gradeNetwork(name);
            }
            
            System.err.println("Running "+description+" test: networks/"+name+"/"); 
            System.err.println("\tScore: "+((int)Math.round(output*100.0))+"%");
            correct += output;
            
            total++;
        }
        filein.close();
        
        System.err.println("-------");
        System.err.println("Total: "+((int)Math.round(correct/total * 100.0))+"%");
        System.err.println("\nThis is an unofficial score, please submit code for final scoring.");
        return correct/total;
    }
    
    public static double gradeNetwork(String name) throws IOException
    {
        ReadNetwork read = new ReadNetwork();
        Network network = read.createNetwork(name);

        return network.autograde(new File("networks/"+name+"/solution.txt"));
    }
    
    public static double gradeNetworkDTA(String name, int num_iter) throws IOException
    {
        ReadNetwork read = new ReadNetwork();
        Network network = read.createNetwork(name);
        
        network.msa(num_iter);

        return network.autograde(new File("networks/"+name+"/solution.txt"));
    }
    
    public static void createSolutions(File testCases) throws IOException
    {
        Scanner filein = new Scanner(testCases);
        
        
        // used to trigger running msa() first before running dynamic network loading
        boolean dta = false;
        int num_iter = 0;
        
        while(filein.hasNext())
        {
            String name = filein.next();
            
            if(name.equalsIgnoreCase("dta"))
            {
                dta = true;
                num_iter = filein.nextInt();
                continue;
            }
            
            if(filein.hasNextLine())
            {
                filein.nextLine();
            }
            
            ReadNetwork read = new ReadNetwork();
            Network network = read.createNetwork(name);

            if(dta)
            {
                network.msa(num_iter);
            }
            
            network.printAutograde(new File("networks/"+name+"/solution.txt"));
        }
        filein.close();
    }
}
