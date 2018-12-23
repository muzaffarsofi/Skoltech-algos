# coding=utf-8

class Node:

  def __init__(self, value, priority):
    self.value = value
    self.priority = priority

class PriorityQueue:

  def __init__(self):
    self.queue = list()

  def insert(self, node):
    if self.size() == 0:
      self.queue.append(node)
    else:
      for x in range(0, self.size()):
        if node.priority >= self.queue[x].priority:
          if x == (self.size()-1):
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
      print(str(x.value)+" - "+str(x.priority))

  def size(self):
    return len(self.queue)


def return_weight(dist):
    if dist % 2 == 0:
        return 1
    else:
        return 2


if __name__=='__main__':
    content = []
    with open('input.txt', 'r') as f:
        content = f.readlines()

    num_nodes, num_edges, s, t = int(content[0]),int(content[1]),int(content[2]),int(content[3])
    visited = [False for idx in range(num_nodes)]
    node_dist = [1e5 for idx in range(num_nodes)]
    node_dist[s] = 0
    
    G = {i:[] for i in range(num_nodes)}
    for elem in content[4:]:
        x,y = elem.split(' ')
        x,y = int(x), int(y)
        
        G[x].append(y)
    
    pq = PriorityQueue()
    pq.insert(Node(s,0))
    while pq.size():
        current = pq.delete()
        for node in G[current.value]:
            if not visited[node]:
                visited[node] = True
                if node_dist[current.value] % 4 == 0:
                    node_dist[node] = node_dist[current.value] + 1
                else:
                    node_dist[node] = node_dist[current.value] + 3
                pq.insert(Node(node, node_dist[node]))
   
    # print(node_dist[t])
    with open('output.txt', 'w') as f:
        f.write(str(node_dist[t]))

