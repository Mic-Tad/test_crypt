class Node:
    value=None
    left_node=None
    right_node=None

    def __init__(self,value=None):
        self.value=value
    
    def add_right_node(self,node):
        self.right_node=node

    def add_left_node(self,node):
        self.left_node=node

    def has_left(self):
        if self.left_node:
            return True
        return False
   
    def set_value(self,value):
        self.value=value
        
    def has_right(self):
        if self.right_node:
            return True
        return False
    
    def __str__(self) -> str:
        return f'Node with value {self.value}'