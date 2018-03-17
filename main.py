import pygame
import nn
import random
import evo

class Cell(object):

    def __init__(self, net, color, radius):
        self.net = net
        self.x = 200
        self.y = 200

        self.x_speed = 0
        self.y_speed = 0
        self.x_accel = 0
        self.y_accel = 0
        self.color = color

        self.radius = radius

    def update(self):
        self.net.run([self.x,self.y,25])
        self.x_accel = self.net.get_out_values()[0]
        self.y_accel = self.net.get_out_values()[1]

    def get_pos(self):
        return [self.x, self.y]

    def get_int_pos(self):
        return [int(self.x),int(self.y)]

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def get_speed(self):
        return [self.x_speed, self.y_speed]

    def set_speed(self, speed):
        self.x_speed = speed[0]
        self.y_speed = speed[1]

    def update_speed(self):
        self.x_speed += self.x_accel
        self.y_speed += self.y_accel

    def get_color(self):
        return self.color

    def get_radius(self):
        return self.radius

class Enemy(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0
        self.x_accel = 0
        self.y_accel = 0
        self.color = color

    def update_speed(self):
        self.x_speed += self.x_accel
        self.y_speed += self.y_accel
        
pygame.init()
width = 800
height = 600

screen = pygame.display.set_mode((width,height))
done = False
clock = pygame.time.Clock()
framerate = 60

net = nn.quick_layered_network([3,5,2], nn.mean)

print(str(len(net.neurons)))
net.run([3,1,5])
print(str(net.get_out_values()))

cells = []
#cells.append(Cell(net,(77, 175, 88), 8))
for i in range(100):
    cells.append(Cell(nn.quick_layered_network([3,2,2,2,2,2,2],nn.mean),(77,175,88),8))

evol = evo.CellEvolution(cells)

while not done:

    screen.fill((0,0,0))
    clock.tick(framerate)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

# new pool
# simulation
# cull
# mutate + fill pool
# repeat

##    for i in cells:
##        i.update()
##        i.update_speed()
##        i.set_pos([i.get_pos()[0]+i.get_speed()[0], i.get_pos()[1]+i.get_speed()[1]])
##        if i.get_pos()[0] < 0:
##            i.set_pos([0, i.get_pos()[1]])
##            i.set_speed([0, i.get_speed()[1]])
##        if i.get_pos()[0] > width:
##            i.set_pos([width, i.get_pos()[1]])
##            i.set_speed([0, i.get_speed()[1]])
##        if i.get_pos()[1] < 0:
##            i.set_pos([i.get_pos()[0], 0])
##            i.set_speed([i.get_speed()[0], 0])
##        if i.get_pos()[1] > height:
##            i.set_pos([i.get_pos()[0], height])
##            i.set_speed([i.get_speed()[0], 0])
##        pygame.draw.circle(screen, i.get_color(), i.get_int_pos(), i.get_radius())

    evol.simulate(screen, width, height)
    
    pygame.display.flip()

pygame.quit()












    
