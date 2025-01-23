import gdstk
import math
import numpy as np
import gdstk
import numpy as np

def pp_ring(
    center, inner_radius, outer_radius, pole_width, pole_spacing, num_poles, layer=0, rring_dist=2.0
):
    """
    Create a periodically poled ring electrode

    Parameters:
        center (tuple): Center of the ring (x, y).
        inner_radius (float): Inner radius of the ring.
        outer_radius (float): Outer radius of the ring.
        pole_width (float): Width of the poling regions.
        pole_spacing (float): Spacing between poling regions.
        num_poles (int): Number of poles to create.
        layer (int): Layer for the GDSII elements.
        rring_dist : distance between inner radius and electrode

    Returns:
        gdstk.Cell: A cell containing the periodically poled ring structure.
    """
    # Create a new cell
    cell = gdstk.Cell("Periodically_Poled_Ring")

    # Create the ring shape
    ring = gdstk.ellipse(
        center=center, inner_radius=inner_radius+rring_dist, radius=outer_radius, layer=layer
    )
    cell.add(ring)

    # Add periodic poles to the ring
    for i in range(num_poles):
        angle_start = 2 * np.pi * i / num_poles
        angle_end = angle_start + pole_width / inner_radius

        # Create each pole as a radial sector
        pole = gdstk.ellipse(
            center=center,
            inner_radius=inner_radius,
            radius=outer_radius,
            initial_angle=angle_start,
            final_angle=angle_end,
            layer=layer + 1,  # Use a different layer for poles
        )
        cell.add(pole)

    return cell

def main():
    # Define parameters
    center = (0, 0)
    inner_radius = 190
    outer_radius = 200
    rring_dist = 5 # Must be less than outer_radius - inner_radius

    pole_width = 1
    pole_spacing = 1
    num_poles = 100

    cell = pp_ring(
        center, inner_radius, outer_radius, pole_width, pole_spacing, num_poles, rring_dist=rring_dist
    )

    # Create a library and save the GDSII file
    lib = gdstk.Library("Poled_Ring")
    lib.add(cell)
    lib.write_gds("./pcells/pp_ring.gds")
    print("GDS file 'pp_ring.gds' created successfully.")

if __name__ == "__main__":
    main()
