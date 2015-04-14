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
        for n in node_index:
            for e in self.edges:
                if e[1]== n:
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
        #print c0
        g.add_node(node(i, n.tag))
        try:
            p = nodes.index(n.getparent())
        except ValueError:
            p = None
        if p is not None:
            g.add_edge((i,p))
            g.add_edge((p,i))
        for c in n:
            #figli
            j = nodes.index(c)
            g.add_edge((i,j))
            g.add_edge((j,i))
        c0 += 1
    return g


def naif(graph):
    sim = []
    for i,n in enumerate(graph.nodes):
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
    print "starting"
    for i, n in enumerate(graph.nodes):
        prevsim.insert(i, [t.num for t in graph.nodes])
        if len(graph.post(n))==0:
            sim.insert(i, set([m.num for m in graph.nodes if m.tag == n.tag]))
        else:
            sim.insert(i, set([m.num for m in graph.nodes if m.tag == n.tag and len(graph.post(n)) != 0]))
        remove.insert(i, graph.pre(prevsim[i]).difference(graph.pre(sim[i])))
    # compute count(w'',u)
    print "counting"
    count = []
    for n in graph.nodes:
        count.insert(n.num,[])
        for m in graph.nodes:
            c = len(graph.post(n.num).intersection(sim[m.num]))
            count[n.num].insert(m.num,c)
    #print count
    flag = True
    while flag:
        print "while"
        flag = False
        for v in graph.nodes:
            print "for v"
            for u in graph.pre([v.num]):
                print "for u " + str(u)
                for w in remove[v.num]:
                    print "for w"
                    if w in sim[u]:
                        print "IF"
                        sim[u].remove(w)
                        for x in graph.pre([w]):
                            print x
                            if count[x][u] == 0:
                                print "removing"
                                remove[u].add(x)
                                flag = True
            prevsim[v.num] = sim[v.num]
            remove[v.num].clear()
    print sim
    return sim

efficient(construct_tree('./ciao.xml'))
