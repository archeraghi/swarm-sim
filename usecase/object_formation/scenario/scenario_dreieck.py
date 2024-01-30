import numpy as np
def scenario(sim):

    #sim.add_agent(-2.5, 3.0)
    #sim.add_agent(-2.5, 1.0)
    #print(sim.grid.get_center())

    #sim.add_agent((0.0, 0.0, 0.0))
    #sim.add_agent((1.0, 0.0, 0.0))
    #sim.add_agent((-1.0, 0.0, 0.0))
    #sim.add_agent((3.0, 0.0, 0.0))
    #sim.add_agent((5.0, -2.0, 0.0))
    #sim.add_agent((7.0, 2.0, 0.0))

    kachelanzahl = 0

    for  i in range(-5, 5, 4):
        for j in range(-10, 10, 4):
            sim.add_agent((i, j, 0.0))



    for  i in range(-6, 5, 1):
        for j in range(-10,10, 2):
            sim.add_item((i, j, 0.0))
            kachelanzahl = kachelanzahl + 1

    for  i in np.arange(-4.5, 5.5, 1):
        for j in range(-11, 9, 2):
            sim.add_item((i, j, 0.0))
            kachelanzahl = kachelanzahl + 1

    print("Kachelanzahl: ", kachelanzahl)





