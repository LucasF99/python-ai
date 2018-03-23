import random
import pygame
import math
import copy

class Cell(object):

    def __init__(self, net, color, radius):
        self.net = net
        self.x = 400
        self.y = 300

        self.x_speed = 0
        self.y_speed = 0
        self.x_accel = 0
        self.y_accel = 0
        self.color = color

        self.radius = radius
        self.max_speed = 2.5
        self.speed_mult = 4

        self.mut_rate = 0.8

        self.health = 100

    def update(self, net_in):
        #self.net.run([(self.x-(w/2))*-2,(self.y-(h/2))*-2,10])
        #print("updating - "+str(net_in))
        self.net.run(net_in)
        self.x_accel = self.net.get_out_values()[0]
        self.y_accel = self.net.get_out_values()[1]

    def eat(self, fm, foods):
        self.health += 70
        fm.foods.remove(foods)

    def get_pos(self):
        return [self.x, self.y]

    def set_mut_rate(self, rate):
        self.mut_rate = rate

    def get_mut_rate(self):
        return self.mut_rate

    def get_int_pos(self):
        return [int(self.x),int(self.y)]

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def get_accel(self):
        return [self.x_accel, self.y_accel]

    def get_speed(self):
        return [self.x_speed, self.y_speed]

    def set_speed(self, speed):
        self.x_speed = speed[0]
        self.y_speed = speed[1]

    def update_speed(self):
        self.x_speed += self.x_accel
        self.y_speed += self.y_accel
        if math.fabs(self.x_speed) > self.max_speed:
            if self.x_speed > 0:
                self.x_speed = self.max_speed
            elif self.x_speed < 0:
                self.x_speed = self.max_speed * (-1)
            else:
                self.x_speed = 0
        if math.fabs(self.y_speed) > self.max_speed:
            if self.y_speed > 0:
                self.y_speed = self.max_speed
            elif self.y_speed < 0:
                self.y_speed = self.max_speed * (-1)
            else:
                self.y_speed = 0

    def get_speed_mult(self):
        return self.speed_mult

    #def get_final_speed(self, fps):
        return [self.x_speed*self.speed_mult/fps, self.y_speed*self.speed_mult/fps]

    def get_final_speed(self, fps):
        return [self.x_speed,self.y_speed]

    def get_color(self):
        return self.color

    def get_radius(self):
        return self.radius

class Enemy(object):

    def __init__(self, x, y, color, radius):
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0
        self.x_accel = 0
        self.y_accel = 0
        self.color = color
        self.radius = radius
        self.accel_mult = 0.4
        self.max_speed = 5

    def update_speed(self):
        self.x_speed += self.x_accel
        self.y_speed += self.y_accel
        if math.fabs(self.x_speed) > self.max_speed:
            if self.x_speed > 0:
                self.x_speed = self.max_speed
            elif self.x_speed < 0:
                self.x_speed = self.max_speed * (-1)
            else:
                self.x_speed = 0
        if math.fabs(self.y_speed) > self.max_speed:
            if self.y_speed > 0:
                self.y_speed = self.max_speed
            elif self.y_speed < 0:
                self.y_speed = self.max_speed * (-1)
            else:
                self.y_speed = 0

    def get_pos(self):
        return [self.x, self.y]

    def get_int_pos(self):
        return [int(self.x),int(self.y)]

    def get_speed(self):
        return [self.x_speed, self.y_speed]

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def set_speed(self, speed):
        self.x_speed = speed[0]
        self.y_speed = speed[1]

    def set_accel(self, accel):
        self.x_accel = accel[0]
        self.y_accel = accel[1]

    def get_color(self):
        return self.color

    def get_radius(self):
        return self.radius

class EnemyManager(object):

    def __init__(self, en_amount):
        self.enemies = []
        self.last_spawn = 1
        for i in range(en_amount):
            if self.last_spawn == 1:
                self.enemies.append(Enemy(0,0,(165,35,35),8))
                self.last_spawn = 2
            elif self.last_spawn == 2:
                self.enemies.append(Enemy(10000,0,(165,35,35),8))
                self.last_spawn = 3
            elif self.last_spawn == 3:
                self.enemies.append(Enemy(0,10000,(165,35,35),8))
                self.last_spawn = 4
            else:
                self.enemies.append(Enemy(10000,10000,(165,35,35),8))
                self.last_spawn = 1

    def update(self, width, height, cell):
        for i in self.enemies:
            i.update_speed()
            if random.randint(1,5)==1: # updates at random instead of every frame
                i.set_accel([i.accel_mult*math.cos(math.atan2(random.uniform(0.4,1.6)*cell.get_pos()[1]-i.get_pos()[1],cell.get_pos()[0]-i.get_pos()[0])),
                            i.accel_mult*math.sin(math.atan2(random.uniform(0.4,1.6)*cell.get_pos()[1]-i.get_pos()[1],cell.get_pos()[0]-i.get_pos()[0]))])
                #i.set_speed([15*i.accel_mult*math.cos(math.atan2(random.uniform(0.4,1.6)*cell.get_pos()[1]-i.get_pos()[1],cell.get_pos()[0]-i.get_pos()[0])),
                #            15*i.accel_mult*math.sin(math.atan2(random.uniform(0.4,1.6)*cell.get_pos()[1]-i.get_pos()[1],cell.get_pos()[0]-i.get_pos()[0]))])
            i.set_pos([i.get_pos()[0]+i.get_speed()[0], i.get_pos()[1]+i.get_speed()[1]])
            if i.get_pos()[0] < 0:
                i.set_pos([0, i.get_pos()[1]])
                i.set_speed([0, i.get_speed()[1]])
            if i.get_pos()[0] > width:
                i.set_pos([width, i.get_pos()[1]])
                i.set_speed([0, i.get_speed()[1]])
            if i.get_pos()[1] < 0:
                i.set_pos([i.get_pos()[0], 0])
                i.set_speed([i.get_speed()[0], 0])
            if i.get_pos()[1] > height:
                i.set_pos([i.get_pos()[0], height])
                i.set_speed([i.get_speed()[0], 0])

    def add_enemy(self):
        if self.last_spawn == 1:
            self.enemies.append(Enemy(0,0,(165,35,35),8))
            self.last_spawn = 2
        elif self.last_spawn == 2:
            self.enemies.append(Enemy(10000,0,(165,35,35),8))
            self.last_spawn = 3
        elif self.last_spawn == 3:
            self.enemies.append(Enemy(0,10000,(165,35,35),8))
            self.last_spawn = 4
        else:
            self.enemies.append(Enemy(10000,10000,(165,35,35),8))
            self.last_spawn = 1

    def draw(self, screen):
        for i in self.enemies:
            pygame.draw.circle(screen, i.get_color(), i.get_int_pos(), i.get_radius())

class Food(object):

    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.pos = pos
        self.size = 4

    def draw(self, screen):
        color = (244, 222, 124)
        pygame.draw.circle(screen, color, [self.x, self.y], self.size)

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.size

class FoodManager(object):

    def __init__(self, food_amount, width, height):
        self.foods = []
        self.width = width
        self.height = height
        for i in range(food_amount):
            self.foods.append(Food([random.randint(0, self.width), random.randint(0, self.height)]))

    def add_food(self):
        self.foods.append(Food([random.randint(0, self.width), random.randint(0, self.height)]))

    def draw(self, screen):
        for i in self.foods:
            i.draw(screen)

class NetworkRender(object):

    def __init__(self, net, w, h):
        self.net = net
        self.neurons = []
        self.synapses = []
        self.longest_chain = 0
        self.neur_connect = [] # neurons connected to each neuron
        self.inp_index = []
        self.out_index = []
        self.estimates = []

        for k in range(len(net.neurons)):
            i = net.neurons[k]
            if k != 0:
                self.neurons.append([self.neurons[k-1][0]+random.randint(10,30)*random.choice([-1,1]),
                                    self.neurons[k-1][1]+random.randint(10,30)*random.choice([-1,1]), i])
            else:
                self.neurons.append([20, 20, i])

        self.min_dist = 20#w/12
        self.s_len = 100# 1.5*math.sqrt((w*h)/len(self.neurons))

        for i in net.synapses:
            self.synapses.append([copy.deepcopy(i.origin.index),
                                copy.deepcopy(i.target.index), i])

        for i in range(len(net.neurons)):
            n = net.neurons[i]
            if n in net.inp:
                self.inp_index.append(i)
            if n in net.out:
                self.out_index.append(i)
            #for j in range(len(n.target)):
            #    self.neur_connect[i].append(j.target)
            #    pass

        for i in range(len(self.inp_index)):
            ni = net.neurons[self.inp_index[i]]
            if ni.target != None:
                pass
            end = False
            dist = 0

    def search_target(self, neur, dist):
        if neur.target != None:
            for i in neur.target:
                t_neur = neur.target.target
                search_target(t_neur, dist)
            else:
                pass

    def find_structure(self):
        n = self.neurons
        for i in self.neurons:
            for j in self.neurons:
                if math.hypot(i[0]-j[0], i[1]-j[1]) < self.min_dist:
                    j[0]+=(self.min_dist/4)*random.choice([1,-1])
                    j[1]+=(self.min_dist/4)*random.choice([1,-1])
        for i in self.synapses:
            if math.hypot(n[i[0]][0]-n[i[1]][0],n[i[1]][0]-n[i[1]][1]) > self.s_len:
                n[i[0]][0] += (n[i[1]][0] - n[i[0]][0])/random.randint(10,25)
                n[i[0]][1] += (n[i[1]][1] - n[i[0]][1])/random.randint(10,25)
                n[i[1]][0] += (n[i[0]][0] - n[i[1]][0])/random.randint(10,25)
                n[i[1]][1] += (n[i[0]][1] - n[i[1]][1])/random.randint(10,25)
        ## Add pressure: applied by synapses over max length and neurons
        ## under min distance, after pressure is determined, neurons
        ## are moved according to it


    def draw(self, screen, x, y):
        for i in self.neurons:
            pygame.draw.circle(screen, (0,0,200), (int(i[0]+x),int(i[1]+y)), 4, 2)
        for i in self.synapses:
            pygame.draw.aaline(screen, (20,20,20),
                            (int(self.neurons[i[0]][0]+x),int(self.neurons[i[0]][1]+y)),
                            (int(self.neurons[i[1]][0]+x),int(self.neurons[i[1]][1]+y)))
