import random
import math

class Network(object):
    # neurons: neurons that aren't input or output
    # inp: input neurons
    # out: output neurons
    def __init__(self, neurons, inp, out):
        self.neurons = neurons
        self.inp = inp
        self.out = out
        self.synapses = []
        for i in self.neurons:
            if i.target != None:
                for j in i.target:
                    self.synapses.append(j)

    def set_input_and_origin(self):
        for i in self.synapses:
            i.set_target_input_syn()
        for i in self.neurons:
            if i.target != None:
                i.set_syn_origin()

    def run(self, in_val):
        # set input neurons
        #print("in val "+str(in_val))
        try:
            for i in range(len(in_val)):
                self.inp[i].append_val(in_val[i])
        except IndexError:
            raise IndexException("Amount of input values does not match amount of input neurons.")
        
        # run synapes
        for i in self.synapses:
            i.run()

        # run middle neurons
        for i in self.neurons:
            i.run()

        #print(str([i.in_val for i in self.inp]))

    def prt(self):
        print("neurons:")
        for i in self.neurons:
            print(str(i.get_out()))
        print("synapses:")
        for i in self.synapses:
            print(str(i.get_out()))

##        # run output neurons (this expects middle neurons
##        # to be linked to output neurons)
##        for i in self.out:
##            i.run()

    def get_out(self):
        # returns list of out neurons
        return self.out

    def get_out_values(self):
        # returns list of out values
        values = []
        for i in self.out:
            values.append(i.get_out())
        return values

class Neuron(object):
    # target: synapse list
    # func: activation function
    def __init__(self, target, func, *args):
        self.target = target
        self.func = func
        self.args = args
        self.in_val = []
        self.val = 0
        self.input_syns = []

    def set_target(self, syns):
        self.target = syns

    def set_syn_origin(self):
        for i in self.target:
            i.origin = self

    def append_val(self, x):
        self.in_val.append(x)

    def set_func(self, func, *args):
        self.func = func
        self.args = args

    def get_func(self):
        return self.func

    def get_args(self):
        return self.args

    def run(self):

        # apply activation funcion to input values
        self.val = self.func(self.in_val, *self.args)
        #print(str(self.in_val))
        self.in_val = []

        # send value to target synapses and run synapses
        if self.target != None:
            for i in self.target:
                i.set_in(self.val)

    def get_out(self):
        return self.val

class Synapse(object):
    # target: single neuron
    # weight: synapse weight
    def __init__(self, target, weight):
        self.target = target
        self.weight = weight
        self.in_val = 0
        self.val = 0
        self.origin = None

    def set_target_input_syn(self):
        if self not in self.target.input_syns:
            self.target.input_syns.append(self)

    def set_weight(self, weight):
        self.weight == weight

    def get_weight(self):
        return self.weight

    def set_target(self, neuron):
        self.target = neuron

    def set_in(self, x):
        self.in_val = x

    def run(self):
        # apply weight to value
        self.val = self.in_val*self.weight
        #print(str(self.val)+" = "+str(self.in_val)+" * "+str(self.weight))

        # send value to target neuron
        self.target.append_val(self.val)

    def get_out(self):
        return self.val

class IndexException(Exception):
    pass

def quick_layered_network(ls, func, *args):
    # ls = layer size list
    # tn = total neurons
    # ts = total synapses
    # prevl = previous layer size (in loop)
    # prevls = sum of previous layer sizes
    # prevss = same, but for synapses
    # temp_tgt = temporary target list for each neuron
    tn = 0
    ts = 0
    prevl = 0
    prevls = 0
    prevss = 0
    for i in ls: # find total number of neurons
        tn += i
    for i in range(len(ls)-1): # find total number of synapses
        ts+=ls[i]*ls[i+1]
    neur = []
    syn = []
    for i in range(tn): # initialize neurons
        neur.append(Neuron(None, func, *args))
    for i in range(ts): # initialize synapses
        syn.append(Synapse(None, random.uniform(-1,1)))
    for k in range(len(ls)-1): # loop through layer sizes, except last
        for i in range(prevls,prevls+ls[k]): # loop through neurons in a layer
            temp_tgt = []
            for j in range(ls[k+1]): # loop through neurons in the next layer to assign synapses
                #temp_tgt.append(syn[prevl*ls[k]+(ls[k+1]*(i-prevls))+j])
                temp_tgt.append(syn[prevss+(ls[k+1]*(i-prevls))+j])
            neur[i].set_target(temp_tgt)
        for i in range(prevss,prevss+ls[k]*ls[k+1]): # loop through synapses in current layer
            syn[i].set_target(neur[prevls+ls[k]+(i%ls[k+1])])

        prevl = ls[k]
        prevss += ls[k]*ls[k+1]
        prevls += ls[k]

    inp = []
    for i in range(ls[0]): # loop through neurons in the first layer
        inp.append(neur[i])
    out = []
    for i in range(tn-ls[len(ls)-1],tn): # loop through neurons in the last layer
        out.append(neur[i])

    net = Network(neur, inp, out)
    return net

def mean(in_val, *args):
    # get mean from input values
    mean = 0
    for i in in_val:
        mean += i
    mean = mean/len(in_val)

    return mean

def sigmoid(in_val, amp):
    mn = mean(in_val)
    if mn < 0:
        result = 1 - 1 / (1 + math.exp(mn))
    else:
        result = 1 / (1 + math.exp(-mn))
    return result * amp

def relu(in_val, m):
    mn = mean(in_val)
    if mn < 0:
        return 0
    else:
        return mn * m

def tanh(in_val, m):
    mn = mean(in_val)
    return math.tanh(mn)*m

def step(in_val, *a):
    mn = mean(in_val)
    if mn > 0:
        return 1
    else:
        return 0

def step_neg(in_val, *a):
    mn = mean(in_val)
    if mn > 0:
        return 1
    else:
        return -1

def cos(in_val, m):
    mn = mean(in_val)
    return m*(math.cos(mn))

def random_func():
    #return random.choice([mean,sigmoid,tanh,relu,step,step_neg])
    return random.choice([mean,sigmoid,tanh,relu,cos])

#
#
#### manually built network - for reference
#
#

# building network

##neurons = []
##synapses = []


##
##for i in range(9):
##    neurons.append(nn.Neuron(None, nn.mean))
##for i in range((3*4)+(4*2)):
##    synapses.append(nn.Synapse(None, random.uniform(-1,1)))

##for i in range(3):
##    # 4 = next layer synapses
##    neurons[i].set_target([synapses[4*i],synapses[4*i+1],synapses[4*i+2],synapses[4*i+3]])
##for i in range(3,7):
##    neurons[i].set_target([synapses[11+(2*i)-5],synapses[11+(2*i)-4]])
##for i in range(12):
##    synapses[i].set_target(neurons[3+(i%4)])
##for i in range(12,20):
##    synapses[i].set_target(neurons[7+(i%2)])
##
##net = nn.Network(neurons, [neurons[0],neurons[1],neurons[2]], [neurons[7],neurons[8]])
