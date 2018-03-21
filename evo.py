import pygame
import sim
import math
import copy
import random
import nn
import statistics

class Evolution(object):

    def __init__(self, pool):
        self.pool = pool

    def cull(self):
        pass

class CellEvolution(Evolution):

    def __init__(self, pool):
        pygame.font.init()
        self.pool = pool
        self.size = len(pool)
        self.fitness = []
        self.best_fit = 0
        self.last_mean_fit = 1
        self.worst_fit = math.inf
        self.font = pygame.font.SysFont('arial', 14)

        for i in range(len(pool)):
            self.fitness.append(0)

    def select(self, n):
        print(str(self.fitness))
        cutoff = 0
        low = 0
        self.best_fit = 0
        self.worst_fit = math.inf
        high_fit = []
        for i in range(n): high_fit.append(0)
        high_pool = []
        for i in range(n): high_pool.append(None)

        for i in range(len(self.fitness)):
            if self.fitness[i] > self.best_fit: # get best fitness value
                self.best_fit = self.fitness[i]
            if self.fitness[i] < self.worst_fit: # get worst fitness value
                self.worst_fit = self.fitness[i]

            if self.fitness[i] >= cutoff:
                low = math.inf
                low_i = None
                for j in range(len(high_fit)):
                    if high_fit[j] < low:
                        low = high_fit[j]
                        low_i = j
                high_fit[low_i] = self.fitness[i]
                high_pool[low_i] = self.pool[i]
                #print("added "+str(self.fitness[i])+" (index "
                #        +str(i)+") to high_fit at index "+str(low_i))
                cutoff = math.inf
                for j in range(len(high_fit)):
                    if high_fit[j] < cutoff:
                        cutoff = high_fit[j]
                        #print("set cutoff to "+str(cutoff))
        self.pool = high_pool

    def populate(self):
        prev_size = len(self.pool)
        print(str(self.fitness))
        mean_fitness = sum(self.fitness)/len(self.fitness)
        print("best fitness: "+str(self.best_fit))
        print("mean fitness: "+str(mean_fitness))
        print("worst fitness: "+str(self.worst_fit))
        diff = self.size - len(self.pool)

        # raise mutation rate if pool is too homogenous
        if mean_fitness == 0 or self.worst_fit == 0:
            mutation_rate = 1
            fit_change_rate = 1
        else:
            mutation_rate = ((self.best_fit/mean_fitness) + (mean_fitness/self.worst_fit))/2
            fit_change_rate = self.last_mean_fit/mean_fitness
        print("mutation rate: "+str(mutation_rate))
        print("fitness change rate: "+str(fit_change_rate))

        for i in range(len(self.pool),self.size):
            self.pool.append(copy.deepcopy(self.pool[random.randint(0, prev_size-1)]))

        for i in range(len(self.pool)): # mutate synapse weight
            for n in range(len(self.pool[i].net.synapses)):
                r = random.randint(1,100)
                #if r <= (1/2)*(mutation_rate)*fit_change_rate*self.pool[i].get_mut_rate()*10:
                if r <= (1/2)*self.pool[i].get_mut_rate()*6:
                    s = self.pool[i].net.synapses[random.randint(0,len(self.pool[i].net.synapses)-1)]
                    s.set_weight(s.get_weight()*random.uniform(0,2)*random.choice([-1,1]))

        for i in range(len(self.pool)): # mutate function type
            for n in self.pool[i].net.neurons:
                r = random.randint(1,100)
                if r <= 5*self.pool[i].get_mut_rate():
                    n.set_func(nn.random_func(),*n.get_args())

        for i in self.pool: # mutate function arguments
            for n in i.net.neurons:
                r = random.randint(1,100)
                if r <= 5*i.get_mut_rate():
                    n.set_func(n.get_func(), *(j*random.uniform(0,2)*random.choice([-1,1]) for j in n.get_args()))

        for i in self.pool: # mutate mutation rate
            r = random.randint(1,100)
            if r <= 10*i.get_mut_rate():
                i.set_mut_rate(i.get_mut_rate()*random.uniform(0.7, 1.3))

        for i in range(len(self.pool)): # crossover
            ni = random.randint(0, len(self.pool)-1)
            for _ in range(len(self.pool[i].net.synapses)):
                r = random.randint(1,100)
                if r <= 50:
                    si = random.randint(0,len(self.pool[i].net.synapses)-1)
                    s = self.pool[i].net.synapses[si]
                    if si < len(self.pool[ni].net.synapses):
                        s.set_weight(self.pool[ni].net.synapses[si])
        self.last_mean_fit=mean_fitness

        for i in range(len(self.pool)): # mutate structure
            j = self.pool[i].net
            r = random.randint(1,100)
            if r<=0*self.pool[i].get_mut_rate():
                o_n = j.neurons[random.randint(0,len(j.neurons)-1)]
                i_n = j.neurons[random.randint(0,len(j.neurons)-1)]
                while i_n.target == None:
                    i_n = j.neurons[random.randint(0,len(j.neurons)-1)]
                s_o = nn.Synapse(o_n, random.uniform(-1,1))
                n = nn.Neuron([s_o], nn.random_func(), random.choice([-1,1]))
                s_i = nn.Synapse(n, random.uniform(-1,1))
                i_n.target.append(s_i)
                i_n.set_syn_origin()
                s_o.set_target_input_syn()
                s_i.set_target_input_syn()
                j.neurons.append(n)
                j.synapses.append(s_o)
                j.synapses.append(s_i)
                print("added neuron to "+str(i))
            r = random.randint(1,100)
            if r<=0*self.pool[i].get_mut_rate():
                n = j.neurons[random.randint(0,len(j.neurons)-1)]
                while n in j.inp or n in j.out:
                    n = j.neurons[random.randint(0,len(j.neurons)-1)]
                for k in n.target:
                    k.target.input_syns.remove(k)
                    j.synapses.remove(k)
                    n.target.remove(k)
                    del k
                for k in n.input_syns:
                    if k in k.origin.target:
                        k.origin.target.remove(k)
                    j.synapses.remove(k)
                    n.input_syns.remove(k)
                    del k
                j.neurons.remove(n)
                print("removed neuron from "+str(i))

    def fitness_func(self):
        pass

    def simulate(self, screen, width, height, framerate, clock):
        #print("pool size: "+str(len(self.pool)))
        self.fitness = []
        for i in range(len(self.pool)):
            #print("INDEX: "+str(i))
            surv_time = 0
            dead = False
            em = sim.EnemyManager(3)
            fm = sim.FoodManager(40, width, height)
            food_tick = 0
            food_threshold = 70
            self.pool[i].set_pos([width/2,height/2])
            self.pool[i].set_speed([random.uniform(-1,1), random.uniform(-1,1)])
            self.pool[i].health=100
            while not dead:

                screen.fill((16,45,45))
                clock.tick(framerate)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            framerate = 60000
                        if event.key == pygame.K_DOWN:
                            framerate = 60

                c = self.pool[i]

                text_surface = self.font.render("Health: "+str(c.health)+
                                                "   Neurons: "+str(len(c.net.neurons)), False, (255,255,255))
                screen.blit(text_surface,(10,10))

                em.update(width, height, self.pool[i])
                em.draw(screen)

                if len(em.enemies) > 0:
                    mean_en_x = sum((j.get_pos()[0]-c.get_pos()[0]) for j in em.enemies)/len(em.enemies)
                    mean_en_y = sum((j.get_pos()[0]-c.get_pos()[0]) for j in em.enemies)/len(em.enemies)
                else:
                    mean_en_x = 0
                    mean_en_y=0

                pos_x = (c.get_pos()[0]-(width/2))/(width/2)
                pos_y = (c.get_pos()[1]-(height/2))/(height/2)

                mean_fd_x = (sum((j.get_pos()[0]-c.get_pos()[0]) for j in fm.foods)/len(fm.foods))/width
                mean_fd_y = (sum((j.get_pos()[0]-c.get_pos()[0]) for j in fm.foods)/len(fm.foods))/height

                #en_x_stdev = statistics.pstdev(list((j.get_pos()[0]-c.get_pos()[0]) for j in em.enemies))
                #en_y_stdev = statistics.pstdev(list((j.get_pos()[0]-c.get_pos()[0]) for j in em.enemies))

                # get closest enemy pos
                closest_dist = math.inf
                closest_food = math.inf
                for j in em.enemies:
                    if math.hypot(j.get_pos()[0]-c.get_pos()[0], j.get_pos()[1]-c.get_pos()[1]) < closest_dist:
                        closest_x = j.get_pos()[0]
                        closest_y = j.get_pos()[1]
                        closest_dist = math.hypot(j.get_pos()[0], j.get_pos()[1])

                for j in fm.foods:
                    if math.hypot(j.get_pos()[0]-c.get_pos()[0], j.get_pos()[1]-c.get_pos()[1]) < closest_food:
                        closest_food_x = j.get_pos()[0]
                        closest_food_y = j.get_pos()[1]
                        closest_food = math.hypot(j.get_pos()[0], j.get_pos()[1])

                rel_food_x = (closest_food_x-c.get_pos()[0])/width
                rel_food_y = (closest_food_y-c.get_pos()[1])/height
                rel_close_x = (closest_x-c.get_pos()[0])/width
                rel_close_y = (closest_y-c.get_pos()[1])/height

                surv_time += 1

                #print("i: "+str(i))
                #self.pool[i].update([c.get_pos()[0],c.get_pos()[1],c.get_speed()[0],c.get_speed()[1],
                #                    rel_close_x, rel_close_y, mean_en_x, mean_en_y, en_x_stdev, en_y_stdev,
                #                    width, height, c.get_accel()[0], c.get_accel()[1], rel_food_x, rel_food_y]) # run net and set accel
                self.pool[i].update([pos_x,pos_y,c.get_speed()[0],c.get_speed()[1],
                                    rel_close_x, rel_close_y, c.health, mean_fd_x, mean_fd_y,
                                    c.get_accel()[0], c.get_accel()[1], rel_food_x, rel_food_y]) # run net and set accel
                self.pool[i].update_speed()

                # update pos
                self.pool[i].set_pos([self.pool[i].get_pos()[0]+(self.pool[i].get_final_speed(framerate)[0]),
                                        self.pool[i].get_pos()[1]+(self.pool[i].get_final_speed(framerate)[1])])
                if self.pool[i].get_pos()[0] < 0:
                    dead = True
                    self.pool[i].set_pos([0, self.pool[i].get_pos()[1]])
                    self.pool[i].set_speed([0, self.pool[i].get_speed()[1]])
                if self.pool[i].get_pos()[0] > width:
                    dead = True
                    self.pool[i].set_pos([width, self.pool[i].get_pos()[1]])
                    self.pool[i].set_speed([0, self.pool[i].get_speed()[1]])
                if self.pool[i].get_pos()[1] < 0:
                    dead = True
                    self.pool[i].set_pos([self.pool[i].get_pos()[0], 0])
                    self.pool[i].set_speed([self.pool[i].get_speed()[0], 0])
                if self.pool[i].get_pos()[1] > height:
                    dead = True
                    self.pool[i].set_pos([self.pool[i].get_pos()[0], height])
                    self.pool[i].set_speed([self.pool[i].get_speed()[0], 0])

                pygame.draw.circle(screen, self.pool[i].get_color(), self.pool[i].get_int_pos(), self.pool[i].get_radius())

                # collision check
                for j in em.enemies:
                    if math.hypot(self.pool[i].get_pos()[0]-j.get_pos()[0],self.pool[i].get_pos()[1]-j.get_pos()[1]) <= self.pool[i].get_radius()+j.get_radius():
                        c.health-=100
                        em.enemies.remove(j)
                for j in fm.foods:
                    if math.hypot(c.get_pos()[0]-j.get_pos()[0],c.get_pos()[1]-j.get_pos()[1]) <= c.get_radius()+j.get_radius():
                        c.eat(fm,j)

                #if len(em.enemies) <= -6+(surv_time/1500)**3:
                if len(em.enemies) <= -3+surv_time/90:
                    em.add_enemy()

                #add food
                if food_tick >= food_threshold:
                    fm.add_food()
                    food_tick = 0

                if c.health <= 0:
                    dead = True

                fm.draw(screen)

                food_tick+=1
                c.health -= 0.3

                pygame.display.flip()

            self.fitness.append(surv_time)

    def old_simulate(self, screen, width, height, fps):
        for i in range(len(self.pool)):
            #self.pool[i].net.prt()
            self.pool[i].update(width, height)
            self.pool[i].update_speed()
            #self.pool[i].set_pos([self.pool[i].get_pos()[0]+(self.pool[i].get_speed()[0]*self.pool[i].get_speed_mult()),
            #                        self.pool[i].get_pos()[1]+(self.pool[i].get_speed()[1]*self.pool[i].get_speed_mult())])
            self.pool[i].set_pos([self.pool[i].get_pos()[0]+(self.pool[i].get_final_speed(fps)[0]),
                                    self.pool[i].get_pos()[1]+(self.pool[i].get_final_speed(fps)[1])])

            print(str(self.pool[10].get_speed()[0])+", "+str(self.pool[10].get_speed()[1]))

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
            #self.surv_time[i]+=1

            pygame.draw.circle(screen, self.pool[i].get_color(), self.pool[i].get_int_pos(), self.pool[i].get_radius())
