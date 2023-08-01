import copy
import graphviz
import uuid
import Node as nd
import xml.etree.cElementTree as ET
from IPython import display
import pm4py
import sys


count = 0
# Translate the Process Tree into an Attack Tree
def P2T(node):
	global count
    # If our current node is an operator
	if not node.operator == None:
		print(node.operator)
		#Create the new node
		parent = nd.Node('tau' + str(count), 'non-observable')
		#DFS on all children
		for child in node.children:
				count = count + 1
				new = P2T(child)
				if new == None:
					continue

			    #Set the relationship(SAND, AND, OR, XOR)
			    #SEQUENCE -> SAND
			    #PARALLEL -> AND
			    #OR       -> OR
			    #XOR      -> XOR
			    #LOOP     -> ?
				new.setParentRelationship(node.operator.name)
				if new.getName() != None:
					attckTreebranch = copy.deepcopy(new)
					attckTreebranch.setID(uuid.uuid4().hex)
					parent.setChildren(attckTreebranch)

		#newp = copy.deepcopy(parent)
		#newp.setID(uuid.uuid4().hex)
		return copy.deepcopy(parent)

    #If our current node is not an operator
	elif node.label != '0':
		print(node.label)
		return nd.Node(node.label, 'observable')

# Convert to xml
# Save the attack tree (bfs access)
def AT2xml(node, filepath):
	tree = ET.Element("tree")
	if node is None:
		return
	queue = [node]
	while len(queue) > 0:
		cur_node = queue.pop(0)
		ET.SubElement(tree, "root", name =cur_node.getName(), state =  "observable", id = cur_node.getID())
		for child in cur_node.getChildren():
			ET.SubElement(tree, "child", name = child.getName(), state =  "observable", parentRelationship = child.getParentRelationship(), parent = cur_node.getID(), id=child.getID())
			queue.append(child)
	ET.ElementTree(tree).write(filepath+".xml")

def Tree2RisQFLan(root, file):
	with open(file, 'w') as file:
		file.write('begin model Empty \n// This is an empty RisQFLan file \n// Fill all the blocks to model your scenario name \n//Here we specify variables and their initial values. This is convenient to express constraints and to ease the analysis\nbegin variables \nend variables \n// Here we specify all the things that can go wrong\n// In particular successful actions of attacker\nbegin attack nodes\n')
		queue = [root]
		while len(queue) > 0:
			cur_node = queue.pop(0)
			file.write(cur_node.getName() + '\n')
			for child in cur_node.getChildren():
				queue.append(child)
		file.write('end attack nodes\n')
		file.write('// Reactive defensive actions\nbegin defense nodes\nend defense nodes\n// Permanent defensive actions\nbegin countermeasure nodes\nend countermeasure nodes\n// The diagram specifies how defensive actions and attacker actions relate to each other\nbegin attack diagram\n')
		queue = [root]
		while len(queue) > 0:
			cur_node = queue.pop(0)
			if len(cur_node.getChildren()) == 0:
				continue
			file.write(cur_node.getName())
			flag = False
			for child in cur_node.getChildren():
				if(not flag):
					operator = child.getParentRelationship()
					if operator == 'SeqAnd':
						file.write(' -OAND-> [')
					elif operator == 'And':
						file.write(' -AND-> {')
					elif operator == 'Or':
						file.write(' -> {')
					elif operator == 'Xor':
						file.write(' -K1-> {')
					else:
						print('no operator')

					flag = True
				else:
					file.write(', ')
				file.write(child.getName())
				queue.append(child)
			if(flag):
				if operator == 'SeqAnd':
					file.write(']\n')
				elif operator == 'And':
					file.write('}\n')
				elif operator == 'Or':
					file.write('}\n')
				elif operator == 'Xor':
					file.write('}\n')
				else:
					continue
		file.write('end attack diagram\n')
		file.write('// Here we can specify classes of attackers with probabilistic behavior\nbegin attackers\n attacker1\nend attackers\n// The effectiveness of a defence depends on the class of attacker and the attack action\nbegin defense effectiveness\nend defense effectiveness\n// Attacks may not be detected \nbegin attack detection rates\nend attack detection rates\n// Attributes of attacks are specified here\nbegin attributes\nend attributes\n// One can here impose additional constraints on the attacker, e.g. based on his budget\nbegin quantitative constraints\nend quantitative constraints\n//Domain-specific actions executed by the attacker\nbegin actions\nend actions\n//Constraints on the execution of actions\nbegin action constraints\nend action constraints\n//The probabilistic behaviour of each attacker\nbegin attacker behaviour\nbegin attack attacker\n= attacker1\nstates = state1\ntransitions = \n	state1 - (succ(' + root.getName() +'),1.0) -> state1\nend attack \nend attacker behaviour\n// Here we specify the attacker we want to consider\nbegin init\nattacker1\nend init\n//Finally, you can specify 3 types of analysis\n//analysis: statistical analysis of quantitative properties\n//exportDTMC: export the state space of the model (if finite) in a discrete time Markov chain in the format supported by the model checkers PRISM and STORM\n//simulate: perform a simulation to debug your model\n\n// In this particular case we are just interested in the likelihood of success of each attack\nbegin analysis\n   query = eval from 1 to 100 by 20 :\n    {'     + root.getName() +    '\n}\n    // Statistical confidence\n    default delta = 0.1\n    alpha = 0.1\n    // Parallelism to be exploited in the machine \n    parallelism = 1\nend analysis\nend model')

# Here we deal directly with a process tree
def main2(filei, fileo):
    # import the process tree
	ProcessTree = pm4py.objects.process_tree.importer.importer.apply(filei)

	#Translate to Attack Tree
	AttackTree = P2T(ProcessTree)
	print("Attack tree translated!")

	#Write Attck Tree to xml
	AT2xml(AttackTree, fileo)

	#Convert to RISQFlan code
	Tree2RisQFLan(AttackTree, fileo + ".bbt")
	print("Attack tree converted to RISQFlan code!")

# Here we take as input a xes file, we derive the process tree and then we translate it into an attack tree 
def main(filexes, fileo):
	# import the log file and derive a process tree
	log = pm4py.read_xes(filexes+".xes")
	ProcessTree = pm4py.discover_process_tree_inductive(log)
    
    # import the process tree
	# ProcessTree = pm4py.objects.process_tree.importer.importer.apply(filei)

	#Translate to Attack Tree
	AttackTree = P2T(ProcessTree)
	print("Attack tree translated!")

	#Write Attck Tree to xml
	AT2xml(AttackTree, fileo)

	#Convert to RISQFlan code
	Tree2RisQFLan(AttackTree, fileo + ".bbt")
	print("Attack tree converted to RISQFlan code!")

if __name__ == "__main__":
    filei = sys.argv[1]
    # filei = "ptree.xml"
    fileo = sys.argv[2]
    # fileo = "atree"
    print("Starting conversion..")
    print("Process tree file:", filei)
    print("Attack tree file:", fileo + ".xml")
    main(filei, fileo)
    print("Conversion completed!")
