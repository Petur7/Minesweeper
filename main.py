from numpy.lib.function_base import append
import pygame
from pygame.locals import *
import sys
from createStructure import creatStructure
import time

def display_text(DISPLAY, character, x, y, block_width, line_width):
    font = pygame.font.Font('freesansbold.ttf', 15)
    text = font.render(character, True, (100,100,100))

    mid_x = (block_width+line_width)*x + block_width/2.5
    mid_y = (block_width+line_width)*y + block_width/3

    DISPLAY.blit(text, (mid_y, mid_x))

def fill_block(DISPLAY, x, y, block_width, line_width):
    pygame.draw.rect(DISPLAY, (180,180,180), (y*(block_width+line_width), x*(block_width+line_width), block_width, block_width))

def fill_bombs(DISPLAY, x, y, block_width, line_width):
    pygame.draw.rect(DISPLAY, (255,0,0), (y*(block_width+line_width), x*(block_width+line_width), block_width, block_width))

def disable(DISPLAY, disable_bombs, block_width, line_width):
    for bomb in disable_bombs:
        pygame.draw.rect(DISPLAY, (0, 255, 0), (bomb[1]*(block_width+line_width), bomb[0]*(block_width+line_width), block_width, block_width))


def explode(DISPLAY, x_axis, y_axis, bombs_pos, block_width, line_width):
    for bomb in bombs_pos:
        pygame.draw.rect(DISPLAY, (1,1,1), (bomb[1]*(block_width+line_width), bomb[0]*(block_width+line_width), block_width, block_width))
    
    font = pygame.font.Font('freesansbold.ttf', 45)
    text = font.render("BOOOM!!!", True, (255,0,0))

    mid_x = x_axis*(block_width+line_width)/2
    mid_y = y_axis*(block_width+line_width)/2

    DISPLAY.blit(text, text.get_rect(center=(mid_y, mid_x)))
    pygame.display.update()

def unflag(DISPLAY, flag_pos, block_width, line_width):
    pygame.draw.rect(DISPLAY, (220,220,220), (flag_pos[1]*(block_width+line_width), flag_pos[1]*(block_width+line_width), block_width, block_width))

def main(x_axis, y_axis, bombs):
    # Initialize program
    pygame.init()

    # Assign FPS a value
    FPS = 30
    FramePerSec = pygame.time.Clock()

    # Setup lines
    block_width = 22
    line_width = 1

    # Setup display
    GREY = pygame.Color(220, 220, 220) 
    LINE_color = pygame.Color(180, 180, 180)
    DISPLAY = pygame.display.set_mode((y_axis*(block_width+line_width) + line_width, x_axis*(block_width+line_width) + line_width))
    # DISPLAY = pygame.display.set_mode((900, 900))
    DISPLAY.fill(GREY)

    # Draw lines
    for row in range(0, y_axis):
        pygame.draw.line(DISPLAY, LINE_color, (row*(block_width+line_width), 0), (row*(block_width+line_width), (block_width+line_width)*x_axis), line_width)
    pygame.draw.line(DISPLAY, LINE_color, ((block_width+line_width)*y_axis, 0), ((block_width+line_width)*y_axis, (block_width+line_width)*x_axis), line_width)

    for column in range(0, x_axis):
        pygame.draw.line(DISPLAY, LINE_color, (0, column*(block_width+line_width)), ((block_width+line_width)*y_axis, column*(block_width+line_width)), line_width)
    pygame.draw.line(DISPLAY, LINE_color, (0, (block_width+line_width)*x_axis), ((block_width+line_width)*y_axis, (block_width+line_width)*x_axis), line_width)

    structure = creatStructure(x_axis, y_axis, bombs)

    exit = False
    visited = []
    bombs_pos = []
    disable_bombs = []
    flags = []
    for row in range(0, x_axis):
        for column in range(0, y_axis):
            if structure[row][column] == -1: bombs_pos.append((row, column))

    # Setup loop
    while bombs_pos:
        
        pygame.display.update()
        if exit:
            time.sleep(5)
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_y = int(mouse[0]/(block_width+line_width))
                mouse_x = int(mouse[1]/(block_width+line_width))
                
                if event.button == 1:
                    queue = [(mouse_x, mouse_y)]
                    while queue:
                        position = queue.pop(0)
                        visited.append(position)
                        if structure[position[0]][position[1]] == 0:
                            fill_block(DISPLAY, position[0], position[1], block_width, line_width)
                        else:
                            if structure[position[0]][position[1]] != -1:
                                display_text(DISPLAY, str(int(structure[position[0]][position[1]])), position[0], position[1], block_width, line_width)
                                break
                        if structure[position[0]][position[1]] == -1:
                            # display_text(DISPLAY, str(int(structure[position[0]][position[1]])), position[0], position[1], block_width, line_width)
                            disable(DISPLAY, disable_bombs, block_width, line_width)
                            explode(DISPLAY, x_axis, y_axis, bombs_pos, block_width, line_width)
                            exit = True
                            break
                           

                        # UP
                        if position[0]-1 >= 0:
                            if not (position[0]-1, position[1]) in visited and not (position[0]-1, position[1]) in queue:
                                if structure[position[0]-1][position[1]] == 0:
                                    queue.append((position[0]-1, position[1]))
                                else:
                                    if structure[position[0]-1][position[1]] != -1:
                                        display_text(DISPLAY, str(int(structure[position[0]-1][position[1]])), position[0]-1, position[1], block_width, line_width)
                                        visited.append((position[0]-1, position[1]))

                        # DOWN
                        if position[0]+1 <= x_axis-1:
                            if (not (position[0]+1, position[1]) in visited) and (not (position[0]+1, position[1]) in queue):
                                if structure[position[0]+1][position[1]] == 0:
                                    queue.append((position[0]+1, position[1]))
                                else:
                                    if structure[position[0]+1][position[1]] != -1:
                                        display_text(DISPLAY, str(int(structure[position[0]+1][position[1]])), position[0]+1, position[1], block_width, line_width)
                                        visited.append((position[0]+1, position[1]))

                        # LEFT
                        if position[1]-1 >= 0:
                            if not (position[0], position[1]-1) in visited and not (position[0], position[1]-1) in queue:
                                if structure[position[0]][position[1]-1] == 0:
                                    queue.append((position[0], position[1]-1))  
                                else:
                                    if structure[position[0]][position[1]-1] != -1:
                                        display_text(DISPLAY, str(int(structure[position[0]][position[1]-1])), position[0], position[1]-1, block_width, line_width)
                                        visited.append((position[0], position[1]-1))
                                

                        # RIGHT
                        if position[1]+1 <= y_axis-1:
                            if not (position[0], position[1]+1) in visited and not (position[0]+1, position[1]+1) in queue:
                                if structure[position[0]][position[1]+1] == 0:
                                    queue.append((position[0], position[1]+1))
                                else:
                                    if structure[position[0]][position[1]+1] != -1:
                                        display_text(DISPLAY, str(int(structure[position[0]][position[1]+1])), position[0], position[1]+1, block_width, line_width)
                                        visited.append((position[0], position[1]+1))
                
                if event.button == 3:
                    if not (mouse_x, mouse_y) in flags:
                        fill_bombs(DISPLAY, mouse_x, mouse_y, block_width, line_width)
                        try:
                            bombs_pos.remove((mouse_x, mouse_y))
                        except:
                            pass
                        else:
                            disable_bombs.append((mouse_x, mouse_y))
                        finally:
                            flags.append((mouse_x, mouse_y))
                    else:
                        unflag(DISPLAY, (mouse_x, mouse_y), block_width, line_width)
                        flags.remove((mouse_x, mouse_y))
                        if structure[mouse_x][mouse_y] == -1:
                            bombs_pos.append((mouse_x, mouse_y))
                            disable_bombs.remove((mouse_x, mouse_y))
                        



        FramePerSec.tick(FPS)
        mouse = pygame.mouse.get_pos()

    font = pygame.font.Font('freesansbold.ttf', 45)
    text = font.render("Succeed", True, (0,0,0))

    mid_x = x_axis*(block_width+line_width)/2
    mid_y = y_axis*(block_width+line_width)/2

    DISPLAY.blit(text, text.get_rect(center=(mid_y, mid_x)))
    pygame.display.update()
    time.sleep(5)

if __name__ == "__main__":
    # main(rows, colums, bombs)
    main(10, 10, 7)