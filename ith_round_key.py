
from sbox import *
from arrays import *
from convert import *

class ith_round_key:
    s_box = sbox.convertHexToString(sbox.sbox)
    round_constants = [
        [0x01, 0x00, 0x00, 0x00],
        [0x02, 0x00, 0x00, 0x00],
        [0x04, 0x00, 0x00, 0x00],
        [0x08, 0x00, 0x00, 0x00],
        [0x10, 0x00, 0x00, 0x00],
        [0x20, 0x00, 0x00, 0x00],
        [0x40, 0x00, 0x00, 0x00],
        [0x80, 0x00, 0x00, 0x00],
        [0x1b, 0x00, 0x00, 0x00],
        [0x36, 0x00, 0x00, 0x00]
    ]


    def generate_key(key, round_no):
        output_key = [[0 for _ in range(4)] for _ in range(4)]
        third_column = arrays.get_col(key, 3)
        shifted_word = ith_round_key.g(third_column)
        substituted = ith_round_key.substitute(shifted_word)
        g = [0 for _ in range(len(substituted))]
        constant = arrays.get_row(ith_round_key.round_constants, round_no - 1)
        for i in range(4):
            g[i] = substituted[i] ^ constant[i]
        integer_key = sbox.convertStringToHex(key)
        temp = g
        for i in range(len(key)):
            temp2 = arrays.get_col(integer_key, i)
            for j in range(len(key[0])):
                output_key[j][i] = temp[j] ^ temp2[j]
                temp[j] = output_key[j][i]
        o_key = sbox.convertHexToString(output_key)
        return o_key

    def g(word):
        temp = word[0]
        word[0] = word[1]
        word[1] = word[2]
        word[2] = word[3]
        word[3] = temp
        return word


    def substitute(input):
        output = [0] * len(input)
        s_box_index = "0123456789ABCDEF"
        for i in range(len(input)):
            indexes = input[i].upper()
            row = s_box_index.index(indexes[0])
            col = s_box_index.index(indexes[1])
            output[i] = sbox.sbox[row][col]
        return output

    def get_key(keys, round):
        output = [[0 for _ in range(4)] for _ in range(4)]
        output = keys[round]
        return output
    

