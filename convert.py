from binascii import *
class convert:
    def textToHex(input_string):
        hex_result = ""
        # Iterate through each character in the input string
        for char in input_string:
            # Get the ASCII value of the character and convert it to a 2-digit hexadecimal string
            hex_char = format(ord(char), '02x')
            # Append the 2-digit hexadecimal string to the result
            hex_result += hex_char
        return hex_result
    

    def hex_to_text(hex_string):
        import binascii
  # Convert the hexadecimal string to bytes.
        bytestring = binascii.unhexlify(hex_string)
  # Try decoding the bytestring using multiple encodings.
        encodings = ["utf-8", "ascii", "latin-1"]
        for encoding in encodings:
            try:
                text = bytestring.decode(encoding)
                return text
            except UnicodeDecodeError:
                pass
  # If the bytestring cannot be decoded using any of the encodings, return None.
        return None

    
    
    def give_cipher(input):
        out=""
        for i in range(len(input)):
            for j in range(len(input[0])):
                out=out+input[j][i]
        return out
    
    def give_text(input):
        out=""
        for i in range(len(input)):
            for j in range(len(input[0])):
                out=out+input[j][i]
        return out


    
