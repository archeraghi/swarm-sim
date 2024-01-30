def scenario(sim):
    starting_point=(0,0)
    #sim.add_particle(0.5,1)
    square_size = sim.config_data.sq_size
    end_point_on_x = () #stores the last point on the first x line
    end_point_on_y = () #stores the last point on the first y line

    # if square_size == 2:
    #     sim.add_particle(1.0, 2.0)
    # if square_size == 3:
    #     sim.add_particle(1.5, 3.0)
    # if square_size == 4:
    #     sim.add_particle(2.0, 4.0)
    # if square_size == 5:
    #     sim.add_particle(2.5, 5.0)
    # if square_size == 6:
    #     sim.add_particle(3.0, 6.0)
    # if square_size == 7:
    #     sim.add_particle(3.5, 7.0)
    # if square_size == 8:
    #     sim.add_particle(4, 8)
    # if square_size == 9:
    #     sim.add_particle(4.5, 9)
    # if square_size == 10:
    #     sim.add_particle(5, 10)


    # if square_size == 2:
    #     sim.add_particle()
    # if square_size == 3:
    #     sim.add_particle()
    # if square_size == 4:
    #     sim.add_particle()
    # if square_size == 5:
    #     sim.add_particle()
    # if square_size == 6:
    #     sim.add_particle()
    # if square_size == 7:
    #     sim.add_particle()
    # if square_size == 8:
    #     sim.add_particle()
    # if square_size == 9:
    #     sim.add_particle()
    # if square_size == 10:
    #     sim.add_particle()



    #creates locations on the x coordinate from the starting_point
    for i in range (0, square_size+1):
        end_point_on_x = (starting_point[0] + i, starting_point[1])
        sim.add_location(end_point_on_x[0], end_point_on_x[1])

    #sim.add_particle(end_point_on_x[0] -0.5 , 1)
    #creates locations on the y coordinate from the starting_point
    for i in range (0,  square_size +1):
        end_point_on_y = (starting_point[0], (starting_point[1] + i))
        if i % 2 == 1:
            sim.add_location(end_point_on_y[0] - 0.5, end_point_on_y[1] )
            continue
        sim.add_location(end_point_on_y[0], end_point_on_y[1])


    #sim.add_particle(end_point_on_y[0] +0.5, end_point_on_y[1] - 1)
    #creates locations on the y coordinate from the ending point of the x coordinate
    for i in range (0,  square_size+1):
        if i % 2 == 1:
            sim.add_location(end_point_on_x[0] + 0.5, end_point_on_x[1] + i)
            continue
        sim.add_location(end_point_on_x[0], end_point_on_x [1]+i )

    #sim.add_particle(end_point_on_x[0]-0.5, end_point_on_x [1]+i-1)


    sim.add_particle(square_size/2+0.5, round(square_size/2))
    #creates locations on the x coordinate from the ending point of the y coordinate
    for i in range (0, square_size+1):
        if square_size % 2 == 1:
            sim.add_location(end_point_on_y[0] + i +0.5, end_point_on_y[1])
        else:
            sim.add_location(end_point_on_y[0] + i, end_point_on_y[1] )


