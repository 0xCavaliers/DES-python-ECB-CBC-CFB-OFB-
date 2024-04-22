import Matrix


# IP change
def ip_change(string, ip_bin):
    assert len(string) == 64
    newstr = ""
    for i in ip_bin:
        newstr += string[i - 1]
    return newstr


# E_expend
def e_expend(string):
    assert len(string) == 32
    newstr = ""
    for i in Matrix.E_MATRIX:
        newstr += string[i - 1]
    assert len(newstr) == 48
    return newstr


# s_change
def s_change(string):
    string = bin(string)[2:]
    while len(string) < 48:
        string = "0" + string
    lop = 6
    start = 0
    newstr = ""
    for i in range(8):
        temp = string[start:start + 6]
        h = int(temp[0] + temp[5], base=2)
        l = int(temp[1:5], base=2)
        index = h * 16 + l
        add = bin(Matrix.S_MATRIX[i][index])[2:]
        if not len(add) % 4 == 0:
            for _ in range(4 - len(add) % 4):
                add = '0' + add
        newstr += add
        start += lop
    # assert len(newstr)==32
    return newstr


def shift(string, count):
    string = string[count:] + string[:count]
    return string


# pbox
def p_change(l_string, r_string, s_sub):
    tmp = ""
    for i in Matrix.P_MATRIX:
        tmp += s_sub[i - 1]
    rn = int(tmp, base=2) ^ int(l_string, base=2)
    rn = bin(rn)[2:]
    while len(rn) < 32:
        rn = "0" + rn
    ln = r_string
    return ln, rn


# product + shift +change
def sonkey(key):
    assert len(key) == 64
    # prepare
    Llist = [57, 49, 41, 33, 25, 17, 9,
             1, 58, 50, 42, 34, 26, 18,
             10, 2, 59, 51, 43, 35, 27,
             19, 11, 3, 60, 52, 44, 36]
    Rlist = [63, 55, 47, 39, 31, 23, 15,
             7, 62, 54, 46, 38, 30, 22,
             14, 6, 61, 53, 45, 37, 29,
             21, 13, 5, 28, 20, 12, 4]
    ln0 = ""
    rn0 = ""
    sonkey = []
    for i in Llist:
        ln0 += key[i - 1]
    for i in Rlist:
        rn0 += key[i - 1]
    shift_counts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    # product
    for i in range(16):
        ln0 = shift(ln0, shift_counts[i])
        rn0 = shift(rn0, shift_counts[i])
        tempson = ln0 + rn0
        sonkeyi = ""
        for i in Matrix.COMPRESS_MATRIXS:
            sonkeyi += tempson[i - 1]
        assert len(sonkeyi) == 48
        sonkey.append(sonkeyi)

    return sonkey


if __name__ == "__main__":
    pass



