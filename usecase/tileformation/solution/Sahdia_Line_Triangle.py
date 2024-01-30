import random

import time

DEBUG = True

# Line phases
phase_move_west = 4
phase_move_east = 1
phase_drop = 13
phase_back = 14
phase_move_southwest = 15
phase_back1 = 18
phase_back2 = 19

# Triangle Phases
phase_pick_tile_for_triangle = 0
phase_move_east_for_triangle = 5
phase_go_place_triangle_zig_1 = 6
phase_go_place_triangle_zig_2 = 7
phase_go_place_triangle_zag_1 = 8
phase_go_place_triangle_zag_2 = 9
phase_place_triangle_tile = 10
phase_leave_triangle = 11
phase_onestep = 20
phase_nop = 0x90

# Directions:
move_east = 1
move_southeast = 2
move_southwest = 3
move_west = 4
move_northwest = 5
move_northeast = 0

#onestep= False

def solution(sim):
    #first task to create a line.
    global take, line, line1, onestep
    for particle in sim.get_particle_list():

        # checks if it is the first round
        if sim.get_actual_round() == 1:

            particle.startTime = time.time()
            particle.lineTime = time.time()

            setattr(particle, "phase", 0)
            setattr(particle, "line", False)
            setattr(particle, "line1", False)
            setattr(particle, "take", False)
            setattr(particle, "moved", False)
            setattr(particle, "move1", False)
            setattr(particle, "move2", False)
            setattr(particle, "drop", False)
            setattr(particle, "moveeast", False)




            if particle.number == 1:

                # first particle starts
                particle.phase = phase_move_west
            elif particle.number == 2:

                # second particle starts
                particle.phase = phase_move_west
            elif particle.number == 3:
                particle.phase = phase_move_west

        if DEBUG:
            print("Round %i, Phase %i, Particle %i" % (sim.get_actual_round(), particle.phase, particle.number))

        # now the phases begin

        if particle.phase == phase_move_west:
            # Starting phase : particle goes in direction southwest, as far as possible
            particle.moved = False

            for possible_position in [move_southwest]:
                if particle.tile_in(dir=possible_position):
                    # if it is possible to move in direction southwest then move to southwest
                        particle.move_to(dir=possible_position)
                        particle.moved = True
                        break

            if not particle.moved:
                # particle has reached the most southwest tile and it cannot move any further in direction southwest
                # next phase
                particle.phase = phase_move_east
                particle.line = True
                particle.take = True
            else:
                continue

        elif particle.phase == phase_move_east:
            # particle moves to the far left.
            if particle.take:

                if particle.tile_in(dir=move_east) or particle.tile_in(
                        dir=move_southeast) or particle.tile_in(
                        dir=move_northwest) or particle.tile_in(dir=move_west):
                    particle.line = False
                particle.take = False
                for possible_position in [move_northwest, move_west, move_northeast]:
                    if particle.tile_in(dir=possible_position):
                        particle.move_to(dir=possible_position)
                        particle.take = True

                        break
            elif not particle.take:
                if DEBUG:
                    print("Tile taken")
                if not particle.line:
                    # when the particle reaches the far left position, it takes the tile from that current position
                    particle.take_tile()
                    if particle.tile_in(dir=move_southeast):
                        # particle moves in direction southeast with the tile
                           particle.move_to(dir=move_southeast)

                    elif particle.tile_in(dir=move_east):
                        # if there is no tile present in southeast direction, particle moves in direction east with the tile
                           particle.move_to(dir=move_east)
                    particle.phase = phase_move_southwest
                    # next phase

                if particle.line:

                    if particle.tile_in(dir=move_southwest):
                        # particle moves to the last tile in the southwest direction, so that it can place the tile at the end of this line.
                        # At the same time, it also checks if there is already a line built or not.
                        particle.move_to(dir=move_southwest)
                        if particle.tile_in(dir=move_east) or particle.tile_in(
                                dir=move_southeast) or particle.tile_in(
                                dir=move_northwest) or particle.tile_in(dir=move_west):
                            particle.line = False
                            particle.take = False

                            particle.line1 = True


        elif particle.phase == phase_move_southwest:
            particle.drop = False
            for possible_position in [move_southwest]:
                if particle.tile_in(dir=possible_position):
                      particle.move_to(dir=possible_position)
                      particle.drop = True

                      break

            if not particle.drop:
                particle.phase = phase_drop
            else:
                continue
        elif particle.phase == phase_drop:
            # particle has reached the last tile in the southwest direction, now it can move one step further in southwest direction, inorder to place the tile it is carrying
                particle.move_to(dir=move_southwest)
                print("Tile Dropped")
                particle.drop_tile()
            # particle drops the tile

                particle.line = False
                particle.take = True

                particle.phase = phase_back1
             # now the back phases begin, where the partciel goes back to the starting after checking if there is already a line built or not
            # phase_back, phase_back1 and phase_back2 are three phases where the particle goes back to the starting of the programm, after checking if there is already a line built or not.
           # if a line is already built, the particle changes to the first phase of traingle, that is phase_pick_tile_for_triangle
        elif particle.phase == phase_back:
                particle.move_to(dir=move_northeast)
                particle.phase = phase_move_east


        elif particle.phase == phase_back1:

            particle.move1 = False

            for possible_position in [move_northeast]:
                if particle.tile_in(dir=move_east) or particle.tile_in(
                        dir=move_southeast) or particle.tile_in(
                        dir=move_northwest) or particle.tile_in(dir=move_west):
                    particle.line1 = False
                    particle.phase = phase_back2
                else:
                    particle.line1 = True
                if particle.tile_in(dir=possible_position):
                        particle.move_to(dir=possible_position)
                        particle.move1 = True

                        break
            if not particle.move1:

                particle.phase = phase_back2


            else:
                continue

        elif particle.phase == phase_back2:
            particle.move2 = False
            for possible_position in [move_southwest]:

                if particle.tile_in(dir=possible_position):
                        particle.move_to(dir=possible_position)
                        particle.move2 = True
                        break
                if not particle.move2:

                    if not particle.line1:
                        particle.phase = phase_back
                    else:

                        if particle.number == 1:
                         particle.phase = phase_pick_tile_for_triangle
                         # one of the partciles starts with making a traingle
                         particle.lineTime = time.time()
                         print("Seconds needed to make Line: " + str(particle.lineTime - particle.startTime))
                        else:
                            particle.phase = phase_onestep
                            # the other partcile waits for some time, before it starts to make a traingle

                        particle.lineTime = time.time()
                        print("Seconds needed to make Line: " + str(particle.lineTime - particle.startTime))

                else:
                    continue

        elif particle.phase == phase_onestep:
            if particle.tile_in(dir=move_northeast):
                particle.move_to(move_northeast)
                particle.phase = phase_onestep
            else:
                particle.phase = phase_pick_tile_for_triangle



        elif particle.phase == phase_pick_tile_for_triangle:

            # after building a line, we need to build a triangle

            # second part of the solution : building a triangle

            if particle.tile_in(dir=move_southwest):

                 particle.move_to(dir=move_southwest)

            else:

                    if not particle.get_particle_in(dir=move_southwest):
                        # a tile is only then taken when both partciels have a distance of atleast two hops from each other
                        # this way the line will not be broken
                        particle.take_tile()

                        particle.phase = phase_move_east_for_triangle
                    else:
                        particle.phase=phase_onestep



        elif particle.phase == phase_move_east_for_triangle:
            # after picking up a tile, the particle moves to the northeast end of the line in order to place the tile


            if particle.tile_in(dir=move_northeast):

                particle.move_to(dir=move_northeast)



            else:

                # particle has reached the northeast end of the line


                if not particle.tile_in(dir=move_east):

                    # the first location in east direction is not reserved, so place the tile

                    particle.move_to(dir=move_east)

                    particle.drop_tile()

                    particle.phase = phase_leave_triangle

                else:

                    particle.move_to(dir=move_east)
                    # if the first location in the east direction is already taken by another tile, particle changes to phase_go_place_triangle_zig_1
                    # from now onwards, tiles are placed in a zig zag manner
                    particle.phase = phase_go_place_triangle_zig_1




        elif particle.phase == phase_go_place_triangle_zig_1:

            if particle.tile_in(dir=move_east):

                particle.move_to(dir=move_east)

                particle.phase = phase_go_place_triangle_zig_2

            else:

                particle.phase = phase_place_triangle_tile



        elif particle.phase == phase_go_place_triangle_zig_2:

            if particle.tile_in(dir=move_southwest):

                particle.move_to(dir=move_southwest)

            else:

                particle.phase = phase_go_place_triangle_zag_1



        elif particle.phase == phase_go_place_triangle_zag_1:

            if particle.tile_in(dir=move_southeast):

                particle.move_to(dir=move_southeast)

                particle.phase = phase_go_place_triangle_zag_2

            else:

                particle.phase = phase_place_triangle_tile




        elif particle.phase == phase_go_place_triangle_zag_2:

            if particle.tile_in(dir=move_northeast):

                particle.move_to(dir=move_northeast)

            else:

                particle.phase = phase_go_place_triangle_zig_1




        elif particle.phase == phase_place_triangle_tile:

            if not particle.tile_in(dir=move_west) and not particle.tile_in(dir=move_northwest):

                particle.move_to(dir=move_east)

            elif particle.tile_in(dir=move_northwest) and not particle.tile_in(dir=move_northeast):

                particle.move_to(dir=move_northeast)

            elif particle.tile_in(dir=move_west) and not particle.tile_in(dir=move_southwest):

                particle.move_to(dir=move_southwest)

            elif particle.tile_in(dir=move_southwest):

                particle.move_to(dir=move_east)

            elif particle.tile_in(dir=move_northeast):

                particle.move_to(dir=move_southeast)

            particle.drop_tile()

            particle.phase = phase_leave_triangle




        elif particle.phase == phase_leave_triangle:

            if particle.tile_in(dir=move_west):

                particle.move_to(dir=move_west)

            elif particle.tile_in(dir=move_northwest):

                particle.move_to(dir=move_northwest)

            elif not particle.tile_in(dir=move_northwest) and not particle.tile_in(
                    dir=move_west) and particle.tile_in(dir=move_southwest) or particle.tile_in(
                    dir=move_northeast):

                particle.phase = phase_pick_tile_for_triangle

            else:

                # finished. we have a triangle.

                particle.phase = phase_nop

                # time needed to make the triangle

                print("Seconds needed to build a triangle from Start: " + str(time.time() - particle.startTime))

                print("Sekunden bis zum triangle ab Linie: " + str(time.time() - particle.lineTime))

            # i = sim.sim.get_actual_round() #anzahl der runde(int)

        elif particle.phase == phase_nop:
            print("Seconds needed to build a triangle from Start: " + str(time.time() - particle.startTime))
            print("Sekunden bis zum triangle ab Linie: " + str(time.time() - particle.lineTime))
            check=True
            for particle in sim.particles:

                if particle.phase!= phase_nop :
                    check=False
            if check==True:
             sim.set_end()

                #only when both partciles have ended the trinagle making, the program ends

            if DEBUG:
                print("*** Finish ***")

            continue

        else:

            if DEBUG:
                print("Unknown Phase: %i" % (particle.phase))

        particle.touch()