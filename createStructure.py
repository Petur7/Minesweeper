import numpy
import random

def Point(structure, x, y) -> numpy.array:
    x_axis = structure.shape[0]
    y_axis = structure.shape[1]

    # UP
    if x - 1 >= 0 and structure[x-1][y] != -1:
        structure[x-1][y] += 1

    # DOWN
    if x + 1 <= x_axis - 1 and structure[x+1][y] != -1:
        structure[x+1][y] += 1

    # LEFT
    if y - 1 >= 0 and structure[x][y-1] != -1:
        structure[x][y-1] += 1

    # RIGHT
    if y + 1 <= y_axis - 1 and structure[x][y+1] != -1:
        structure[x][y+1] += 1

    # UP LEFT
    if x - 1 >= 0 and y - 1 >= 0 and structure[x-1][y-1] != -1:
        structure[x-1][y-1] += 1

    # UP RIGHT
    if x - 1 >= 0 and y + 1 <= y_axis - 1 and structure[x-1][y+1] != -1:
        structure[x-1][y+1] += 1

    # DOWN LEFT
    if x + 1 <= x_axis -1 and y - 1 >= 0 and structure[x+1][y-1] != -1:
        structure[x+1][y-1] += 1

    # DOWN RIGHT
    if x + 1 <= x_axis -1 and y + 1 <= y_axis - 1 and structure[x+1][y+1] != -1:
        structure[x+1][y+1] += 1

    return structure


def creatStructure(x_axis, y_axis, bombs) -> numpy.array:
   
    # Create structure with 0
    structure = numpy.zeros((x_axis, y_axis))
    
    # Create bombs
    for bomb in range(0, bombs):
        while True:
            X_axis_random = random.randint(0, x_axis-1)
            Y_axis_random = random.randint(0, y_axis-1)
            
            # print("x: " + str(X_axis_random) + "\ny: " + str(Y_axis_random))

            if structure[X_axis_random][Y_axis_random] != -1:
                # Set -1 at the bombs position
                structure[X_axis_random][Y_axis_random] = -1
                structure = Point(structure, X_axis_random, Y_axis_random)
                break         
            
            # If the position has bomb before then create another position
            if structure[X_axis_random][Y_axis_random] == -1:
                continue
    
    return structure


if __name__ == "__main__":
    structure = creatStructure(9, 9, 5)
    print(structure)