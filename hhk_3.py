from lxml import etree


def naif(document):
    # open the XML file
    tree = etree.parse(document)
    # get the root node
    root = tree.getroot()
    # get all nodes in the tree
    nodes = [node for node in root.iter()]
    # initialize simulators
    sim = {node: tree.findall('.//' + node.tag) for node in nodes}
    # computer forward simulation
    return forward_simulation(nodes, sim)
    # TODO: forward simulation
    #print_sim(nodes, sim)


def forward_simulation(nodes, sim):
    counter = 0
    c = 0
    # for each node u verify Forward Simulation
    flag = True

    while flag:
        #print "while: " + str(c)
        flag = False
        for u in nodes:
            # v = post(u)
            for v in u:
                # w = sim[v]
                if u is not None:
                    for w in sim[u]:
                        #print "inner for "  + str(counter)
                        # intersection between post(w) and sim(v)
                        if len([val for val in w if val in sim[v]]) == 0:
                            flag = True
                            # remove w from the simulator of u
                            sim[u].remove(w)
                        counter += 1
        c += 1
    return sim


def efficient(document):
    # open the XML file
    tree = etree.parse(document)
    # get the root node
    root = tree.getroot()
    # get all nodes in the tree
    nodes = {root: 0}
    l = list(root.iterdescendants())
    nodes.update(dict(zip(l, range(1, len(l) + 1))))
    # initialize sets
    sim = {root: root}
    # renamed prevsim(v) to oldsim to avoid confusion
    oldsim = {}
    remove = {}
    count = {}
    # counters for debugging
    c1 = 0
    c2 = 0
    ##print "starting operations"
    # initialize sim(v), prevsim(v) and count(w'',u)
    # total cost is O(n^2) + O(mn) + O(mn) = O(mn) with m>n
    for node in nodes:

        ##print "initializing node " + str(c1)
        # prevsim(v) is assigned in O(1)
        oldsim[node] = nodes
        # sim(v) is calculated in O(n^2)
        if len(node) == 0:
            sim[node] = {n: nodes[n] for n in nodes if n.tag == node.tag}
        else:
            sim[node] = {n: nodes[n] for n in nodes if n.tag == node.tag and len(n) != 0}

        # remove vector is calculated in O(mn)
        ##print "initializing remove"
        remove[node] = pre(oldsim[node], nodes)
        # print remove[node]
        # print "remove of node " + node.text.strip()
        for n in pre(sim[node], nodes):
            try:
                del remove[node][n]
                #print "removed node " + n.text.strip()
            except KeyError:
                pass
        if len(remove[node]) == 0:
            del remove[node]
        ##print "remove done"

        c1 += 1
        ##print "node done"
    # printnodes(oldsim)
    # print "\nsim: "
    #printnodes(sim)
    #print "\nremove: "
    #printnodes(remove)

    # implement 2D array as a tuple-indexed dictionary
    # count is calculated in O(mn)
    ##print "initializing count(x,u)"
    for node in nodes:
        count.update(getcount(node, sim))
    ##print "count done"

    # F-Similarity Check
    # we store keys in remove only if remove(v)!=0, so when all remove(v) = 0 our dictionary is empty
    while len(remove) != 0:
        print len(remove)
        ##print "while cycle " + str(c2)
        # print "length of remove " + str(len(remove))
        c3 = 0
        keys = remove.keys()
        for node in keys:
            ##print "internal for cycle : " + str(c3)  #+ " NODE = " + node.text.strip()
            #print node
            if node != root:
                for u in [node.getparent()]:
                    print u.text
                    for w in remove[node]:
                        if w in sim[u]:
                            #print "deleting " + w.text.strip() + " from " + u.text.strip()
                            del sim[u][w]
                            # decrement count
                            # count[(w.getparent(), u)] -= 1
                            for x in w.getparent():
                                count[(x, u)] -= 1
                                # remove[u] could not exist
                                if count[(x, u)] == 0:
                                    if u in remove:
                                        remove[u].update({x: nodes[x]})
                                    else:
                                        remove[u] = {x: nodes[x]}
            oldsim[node] = sim[node]
            del remove[node]
            #print len(remove)
            c3 += 1
        c2 += 1
    ##print_sim(nodes, sim)
    return sim


def getcount(node, sim):
    # count(w'',u) =  post(w'') intersection sim(u)
    # we computer count(node, u) for all u given node
    c = []
    count = {}
    # for every simulator set with
    for u in sim:
        # p = post(node)
        if len(node) == 0:
            count[(node, u)] = 0
        else:
            for p in node:
                try:
                    x = sim[u][p]
                    c.append(x)
                except KeyError:
                    # print "getcountkeyerror"
                    pass
            count[(node, u)] = len(c)
    return count


def pre(nodelist, nodes):
    res = {}
    for n in nodelist:
        x = n.getparent()
        if x is not None:
            res[x] = nodes[x]
    # res = {n.getparent(): nodelist[n] for n in nodelist if n.getparent() is not None}
    return res


def print_sim(nodes, sim):
    for x in nodes:
        #print 'simulators of node ' + x.text.strip() + ':\n'
        for y in sim[x]:
            print y.text.strip() + '\n'


naif('ciao.xml')