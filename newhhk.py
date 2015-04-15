from lxml import etree


class graph:
    def __init__(self):
        self.nodes = []
        self.edges = set([])

    def add_node(self,node):
        self.nodes.insert(node.num,node)

    def add_edge(self,tuple):
        self.edges.update([tuple])

    def post(self,node_index):
        p = []
        for e in self.edges:
            if e[0] == node_index:
                p.append(e[1])
        return set(p)

    def pre(self,node_index):
        p = []
        for i in node_index:
            for e in self.edges:
                if e[1] == i:
                    p.append(e[0])
        return set(p)

    def __str__(self):
        print str(self.edges) + "\n"
        for n in self.nodes:
            print n
        return "\n"

class node:
    def __init__(self,num,tag):
        self.num = num
        self.tag = tag

    def __str__(self):
        return "nodo " + str(self.num) + " |tag: " + str(self.tag)


def construct_tree(document):
    g = graph()
    root = etree.parse(document).getroot()
    nodes = [n for n in root.iter()]
    c0 = 0
    for i,n in enumerate(nodes):
        print "construction " + str(c0)
        g.add_node(node(i, n.tag))
        try:
            p = nodes.index(n.getparent())
        except ValueError:
            p = None
        if p is not None:
            g.add_edge((p,i))
            #g.add_edge((p,i))
        for c in n:
            #figli
            j = nodes.index(c)
            g.add_edge((i,j))
            #g.add_edge((j,i))
        c0 += 1
    return g


def naif(graph):
    sim = []
    for i,n in enumerate(graph.nodes):
        print "starting " + str(i)
        sim.insert(i,set([m.num for m in graph.nodes if m.tag == n.tag]))
    flag = True
    c = 0
    print "begin while"
    while flag:
        print c
        c += 1
        flag = False
        for u in graph.nodes:
            for v in graph.post(u.num):
                rem = set([])
                for w in sim[u.num]:
                    if len(graph.post(w).intersection(sim[v]))==0:
                        print str(u.num) +" "+ str(v) +" "+ str(w) + " removed"
                        #sim[u.num].remove(w)
                        rem.add(w)
                        flag = True
                    else:
                         print str(u.num) +" "+ str(v) +" "+ str(w)
                sim[u.num] = sim[u.num].difference(rem)
    return sim


def efficient(graph):
    sim = []
    prevsim = []
    remove = []
    for i, n in enumerate(graph.nodes):
        print "starting " + str(i)
        prevsim.insert(i, range(len(graph.nodes)))
        if not graph.post(n):
            sim.insert(i, set([m.num for m in graph.nodes if m.tag == n.tag]))
        else:
            sim.insert(i, set([m.num for m in graph.nodes if m.tag == n.tag and graph.post(n)]))
        print "remove " + str(i)
        #print graph.edges
        #print graph.pre(sim[i])
        #print prevsim[i]
        remove.insert(i, graph.pre(prevsim[i]).difference(graph.pre(sim[i])))
        #print remove[i]   

    # compute count(w'',u)
    print "counting"
    count = []
    for n in graph.nodes:
        count.insert(n.num,[])
        for m in graph.nodes:
            print n.num, m.num
            c = len(graph.post(n.num).intersection(sim[m.num]))
            count[n.num].insert(m.num,c)
    #print count
    flag = True
    c = 0
    d = 0
    while flag:
        print "while " + str(c)
        c += 1
        flag = False
        for v in graph.nodes:
            print "for v " + str(v.num)
            if remove[v.num]:
                for u in graph.pre([v.num]):
                    #print "for u " + str(u)
                    #print remove[v.num]
                    for w in remove[v.num]:
                        #print "for w"
                        #print str(d)
                        d += 1
                        if w in sim[u]:
                            print "IF"
                            sim[u].remove(w)
                            for x in graph.pre([w]):
                                #print x
                                if count[x][u] == 0:
                                    print "removing"
                                    remove[u].add(x)
                                    count[x][u] -= 1
                                    flag = True
                prevsim[v.num] = sim[v.num]
                remove[v.num].clear()
    #print sim
    return sim

x = naif(construct_tree('ciao.xml'))
y = efficient(construct_tree('ciao.xml'))

print x == y
