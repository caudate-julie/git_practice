import sys
import pygame
from random import random, randrange
from math import cos, sin, sqrt
from vector import vector

from graph import Graph

WHITE = (255, 255, 255)
RED   = (250, 100, 100)
BLACK = (  0,   0,   0)

# window and drawing

WIDTH = 800     # size of window
HEIGHT = 600
MARGIN = 50

CENTER = vector(WIDTH / 2, HEIGHT / 2)  #shortcut for center point
RADIUS = min(HEIGHT, WIDTH) / 2 - MARGIN   # shortcut for leaf-circle radius

STEP = 1          # for now - single movement

EPSILON = 1       # to avoid twitches around precise point

def create_window():
    """Create and return window with initial settings."""
    pygame.init()
    speed = [2, 2]
    return pygame.display.set_mode((WIDTH, HEIGHT))

def draw_graph(screen, g):
    for i in range(g.size):
        # draw a vertex.
        V = g.V[i]
        if V.degree == 0:   # not empty one.
            continue

        pygame.draw.circle(screen, RED, [int(V.x), int(V.y)], 4)
        font = pygame.font.Font(None, 24)
        text = font.render(str(i), 0, BLACK, WHITE)
        text.set_alpha(100)
        screen.blit(text, (V.x - 5, V.y - 20))

        # draw edges
        for j in range(g.size):
            if i >= j or not g.E[i][j]: continue
            W = g.V[j]
            pygame.draw.line(screen, RED, [V.x, V.y], [W.x, W.y], 1)

    # show current graph energy
    font = pygame.font.Font(None, 20)
    text = font.render(str(round(g.weight, 2)), 0, BLACK, WHITE)
    screen.blit(text, (10, 10))

def coords_in_bound(x, y):
    # coords are within screen margin
    return (x >= MARGIN and x <= WIDTH - MARGIN
            and y >= MARGIN and y <= HEIGHT - MARGIN)

def orthogonal_directions(x, y):
    """Return for unit vectors, tilted at random angle, and (0, 0)."""
    directions = [(0, 0), (STEP, 0), (0, STEP), (-STEP, 0), (0, -STEP)]
    alpha = random() * 2 * 3.1415926
    for d in directions:
        d = (d[0] * cos(alpha), d[1] * sin(alpha))
    return [d for d in directions if coords_in_bound(x + d[0], y + d[1])]

def arc_directions(x, y, R):
    eps = 0.001
    directions = [
                  (0, 0),
                  (x - x*cos(eps) + y*sin(eps), y - y*cos(eps) - x*sin(eps)),
                  (x - x*cos(eps) - y*sin(eps), y - y*cos(eps) + x*sin(eps)),
                 ]
    
    return directions

def possible_directions(g, i):
    V = g.V[i]
    if g.is_tree:
        to_center = CENTER - vector(V.x, V.y)
        dist = to_center.mod()
        if dist - RADIUS > EPSILON:
            # move all vertices into the leaf-circle
            print i, "going in"
            return [to_center.unit().tuple()]
        if V.degree == 1 and RADIUS - dist > EPSILON:
            # move all leafs at the boundary of leaf-circle
            return [(-to_center).unit().tuple()]
        if V.degree == 1:
            return arc_directions(V.x, V.y, RADIUS)

    return orthogonal_directions(V.x, V.y)

def move_vertex(g, i):
    if g.V[i].degree == 0: return

    directions = possible_directions(g, i)
    V = g.V[i]
    x, y = V.x, V.y
    weights = []

    for d in directions:
        g.set_coords(i, x + d[0], y + d[1])
        weights.append(g.weight)

    best = weights.index(min(weights))
    new_x, new_y = x + directions[best][0], y + directions[best][1]
    g.set_coords(i, new_x, new_y)


def show_help():
    return "NO ONE WILL HELP YOU!"


def parse_command(message, g):
    words = message.split();
    # add a new edge.
    if words[0] == "add" and len(words) == 3:
        try:
            i, j = int(words[1]), int(words[2])
        except: pass  # error message at the end of the function
        else:
            if g.in_bounds(i) and g.in_bounds(j): 
                g.add_edge(i, j)
                return ""

    # delete existing edge
    elif words[0] == "del" and len(words) == 3:
        try:
            i, j = int(words[1]), int(words[2])
        except: pass  # error message at the end of the function
        else:
            if g.in_bounds(i) and g.in_bounds(j):
                g.delete_edge(i, j)
            return ""

    # change edge weight coefficient
    elif words[0] == "edge" and len(words) == 2:
        try:
            c = int(words[1])
        except: pass  # error message at the end of the function
        else:
            Graph.EDGE_COEFF = c
            g.reset_weight()
            return ""

    # change vertex weight coefficient
    elif words[0] == "vertex" and len(words) == 2:
        try:
            c = int(words[1])
        except: pass  # error message at the end of the function
        else:
            Graph.VERTEX_COEFF = c * 100  # so edge and vertex coeffs are ~ same
            g.reset_weight()
            return ""

    elif words[0] == "help":
        return show_help()
        
    return "Command not found. Press ESC."

def key_handler(message, key, g):
    if key == pygame.K_BACKSPACE:
        return message[:-1] if len(message) > 0 else ""
    if key == pygame.K_RETURN:
        return parse_command(message, g)
    if key == pygame.K_ESCAPE:
        return ""
    if key == pygame.K_SPACE:
        return message + " "
    return message + pygame.key.name(key)

def gameloop(screen, g):
    clock = pygame.time.Clock()
    message = ""
    while True:
        clock.tick(200)
        move_vertex(g, randrange(g.size))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                message = key_handler(message, event.key, g)

        screen.fill(WHITE)
        draw_graph(screen, g)
        font = pygame.font.Font(None, 20)
        text = font.render(message, 0, BLACK, WHITE)
        screen.blit(text, (10, 30))
        pygame.display.flip()

def set_initial_coords(g):
    for i in range(g.size):
        g.set_coords(
            i, 
            randrange(MARGIN, WIDTH - MARGIN), 
            randrange(MARGIN, HEIGHT - MARGIN)
            )


print "Hello!"
g = Graph(10)
set_initial_coords(g)
g.add_edge(1, 2)
g.add_edge(2, 3)
g.add_edge(3, 4)
#g.add_edge(4, 2)

screen = create_window()
gameloop(screen, g)