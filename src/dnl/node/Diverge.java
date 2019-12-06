/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dnl.node;

import dnl.Params;
import dnl.link.Link;

/**
 * This class represents a diverge: where 1 upstream link branches out into 2 or more downstream links.
 * 
 * @author 
 */
public class Diverge extends Node
{
    public Diverge(int id, double longitude, double latitude, double elevation)
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
