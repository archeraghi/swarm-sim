import random


def solution(world):
    minAgentHeight = 0
    maxAgentHeight = 0
    stopiftowerbuilt = False

    if world.get_actual_round() % 1 == 0:


        for agent in world.get_agent_list():
            # print(world.get_actual_round(), " Agent No.", agent.number, "  Coordinates", agent.coordinates, " Height", agent.coordinates[1], "  Number of Agents", world.get_amount_of_agents())

            if agent.coordinates[1] > maxAgentHeight:
                maxAgentHeight = agent.coordinates[1]
            if agent.coordinates[1] < minAgentHeight:
                minAgentHeight = agent.coordinates[1]

            # Check whether in the direction of SE, SW are agents or items
            # These directions are all relative to the current agent: First value is X coordinate (left right), second is the Y coordinate (up down), the third coordinate is for 3D coordinate systems but not used in 2D-Hex-Grid
            dirNE = (0.5,   1, 0)
            dirNW = (-0.5, 1, 0)
            dirSE = (0.5,  -1, 0)
            dirSW = (-0.5, -1, 0)
            dirW = (-1, 0, 0)
            dirE = (1, 0, 0)
            dirStand = (0,0,0)

            iteminE = agent.item_in(dirE)
            iteminW = agent.item_in(dirW)
            iteminSE = agent.item_in(dirSE)
            iteminSW = agent.item_in(dirSW)
            iteminNE = agent.item_in(dirNE)
            iteminNW = agent.item_in(dirNW)

            agentinE = agent.agent_in(dirE)
            agentinW = agent.agent_in(dirW)
            agentinSE = agent.agent_in(dirSE)
            agentinSW = agent.agent_in(dirSW)
            agentinNE = agent.agent_in(dirNE)
            agentinNW = agent.agent_in(dirNW)

            freeW = not agent.agent_in(dirW) and not agent.item_in(dirW)
            freeE = not agent.agent_in(dirE) and not agent.item_in(dirE)
            freeNW = not agent.agent_in(dirNW) and not agent.item_in(dirNW)
            freeNE = not agent.agent_in(dirNE) and not agent.item_in(dirNE)
            freeSW = not agent.agent_in(dirSW) and not agent.item_in(dirSW)
            freeSE = not agent.agent_in(dirSE) and not agent.item_in(dirSE)

            dirNotSetYet = (0,0,1)
            nextdirection = dirNotSetYet # characterizes an invalid state, will be changed later




            # CASE Begin: FALLING Start  - freeSW and freeSE -   Check whether Agent needs to fall
            if freeSW and freeSE:
                yposition = agent.coordinates[1]

                # We know already that this agent must fall, it will be in a zig (SE) - zag (SW) pattern, depending on the height (y - coordinate)
                if (yposition % 2) == 0:
                    nextdirection = dirSW
                else:
                    nextdirection = dirSE
            # CASE End: FALLING End  - freeSW and freeSE -   Check whether Agent needs to fall



            # CASE Begin: Agent is alone on the floor - Walk Left - Right -  iteminSE and iteminSW  - and nothing is above it
                # Walk to left of right if possible, otherwise stand
            if not agentinW and not agentinE:

                if nextdirection == dirNotSetYet and iteminSE and iteminSW :
                    # Move left or right
                    randdirection = random.choice((dirW, dirE))
                    nextdirection = dirStand

                    if randdirection == dirW and freeW and not agentinNE:
                        nextdirection = randdirection
                    if randdirection == dirE and freeE and not agentinNW:
                        nextdirection = randdirection

                if nextdirection == dirNotSetYet and agentinSE and iteminSW and not agentinNW:
                    # Move left or right
                    randdirection = random.choice((dirStand, dirE))
                    nextdirection = dirStand
                    if randdirection == dirE and freeE:
                        nextdirection = randdirection

                if nextdirection == dirNotSetYet and agentinSW and iteminSE and not agentinNE:
                    # Move left or right
                    randdirection = random.choice((dirStand, dirW))
                    nextdirection = dirStand
                    if randdirection == dirW and freeW:
                        nextdirection = randdirection

                if nextdirection == dirNotSetYet and freeSE and iteminSW and not agentinNE and freeW:
                    # Move left
                    nextdirection = dirW

                if nextdirection == dirNotSetYet and freeSW and iteminSE and not agentinNW and freeE:
                    # Move left
                    nextdirection = dirE
                # CASE End: Agent is on the floor - Walk Left -Right - iteminSE and iteminSW  - and nothing is above it





            # CASE Begin: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E
            if nextdirection == dirNotSetYet and agentinSW and agentinSE and freeE and agentinNE and not agentinNW :
                nextdirection = dirE    # freeE is True
            # CASE End: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E
            # Why not also case for W?
            if nextdirection == dirNotSetYet and agentinSW and agentinSE and freeW and agentinNW and not agentinNE:
                nextdirection = dirW
            # CASE End: Agent is on 2 agents - agentinSW and agentinSE - and carries an agent in NE, walk E


            if nextdirection == dirNotSetYet and freeNE and freeE and agentinSE and not agentinNW :
                nextdirection = dirE    # freeE is True



            # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and carrying nothing
                    # climb on agent in W if possible AND no other agent is on top of you
            if nextdirection == dirNotSetYet and (agentinW and freeNW) and ((not agentinNE) or (agentinNE and agentinE)):
                nextdirection = dirNW

                    # climb on agent in E if possible AND no other agent is on top of you
            if nextdirection == dirNotSetYet  and  (agentinE and freeNE) and ((not agentinNW) or (agentinNW and agentinW)):
                nextdirection = dirNE
            # CASE Begin: CLIMBING - Try climb NW, then try climb NE. Must be free, and


            # CASE Begin: TOWER SHIFT LEFT AND RIGHT
            # if standing only on agent in SE, check whether we need to move to E
            if nextdirection == dirNotSetYet and agentinSE and not agentinSW and freeE and not agentinNW :
                nextdirection = dirE

            if nextdirection == dirNotSetYet and agentinSW and not agentinSE and freeW and not agentinNE:
                yposition = agent.coordinates[1]
                nextdirection = dirW
            # CASE END: TOWER SHIFT LEFT AND RIGHT






            # CASE DEFAULT: If no direction selected, do not move
            if nextdirection == dirNotSetYet:
                nextdirection = dirStand


            # FINAL MOVE: if the agent is not falling currently, walk in the selected direction
            if nextdirection != dirNotSetYet:
                agent.move_to(nextdirection)

        # For next step: define the goal of the simulation, e.g. to build a tower of 6 agents and then terminate the simulation

        towerheight = maxAgentHeight - minAgentHeight + 1
        print("Round: ",world.get_actual_round(), "MaxHeight: ", maxAgentHeight , "Minheight: ", minAgentHeight , "Towerheight: ", towerheight ,"  Agent No.", agent.number, "  Coordinates", agent.coordinates, " Height", agent.coordinates[1],  "  Number of Agents", world.get_amount_of_agents())

        TowerHasBeenBuilt = (towerheight == world.get_amount_of_agents())
        if TowerHasBeenBuilt and stopiftowerbuilt:
            # world.csv_round.success()
            world.set_successful_end()