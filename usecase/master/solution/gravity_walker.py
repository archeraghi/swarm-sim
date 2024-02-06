import random


def solution(world):

    if world.get_actual_round() % 1 == 0:
        for agent in world.get_agent_list():

            # Check whether in the direction of SE, SW are agents or items
            dirNE = (0.5,   1, 0)
            dirNW = (-0.5, 1, 0)
            dirSE = (0.5,  -1, 0)
            dirSW = (-0.5, -1, 0)
            dirW = (-1,    0, 0)
            dirE = (-1, 0, 0)
            checkiteminSE = agent.item_in(dirSE)
            checkiteminSW = agent.item_in(dirSW)
            checkagentinSE = agent.agent_in(dirSE)
            checkagentinSW = agent.agent_in(dirSW)

            AgentAllowedMovementAsNotFalling = True
            if not (checkiteminSE or checkiteminSW or checkagentinSE or checkagentinSW):
                yposition = agent.coordinates[1]
                print("Agent must fall,  agent ", agent.coordinates, "   yposition: ", yposition )
                AgentAllowedMovementAsNotFalling = False
                if (yposition % 2) == 0:
                    print("{0} is Even".format(yposition))
                    agent.move_to(dirSW)
                else:
                    print("{0} is Odd".format(yposition))
                    agent.move_to(dirSE)



            # Select next direction to potentially walk to
            nextdirection = random.choice(world.grid.get_directions_list()) # can be NW, NE, w, E, SW, SE

            # Check whether selected direction is colliding with an item,
            # if yes: reroll the direction
            #while agent.item_in(nextdirection):
            canWalkUp = False

            # Conditions When We Need To Reroll the Direction

            while True:
                RerollCondition = False
                if agent.item_in(nextdirection): # Reroll as we walk into a wall
                    RerollCondition = True

                if canWalkUp == False and nextdirection == dirNW and not agent.item_in(dirW) and not agent.agent_in(dirW) : # Reroll as we walk NW upwards, without having an agent or item to climb on
                    RerollCondition = True

                if canWalkUp == False and nextdirection == dirNE and not agent.item_in(dirE) and not agent.agent_in(dirE) : # Reroll as we walk NE upwards, without having an agent or item to climb on
                    RerollCondition = True

                if RerollCondition == False : # Next direction is fine, go ahead
                    break

                nextdirection = random.choice(world.grid.get_directions_list())   # reroll next direction



            #print(world.get_actual_round(), " Agent No.", agent.number, "   Current Coord:", agent.get_location(), "   Aimed Direction:", nextdirection, "   is item: ", agent.item_in(nextdirection))

            # if the agent is not falling currently, walk in the selected direction
            if AgentAllowedMovementAsNotFalling:
                agent.move_to(nextdirection)

        # For next step: define the goal of the simulation, e.g. to build a tower of 6 agents and then terminate the simulation
        TowerOfSixAgentsHasBeenBuilt = False
        if TowerOfSixAgentsHasBeenBuilt:
            sim.success_termination()
'''
weCanClimbOnWestNeighbor = False
            if agent.agent_in(dirW) and nextdirection == dirNW and not agent.agent_in(dirNW) and not agent.item_in(dirNW):
                weCanClimbOnWestNeighbor = True

            weCanClimbOnEastNeighbor = False
            if agent.agent_in(dirE) and nextdirection == dirNE and not agent.agent_in(dirNE) and not agent.item_in(
                    dirNE):
                weCanClimbOnEastNeighbor = True

        ValidDirectionsSelected = False
        if weCanClimbOnWestNeighbor and AgentAllowedMovementAsNotFalling:
            ValidDirectionsSelected = True
        if weCanClimbOnEastNeighbor and AgentAllowedMovementAsNotFalling:
            ValidDirectionsSelected = True
        if (nextdirection == dirNW or nextdirection == dirNE) and canWalkUp == True:
            ValidDirectionsSelected = True

        while agent.item_in(nextdirection) and not ValidDirectionsSelected:
                nextdirection = random.choice(world.grid.get_directions_list())
'''