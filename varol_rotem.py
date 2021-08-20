import pytest
import itertools
import functools

def gen_enum( n, relation):
    a = list(range(n+1))
    ap = list(range(n+1))

    yield a, ap
    k = n
    while True:
        j = ap[k]
        l = a[j-1]
        if (l,k) in relation:
            while j < k:
                l = a[j+1]
                a[j] = l
                ap[l] = j
                j += 1
            ap[k] = k
            a[k] = ap[k]
            k -= 1
            if k == 0:
                break
        else:
            # V4
            a[j-1] = k
            a[j] = l
            ap[k] = j-1
            ap[l] = j
            yield a, ap
            k = n

class EnumIter:
    def __init__(self, n, relation):
        self.n = n
        self.relation = relation

    def __iter__(self):
        self.a = list(range(self.n+1))
        self.ap = list(range(self.n+1))

        self.first = True

        return self

    def __next__(self):
        if self.first:
            self.first = False
            return self.a, self.ap

        k = self.n
        while True:
            j = self.ap[k]
            l = self.a[j-1]
            if (l,k) in self.relation:
                while j < k:
                    l = self.a[j+1]
                    self.a[j] = l
                    self.ap[l] = j
                    j += 1
                self.ap[k] = k
                self.a[k] = self.ap[k]
                k -= 1
                if k == 0:
                    raise StopIteration
            else:
                # V4
                self.a[j-1] = k
                self.a[j] = l
                self.ap[k] = j-1
                self.ap[l] = j
                return self.a, self.ap



def mk_relation(n):
    relation = set()
    def product( s0, s1):
        for a,b in itertools.product( s0, s1):
            relation.add( (a,b))

    def chain( s):
        for i in range(len(s)):
            for j in range(i+1,len(s)):
                relation.add( (s[i], s[j]))

    product( [0], list(range(1,n+1)))

    #chain( list(range(1,n+1)))
    product([1], [2,3,4])

    product([3], [4])
    return relation

examples = [(5,mk_relation(5)), (4,mk_relation(4))]

@pytest.mark.parametrize("n,relation", examples)
def test_A(n,relation):
    print(n,relation)
    for a, ap in gen_enum( n, relation):
        print(a,ap)

@pytest.mark.parametrize("n,relation", examples)
def test_B(n,relation):
    print(n,relation)
    for a, ap in iter(EnumIter( n, relation)):
        print(a,ap)

def runit(n=10):
    relation = set()
    def product( s0, s1):
        for a,b in itertools.product( s0, s1):
            relation.add( (a,b))

    def chain( s):
        for i in range(len(s)):
            for j in range(i+1,len(s)):
                relation.add( (s[i], s[j]))

    product( [0], list(range(1,n+1)))

    #chain( list(range(1,n+1)))
    #product([1], [2])
    #product([2], [3])
    #product([3], [4])

    return sum(1 for (a,ap) in iter(EnumIter( n, relation)))

@pytest.mark.skip
def test_AB(benchmark):
    count = benchmark(runit)
    assert functools.reduce(lambda a,b: a*b, range(1,11)) == count


@pytest.mark.parametrize("n,relation", examples)
def test_check(n,relation):

    def invert( a):
        ap = list(range(len(a)))
        for idx, x in enumerate(a):
            ap[x] = idx
        return ap

    perms = set()
    for a, ap in gen_enum( n, relation):
        assert ap == invert(a)
        perms.add( tuple( a[1:]))

    def check( ap, relation):
        return all( ap[a] < ap[b] for a,b in relation)

    perms2 = set()
    for a in itertools.permutations(list(range(1,n+1))):
        cand = check( (invert((0,)+a)), relation)
        if cand:
            perms2.add( tuple( a))

    assert perms == perms2
    print(perms)
