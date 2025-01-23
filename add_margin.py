import numpy
import gdstk
import sys

# Usage
# Creates a gds file with the original pcell and the new pcell with a margin added

if __name__ == '__main__':
  
  # User define
  input_file = 'pcells/6ring_HN_Jason.gds'
  output_file = 'dev_out.gds'
  margin = 4 
  layer_of_margin = 4
  # Put the names of cells from your input file that you want to add a margin to in a list 
  # cell_names = ["device_ring_electrode", "device_ring_racetrack", "grating_coupler"]
  cell_names = ["device_tot"]

  lib = gdstk.Library()  
  library =  gdstk.read_gds(input_file)
  for cell_name in cell_names:
    temp_cell = lib.new_cell(f'{cell_name}_margin')
    old_cell = library[cell_name]

    polygons = old_cell.get_polygons()
  
    for polygon in polygons:
      expanded_polygon = gdstk.offset(polygon, distance=margin)
      result = gdstk.boolean(polygon, expanded_polygon, 'xor', layer=layer_of_margin)
      temp_cell.add(polygon)
      temp_cell.add(result[0])
      
  
  lib.write_gds(output_file)
