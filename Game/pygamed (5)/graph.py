from math import inf
import random
import queue
import copy

def bfs(graph):
    q = queue.Queue()
    lengths = [-1 for i in range(9)]

    q.put(1)
    lengths[0] = 0
    while not q.empty():
        ch = q.get()
        for i in graph[ch - 1]:
            if lengths[i - 1] == -1:
                lengths[i - 1] = lengths[ch - 1] + 1;
                q.put(i)
    return lengths


def build_graph():
    graph = [[2, 4], [1, 3, 5], [2, 6], [1, 5, 7], [2, 4, 6, 8], [3, 5, 9], [4, 8], [7, 5, 9], [6, 8]]
    for i in range(5):
        r1 = random.randint(0, 8)
        r2 = random.choice(graph[r1])
        graph[r1].remove(r2)
        graph[r2-1].remove(r1+1)
        l = bfs(graph)
        print(l)
        flg = False
        for i in l:
            if i == -1:
                flg = True
                break
        if flg:
            graph[r1].append(r2)
            graph[r2-1].append(r1+1)

    return graph

def pretty_print(g):
  print(g[0:3])
  print(g[3:6])
  print(g[6:])

def rec_build_graph(depth = 5, graph = [[2, 4], [1, 3, 5], [2, 6], [1, 5, 7], [2, 4, 6, 8], [3, 5, 9], [4, 8], [7, 5, 9], [6, 8]]):
  if depth:
    r1i = random.randint(0, 8)
    r2 = random.choice(graph[r1i])
    gr2 = copy.deepcopy(graph)
    gr2[r1i].remove(r2)
    gr2[r2-1].remove(r1i+1)
    l = bfs(gr2)
    flg = False
    for i in l:
        print(i)
        if i == -1:
            flg = True
            break
    if flg:
      return rec_build_graph(depth, graph)
    else:
      return rec_build_graph(depth-1, gr2)
  else:
    return graph
    
  
  
def create_level(depth=4):
  g = rec_build_graph(depth)
  doors = [[], [], [], [], [], [], [], [], []]
  for v in range(1,10):
    for s in g[v-1]:
      if v+1 == s:
        doors[v-1].append("right")
      if v-1 == s:
        doors[v-1].append("left")
      if v+3 == s:
        doors[v-1].append("down")
      if v-3 == s:
        doors[v-1].append("up")
  pretty_print(g)
  return doors