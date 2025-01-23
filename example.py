# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 00:16:31 2024

@author: Seho
"""
import sys
# sys.path.append(r"C:\Users\Seho\Box\LAB09_PythonFiles")

import gdstk
import numpy
import GenGDSTKParts as Gen
import numpy as np

lib = gdstk.Library()

# Edge coupler
# for width in [2,2.5,3,3.5,4,4.5,5]:
#     diameter = 200
#     cell_name = "EdgeCoupler_width_" + str(width)
#     pointsets = [(0,diameter/2),(-diameter/2,diameter/2),(-diameter,diameter/2),(-diameter,0)]
#     cellEC = Gen.Bezier(pointsets,width,cell_name,1);
#     lib.add(cellEC)

# for diameter in [40, 400]:
#     width = 3
#     cell_name = "EdgeCoupler_dia_" + str(diameter)
#     pointsets = [(0,diameter/2),(-diameter/2,diameter/2),(-diameter,diameter/2),(-diameter,0)]
#     cellEC = Gen.Bezier(pointsets,width,cell_name,1);
#     lib.add(cellEC)

# Chip
width = 13500
length = 12000
cell_name = "grating_coupler"
corner1 = (-width/2,-length/2)
corner2 = (width/2,length/2)
# cellEC = Gen.rectangle(corner1,corner2,cell_name,2)
cellEC = Gen.GC2(2.5,  FillFactor=0.4, cell_name="grating_coupler")
# cellEC = Gen.GC4(10)

lib.add(cellEC)
lib.write_gds("pcells/hn_gc.gds")