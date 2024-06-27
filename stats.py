import random
import time
import math
import gc
import sys
from smt import SparseMerkleTree,smt_verify_proof,global_counter_smt
from imt import IndexedMerkleTree,verify_non_membership_proof,global_counter_imt,imt_verify_proof
from mt import MerkleTree,verify_proof,global_counter_bmt
from hashing import get_hash


N=35000

def total_size(obj, seen=None):
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    
    if isinstance(obj, dict):
        size += sum([total_size(v, seen) for v in obj.values()])
        size += sum([total_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += total_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([total_size(i, seen) for i in obj])
    
    return size

def generate_int(h=2**32,n=2**16+2*N):
    range_start = 1
    range_end = h
    num_unique_integers = n

    return random.sample(range(range_start, range_end), num_unique_integers)

def generate_str(h=2**32,n=2**16+2*N):
    range_start = 1
    range_end = h
    num_unique_integers = n

    return [str(i) for i in random.sample(range(range_start, range_end), num_unique_integers)]

if __name__=='__main__':
    n=2**int(math.log2(N-1)+1)
    
    h=int(math.log2(n)+1)
    d={'time create BMT:':[],
       'time create IMT:':[],
       'time add BMT:':[],
       'time add IMT:':[],
       'time add SMT:':[],
       'time get mem BMT:':[],
       'time get mem IMT:':[],
       'time get mem SMT:':[],
       'time get nonmem IMT:':[],
       'time get nonmem SMT:':[],
       'time verify mem BMT:':[],
       'time verify mem IMT:':[],
       'time verify mem SMT:':[],
       'time verify nonmem IMT:':[],
       'time verify nonmem SMT:':[],
       }
    
    d_o={'oper create BMT:':[],
       'oper create IMT:':[],
       'oper add BMT:':[],
       'oper add IMT:':[],
       'oper add SMT:':[],
       'oper get mem BMT:':[],
       'oper get mem IMT:':[],
       'oper get mem SMT:':[],
       'oper get nonmem IMT:':[],
       'oper get nonmem SMT:':[],
       'oper verify mem BMT:':[],
       'oper verify mem IMT:':[],
       'oper verify mem SMT:':[],
       'oper verify nonmem IMT:':[],
       'oper verify nonmem SMT:':[],
       }
    
    d_s={'size mem BMT:':[],
         'size mem IMT:':[],
         'size mem SMT:':[],
         'size nonmem IMT:':[],
         'size nonmem SMT:':[],
    }
    curr_counter_imt = {
    'hash of 2':0,
    'hash of 3':0,
    'element search and insertions':0,
    'comparisons/assigments/appending':0,
    'node creation':0
}
    curr_counter_bmt = {
    'hash of 2':0,
    'hash of 1':0,
    'element search and insertions':0,
    'comparisons/assigments/appending':0,
    'node creation':0
}
    curr_counter_smt = {
    'hash of 2':0,
    'hash of 1':0,
    'element search and insertions':0,
    'comparisons/assigments/appending':0,
    'node creation':0
}
    ar_base=generate_str()
    ar_int_base=generate_int()

    ar_to_add=ar_base[n:n+N]
    ar_non_mem=ar_base[n+N:n+2*N]

    ar_int_to_add=ar_int_base[n:n+N]
    ar_int_non_mem=ar_int_base[n+N:n+2*N]
    smt=SparseMerkleTree()

    t=time.time()
    mt=MerkleTree(ar_base[:n],h=h)
    dt=time.time()-t
    d['time create BMT:'].append(dt)
    d_o['oper create BMT:'].append([(k,v-curr_counter_bmt[k]) for k,v in global_counter_bmt.items()])
    for k,v in global_counter_bmt.items():
        curr_counter_bmt[k]=v

    t=time.time()
    imt=IndexedMerkleTree(arr=ar_int_base[:n],h=h)
    dt=time.time()-t
    d['time create IMT:'].append(dt)
    
    d_o['oper create IMT:'].append([(k,v-curr_counter_imt[k]) for k,v in global_counter_imt.items()])
    for k,v in global_counter_imt.items():
        curr_counter_imt[k]=v

    for i in range(N):
        mt.add_leaf(ar_to_add[i])
    dt=time.time()-t
    d['time add BMT:'].append(dt)
    d_o['oper add BMT:'].append([(k,v-curr_counter_bmt[k]) for k,v in global_counter_bmt.items()])
    for k,v in global_counter_bmt.items():
        curr_counter_bmt[k]=v
    t=time.time()
    for i in range(N):
        imt.add_leaf(ar_int_to_add[i])
    dt=time.time()-t
    d['time add IMT:'].append(dt)
    
    d_o['oper add IMT:'].append([(k,v-curr_counter_imt[k]) for k,v in global_counter_imt.items()])
    for k,v in global_counter_imt.items():
        curr_counter_imt[k]=v

    bmt_proofs=[]
    bmt_hashes=[]
    t=time.time()
    for i in range(N):
        el=mt.get_membership_proof(ar_to_add[i])
        bmt_proofs.append(el[0])
        bmt_hashes.append(el[1])
    dt=time.time()-t

    d['time get mem BMT:'].append(dt)
    d_s['size mem BMT:'].append(total_size(bmt_proofs))
    d_o['oper get mem BMT:'].append([(k,v-curr_counter_bmt[k]) for k,v in global_counter_bmt.items()])
    for k,v in global_counter_bmt.items():
        curr_counter_bmt[k]=v
    imt_proofs=[]
    imt_hashes=[]
    

    
    t=time.time()
    for i in range(N):
        el=imt.get_membership_proof(ar_int_to_add[i])
        imt_proofs.append(el[0])
        imt_hashes.append(el[1])
    dt=time.time()-t
    
    d['time get mem IMT:'].append(dt)
    d_s['size mem IMT:'].append(total_size(imt_proofs))
    
    d_o['oper get mem IMT:'].append([(k,v-curr_counter_imt[k]) for k,v in global_counter_imt.items()])
    for k,v in global_counter_imt.items():
        curr_counter_imt[k]=v


    bmt_verified=[]
    t=time.time()
    for hash,proof in zip(bmt_hashes,bmt_proofs):
        bmt_verified.append(verify_proof(hash, proof,mt.root))
    dt=time.time()-t

    d['time verify mem BMT:'].append(dt)
    d_o['oper verify mem BMT:'].append([(k,v-curr_counter_bmt[k]) for k,v in global_counter_bmt.items()])
    for k,v in global_counter_bmt.items():
        curr_counter_bmt[k]=v
    imt_verified=[]
    t=time.time()
    for hash,proof in zip(imt_hashes,imt_proofs):
        imt_verified.append(imt_verify_proof(hash, proof,imt.root))
    dt=time.time()-t
   
    d['time verify mem IMT:'].append(dt)
   
    d_o['oper verify mem IMT:'].append([(k,v-curr_counter_imt[k]) for k,v in global_counter_imt.items()])
    for k,v in global_counter_imt.items():
        curr_counter_imt[k]=v


    imt_non_proofs=[]
    imt_nul_hashes=[]

    t=time.time()
    for i in ar_int_non_mem:
        el=imt.get_non_membership_proof(i)
        imt_non_proofs.append((i,el[0],el[2]))
        imt_nul_hashes.append(el[1])
    dt=time.time()-t
    d['time get nonmem IMT:'].append(dt)
    d_s['size nonmem IMT:'].append(total_size(imt_non_proofs))
    
    d_o['oper get nonmem IMT:'].append([(k,v-curr_counter_imt[k]) for k,v in global_counter_imt.items()])
    for k,v in global_counter_imt.items():
        curr_counter_imt[k]=v

    imt_verified_non=[]

    t=time.time()
    for hash, proof in zip(imt_nul_hashes,imt_non_proofs):
        imt_verified_non.append(verify_non_membership_proof(hash,*proof,imt.root))
    dt=time.time()-t
    d['time verify nonmem IMT:'].append(dt)

    
    d_o['oper verify nonmem IMT:'].append([(k,v-curr_counter_imt[k]) for k,v in global_counter_imt.items()])
    for k,v in global_counter_imt.items():
        curr_counter_imt[k]=v

    del mt
    del imt
    collected = gc.collect()

    
    t=time.time()

    for i in ar_base[:n]:
        smt.add_leaf(i)
    dt=time.time()-t
    d['time add SMT:'].append(dt)
    d_o['oper add SMT:'].append([(k,v-curr_counter_smt[k]) for k,v in global_counter_smt.items()])
    for k,v in global_counter_smt.items():
        curr_counter_smt[k]=v
    smt_proofs=[]
    smt_hashes=[]
    t=time.time()
    for i in range(N):
        el=smt.get_membership_proof(ar_to_add[i])
        smt_proofs.append(el[0])
        smt_hashes.append(el[1])
    dt=time.time()-t

    d['time get mem SMT:'].append(dt)
    d_s['size mem SMT:'].append(total_size(smt_proofs))
    d_o['oper get mem SMT:'].append([(k,v-curr_counter_smt[k]) for k,v in global_counter_smt.items()])
    for k,v in global_counter_smt.items():
        curr_counter_smt[k]=v

    smt_verified=[]
    t=time.time()
    for hash,proof in zip(smt_hashes,smt_proofs):
        smt_verified.append(smt_verify_proof(hash, proof, smt.root))
    dt=time.time()-t
    d['time verify mem SMT:'].append(dt)
    d_o['oper verify mem SMT:'].append([(k,v-curr_counter_smt[k]) for k,v in global_counter_smt.items()])
    for k,v in global_counter_smt.items():
        curr_counter_smt[k]=v

    smt_non_proofs=[]


    t=time.time()
    for i in ar_non_mem:
        smt_non_proofs.append(smt.get_non_membership_proof(i))
    dt=time.time()-t
    d['time get nonmem SMT:'].append(dt)
    d_s['size nonmem SMT:'].append(total_size(smt_non_proofs))
    d_o['oper get nonmem SMT:'].append([(k,v-curr_counter_smt[k]) for k,v in global_counter_smt.items()])
    for k,v in global_counter_smt.items():
        curr_counter_smt[k]=v
    smt_verified_non=[]


    t=time.time()
    for proof in smt_non_proofs:
        hash=get_hash('')
        smt_verified_non.append(smt_verify_proof(hash,proof,smt.root))
    dt=time.time()-t
    d['time verify nonmem SMT:'].append(dt)
    d_o['oper verify nonmem SMT:'].append([(k,v-curr_counter_smt[k]) for k,v in global_counter_smt.items()])
    for k,v in global_counter_smt.items():
        curr_counter_smt[k]=v
        
    for k,v in d.items():
        print(N,k,v[0])

    for k,v in d_s.items():
        print(N,k,v[0])

    for k,v in d_o.items():
        print(k,v)


    