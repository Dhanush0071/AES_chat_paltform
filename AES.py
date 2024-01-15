from ith_round_key import *
from convert import *
from arrays import *
from AES_rounds import *

# input_str = input("enter the format, format should be like <message file directory> <cipher text file directory> <plaintext file directory> : ")
# input_list = input_str.split()

# if len(input_list) < 3:
#     print("Please provide three strings separated by spaces.")
# else:
#     string1, string2, string3 = input_list[:3]


# input_file = string1
# cipher_file= string2
# output_file=string3

# with open(input_file, 'r') as f:
#     content = f.read()
# x=content.split("\n")
# output=""
# for i in x:
#     output+=i
# # Split the content into 16-character lines
# lines = [output[i:i+16] for i in range(0, len(output), 16)]

# # Calculate the number of spaces needed to pad the last line to 16 characters
# last_line = lines[-1]
# padding_spaces = 16 - len(last_line)
# if padding_spaces > 0:
#     lines[-1] = last_line + ' ' * padding_spaces

# key="Thats my Kung Fu"

def encrypt(msgs,key):
    with open("cipher_text.txt", 'w') as f:
        for i in range(len(msgs)):
            #print(msgs[i])
            inp=msgs[i]
            inp_hex=convert.textToHex(inp)
            key_hex=convert.textToHex(key)
            nb1=arrays.get_nibble_array(arrays.give_hex_array(inp_hex))
            key0=arrays.get_nibble_array(arrays.give_hex_array(key_hex))
            x=ith_round_key.generate_key(key0,1)

            #round 0
            r0_text=AES_rounds.AddRoundKey(nb1,key0)
            previous_key=key0
            previous_output=r0_text

            #round 1 to 9

            for i in range(1,10):
                present_key=ith_round_key.generate_key(previous_key,i)
                substituted_bytes_text=AES_rounds.SubstituteBytes(previous_output)
                row_shifted_text=AES_rounds.ShiftRows(substituted_bytes_text)
                Mix_columns_text=AES_rounds.MixColumns(row_shifted_text)
                previous_output=AES_rounds.AddRoundKey(Mix_columns_text, present_key)
                previous_key=present_key

            #round 10
            present_key=ith_round_key.generate_key(previous_key,10)
            substituted_bytes_text=AES_rounds.SubstituteBytes(previous_output)
            row_shifted_text=AES_rounds.ShiftRows(substituted_bytes_text)
            previous_output=AES_rounds.AddRoundKey(row_shifted_text, present_key)
            cipher_text=convert.give_cipher(previous_output)

            f.write(cipher_text + '\n')

# encrypt(lines,key)

def decrypt(cipher_text,key):
    
    #with open(output_file, 'w') as f:
        outp=""
        key_hex=convert.textToHex(key)
        key0=arrays.get_nibble_array(arrays.give_hex_array(key_hex))
        p_k=key0
        keys = [[["" for _ in range(4)] for _ in range(4)] for _ in range(11)]

        for i in range(11):
            keys[i]=np.transpose(p_k)
            if i<=9:
                p_k=ith_round_key.generate_key(p_k,i+1)
        for t in range(len(cipher_text)):
            #print(cipher_text[t])
            inp=cipher_text[t]
            input_hex=convert.textToHex(inp)
            nbl=arrays.get_nibble_array(arrays.give_hex_array(inp))
            
            #nbl=np.transpose(nbl)

            #round 0
            previous_key=np.transpose(ith_round_key.get_key(keys,10))
            r0_cipher_text=AES_rounds.AddRoundKey(nbl, previous_key)
            previous_output=r0_cipher_text

            

            for i in range(9,0,-1):
                present_key=np.transpose(ith_round_key.get_key(keys,i))
                inverse_shift_rows=AES_rounds.InverseShiftRows(previous_output)
                inverse_sub_bytes=AES_rounds.InverseSubstituteBytes(inverse_shift_rows)
                add_rnd_key=AES_rounds.AddRoundKey(inverse_sub_bytes,present_key)
                previous_output=AES_rounds.InverseMixColumns(add_rnd_key)
        
                    
            #print("prev out :  ",previous_output)
        

            #round 10
            present_key=np.transpose(ith_round_key.get_key(keys,0))
            inverse_shift_rows=AES_rounds.InverseShiftRows(previous_output)
            inverse_sub_bytes=AES_rounds.InverseSubstituteBytes(inverse_shift_rows)
            previous_output=AES_rounds.AddRoundKey(inverse_sub_bytes, present_key)

            #previous_output=np.transpose(previous_output)
            plain_text=convert.give_text(previous_output)
            #print("plain text : ",plain_text)
            #f.write(convert.hex_to_text(plain_text)+ '\n')
            outp+=convert.hex_to_text(plain_text)
        
        out=outp.split(".")
        with open("decrypted_text.txt", 'w') as f:
            for txt in out:
                f.write(txt+ '\n')


# with open(cipher_file, 'r') as f:
#     content = f.read()
# lines = [content[i:i+33] for i in range(0, len(content), 33)]
# for i in range(len(lines)):
#     x=lines[i]
#     lines[i]=x[0:32]

# decrypt(lines,key)

#C:\\Users\\ASUS\\Desktop\\message.txt C:\\Users\\ASUS\\Desktop\\ciher_text.txt C:\\Users\\ASUS\\Desktop\\plain.txt