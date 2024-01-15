import numpy as np
class arrays:
    def get_col(arr,col_no):
        a=np.array(arr)
        return a[:,col_no]

    def get_row(arr,row_no):
        a=np.array(arr)
        return a[row_no,:]
    
    def get_nibble_array(arr):
        nibble=[["" for _ in range(4)]for _ in range(4)]
        index=0
        for i in range(len(nibble)):
            for j in range(len(nibble[0])):
                nibble[j][i]=arr[index]
                index+=1
        return nibble
    
    def give_hex_array(input_hex):
        arr=["" for _ in range(16)]
        index=0
        for i in range(0,len(input_hex),2):
            part=input_hex[i:i+2]
            arr[index]=part
            index+=1
        return arr