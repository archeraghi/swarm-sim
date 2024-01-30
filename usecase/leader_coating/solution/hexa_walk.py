def solution(world):
    for particle in world.get_particle_list():
        global ttl
        global max
        global direction

        dirs = world.grid.get_directions_list()

        if world.get_actual_round() == 1:
            max = 0
            ttl = 0
            direction = dirs[5]
            layer = 1
        if ttl == 6*layer and direction == dirs[0] :
            layer+=1


        if ttl == 0:
            print("Round ", world.get_actual_round())
            ttl = max
            if direction == dirs[0]:
                direction = dirs[1]
            elif direction == dirs[1]:
                direction = dirs[2]
            elif direction == dirs[2]:
                direction = dirs[3]
            elif direction == dirs[3]:
                direction = dirs[4]
            elif direction == dirs[4]:
                direction = dirs[5]
            elif direction == dirs[5]:
                direction = dirs[0]

        particle.create_location()
        particle.move_to(direction)
        ttl = ttl - 1
