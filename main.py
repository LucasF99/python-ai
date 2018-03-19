import pygame
import nn
import random
import evo
import sim

pygame.init()
width = 800
height = 600

screen = pygame.display.set_mode((width,height))
done = False
clock = pygame.time.Clock()
framerate = 60000

cells = []
#cells.append(Cell(net,(77, 175, 88), 8))

for i in range(100):
    cells.append(sim.Cell(nn.quick_layered_network([14,20,10,2],random.choice([nn.mean, nn.sigmoid, nn.tanh, nn.relu, nn.step, nn.step_neg]), random.choice([-1,1])),(77,175,88),8))
    cells[i].net.neurons[len(cells[i].net.neurons)-1].set_func(nn.tanh, 3)
    cells[i].net.neurons[len(cells[i].net.neurons)-2].set_func(nn.tanh, 3)

evol = evo.CellEvolution(cells)

#for i in range(20):
while True:
    evol.populate()
    evol.simulate(screen, width, height, framerate, clock)
    evol.select(4)

#while not done:
#
#    screen.fill((16,45,45))
#    clock.tick(framerate)
#
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            done = True
#
#    evol.simulate(screen, width, height, framerate)
#
#    pygame.display.flip()

# new pool
# simulation
# select
# mutate + fill pool
# repeat

pygame.quit()
