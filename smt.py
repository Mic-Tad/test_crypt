from node import Node
from hashing import get_hash_from_two,get_hash,get_default_hashes
from other import hex_to_bin,pad_binary_number

global_counter_smt = {
    'hash of 2':0,
    'hash of 1':0,
    'element search and insertions':0,
    'comparisons/assigments/appending':0,
    'node creation':0
}

class SparseMerkleTree:
    root=None
    h=0
    def_hashes=None
    def __init__(self,node=Node(),h=255) -> None:
        global global_counter_smt
        self.root=node
        self.h=h
        self.def_hashes=get_default_hashes(self.h)
        global_counter_smt['hash of 2']+=self.h
        global_counter_smt['hash of 1']+=1
        global_counter_smt['comparisons/assigments/appending']+=3

    def add_leaf(self,value):
        global global_counter_smt
        hash_val=get_hash(value)
        bin_val=pad_binary_number(hex_to_bin(hash_val),self.h)
        non_mem_proof=self.get_non_membership_proof(value)
        if not smt_verify_proof(hash_val, non_mem_proof,self.root):
            self.update(hash_val,bin_val,self.root)
        else:
            print('leaf alrady exists')
        global_counter_smt['hash of 1']+=1
        global_counter_smt['comparisons/assigments/appending']+=12


    def update(self, value, bin_value, curr_node:Node, i=0):
        global global_counter_smt
        node_to_update=curr_node

        if i==self.h:
            node_to_update.set_value(value)
            return
        
        if int(bin_value[i]):
            if not curr_node.has_right():
                curr_node.add_right_node(Node())
                curr_node.add_left_node(Node(self.def_hashes[self.h-i-1]))
                global_counter_smt['node creation']+=2
                global_counter_smt['comparisons/assigments/appending']+=3
            curr_node=curr_node.right_node
        else:
            if not curr_node.has_left():
                curr_node.add_left_node(Node())
                curr_node.add_right_node(Node(self.def_hashes[self.h-i-1]))
                global_counter_smt['node creation']+=2
                global_counter_smt['comparisons/assigments/appending']+=3
            curr_node=curr_node.left_node
        i+=1
        self.update(value,bin_value,curr_node,i)
        node_to_update.set_value(get_hash_from_two(node_to_update.left_node.value,node_to_update.right_node.value))
        global_counter_smt['hash of 2']+=1
        global_counter_smt['comparisons/assigments/appending']+=7

    def find_membership_proof(self, bin_value, curr_node:Node, i=0, proof=[]):
        global global_counter_smt

        if i==self.h:
            return
        
        if int(bin_value[i]):
            if not curr_node.has_right():
                curr_node.add_right_node(Node(self.def_hashes[self.h-i-1]))
                curr_node.add_left_node(Node(self.def_hashes[self.h-i-1]))
                global_counter_smt['node creation']+=2
                global_counter_smt['comparisons/assigments/appending']+=4
            proof.append((curr_node.left_node.value,0))
            curr_node=curr_node.right_node
        else:
            if not curr_node.has_left():
                curr_node.add_left_node(Node(self.def_hashes[self.h-i-1]))
                curr_node.add_right_node(Node(self.def_hashes[self.h-i-1]))
                global_counter_smt['node creation']+=2
                global_counter_smt['comparisons/assigments/appending']+=4
            proof.append((curr_node.right_node.value,1))
            curr_node=curr_node.left_node
        i+=1
        self.find_membership_proof(bin_value,curr_node,i,proof=proof)
        global_counter_smt['comparisons/assigments/appending']+=4



    def get_membership_proof(self, target_data):
        global global_counter_smt

        hash_val=get_hash(target_data)
        bin_val=pad_binary_number(hex_to_bin(hash_val),self.h)
        proof=[]
        self.find_membership_proof(bin_val, self.root, proof=proof)
        global_counter_smt['hash of 1']+=1
        global_counter_smt['comparisons/assigments/appending']+=10
        return list(reversed(proof)),hash_val
        
    def get_non_membership_proof(self, target_data):
        hash_val=get_hash(target_data)
        bin_val=pad_binary_number(hex_to_bin(hash_val),self.h)
        
        proof=[]
        self.find_non_membership_proof(bin_val, self.root, proof=proof)
        global_counter_smt['hash of 1']+=1
        global_counter_smt['comparisons/assigments/appending']+=10
        return list(reversed(proof))
    
    def find_non_membership_proof(self, bin_value, curr_node:Node, i=0, proof=[]):
        global global_counter_smt

        if i==self.h:
            return
        if not curr_node.has_right() or not curr_node.has_left():
            curr_node.add_right_node(Node(self.def_hashes[self.h-i-1]))
            curr_node.add_left_node(Node(self.def_hashes[self.h-i-1]))
        

        if int(bin_value[i]):
            proof.append((curr_node.left_node.value,0))
            curr_node=curr_node.right_node
        else:
            proof.append((curr_node.right_node.value,1))
            curr_node=curr_node.left_node
        i+=1
        self.find_non_membership_proof(bin_value,curr_node,i,proof=proof)
        global_counter_smt['comparisons/assigments/appending']+=7

    def print_tree(self, node:Node, prefix="", is_left=True):
        
        if node is not None:
            print(prefix + ("└── " if is_left else "┌── ") + str(node.value)[:5])
            new_prefix = prefix + ("    " if is_left else "│   ")
            
            self.print_tree(node.right_node, new_prefix, False)
            
            self.print_tree(node.left_node, new_prefix, True)


def smt_verify_proof(target_hash, proof, root):
    global global_counter_smt
    
    current_hash = target_hash
    
    for sibling,side in proof:
        if side:
            current_hash=get_hash_from_two(current_hash,sibling)
        else:
            current_hash=get_hash_from_two(sibling,current_hash)
        global_counter_smt['hash of 2']+=1
        global_counter_smt['comparisons/assigments/appending']+=2
        
    global_counter_smt['comparisons/assigments/appending']+=2
    return current_hash == root.value

if __name__=='__main__':
    smt=SparseMerkleTree(h=3)
    a,b,c='0','1','12231'
    smt.add_leaf(a)
    smt.add_leaf(b)
    
    smt.add_leaf(c)
    
    pr,hash_a=smt.get_membership_proof(a)
    smt.print_tree(smt.root)
    pr,hash_c=smt.get_membership_proof(c)
    print(smt_verify_proof(hash_c,pr,smt.root))
    d='5'
    npr=smt.get_non_membership_proof(d)
    
    print(smt_verify_proof(get_hash(''),npr,smt.root))