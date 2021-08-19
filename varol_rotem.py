import itertools

def enum( n, relation):
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

def test_A():
    relation = set()
    def product( s0, s1):
        for a,b in itertools.product( s0, s1):
            relation.add( (a,b))

    def chain( s):
        for i in range(len(s)):
            for j in range(i+1,len(s)):
                relation.add( (s[i], s[j]))

    n = 6

    product( [0], list(range(1,n+1)))

    #chain( list(range(1,n+1)))
    product([1], [2,3,4])

    product([3], [4])

    def invert( a):
        ap = list(range(len(a)))
        for idx, x in enumerate(a):
            ap[x] = idx
        return ap

    perms = set()
    for a, ap in enum( n, relation):
        assert ap == invert(a)
        perms.add( tuple( a[1:]))

    def check( a, relation):
        for i in range(len(a)):
            for j in range(i+1,len(a)):
                if (a[j], a[i]) in relation:
                    return False
        return True

    perms2 = set()
    for a in itertools.permutations(list(range(1,n+1))):
        if check( a, relation):
            perms2.add( tuple( a))

    assert perms == perms2
    print(perms)
