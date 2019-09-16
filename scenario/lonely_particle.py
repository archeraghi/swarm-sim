import scenario.std_lib as std
import lib.header as header
def scenario(world):
    world.add_particle(0,0)
    std.add_tiles_as_hexagon(world, 10, color=header.dark_green)
