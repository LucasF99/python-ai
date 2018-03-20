import random
import pygame
import math

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

        self.mut_rate = 0.3

        self.health = 100

    def update(self, net_in):
        #self.net.run([(self.x-(w/2))*-2,(self.y-(h/2))*-2,10])
        self.net.run(net_in)
        self.x_accel = self.net.get_out_values()[0]
        self.y_accel = self.net.get_out_values()[1]

    def eat(self, fm, foods):
        self.health += 90
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
        self.accel_mult = 0.6
        self.max_speed = 6

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
