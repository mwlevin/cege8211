/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl.node;

import dnl.Params;
import dnl.link.Link;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * This class represents a merge: where 2 or more upstream links combine into 1 downstream link.
 * 
 * @author 
 */
public class Merge extends Node
{
    public Merge(int id, double longitude, double latitude, double elevation)
    {
        super(id, longitude, latitude, elevation);
    }
    
    public void step()
    {
        // fill this in
    }
    
    public void update()
    {
        // fill this in
    }
}
