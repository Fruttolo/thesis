import sys
from lxml import etree


def naif(document):
    # open the XML file
    tree = etree.parse(document)
    # get the root node
    root = tree.getroot()
    # get all nodes in the tree
    nodes = [node for node in root.iterdescendants()]
    # initialize simulators
    sim = {node: tree.findall('.//' + node.tag) for node in nodes}
    # computer forward simulation
    sim = forwardsimulation(nodes, sim)
    # TODO: forward simulation
    return sim


def forwardsimulation(nodes, sim):
    counter = 0
    # for each node u verify Forward Simulation
    for u in nodes:
        print counter
        # v = post(u)
        for v in u:
            # w = sim[v]
            if u is not None:
                for w in sim[u]:
                    # intersection between post(w) and sim(v)
                    if len([val for val in w if val in sim[v]]) == 0:
                        # remove w from the simulator of u
                        sim[u].remove(w)
                        counter += 1
    return sim


def get_remove(nodes, poldsim, psim):
    temp = [0 for x in nodes]
    for n in poldsim:
        i = nodes.index(n)
        temp[i] = 1
    for m in psim:
        j = nodes.index(m)
        temp[j] = 0
    return temp




def efficient(document):
    # open the XML file
    tree = etree.parse(document)
    # get the root node
    root = tree.getroot()
    # get all nodes in the tree
    nodes = [node for node in root.iterdescendants()]
    # initialize sets
    sim = []
    sim[0] = 0
    oldsim = []
    rem = []
    c1 = 0
    c2 = 0
    # initialize sim() and prevsim()
    for node in nodes:
        i = nodes.index(node)
        print "initializing node " + str(c1) + "(" + str(nodes.index(node)) + ")"
        # prevsim(v)
        oldsim[i] = nodes
        # sim(v)
        if len(node) == 0:
            sim[i] = tree.findall('.//' + node.tag)
        else:
            sim[i] = [n for n in tree.findall('.//' + node.tag) if len(node) != 0]
            # remove vector
            # TODO: array implementation
        rem[i] = get_remove(nodes, pre(oldsim[i]), pre(sim[i]))
        c1 += 1
        print "done"
    # implement 2D array as a tuple-indexed dictonary
    print "inizializzo count(x,u)"
    count = getCount(nodes, sim)
    print "done"
    # F-Similarity Check
    # we store keys in remove only if remove(v)!=0, so when all remove(v) = 0 our dictonary is empty
    while len(remove) != 0:
        print "while cycle " + str(c2)
        # print "length of remove " + str(len(remove))
        c3 = 0
        for node in remove:
            if remove[]
            "for interno: " + str(c3)
            for u in node.getparent():
                for w in remove[node]:
                    if w in sim[u]:
                        sim[u].remove(w)
                        # decrement count
                        count[(w.getparent(), u)] -= 1
                        for x in w.getparent():
                            if count[(x, u)] == 0:
                                if u in remove:
                                    remove[u].append(x)
                                else:
                                    remove[u] = [x]
            oldsim[node] = sim[node]
            del remove[node]
            c3 += 1
        c2 += 1
    # print_sim(nodes,sim)
    return sim


def getCount(nodes, sim):
    count = {}
    for a in nodes:
        for b in nodes:
            count[(a, b)] = len([val for val in a if val in sim[b]])
    return count


def pre(nodelist):
    res = [n.getparent() for n in nodelist]
    return res


def print_sim(nodes, sim):
    for x in nodes:
        print 'simulators of node ' + x.text.strip() + ':\n'
        for y in sim[x]:
            print y.text.strip() + '\n'

"""
doc = 'prova.xml'
if sys.argv[1] == 1:
    efficient(doc)
if sys.argv[1] == 0:
    naif(doc)
"""