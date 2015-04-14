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
        print c0
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

                    #TODO: test for emptyness

def naif(graph):
    sim = []
    for i,n in enumerate(graph.nodes):
        sim.insert(i,set([m.num for m in graph.nodes if m.tag == n.tag]))
    flag = True
    #c = 0
    #print "begin while"
    while flag:
        #print c
        #c += 1
        flag = False
        for u in graph.nodes:
            for v in graph.post(u.num):
                rem = set([])
                for w in sim[u.num]:
                    if len(graph.post(w).intersection(sim[v]))==0:
                        #print str(u.num) +" "+ str(v) +" "+ str(w) + " removed"
                        #sim[u.num].remove(w)
                        rem.add(w)
                        flag = True
                    #else:
                         #print str(u.num) +" "+ str(v) +" "+ str(w)
                sim[u.num] = sim[u.num].difference(rem)
    return sim

naif(construct_tree('/home/luca/tesi/ciao.xml'))
