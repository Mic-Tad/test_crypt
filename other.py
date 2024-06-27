def hex_to_bin(val):
    scale = 16 
    num_of_bits = 8

    return bin(int(val, scale))[2:].zfill(num_of_bits)

def pad_binary_number(bin_num, h):
    num_zeros = h - len(bin_num)
    padded_bin_num = '0' * num_zeros + bin_num
    return padded_bin_num

def pad_list(arr,n):
    return arr+['' for _ in range(n-len(arr))]

def pad_triple_list(arr,n):
    return arr+[[0,0,0] for _ in range(n-len(arr))]