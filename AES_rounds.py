import numpy as np
from arrays import *
from sbox import *
from MixTables import *

class AES_rounds:
    column_shuffle_matrix= [[0x02,0x03,0x01,0x01],[0x01,0x02,0x03,0x01],[0x01,0x01,0x02,0x03],[0x03,0x01,0x01,0x02]]
    inverse_column_shuffle_matrix= [[0x0e,0x0b,0x0d,0x09],[0x09,0x0e,0x0b,0x0d],[0x0d,0x09,0x0e,0x0b],[0x0b,0x0d,0x09,0x0e]]
    s_box=sbox.convertHexToString(sbox.sbox)
    inv_sbox=sbox.convertHexToString(sbox.invsbox)

    def SubstituteBytes(plain_text):
        substituted_text= [["" for _ in range(len(plain_text[0]))] for _ in range(len(plain_text))]
        s_box_index="0123456789ABCDEF"
        for i in range(len(substituted_text)):
            for j in range(len(substituted_text[0])):
                indexes=plain_text[i][j].upper()
                row=s_box_index.index(indexes[0])
                col=s_box_index.index(indexes[1])
                substituted_text[i][j]=AES_rounds.s_box[row][col]
        return substituted_text
    
    def ShiftRows(substituted_text):
        row_shifted_text= [["" for _ in range(len(substituted_text[0]))] for _ in range(len(substituted_text))]
        for i in range(len(substituted_text)):
            for j in range(len(substituted_text[0])):
                row_shifted_text[i][(j-i+4)%(4)]=substituted_text[i][j]
        return row_shifted_text
    
    def MixColumns(row_shifted_text):
        intermediate_output=[[0 for _ in range(4)]for _ in range(4)]
        integer_row_shifted_text=sbox.convertStringToHex(row_shifted_text)
        for i in range(4):
            mixrow=arrays.get_row(AES_rounds.column_shuffle_matrix,i)
            for j in range(4):
                mixcol=arrays.get_col(row_shifted_text,j)
                for k in range(4):
                    s_box_index="0123456789ABCDEF"
                    indexes=mixcol[k].upper()
                    row=s_box_index.index(indexes[0])
                    col=s_box_index.index(indexes[1])
                    if(mixrow[k]==0x02):
                        intermediate_output[i][j]=intermediate_output[i][j]^MixTables.mc2[row][col]
                    elif(mixrow[k]==0x03):
                        intermediate_output[i][j]=intermediate_output[i][j]^MixTables.mc3[row][col]
                    else:
                        intermediate_output[i][j]=intermediate_output[i][j]^int(mixcol[k],16)
        output=sbox.convertHexToString(intermediate_output)
        return output
    
    def AddRoundKey(column_mixed_text,key):
        intcolumn_mixed_text=np.array(sbox.convertStringToHex(column_mixed_text))
        intkey=sbox.convertStringToHex(key)
        intermediate_output=[[0 for _ in range(4)] for _ in range(4)]
        for i in range(len(key)):
            for j in range(len(key[0])):
                intermediate_output[i][j]=intkey[i][j]^intcolumn_mixed_text[i][j]
        output=sbox.convertHexToString(intermediate_output)
        return output
    
    def InverseSubstituteBytes(cipher_text):
        inverse_substituted_text=[["" for _ in range(len(cipher_text[0]))] for _ in range(len(cipher_text))]
        inv_s_box_index="0123456789ABCDEF"
        for i in range(len(inverse_substituted_text)):
            for j in range(len(inverse_substituted_text[0])):
                indexes=cipher_text[i][j].upper()
                row=inv_s_box_index.index(indexes[0])
                col=inv_s_box_index.index(indexes[1])
                inverse_substituted_text[i][j]=AES_rounds.inv_sbox[row][col]
        return inverse_substituted_text
    
    def InverseShiftRows(inverse_substituted_text):
        inverse_row_shifted_text=[["" for _ in range(len(inverse_substituted_text[0]))]for _ in range(len(inverse_substituted_text))]
        for i in range(len(inverse_substituted_text)):
            for j in range(len(inverse_substituted_text[0])):
                inverse_row_shifted_text[i][(j+i+4)%(4)]=inverse_substituted_text[i][j]
        return inverse_row_shifted_text
    
    def InverseMixColumns(Add_round_key_text):
        intermediate_output=[[0 for _ in range(4)]for _ in range(4)]
        integer_add_round_key=sbox.convertStringToHex(Add_round_key_text)

        for i in range(4):
            invmixrow=arrays.get_row(AES_rounds.inverse_column_shuffle_matrix,i)
            for j in range(4):
                invmixcol=arrays.get_col(Add_round_key_text,j)
                for k in range(4):
                    s_box_index="0123456789ABCDEF"
                    indexes=invmixcol[k].upper()
                    row=s_box_index.index(indexes[0])
                    col=s_box_index.index(indexes[1])
                    if(invmixrow[k]==0x0e):
                        intermediate_output[i][j]=intermediate_output[i][j]^MixTables.mc14[row][col]
                    elif(invmixrow[k]==0x0b):
                        intermediate_output[i][j]=intermediate_output[i][j]^MixTables.mc11[row][col]
                    elif(invmixrow[k]==0x0d):
                        intermediate_output[i][j]=intermediate_output[i][j]^MixTables.mc13[row][col]
                    else:
                        intermediate_output[i][j]=intermediate_output[i][j]^MixTables.mc9[row][col]
        output=sbox.convertHexToString(intermediate_output)
        return output

