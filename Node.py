import uuid

#Class representing a node of the Process Tree or Attack Tree
class Node:
    
    def __init__(self, name, state, parentRelationship = ''):
        self.name = name
        self.state = state
        self.parentRelationship = parentRelationship
        self.children = []
        self.id = uuid.uuid4().hex
        self.value = 0
        
    def setChildren(self, child):
        self.children.append(child)
        
    def getChildren(self):
        return self.children
    
    def getName(self):
        return self.name
    
    def getID(self):
        return self.id
    
    def setID(self, id):
        self.id = id
    
    def getState(self):
        return self.state
    
    def getParentRelationship(self):
        return self.parentRelationship
    
    def printChildren(self):
        for child in self.children:
            print(child.getName())
            
    def setParentRelationship(self, parentRelationship):
        if parentRelationship == 'SEQUENCE':
            self.parentRelationship = 'SeqAnd'
        elif parentRelationship == 'PARALLEL':
            self.parentRelationship = 'And'
        elif parentRelationship == 'OR':
            self.parentRelationship = 'Or'
        elif parentRelationship == 'XOR':
            self.parentRelationship = 'Xor'
        else:
            print('Do not recognise operator')
    
    def get_leaf_nodes(self):
        leafs = []
        def _get_leaf_nodes( node):
            if node is not None:
                if len(node.getChildren()) == 0:
                    leafs.append(node)
                for n in node.getChildren():
                    _get_leaf_nodes(n)
        _get_leaf_nodes(self)
        return leafs

    def updateValue(self, value):
        self.value = value
    
    def getValue(self):
        return self.value
        
