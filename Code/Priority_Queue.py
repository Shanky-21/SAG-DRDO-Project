"""class Node:
    def __init__(self, info, priority):
        self.info = info
        self.priority = priority """

class PriorityQueue:
    def __init__(self):
        self.queue = list()
    
    def insert(self, node):
        if self.size() == 0:
            self.queue.append(node)
        else:
            for x in range(0, self.size()):
                if node[0] >= self.queue[x][0]:
                    if x == (self.size() - 1):
                        self.queue.insert(x+1, node)
                    else:
                        continue
                else:
                    self.queue.insert(x, node)
                    return True
    def delete(self):
        return self.queue.pop(0)
    
    def show(self):
        for x in self.queue:
            print(str(x[1]+" - "+str(x[0])))
    def size(self):
        return len(self.queue)
        # print(print(self.queue[:]))
    def top(self):
        return self.queue[0]
    def __print__(self):
        pass
