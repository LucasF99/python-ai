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

for i in range(50):
    cells.append(sim.Cell(nn.quick_layered_network([13,8,8,2],nn.random_func(), random.choice([-1,1])),(77,175,88),8))
    cells[i].net.neurons[len(cells[i].net.neurons)-1].set_func(nn.tanh, 3)
    cells[i].net.neurons[len(cells[i].net.neurons)-2].set_func(nn.tanh, 3)

    n = cells[i].net
    na = nn.Neuron(None, nn.random_func(), random.choice([-1,1]))
    nb = nn.Neuron(None, nn.random_func(), random.choice([-1,1]))
    nc = nn.Neuron(None, nn.random_func(), random.choice([-1,1]))
    nd = nn.Neuron(None, nn.random_func(), random.choice([-1,1]))
    sa = nn.Synapse(na, random.uniform(-1,1))
    sb = nn.Synapse(nb, random.uniform(-1,1))
    sc = nn.Synapse(nc, random.uniform(-1,1))
    sd = nn.Synapse(nd, random.uniform(-1,1))
    na.set_target([sb])
    nb.set_target([sc])
    nc.set_target([sd])
    nd.set_target([sa])
    se = nn.Synapse(na, random.uniform(-1,1))
    sf = nn.Synapse(n.neurons[-3], random.uniform(-1,1))
    n.neurons[-3].target.append(se)
    na.target.append(sf)
    n.neurons.append(na)
    n.neurons.append(nb)
    n.neurons.append(nc)
    n.neurons.append(nd)
    n.synapses.append(sa)
    n.synapses.append(sb)
    n.synapses.append(sc)
    n.synapses.append(sd)
    n.synapses.append(se)
    n.synapses.append(sf)

    n.set_input_and_origin()

evol = evo.CellEvolution(cells)

#for i in range(20):
while True:
    evol.populate()
    evol.simulate(screen, width, height, framerate, clock)
    evol.select(5)

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
