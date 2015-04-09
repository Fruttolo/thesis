from lxml import etree
import sys

def naif(document):
	
	#open the XML file
	tree = etree.parse(document)
	
	#get the root node
	root = tree.getroot()
	
	#get all nodes in the tree
	nodes = [node for node in root.iterdescendants()]
	#initialize simulators
	sim = {node : tree.findall('.//'+node.tag) for node in nodes}
	#computer forward simulation 
	sim = forwardSimulation(nodes,sim)
	#TODO: forward simulation
	return sim

def forwardSimulation(nodes,sim):
	#for each node u verify Forward Simulation
	for u in nodes:
		# v = post(u)
		for v in u:
			#w = sim[v]
			if u!=None:
				for w in sim[u]:
					#intersection between post(w) and sim(v)
					if len([val for val in w if val in sim[v]])==0:
						#remove w from the simulator of u
						sim[u].remove(w)
	return sim


def efficient(document):
	#open the XML file
	tree = etree.parse(document)
	#get the root node
	root = tree.getroot()
	#get all nodes in the tree
	nodes = [node for node in root.iterdescendants()]
	#initilize sets
	sim = {}
	sim[root] = root
	oldsim = {}
	#oldsim = {node: nodes for node in nodes}
	remove = {}

	#initilize sim() and prevsim()
	for node in nodes:
		#prevsim(v)
		oldsim[node] = list(nodes)
		#print oldsim[node]
		#sim(v)
		if len(node) == 0:
			sim[node] = tree.findall('.//'+node.tag)
		else:
			sim[node] = [ n for n in tree.findall('.//'+node.tag) if len(node)!=0]
		#remove vector
		remove[node] = [val for val in pre(oldsim[node]) if val in pre(sim[node])]

	#implement 2D array as a tuple-indexed dictonary	
	count = getCount(nodes,sim)
	

	#F-Similarity Check
	#we store keys in remove only if remove(v)!=0, so when all remove(v) = 0 our dictonary is empty
	while len(remove)!=0:
		for node in remove:
			for u in node.getparent():
				for w in remove[node]:
					
					if w in sim[u]:
						sim[u].remove(w)
						#decrementa count
						count[(w.getparent,u)] -= 1
						for x in w.getparent():
							if count[(x,u)] == 0:
								if u in remove: remove[u].append(x)
								else: remove[u] = [x]
		oldsim[node] = sim[node]
		del remove[node]
	print_sim(nodes,sim)
	return sim




def getCount(nodes,sim):
	count = {}
	for a in nodes:
		for b in nodes:
			count[(a,b)] = len([val for val in a if val in sim[b]])
	return count

def pre(nodelist):
	res = [n.getparent() for n in nodelist]
	return res

def print_sim(nodes,sim):
	for x in nodes:
		print 'simulators of node ' + x.text.strip() + ':\n'
		for y in sim[x]:
			print y.text.strip() + '\n'


if __name__ == "__main__":
	doc = sys.argv[1]
	if sys.argv[2] == 0:
		naif(doc)
		print >>sys.stdout, "naif"
	if sys.argv[2] == 1:
		efficient(doc)
		print >>sys.stdout, "efficent"
