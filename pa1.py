# CH 2.5 Algorithm Design
# I found that only considering the weight or the revenue of each client will not give an optimal solution
# when we take the ratio renvenue/bandwidth we can see that this may produce a better result and it does compared
# to the other possible solutions I've tried
# it forces the heap to prioritize clients with the most $/gb essentially with sounds like a natural optimal solution
# that is the greedy rule this algorithm follows

class Request:
    id = 0
    def __init__(self, revenue, bandwidth):

        self.r = revenue
        self.b = bandwidth
        self.weight = float(self.r/self.b)

class Heap:    
    def __init__(self, requests):
        self.heap:Request = [None] * requests
        self.used_spots = 0

    def heapify_up(self, i):    # O(logn)
        if(i > 0):
            j =  int(i/2)
            if(self.heap[i].weight > self.heap[j].weight):
                temp = self.heap[i]
                self.heap[i] = self.heap[j]
                self.heap[j] = temp

                self.heapify_up(j)
    
    def heapify_down(self,i):   # O(logn)
        j = None
        if (2*i > self.used_spots): return 0
        elif (2*i < self.used_spots):
            left = 2*i
            right = 2*i+1
            if(self.heap[right] == None): j = left
            elif(self.heap[right].weight > self.heap[left].weight):
                j = right
            else: j = left
            
        elif (2*i == self.used_spots):
            j = 2*i-1

        if(self.heap[0] != None and self.heap[j].weight > self.heap[i].weight):
            temp = self.heap[j]
            self.heap[j] = self.heap[i]
            self.heap[i] = temp

            self.heapify_down(j)
    
    def insert(self, v):    # O(logn)
        self.heap[self.used_spots] = v
        self.heapify_up(self.used_spots)
        self.used_spots += 1

    def remove(self,i):     # O(logn)
        if(self.heap[i] != None):
            node = self.heap[i]
            self.heap[i] = self.heap[self.used_spots-1]
            self.heap[self.used_spots-1] = None
            self.used_spots -= 1

            self.heapify_down(i)
            return node
        
fp = open("pa1input.txt")
contents = fp.readlines()

bandwidth_capacity = int(contents[0])
potential_clients = int(contents[1])

requests = contents[2:potential_clients+2]
request_objs = [Request(int(r.split(",")[0]), int(r.split(",")[1])) for r in requests]
for i in range(len(request_objs)):
    request_objs[i].id = i

pqueue = Heap(potential_clients)

[pqueue.insert(r) for r in request_objs]    # O(nlog(n))
sorted = [pqueue.remove(0) for r in range(potential_clients)] # O(nlog(n))

def compute_net_profit(units_available, request:Request):
    p = request.r
    n = -1.1*((request.b-units_available)/request.b)*request.r
    return (request,p+n)

def pull_clients(sorted_list):      # O(n)
    used_bandwidth = 0; revenue = 0
    clients = []
    for node in sorted_list:
        if(used_bandwidth + node.b <= bandwidth_capacity): 
            clients.append(node)
            used_bandwidth += node.b
            revenue += node.r
            
    #print(used_bandwidth, revenue,"\n")

    remaining = bandwidth_capacity - used_bandwidth
    sublease_options = []

    for node in sorted_list:
        if(not clients.__contains__(node)):
            sublease_options.append(compute_net_profit(remaining, node))

    m = 0
    mnode = None
    for s in sublease_options:  # which sublease option makes the most money
        if s[1] > m: m = s[1]; mnode = s
    
    if(m > 0):  # we choose to sublease
        print("1\n"+"("+str(mnode[0].id),str(mnode[0].b-remaining)+")")
        used_bandwidth += remaining
        revenue += m
    
    [print(c.id) for c in clients]
    #print(used_bandwidth, revenue)

pull_clients(sorted)

# the upper bound is O(nlog(n))