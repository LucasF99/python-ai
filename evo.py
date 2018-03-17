import pygame

class Evolution(object):

    def __init__(self, pool):
        self.pool = pool

    def cull(self):
        pass

class CellEvolution(Evolution):

    def __init__(self, pool):
        self.pool = pool
        self.surv_time = []

        for i in range(len(pool)):
            self.surv_time.append(0)

    def cull(self):
        pass

    def fitness(self):
        pass

    def simulate(self, screen, width, height):
        for i in range(len(self.pool)):
            self.pool[i].update()
            self.pool[i].update_speed()
            self.pool[i].set_pos([self.pool[i].get_pos()[0]+self.pool[i].get_speed()[0], self.pool[i].get_pos()[1]+self.pool[i].get_speed()[1]])
            if self.pool[i].get_pos()[0] < 0:
                self.pool[i].set_pos([0, self.pool[i].get_pos()[1]])
                self.pool[i].set_speed([0, self.pool[i].get_speed()[1]])
            if self.pool[i].get_pos()[0] > width:
                self.pool[i].set_pos([width, self.pool[i].get_pos()[1]])
                self.pool[i].set_speed([0, self.pool[i].get_speed()[1]])
            if self.pool[i].get_pos()[1] < 0:
                self.pool[i].set_pos([self.pool[i].get_pos()[0], 0])
                self.pool[i].set_speed([self.pool[i].get_speed()[0], 0])
            if self.pool[i].get_pos()[1] > height:
                self.pool[i].set_pos([self.pool[i].get_pos()[0], height])
                self.pool[i].set_speed([self.pool[i].get_speed()[0], 0])
            self.surv_time[i]+=1
                
            pygame.draw.circle(screen, self.pool[i].get_color(), self.pool[i].get_int_pos(), self.pool[i].get_radius())
