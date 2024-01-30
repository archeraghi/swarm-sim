import random
import math
from core.swarm_sim_header import *

DEBUG = True

# directions
move_east = (1, 0, 0)
move_southeast = (0.5, -1, 0)
move_southwest = (-0.5, -1, 0)
move_west = (-1, 0, 0)
move_northwest = (-0.5, 1, 0)
move_northeast = (0.5, 1, 0)

# Phases
phase_startCounting = 1
phase_backtracking = 2
phase_countingFinished = 3
phase_countupObjects = 4
phase_waitforsubjects1 = 5
phase_startObject = 6
phase_PickupObject = 7
phase_PlaceObject = 8
phase_checkifready = 9
phase_waitforsubjects2 = 10
phase_end = 11

# NONE TYPE BEI NEXT TARGET!!!! NOCHMAL ÜBERPRÜFEN!!!
# WENN MAN PARTIKEL ENTFERNT UND WIEDER HINZUFÜGT GIBT ES KEINEN LEADER MEHR!!!
def solution(world):
    global numberoftiles
    for particle in world.get_agent_list():

        # First round
        if world.get_actual_round() == 1:
            setattr(particle, "phase", 0)
            setattr(particle, "numberoftiles", 0)
            setattr(particle, "nextTarget", (0, 0, 0))
            setattr(particle, "nextTile", (0, 0, 0))
            setattr(particle, "keeptarget", False)
            setattr(particle, "countedTiles", [])

            particle.phase = phase_startCounting
           # particle.create_location()
            particle.write_to_with(world.get_item_map_coordinates()[particle.coordinates], "tile", "counted")
            particle.countedTiles.append(particle.coordinates)

        if DEBUG:
            print("Round %i, Phase %i, Particle %i, number of tiles %i" % (
            world.get_actual_round(), particle.phase, particle.number, len(particle.countedTiles)))

        if particle.phase == phase_startCounting:
            startCounting(world, particle)

        elif particle.phase == phase_backtracking:
            backtracking(world, particle)

        elif particle.phase == phase_countingFinished:
            # each particle tells the leader its number of tiles counted
            particle.write_to_with(world.get_agent_list()[0], particle.number, len(particle.countedTiles))
            particle.phase = phase_waitforsubjects1

        elif particle.phase == phase_waitforsubjects1:
            waitingforagents(world, phase_waitforsubjects1, phase_countupObjects)

        elif particle.phase == phase_countupObjects:
            countupObjects(world, particle)

        elif particle.phase == phase_waitforsubjects2:
            waitingforagents(world, phase_waitforsubjects2, phase_startObject)

        elif particle.phase == phase_startObject:
            startObject(world, particle)

        elif particle.phase == phase_PickupObject:
            PickupObject(world, particle)

        elif particle.phase == phase_PlaceObject:
            PlaceObject(world, particle)

        elif particle.phase == phase_checkifready:
            checkifready(world, particle)

        elif particle.phase == phase_end:
            end(world, particle)

        else:
            if DEBUG:
                print("Unknown Phase: %i" % (particle.phase))

############################# methods of phases ###############################################################

def startCounting(world, particle):
    # count until there are no uncounted tiles in the immediate vicinity
    possible_directions = possibleDirections(world, particle)

    if not possible_directions:
        particle.phase = phase_backtracking
    else:
        particle.move_to(random.choice(possible_directions))
        #particle.create_location()
        particle.write_to_with(world.get_item_map_coordinates()[particle.coordinates], "tile", "counted")
        particle.countedTiles.append(particle.coordinates)

def backtracking(world, particle):
    # go back the walked way and look for uncounted tiles
    walkedPath = particle.get_walkedPath()

    if not walkedPath:
        particle.phase = phase_startCounting
        possible_directions = possibleDirections(world, particle)

        if not possible_directions:
            particle.phase = phase_countingFinished

    else:
        wayback = particle.get_wayback(walkedPath)
        particle.move_to(wayback[0])
        walkedPath.pop()
        walkedPath.pop()
        particle.set_walkedPath(walkedPath)
        particle.phase = phase_startCounting

def countupObjects(world, particle):
    if particle.number == 1:
        # Leader adds up all tiles
        particle.numberoftiles = countuptiles(world, particle)
        print("counted number of tiles: ", particle.numberoftiles)
        if world.check_count(particle.numberoftiles):
            print("Count successful")
        else:
            print("Count unsuccessful")

        # Leader calculates the coordinates of the tiles for the object
        object = objectcoordinates(particle)
        i = 0
        j = 10000
        while i < particle.numberoftiles:
            particle.write_to_with(world.get_agent_list()[0], j, object[i])
            i = i + 1
            j = j + 1
        particle.write_to_with(world.get_agent_list()[0], j, "end")

    # each particle communicates the coordinates of the counted tiles to the leader
    for coordinate in particle.countedTiles:
        i = 1000
        while particle.read_from_with(world.get_agent_list()[0], i) is not None:
            i = i + 1
        particle.write_to_with(world.get_agent_list()[0], i, coordinate)

    particle.phase = phase_waitforsubjects2

def startObject(world, particle):
    # particle has target ==> particle needs next tile coordinate
    if particle.keeptarget == True:
        particle.keeptarget = False
        i = 1000
        while particle.read_from_with(world.get_agent_list()[0], i) == "deleted":
            i = i + 1
        particle.nextTile = particle.read_from_with(world.get_agent_list()[0], i)
        if particle.nextTile is None:
            particle.phase = phase_checkifready
        else:
            particle.write_to_with(world.get_agent_list()[0], i, "deleted")
            particle.phase = phase_PickupObject

    # particle has no target ==> particle needs tile and target coordinates
    else:
        j = 10000
        while particle.read_from_with(world.get_agent_list()[0], j) == "occupied":
            j = j + 1
        if particle.read_from_with(world.get_agent_list()[0], j) == "end":
            particle.phase = phase_checkifready
        else:
            particle.nextTarget = particle.read_from_with(world.get_agent_list()[0], j)
            particle.write_to_with(world.get_agent_list()[0], j, "occupied")
            if not particle.carries_item():
                i = 1000
                while particle.read_from_with(world.get_agent_list()[0], i) == "deleted":
                    i = i + 1
                particle.nextTile = particle.read_from_with(world.get_agent_list()[0], i)
                particle.write_to_with(world.get_agent_list()[0], i, "deleted")

            particle.phase = phase_PickupObject

def PickupObject(world, particle):
    currentPosition = particle.coordinates
    # check if particle carries item
    if not particle.carries_item():
        # check if the next tile coordinate is none
        if particle.nextTile is None:
            particle.phase = phase_startObject
            particle.keeptarget = True

        # check if particle is already on the position of the next tile
        elif currentPosition == particle.nextTile:
            if particle.is_on_item():
                if particle.read_from_with(world.get_item_map_coordinates()[particle.coordinates], "tile") == "counted":
                    # take tile and write in the memory of the tile
                    particle.write_to_with(world.get_item_map_coordinates()[particle.coordinates], "tile", "postponed")
                    particle.take_item()
                    particle.phase = phase_PlaceObject

                else:
                    # tile must not be moved, target coordinates are kept
                    particle.keeptarget = True
                    particle.phase = phase_startObject

            else:
                # if there is no tile
                particle.phase = phase_startObject

        else:
            # if particle is not on the right coordinates then move to the right coordinates
            movetocoordinate(particle, currentPosition, particle.nextTile)

    else:
        particle.phase = phase_PlaceObject

def PlaceObject(world, particle):
    currentPosition = particle.coordinates
    # check if the next target coordinate is none
    if particle.nextTarget is None:
        particle.phase = phase_startObject

    # check if particle is already on the position of the next coordinate
    elif currentPosition == particle.nextTarget:
        if particle.is_on_item():
            # if there is already a tile then write in the memory of this tile
            if particle.read_from_with(world.get_item_map_coordinates()[particle.coordinates], "tile") == "counted":
                particle.write_to_with(world.get_item_map_coordinates()[particle.coordinates], "tile", "postponed")

        else:
            # if on the position is no tile then drop the tile
            particle.drop_item()

        particle.phase = phase_startObject

    else:
        # if particle is not on the right coordinates then move to the right coordinates
        movetocoordinate(particle, currentPosition, particle.nextTarget)

def checkifready(world, particle):
    # if particle still has a tile then drop it and tell the leader
    if particle.carries_item():
        if not particle.is_on_item():
            particle.drop_item()
            i = 1000
            while not particle.read_from_with(world.get_agent_list()[0], i) == "deleted":
                i = i + 1
            particle.write_to_with(world.get_agent_list()[0], i, particle.coordinates)
            particle.write_to_with(world.get_item_map_coordinates()[particle.coordinates], "tile", "counted")
    else:
        particle.phase = phase_end

    particle.move_to(move_northwest)


def end(world, particle):
    particle.move_to(move_northwest)
    # wait for all particles
    check = True
    for particle in world.agents:

        if particle.phase != phase_end:
            check = False
    if check == True:
        # check if the formation is correct
        if world.check_formation():
            print("Formation Construction successful")
        else:
            print("Formation Construction unsuccessful")
        # terminate
        world.set_successful_end()
        particle.phase = phase_checkifready

        if DEBUG:
            print("*** Finish ***")

    return 0

################################### other methods ##########################################################

def possibleDirections(world, particle):
    # look for possible directions to move
    directions = [move_east, move_southwest, move_southeast, move_west, move_northeast, move_northwest]
    possible_directions = []
    for direction in directions:
        if not particle.agent_in(direction) and particle.item_in(direction) and not particle.read_from_with(
                world.get_item_map_coordinates()[get_coordinates_in_direction(particle.coordinates, direction)],
                "tile") == "counted":
            possible_directions.append(direction)

    return possible_directions


def waitingforagents(world, waitphase, continuationphase):
    # wait for all particles until they all are in this phases
    check = True
    for particle in world.agents:

        if particle.phase != waitphase:
            check = False

    if check == True:
        for particle in world.agents:
            particle.phase = continuationphase


def objectcoordinates(particle):
    # see which tile formation should be formed and calculate its coordinates
    s_rhombus = math.sqrt(particle.numberoftiles)
    s_triangle = -0.5 + math.sqrt(0.25 + 2 * particle.numberoftiles)
    s_hexagon = 0.5 + math.sqrt(0.25 - ((1 - particle.numberoftiles) / 3))

    object = []

    if s_triangle.is_integer():
        # triangle coordinates:
        x = 0
        y = 0
        z = 0
        s_triangle2 = s_triangle
        while y < s_triangle:
            while x < s_triangle2 + z:
                object.append((x, y, 0))
                x = x + 1

            y = y + 1
            z = z + 0.5
            x = z
            s_triangle2 = s_triangle2 - 1

    elif s_rhombus.is_integer():
        # rhombus coordinates:
        x = 0
        y = 0
        z = 0
        while y < s_rhombus:
            while x < s_rhombus + z:
                object.append((x, y, 0))
                x = x + 1

            y = y + 1
            z = z + 0.5
            x = z

    elif s_hexagon.is_integer():
        # hexagon coordinates:
        x = 0.5
        y = 1
        i = 1
        phase = 1

        object.append((0, 0, 0))

        while i < s_hexagon:
            j = 1
            while j <= i:
                if not phase == 7:
                    object.append((x, y, 0))
                if phase == 1:
                    x = x + 0.5
                    y = y - 1
                elif phase == 2:
                    x = x - 0.5
                    y = y - 1
                elif phase == 3:
                    x = x - 1
                elif phase == 4:
                    x = x - 0.5
                    y = y + 1
                elif phase == 5:
                    x = x + 0.5
                    y = y + 1
                elif phase == 6:
                    x = x + 1
                else:
                    i = i + 1
                    j = i
                    x = x + 0.5
                    y = y + 1
                    phase = 0
                j = j + 1
            phase = phase + 1

    else:
        # line coordinates:
        x = 0
        y = 0
        z = 0

        while z < particle.numberoftiles:
            object.append((x, y, 0))
            x = x + 0.5
            y = y + 1
            z = z + 1

    return object


def countuptiles(world, particle):
    numberofparticles = world.get_amount_of_agents()
    i = 1
    while i <= numberofparticles:
        zahl = particle.read_from_with(world.get_agent_list()[0], i)
        if zahl is not None:
            particle.numberoftiles = particle.numberoftiles + zahl
        else:
            numberofparticles = numberofparticles + 1
        i = i + 1

    return particle.numberoftiles


def movetocoordinate(particle, currentPosition, coordinate):
    # move to the correct coordinates
    directions = [move_northeast, move_east, move_southeast, move_northwest, move_west, move_southwest]
    if currentPosition[0] <= coordinate[0] and currentPosition[1] < coordinate[1]:
        if particle.agent_in(move_northeast):
            particle.move_to(random.choice(directions))

        else:
            particle.move_to(move_northeast)

    elif currentPosition[0] >= coordinate[0] and currentPosition[1] < coordinate[1]:
        if particle.agent_in(move_northwest):
            particle.move_to(random.choice(directions))

        else:
            particle.move_to(move_northwest)

    elif currentPosition[0] <= coordinate[0] and currentPosition[1] > coordinate[1]:
        if particle.agent_in(move_southeast):
            particle.move_to(random.choice(directions))

        else:
            particle.move_to(move_southeast)

    elif currentPosition[0] >= coordinate[0] and currentPosition[1] > coordinate[1]:
        if particle.agent_in(move_southwest):
            particle.move_to(random.choice(directions))

        else:
            particle.move_to(move_southwest)

    elif currentPosition[0] > coordinate[0]:
        if particle.agent_in(move_west):
            particle.move_to(random.choice(directions))

        else:
            particle.move_to(move_west)

    elif currentPosition[0] < coordinate[0]:
        if particle.agent_in(move_east):
            particle.move_to(random.choice(directions))

        else:
            particle.move_to(move_east)
