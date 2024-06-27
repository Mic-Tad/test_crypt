import hashlib
import math
from node import Node
from hashing import get_hash,get_hash_from_two
from other import pad_list,pad_binary_number


global_counter_bmt = {
    'hash of 2':0,
    'hash of 1':0,
    'element search and insertions':0,
    'comparisons/assigments/appending':0,
    'node creation':0
}

class MerkleTree:
    root=None
    height=0
    def __init__(self, data_blocks, h=-1):
        global global_counter_bmt
        if h>=0:
            self.height=h
        else:
            self.height=int(math.log2(len(data_blocks)-1)+1)
        self.data_blocks=data_blocks
        db=pad_list(data_blocks,2**self.height)
        db=[get_hash(data) for data in db]
        self.leaves = [Node(data) for data in db]
        self.dict_leaves={data:i for i,data in enumerate(db)}
        
        self.root=self.compute_root(self.leaves)
        global_counter_bmt["hash of 1"]+=len(db)
        global_counter_bmt["node creation"]+=len(db)
        global_counter_bmt["comparisons/assigments/appending"]+=10
        
    def add_leaf(self, value):
        global global_counter_bmt

        hashed_val=get_hash(value)
        global_counter_bmt["hash of 1"]+=1
        self.data_blocks.append(hashed_val)
        self.leaves.append(Node(self.data_blocks[-1]))
        index=pad_binary_number(bin(len(self.data_blocks)-1)[2:],self.height)
        self.dict_leaves[self.data_blocks[-1]]=len(self.data_blocks)-1
        self.update(hashed_val,index,self.root)
        global_counter_bmt["comparisons/assigments/appending"]+=13
        global_counter_bmt["node creation"]+=1

    def update(self, value, index, curr_node:Node, i=0):
        global global_counter_bmt

        node_to_update=curr_node
        if i==self.height:
            node_to_update.set_value(value)
            global_counter_bmt["comparisons/assigments/appending"]+=1
            return
        
        if int(index[i]):
            curr_node=curr_node.right_node
        else:
            curr_node=curr_node.left_node
        
        i+=1
        self.update(value,index,curr_node,i)
        node_to_update.set_value(get_hash_from_two(node_to_update.left_node.value,node_to_update.right_node.value))
        global_counter_bmt["hash of 2"]+=1

        global_counter_bmt["comparisons/assigments/appending"]+=7

    def compute_root(self, leaves):
        global global_counter_bmt
        global_counter_bmt["comparisons/assigments/appending"]+=1
        nodes=leaves.copy()
        for _ in range(self.height):
            ar=[]
            for i in range(len(nodes)//2):
                node=Node(get_hash_from_two(nodes[i*2].value,nodes[i*2+1].value))
                node.add_right_node(nodes[i*2+1])
                node.add_left_node(nodes[i*2])
                global_counter_bmt['node creation']+=1
                global_counter_bmt['hash of 2']+=1
                ar.append(node)
                global_counter_bmt['comparisons/assigments/appending']+=6
            nodes=ar
            global_counter_bmt["comparisons/assigments/appending"]+=2
        
        return ar[0]


    def get_membership_proof(self, target_data):
        global global_counter_bmt

        target_hash = get_hash(target_data)
        global_counter_bmt["hash of 1"]+=1
        if target_hash not in self.dict_leaves:
            return None
        
        index = pad_binary_number(bin(self.dict_leaves[target_hash])[2:],self.height)

        proof = []
        curr_node:Node=self.root
        
        for i in index:
            if int(i):
                proof.append((curr_node.left_node.value,0))
                curr_node=curr_node.right_node
            else:
                proof.append((curr_node.right_node.value,1))
                curr_node=curr_node.left_node
            global_counter_bmt["comparisons/assigments/appending"]+=3
        global_counter_bmt["comparisons/assigments/appending"]+=9
        return list(reversed(proof)),target_hash
    

    def print_tree(self, node:Node, prefix="", is_left=True):
        
        if node is not None:
            print(prefix + ("└── " if is_left else "┌── ") + str(node.value)[:5])
            new_prefix = prefix + ("    " if is_left else "│   ")
            
            self.print_tree(node.right_node, new_prefix, False)
            
            self.print_tree(node.left_node, new_prefix, True)



def verify_proof(target_hash, proof, root):
    global global_counter_bmt
    current_hash = target_hash
    
    for sibling,side in proof:
        if side:
            current_hash=get_hash_from_two(current_hash,sibling)
        else:
            current_hash=get_hash_from_two(sibling,current_hash)
        global_counter_bmt['hash of 2']+=1
        global_counter_bmt['comparisons/assigments/appending']+=2
        
    global_counter_bmt['comparisons/assigments/appending']+=2
    return current_hash == root.value

if __name__=='__main__':
    data_blocks = ["a", "b", "c"]
    merkle_tree = MerkleTree(data_blocks,h=3)
    merkle_tree.print_tree(merkle_tree.root)

    merkle_tree.add_leaf('d')
    merkle_tree.print_tree(merkle_tree.root)

    merkle_tree.add_leaf('e')
    merkle_tree.print_tree(merkle_tree.root)

    proof,target_hash = merkle_tree.get_membership_proof("e")
    print("Merkle Root:", merkle_tree.root)
    print("Proof for 'a':", proof)

    is_valid = verify_proof(target_hash, proof,merkle_tree.root)
    print("Is the proof valid?", is_valid)
