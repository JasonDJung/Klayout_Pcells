# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 22:44:59 2024

@author: seho2
"""

import gdstk
import math
import numpy as np


# call gdstk library
lib = gdstk.Library()  

def rectangle(corner1,corner2,cell_name,layer):
    cell = lib.new_cell(cell_name)
    
    path = gdstk.rectangle(corner1,corner2,layer,datatype=0)
    cell.add(path)
    
    return cell

def BezierCurve(radius,width,cell_name,layer=1):
    cell = lib.new_cell(cell_name)
    NumOfPts = math.ceil(radius*100)  
    # bezier
    points_references = [(radius,0),(radius,radius),(0,radius)]
    points_curve = [points_references[0]]

    for t in np.linspace(0,1, num=NumOfPts):
        x_temp = points_references[0][0]*((1-t)**2)+2*t*(1-t)*points_references[1][0]+points_references[2][0]*(t**2)
        y_temp = points_references[0][1]*((1-t)**2)+2*t*(1-t)*points_references[1][1]+points_references[2][1]*(t**2)
        points_curve.append((x_temp,y_temp))
    
    # path
    path_bezier = gdstk.FlexPath(points_curve, width,layer)
    cell.add(path_bezier)
    
    return cell

def Bezier(pointsets,width,cell_name,layer0=1):
    cell = lib.new_cell(cell_name)
    # path
    path = gdstk.FlexPath((0,0), width,layer=layer0, tolerance=1e-6)
    path.bezier(pointsets) # point sets: [(4, 1), (4, 3), (0, 5)]
    cell.add(path)
    
    return cell

def Arc(radius,initial_angle,final_angle,width,cell_name,layer0=1):
    cell = lib.new_cell(cell_name)
    # path
    path = gdstk.FlexPath(((0,0)), width,layer=layer0, tolerance=1e-5)
    path.arc(radius,initial_angle,final_angle) # point sets: [(4, 1), (4, 3), (0, 5)]
    cell.add(path)
    
    return cell

def Racetrack(width,radius,InteractionLength,cell_name,DrawingLayer=1):    
    cell = lib.new_cell(cell_name)
    
    # upper bezier
    path = gdstk.FlexPath((radius,InteractionLength/2), width,layer=DrawingLayer, tolerance=1e-5,datatype=0)
    pointsets = [(radius,radius+InteractionLength/2),(0,radius+InteractionLength/2),(-radius,radius+InteractionLength/2),(-radius,InteractionLength/2)]
    path.bezier(pointsets) # point sets: [(4, 1), (4, 3), (0, 5)]
    cell.add(path)
    
    # interaction part1
    corner1 = (radius-width/2,-InteractionLength/2)
    corner2 = (radius+width/2,InteractionLength/2)
    path = gdstk.rectangle(corner1,corner2,layer=DrawingLayer,datatype=0)
    cell.add(path)
    # interaction part2
    corner1 = (-radius-width/2,-InteractionLength/2)
    corner2 = (-radius+width/2,InteractionLength/2)
    path = gdstk.rectangle(corner1,corner2,layer=DrawingLayer,datatype=0)
    cell.add(path)
    
    # lower bezier
    path = gdstk.FlexPath((radius,-InteractionLength/2), width,layer=DrawingLayer, tolerance=1e-5)
    pointsets2 = [(radius,-radius-InteractionLength/2),(0,-radius-InteractionLength/2),(-radius,-radius-InteractionLength/2),(-radius,-InteractionLength/2)]
    path.bezier(pointsets2) # point sets: [(4, 1), (4, 3), (0, 5)]
    cell.add(path)
    
    return cell


def GC2(width, tap_l=18, ArcAngle=np.pi*35/180, GC_footprint=20, GC_separation=200, pitch = 0.485, FillFactor=0.4, straight_length=100, cell_name="GC2_test", DrawingLayer=1):
    # Creates a two grating couplers connected by a bezier bend in the shape of a semicircle
    # @ params
    #    width               width of waveguide
    #    tap_l               taper length of the grating coupler
    #    ArcAngle            Angle of the grating coupler
    #    GC_footprint        Size of the cell
    #    GC_separation       Separation between the two grating couplers
    #    pitch               Separation between each tooth of the grating coupler
    #    FillFactor          Measure of how dense the grating coupler is
    #    straight_length     The length of the waveguide between the end of the bezier bend and the grating coupler
    #    cell_name           User defined name for the cell
    #    DrawingLayer        Layer 
    
    # @ Ret
    #   pcell object
     
    # Generate GC------------------------------------------------------------------
    cell = lib.new_cell(cell_name)
    NumOfCycle = math.floor(GC_footprint/pitch)
    
    #cell_str = "GC_" + str(pitch) + "_" + str(FillFactor)
    #cell = lib.new_cell(cell_str)
    
    r_pitch = tap_l
    length_tooth = math.floor(pitch*FillFactor/0.001)
    length_tooth = 0.001*length_tooth
    
    # tapered part
    tapered = gdstk.ellipse((-GC_separation/2,0),r_pitch,
                            initial_angle=-np.pi/2-ArcAngle/2,
                            final_angle=-np.pi/2+ArcAngle/2,
                          layer=DrawingLayer)
    
    tapered2 = gdstk.ellipse((GC_separation/2,0),r_pitch,
                            initial_angle=-np.pi/2-ArcAngle/2,
                            final_angle=-np.pi/2+ArcAngle/2,
                          layer=DrawingLayer)        
    
    cell.add(tapered, tapered2)
    
    # teeth part
    for n in range(1,NumOfCycle):
        r_pitch = r_pitch+pitch
        r_in = r_pitch-length_tooth;
        tooth = gdstk.ellipse((-GC_separation/2,0),r_pitch,r_in,
                              initial_angle=-np.pi/2-ArcAngle/2,
                              final_angle=-np.pi/2+ArcAngle/2,
                              layer=DrawingLayer)
        tooth2 = gdstk.ellipse((GC_separation/2,0),r_pitch,r_in,
                              initial_angle=-np.pi/2-ArcAngle/2,
                              final_angle=-np.pi/2+ArcAngle/2,
                              layer=DrawingLayer)            
        
        cell.add(tooth, tooth2)
   
    # WG---------------------------------------------------------------------------
    #width = 0.4 
    radius = GC_separation/2
    NumOfPts = math.ceil(radius*500/62.5)
    h = width/2/math.tan(ArcAngle/2) - straight_length;
    
    # bezier
    points_references = [(radius,-h),(radius,radius-h),(0,radius-h)]
    points_curve = [points_references[0]]
    for t in np.linspace(0, 1, num=NumOfPts):
        x_temp = points_references[0][0]*((1-t)**2)+2*t*(1-t)*points_references[1][0]+points_references[2][0]*(t**2)
        y_temp = points_references[0][1]*((1-t)**2)+2*t*(1-t)*points_references[1][1]+points_references[2][1]*(t**2)
        points_curve.append((x_temp,y_temp))
        if t == 0:
            x_start = (x_temp)
            y_start = (y_temp)


    path1 = gdstk.FlexPath([(x_start, y_start), (x_start, y_start - straight_length)], width, layer=1)
    
    
    # path
    path_bezier = gdstk.FlexPath(points_curve, width,layer=1)
    cell.add(path_bezier)
    cell.add(path1)

    points_references = [(-radius,0-h),(-radius,radius-h),(0,radius-h)]
    points_curve = [points_references[0]]

    for t in np.linspace(0,1, num=NumOfPts):
        x_temp = points_references[0][0]*((1-t)**2)+2*t*(1-t)*points_references[1][0]+points_references[2][0]*(t**2)
        y_temp = points_references[0][1]*((1-t)**2)+2*t*(1-t)*points_references[1][1]+points_references[2][1]*(t**2)
        points_curve.append((x_temp,y_temp))
        if t == 0:
            x_start = (x_temp)
            y_start = (y_temp)


    path2 = gdstk.FlexPath([(x_start, y_start), (x_start, y_start - straight_length)], width, layer=1)
    cell.add(path2)
    # path
    path_bezier = gdstk.FlexPath(points_curve, width,layer=1)
    cell.add(path_bezier)
    

    return cell

def GC4(width, tap_l=18, ArcAngle=np.pi*35/180, GC_footprint=20, GC_separation=250, pitch_TE=0.485, pitch_TM=0.485, FillFactor=0.4, cell_name="GC4_test", DrawingLayer=1):
    # Generate GC------------------------------------------------------------------
    cell = lib.new_cell(cell_name)
    NumOfCycle_TE = math.floor(GC_footprint/pitch_TE)
    NumOfCycle_TM = math.floor(GC_footprint/pitch_TM)
    
    # TE gratings
    for ii in range(1,3):
        r_pitch = tap_l
        length_tooth = math.floor(pitch_TE*FillFactor/0.001)
        length_tooth = 0.001*length_tooth
        # tapered part
        tapered = gdstk.ellipse((-3*GC_separation/2+2*(ii-1)*GC_separation,0),r_pitch,
        initial_angle=-np.pi/2-ArcAngle/2,
        final_angle=-np.pi/2+ArcAngle/2,layer=DrawingLayer)      
        cell.add(tapered)

        # teeth part
        for n in range(1,NumOfCycle_TE):
            r_pitch = r_pitch+pitch_TE
            r_in = r_pitch-length_tooth;
            tooth = gdstk.ellipse((-3*GC_separation/2+2*(ii-1)*GC_separation,0),r_pitch,r_in,
                                  initial_angle=-np.pi/2-ArcAngle/2,
                                  final_angle=-np.pi/2+ArcAngle/2,
                                  layer=DrawingLayer)       
            cell.add(tooth)
            
    # TM gratings
    for ii in range(1,3):
        r_pitch = tap_l
        length_tooth = math.floor(pitch_TM*FillFactor/0.001)
        length_tooth = 0.001*length_tooth
        # tapered part
        tapered = gdstk.ellipse((-GC_separation/2+2*(ii-1)*GC_separation,0),r_pitch,
        initial_angle=-np.pi/2-ArcAngle/2,
        final_angle=-np.pi/2+ArcAngle/2,layer=DrawingLayer)      
        cell.add(tapered)

        # teeth part
        for n in range(1,NumOfCycle_TM):
            r_pitch = r_pitch+pitch_TM
            r_in = r_pitch-length_tooth;
            tooth = gdstk.ellipse((-GC_separation/2+2*(ii-1)*GC_separation,0),r_pitch,r_in,
                                  initial_angle=-np.pi/2-ArcAngle/2,
                                  final_angle=-np.pi/2+ArcAngle/2,
                                  layer=DrawingLayer)      
            cell.add(tooth)
            
    # WG---------------------------------------------------------------------------
    radius = GC_separation/4
    NumOfPts = math.ceil(radius*500/62.5)
    h = width/2/math.tan(ArcAngle/2);

    # left part
    P1set = [(-3*GC_separation/2,-h),(-3*GC_separation/2+radius,radius-h),(-GC_separation/2,-h),(-GC_separation/2-radius,radius-h),(-GC_separation,2*radius-h)]
    P2set = [(-3*GC_separation/2,radius-h),(-3*GC_separation/2+2*radius,radius-h),(-GC_separation/2,radius-h),(-2*GC_separation/2,radius-h),(-GC_separation,4*radius-h)]
    P3set = [(-3*GC_separation/2+radius,radius-h),(-3*GC_separation/2+2*radius,2*radius-h),(-GC_separation/2-radius,radius-h),(-2*GC_separation/2,2*radius-h),(-GC_separation/2,4*radius-h)]

    for ii in range(0,len(P1set)):
        # bezier
        P1 = P1set[ii]
        P2 = P2set[ii]
        P3 = P3set[ii]
        points_references = [P1,P2,P3]
        points_curve = [points_references[0]]
        for t in np.linspace(0,1, num=NumOfPts):
            x_temp = points_references[0][0]*((1-t)**2)+2*t*(1-t)*points_references[1][0]+points_references[2][0]*(t**2)
            y_temp = points_references[0][1]*((1-t)**2)+2*t*(1-t)*points_references[1][1]+points_references[2][1]*(t**2)
            points_curve.append((x_temp,y_temp))
        
        # path
        path_bezier = gdstk.FlexPath(points_curve, width,layer=DrawingLayer)
        cell.add(path_bezier)
    
    # right part
    P1set = [(3*GC_separation/2,-h),(3*GC_separation/2-radius,radius-h),(GC_separation/2,-h),(GC_separation/2+radius,radius-h),(GC_separation,2*radius-h)]
    P2set = [(3*GC_separation/2,radius-h),(3*GC_separation/2-2*radius,radius-h),(GC_separation/2,radius-h),(2*GC_separation/2,radius-h),(GC_separation,4*radius-h)]
    P3set = [(3*GC_separation/2-radius,radius-h),(3*GC_separation/2-2*radius,2*radius-h),(GC_separation/2+radius,radius-h),(2*GC_separation/2,2*radius-h),(GC_separation/2,4*radius-h)]

    for ii in range(0,len(P1set)):
        # bezier
        P1 = P1set[ii]
        P2 = P2set[ii]
        P3 = P3set[ii]
        points_references = [P1,P2,P3]
        points_curve = [points_references[0]]
        for t in np.linspace(0,1, num=NumOfPts):
            x_temp = points_references[0][0]*((1-t)**2)+2*t*(1-t)*points_references[1][0]+points_references[2][0]*(t**2)
            y_temp = points_references[0][1]*((1-t)**2)+2*t*(1-t)*points_references[1][1]+points_references[2][1]*(t**2)
            points_curve.append((x_temp,y_temp))
        
        # path
        path_bezier = gdstk.FlexPath(points_curve, width,layer=DrawingLayer)
        cell.add(path_bezier)       
    return cell
    



def DRT(width,radius_out,InteractionLength,WG_gap,cell_name,DrawingLayer=1):
    # WG gap: WG edge to WG edge
    # NumOfPts = math.ceil(radius_out*500/62.5)
    # RaceTrack Out------------------------------------------------------------------------------
    # lib = gdstk.Library()
    
    # RaceTrack Out------------------------------------------------------------------------------
    # lib = gdstk.Library()
    cell = lib.new_cell(cell_name)
    radius = radius_out
    NumOfPts = math.ceil(radius*500/62.5)
    
    # bezier
    points_references = [(radius,InteractionLength/2),(radius,InteractionLength/2+radius),(0,InteractionLength/2+radius)]
    points_curve = [points_references[0]]
    for t in np.linspace(0,1, num=NumOfPts):
        x_temp = points_references[0][0]*((1-t)**2)+2*t*(1-t)*points_references[1][0]+points_references[2][0]*(t**2)
        y_temp = points_references[0][1]*((1-t)**2)+2*t*(1-t)*points_references[1][1]+points_references[2][1]*(t**2)
        points_curve.append((x_temp,y_temp))
    
    # path
    path_bezier = gdstk.FlexPath(points_curve, width,layer=DrawingLayer)
    cell.add(path_bezier)
    
    #bezier
    points_references = [(-radius,InteractionLength/2),(-radius,InteractionLength/2+radius),(0,InteractionLength/2+radius)]
    points_curve = [points_references[0]]
    for t in np.linspace(0,1, num=NumOfPts):
        x_temp = points_references[0][0]*((1-t)**2)+2*t*(1-t)*points_references[1][0]+points_references[2][0]*(t**2)
        y_temp = points_references[0][1]*((1-t)**2)+2*t*(1-t)*points_references[1][1]+points_references[2][1]*(t**2)
        points_curve.append((x_temp,y_temp))
    
    # path
    path_bezier = gdstk.FlexPath(points_curve, width,layer=DrawingLayer)
    cell.add(path_bezier)
    
    # Interaction region
    path_line = gdstk.FlexPath([(-radius,InteractionLength/2),(-radius,-InteractionLength/2)], width,layer=1)
    cell.add(path_line)
    
    # bezier
    points_references = [(radius,-InteractionLength/2),(radius,-InteractionLength/2-radius),(0,-InteractionLength/2-radius)]
    points_curve = [points_references[0]]
    for t in np.linspace(0,1, num=NumOfPts):
        x_temp = points_references[0][0]*((1-t)**2)+2*t*(1-t)*points_references[1][0]+points_references[2][0]*(t**2)
        y_temp = points_references[0][1]*((1-t)**2)+2*t*(1-t)*points_references[1][1]+points_references[2][1]*(t**2)
        points_curve.append((x_temp,y_temp))
    
    # path
    path_bezier = gdstk.FlexPath(points_curve, width,layer=1)
    cell.add(path_bezier)
    
    #bezier
    points_references = [(-radius,-InteractionLength/2),(-radius,-InteractionLength/2-radius),(0,-InteractionLength/2-radius)]
    points_curve = [points_references[0]]
    for t in np.linspace(0,1, num=NumOfPts):
        x_temp = points_references[0][0]*((1-t)**2)+2*t*(1-t)*points_references[1][0]+points_references[2][0]*(t**2)
        y_temp = points_references[0][1]*((1-t)**2)+2*t*(1-t)*points_references[1][1]+points_references[2][1]*(t**2)
        points_curve.append((x_temp,y_temp))
    
    # path
    path_bezier = gdstk.FlexPath(points_curve, width,layer=1)
    cell.add(path_bezier)
    
    # Interaction region
    path_line = gdstk.FlexPath([(radius,-InteractionLength/2),(radius,InteractionLength/2)], width,layer=1)
    cell.add(path_line)
    
    # RaceTrack In------------------------------------------------------------------------------
    #lib = gdstk.Library()
    radius_in = radius_out-WG_gap-width
    radius = radius_in
    
    # bezier
    points_references = [(radius,InteractionLength/2),(radius,InteractionLength/2+radius),(0,InteractionLength/2+radius)]
    points_curve = [points_references[0]]
    for t in np.linspace(0,1, num=NumOfPts):
        x_temp = points_references[0][0]*((1-t)**2)+2*t*(1-t)*points_references[1][0]+points_references[2][0]*(t**2)
        y_temp = points_references[0][1]*((1-t)**2)+2*t*(1-t)*points_references[1][1]+points_references[2][1]*(t**2)
        points_curve.append((x_temp,y_temp))
    
    # path
    path_bezier = gdstk.FlexPath(points_curve, width,layer=DrawingLayer)
    cell.add(path_bezier)
    
    #bezier
    points_references = [(-radius,InteractionLength/2),(-radius,InteractionLength/2+radius),(0,InteractionLength/2+radius)]
    points_curve = [points_references[0]]
    for t in np.linspace(0,1, num=NumOfPts):
        x_temp = points_references[0][0]*((1-t)**2)+2*t*(1-t)*points_references[1][0]+points_references[2][0]*(t**2)
        y_temp = points_references[0][1]*((1-t)**2)+2*t*(1-t)*points_references[1][1]+points_references[2][1]*(t**2)
        points_curve.append((x_temp,y_temp))
    
    # path
    path_bezier = gdstk.FlexPath(points_curve, width,layer=DrawingLayer)
    cell.add(path_bezier)
    
    # Interaction region
    path_line = gdstk.FlexPath([(-radius,InteractionLength/2),(-radius,-InteractionLength/2)], width,layer=1)
    cell.add(path_line)
    
    # bezier
    points_references = [(radius,-InteractionLength/2),(radius,-InteractionLength/2-radius),(0,-InteractionLength/2-radius)]
    points_curve = [points_references[0]]
    for t in np.linspace(0,1, num=NumOfPts):
        x_temp = points_references[0][0]*((1-t)**2)+2*t*(1-t)*points_references[1][0]+points_references[2][0]*(t**2)
        y_temp = points_references[0][1]*((1-t)**2)+2*t*(1-t)*points_references[1][1]+points_references[2][1]*(t**2)
        points_curve.append((x_temp,y_temp))
    
    # path
    path_bezier = gdstk.FlexPath(points_curve, width,layer=1)
    cell.add(path_bezier)
    
    #bezier
    points_references = [(-radius,-InteractionLength/2),(-radius,-InteractionLength/2-radius),(0,-InteractionLength/2-radius)]
    points_curve = [points_references[0]]
    for t in np.linspace(0,1, num=NumOfPts):
        x_temp = points_references[0][0]*((1-t)**2)+2*t*(1-t)*points_references[1][0]+points_references[2][0]*(t**2)
        y_temp = points_references[0][1]*((1-t)**2)+2*t*(1-t)*points_references[1][1]+points_references[2][1]*(t**2)
        points_curve.append((x_temp,y_temp))
    
    # path
    path_bezier = gdstk.FlexPath(points_curve, width,layer=1)
    cell.add(path_bezier)
    
    # Interaction region
    path_line = gdstk.FlexPath([(radius,-InteractionLength/2),(radius,InteractionLength/2)], width,layer=1)
    cell.add(path_line)
    return cell