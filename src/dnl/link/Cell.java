/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl.link;

import dnl.Params;

/**
 * This class represents a single cell in the cell transmission model.
 * It should be constructed as needed by class CTM.
 * 
 * @author 
 */
public class Cell 
{
    /**
     * This is the CTM link that this cell belongs to.
     * Having a reference is useful...
     */
    private CTM link;
    
    
    /**
     * Having references to the previous and next cell is probably useful for propagating flow.
     * These are initially null! You have to set these references in class CTM AFTER all the cells have been constructed.
     * Use setNextCell(), setPrevCell() to update these references.
     */
    private Cell prev, next;
    
    
    /**
     * Constructs a Cell as part of the given CTM link.
     * You may want to add additional parameters here.
     */
    public Cell(CTM link)
    {
        this.link = link;
    }
    
    public double getOccupancy()
    {
        // fill this in
        return 0.0;
    }
    
    /**
     * Update the reference to the next (downstream) cell.
     */
    public void setNextCell(Cell next)
    {
        this.next = next;
    }
    
    /**
     * Update the reference to the previous (upstream) cell.
     */
    public void setPrevCell(Cell prev)
    {
        this.prev = prev;
    }
    
    
    
    public void step()
    {
        // fill this in
    }
    
    public void update()
    {
        // fill this in
    }
    
    public double getSendingFlow()
    {
        // fill this in
        return 0.0;
    }
    
    public double getReceivingFlow()
    {
        // fill this in
        return 0.0;
    }
    
    public void addFlow(double y)
    {
        // fill this in
    }
    
    public void removeFlow(double y)
    {
        // fill this in
    }
}
