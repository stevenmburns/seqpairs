import pytest
from itertools import product, combinations, permutations
from collections import defaultdict

class Graph:
    def __init__(self, edges, N):
        self.N = N
        self.adjList = defaultdict(list)
        self.indegree = defaultdict(int)
        for (src, dest) in edges:
            self.adjList[src].append(dest)
            self.indegree[dest] += 1

        self.paths = []

    @property
    def count(self):
        return len(self.paths)

    def findAllTopologicalOrders(self, path, discovered):
        for v in range(self.N):
            if self.indegree[v] == 0 and v not in discovered:
                for u in self.adjList[v]:
                    self.indegree[u] -= 1
                path.append(v)
                discovered.add(v)
                self.findAllTopologicalOrders(path, discovered)
                for u in self.adjList[v]:
                    self.indegree[u] += 1
                path.pop()
                discovered.remove(v)

        if len(path) == self.N:
            self.paths.append(tuple(path))

 
    def printAllTopologicalOrders(self):
        self.findAllTopologicalOrders([], set())
        print(self.count)
        #print(self.paths)
 

def sequence_pair_to_constraint_graphs(N, perm0, perm1):
    assert list(range(N)) == list(sorted(perm0))
    assert list(range(N)) == list(sorted(perm1))

    inv0 = {}
    for (idx, x) in enumerate(perm0):
        inv0[x] = idx

    inv1 = {}
    for (idx, x) in enumerate(perm1):
        inv1[x] = idx

    horiz = set()
    vert = set()

    for (a, b) in combinations(range(N), 2):
        if inv0[a] < inv0[b] and inv1[a] < inv1[b]:
            horiz.add((a, b))
        if inv0[a] < inv0[b] and inv1[b] < inv1[a]:
            vert.add((a, b))
        if inv0[b] < inv0[a] and inv1[b] < inv1[a]:
            horiz.add((b, a))
        if inv0[b] < inv0[a] and inv1[a] < inv1[b]:
            vert.add((b, a))

    return horiz, vert
            
def test_sp():
    N = 3
    for perm0, perm1 in product(permutations(range(N)), permutations(range(N))):
        sequence_pair_to_constraint_graphs(N, perm0, perm1)


def test_cmp():
    edges0 = []
    edges1 = []
 
    hc = []
    vc = []

    def h_const(a, b):
        hc.append((a,b))

    def v_const(a, b):
        vc.append((a, b))

    def h_chain(ch):
        for a, b in zip(ch[:-1], ch[1:]):
            hc.append((a, b))

    def v_chain(ch):
        for a, b in zip(ch[:-1], ch[1:]):
            vc.append((a, b))

    def h_pairs(s0, s1):
        for a, b in product(s0, s1):
            hc.append((a, b))

    def v_pairs(s0, s1):
        for a, b in product(s0, s1):
            vc.append((a, b))

    def semantic():
        for (a, b) in hc:
            edges0.append((a,b))
            edges1.append((a,b))

        for (a, b) in vc:
            edges0.append((a,b))
            edges1.append((b,a))


    v_chain( [0, 1, 2, 3])
    h_pairs( [4, 6], [5, 7])
    v_pairs( [3], [4, 6, 5, 7])
    semantic()
 
    N = 8
 
    g0 = Graph(edges0, N)
    g0.printAllTopologicalOrders()
    g1 = Graph(edges1, N)
    g1.printAllTopologicalOrders()

    s0 = set(edges0)
    s1 = set(edges1)

    count = 0
    for perm0, perm1 in product(g0.paths, g1.paths):
        if count % 10000 == 0:
            print(f"count={count}")
        horiz, vert = sequence_pair_to_constraint_graphs(N, perm0, perm1)
        for a, b in hc:
            assert (a, b) in horiz
        for a, b in vc:
            assert (a, b) in vert

        count += 1
    print(f"count={count}")
