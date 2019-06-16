#p = "p"
#q = "q"
#impl = "=>"
#neg = "~"

#def testMPValidity(ant, cons, operator):
#    expr = ant+operator+cons
#    print(expr == "p=>q")

##testMPValidity(p,q,impl)
##testMPValidity(q,p,impl)
##testMPValidity(impl,p,"blah")


#def printPath(props):
#    ants = props[0]
#    consqs = props[1]
#    path = [p+impl for p in ants]
#    path.append([impl+q for q in consqs])
#    path.append(detectCycles(path))
#    print(path)

#def detectCycles(path):
#    cycles = []
#    for p in path:
#        for q in path:
#            if p == q and path.index(q) < path.index(p):
#                print("got here")
#                cycles.append(addCycle(p,q))
#    return cycles

#def addCycle(p,q):
#    x = p+"===>"+q+"\n"
#    x += "|    /\ \n"
#    x += "|_____|"
#    return x

#printPath([p,q,q])

#props = [SimpleProp("P"), SimpleProp("Q"), ComplexProp("P",">","Q")]

#prop = ComplexProp(~props[0], ">", ~props[1])

#print(prop)
#props.append(findTrans(props))



#def findTrans(props):
#    d = {}
#    for p in props:
#        d[p[0]] = (p[1], p[2])
#    ants = d.keys()
#    for a in ants:
#        consq = d[a][1]
#        if consq in ants:
#            d[a] = (d[a],d[d[a]])
#    return d


#results = findTrans(props)
#for r in results:
#    for v in results[r]:
#        print(r[0][0]+r[0][1]+r[0][2])