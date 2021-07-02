key = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&+-.=?^{}"

decode_dict = {}
for i in range(len(key)):
    decode_dict[key[i]] = i


def decode_string(char_string):
    result = 0
    for char in char_string:
        result *= 74
        result += decode_dict[char]
    return result
