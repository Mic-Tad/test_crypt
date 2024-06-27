import hashlib

def get_default_hashes(n=256):
    s=b''
    arr=[]
    for _ in range(n):
        hash_s=hashlib.sha256(s).hexdigest()
        s=bytes.fromhex(hash_s)+bytes.fromhex(hash_s)
        arr.append(hash_s)
    return arr

def get_hex_hash_of_bytes(val):
    return hashlib.sha256(val).hexdigest()

def get_hash(value):
    return get_hex_hash_of_bytes(value.encode('utf-8'))

def get_hash_from_two(val1,val2):
    return get_hex_hash_of_bytes(bytes.fromhex(val1)+bytes.fromhex(val2))

def get_hash_from_three(val1,val2,val3):
    val1=str(val1).encode('utf-8')
    val2=str(val2).encode('utf-8')
    val3=str(val3).encode('utf-8')
    return get_hex_hash_of_bytes(val1+val2+val3)

def get_default_triple_hashes(n=32):
    s=[0,0,0]
    hash_s=get_hash_from_three(*s)
    print(hash_s)
    arr=[]
    for h in range(n+1):
        if h >0:
            hash_s=hashlib.sha256(s).hexdigest()
        s=bytes.fromhex(hash_s)+bytes.fromhex(hash_s)
        if h==0:
            continue
        arr.append(hash_s)
    return arr
if __name__=='__main__':

    get_default_triple_hashes()