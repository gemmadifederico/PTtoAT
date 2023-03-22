#update the values in nodes
def dfs(element, node):
    if node == None:
        return
    
    if node.getName() == element:
        node.updateValue(1)
        return
    
    for child in node.getChildren():
        dfs(element, child)
        
    return

#clear the values in nodes
def clear(node):
    if node == None:
        return
    
    for child in node.getChildren():
        clear(child)
    
    node.updateValue(0)

    return

#Check the value of the node
def check(node):
    
    if len(node.getChildren()) == 0:
        return 
    
    relation = node.getChildren()[0].getParentRelationship()
    value = 0

    for child in node.getChildren():
        check(child)
        value = value + child.getValue()

    if relation == 'disjunction':
        if value > 0:
            node.updateValue(1)
    
    if relation == 'conjunction':
        if value == len(node.getChildren()):
            node.updateValue(1)
    return

# Replay the traces on the Attack Tree
def replay(trace):
    for element in trace:
        dfs(element, root)
    check(root)
    return root.getValue()