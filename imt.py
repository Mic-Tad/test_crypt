from node import Node
from other import pad_binary_number,pad_triple_list
from hashing import get_hash_from_two,get_hash_from_three,get_default_triple_hashes,get_hash
from sortedcontainers import SortedList

global_counter_imt = {
    'hash of 2':0,
    'hash of 3':0,
    'element search and insertions':0,
    'comparisons/assigments/appending':0,
    'node creation':0
}

class IndexedMerkleTree:
    root=None
    h=0
    array=[]
    sorted_ar=SortedList()
    hash_val_dict=dict()
    val_dict=dict()

    def __init__(self,node=Node(),h=32,arr=[]) -> None:
        global global_counter_imt
        self.root=node
        self.h=h
        self.array.append([0,0,0])
        self.sorted_ar.add(0)
        self.hash_val_dict[get_hash_from_three(*self.array[0])]=0
        self.val_dict[self.array[0][0]]=0
        if len(arr)==0:
            pass
        else:
            self.add_array(arr)
            self.root=self.compute_root()
        global_counter_imt['comparisons/assigments/appending']+=8

    def add_array(self,arr):
        global global_counter_imt
        for i in arr:
            el=self.find_nullifier(i)
            ind=self.val_dict[el]
            hash_prenull=get_hash_from_three(*self.array[ind])
            
            item_to_append=[i,self.array[ind][1],self.array[ind][2]]
            item_to_change=[self.array[ind][0],len(self.array),i]
            self.sorted_ar.add(i)
            self.array.append(item_to_append)
            self.array[ind]=item_to_change
            hash_val=get_hash_from_three(*item_to_append)
            hash_null=get_hash_from_three(*item_to_change)
            self.val_dict[i]=len(self.array)-1
            self.hash_val_dict[hash_val]=len(self.array)-1
            del self.hash_val_dict[hash_prenull]
            self.hash_val_dict[hash_null]=ind
            global_counter_imt['hash of 3']+=3
            global_counter_imt['element search and insertions']+=1
            global_counter_imt['comparisons/assigments/appending']+=15
            

    def compute_root(self):
        global global_counter_imt
        nodes=[Node(get_hash_from_three(*i)) for i in pad_triple_list(self.array,2**(self.h))]
        global_counter_imt['hash of 3']+=len(nodes)
        global_counter_imt['node creation']+=len(nodes)
        for _ in range(self.h):
            ar=[]
            for i in range(len(nodes)//2):
                node=Node(get_hash_from_two(nodes[i*2].value,nodes[i*2+1].value))
                node.add_right_node(nodes[i*2+1])
                node.add_left_node(nodes[i*2])
                global_counter_imt['node creation']+=1
                global_counter_imt['hash of 2']+=1
                ar.append(node)
                global_counter_imt['comparisons/assigments/appending']+=6
            nodes=ar
            global_counter_imt['comparisons/assigments/appending']+=2
        global_counter_imt['comparisons/assigments/appending']+=1
        return ar[0]
        

    """def compute_def_root(self):
        default_hashes=get_default_triple_hashes(n=self.h)
        
        hash_zero=get_hash_from_three(*[0,0,0])
        
        nodes=[Node(hash_zero) for _ in range(2**self.h)]
        for k in range(self.h):
            ar=[]
            for i in range(len(nodes)//2):
                node=Node(default_hashes[k])
                node.add_right_node(nodes[i*2+1])
                node.add_left_node(nodes[i*2])
                ar.append(node)
            nodes=ar
        return ar[0]"""

    def find_nullifier(self, value):
        global global_counter_imt

        index = self.sorted_ar.bisect_left(value)
        global_counter_imt['element search and insertions']+=1
        global_counter_imt['comparisons/assigments/appending']+=3
        if index<len(self.sorted_ar)-1 and self.sorted_ar[index]==value:
            return None
        if index > 0:
            global_counter_imt['comparisons/assigments/appending']+=2
            return self.sorted_ar[index - 1]
        return None
    
    def add_leaf(self,value):
        global global_counter_imt

        el=self.find_nullifier(value)
        global_counter_imt['element search and insertions']+=1

        if el is None:
            print('not Found')
            return
        ind=self.val_dict[el]
        
        mem_proof, hash_prenull=self.get_membership_proof(el)
        global_counter_imt['comparisons/assigments/appending']+=4
        if imt_verify_proof(hash_prenull, mem_proof,self.root):
            item_to_append=[value,self.array[ind][1],self.array[ind][2]]
            self.array.append(item_to_append)
            self.sorted_ar.add(value)
            
            item_to_change=[self.array[ind][0],len(self.array)-1,value]
            self.array[ind]=item_to_change
            hash_val=get_hash_from_three(*item_to_append)
            hash_null=get_hash_from_three(*item_to_change)
            self.hash_val_dict[hash_val]=len(self.array)-1
            del self.hash_val_dict[hash_prenull]
            self.hash_val_dict[hash_null]=ind
            self.val_dict[value]=len(self.array)-1
            global_counter_imt['hash of 3']+=3
            global_counter_imt['element search and insertions']+=1
            ind1 = pad_binary_number(bin(ind)[2:],self.h)
            ind2 = pad_binary_number(bin(item_to_change[1])[2:],self.h)
            self.update(hash_null,ind1,self.root)
            self.update(hash_val,ind2,self.root)
            global_counter_imt['comparisons/assigments/appending']+=17+5*2

        else:
            print('Low nullifier is not in the tree')
            return
        
    def update(self, value, index, curr_node:Node, i=0):
        global global_counter_imt

        node_to_update=curr_node
        if i==self.h:
            node_to_update.set_value(value)
            global_counter_imt['comparisons/assigments/appending']+=2
            return
        
        if int(index[i]):
            curr_node=curr_node.right_node
        else:
            curr_node=curr_node.left_node
            
        
        i+=1
        self.update(value,index,curr_node,i)
        node_to_update.set_value(get_hash_from_two(node_to_update.left_node.value,node_to_update.right_node.value))
        global_counter_imt['hash of 2']+=1
        global_counter_imt['comparisons/assigments/appending']+=4

    def get_membership_proof(self,value):
        global global_counter_imt

        ind=self.val_dict[value]
        hash_value=get_hash_from_three(*self.array[ind])
        global_counter_imt['hash of 3']+=1
        if hash_value not in self.hash_val_dict:
            return None
        
        index = pad_binary_number(bin(self.hash_val_dict[hash_value])[2:],self.h)

        proof = []
        curr_node:Node=self.root
        
        for i in index:
            if int(i):
                proof.append((curr_node.left_node.value,0))
                curr_node=curr_node.right_node
            else:
                proof.append((curr_node.right_node.value,1))
                curr_node=curr_node.left_node
            global_counter_imt['comparisons/assigments/appending']+=3
        global_counter_imt['comparisons/assigments/appending']+=14
        return list(reversed(proof)), hash_value
        
    def get_non_membership_proof(self, value):
        global global_counter_imt
        el=self.find_nullifier(value)
        global_counter_imt['element search and insertions']+=1
        ind=self.val_dict[el]
        mem_proof,hash_null=self.get_membership_proof(el)
        global_counter_imt['comparisons/assigments/appending']+=4
        return self.array[ind],hash_null,mem_proof

        

    def print_tree(self, node:Node, prefix="", is_left=True):
        
        if node is not None:
            print(prefix + ("└── " if is_left else "┌── ") + str(node.value)[:5])
            new_prefix = prefix + ("    " if is_left else "│   ")
            
            self.print_tree(node.right_node, new_prefix, False)
            
            self.print_tree(node.left_node, new_prefix, True)




def verify_non_membership_proof(hash_null, value, nullifier,  mem_proof,root):
    global global_counter_imt
    
    
    if imt_verify_proof(hash_null, mem_proof,root):

        global_counter_imt['comparisons/assigments/appending']+=7
        return nullifier[0]<value and (nullifier[2]>value or nullifier[2]==0)
    return False
        
def imt_verify_proof(target_hash, proof, root):
    current_hash = target_hash
    
    for sibling,side in proof:
        if side:
            current_hash=get_hash_from_two(current_hash,sibling)
        else:
            current_hash=get_hash_from_two(sibling,current_hash)
        global_counter_imt['hash of 2']+=1
        global_counter_imt['comparisons/assigments/appending']+=2
        
    global_counter_imt['comparisons/assigments/appending']+=2
    return current_hash == root.value

if __name__=='__main__':

    imt1=IndexedMerkleTree(arr=[5,2,3,],h=4)
    imt1.print_tree(imt1.root)
    a,b,c=7,9,12231
    imt1.add_leaf(a)
    imt1.add_leaf(b)
    imt1.print_tree(imt1.root)
    pr1,hash_b=imt1.get_membership_proof(b)
    
    print(imt_verify_proof(hash_b,pr1,imt1.root))
    """smt=IndexedMerkleTree(h=4)
    a,b,c=2,1,12231
    smt.add_leaf(a)
    smt.add_leaf(b)
    
    smt.add_leaf(c)
    
    pr,hash_a=smt.get_membership_proof(a)
    
    pr1,hash_c=smt.get_membership_proof(c)
    
    print(smt.verify_membership_proof(hash_c,pr1,smt.root))
    d=5
    nullifier,hash_null,npr=smt.get_non_membership_proof(d)
    smt.add_leaf(b)
    
    smt.print_tree(smt.root)
    

    print(smt.verify_non_membership_proof(hash_null,d,nullifier,npr))"""