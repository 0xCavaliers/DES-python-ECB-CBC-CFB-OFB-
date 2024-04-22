import time
import des
import readandwrite as rw  # 读取文件
import Matrix  # 数据模块
import argparse


# DES算法主题
def DES(plain, key, flag=1):
    # 对明文
    ipstr = des.ip_change(plain, Matrix.IP_MATRIX)
    ln = ipstr[:32]
    rn = ipstr[32:64]
    # 子秘钥生成
    sonkey = des.sonkey(key)
    if flag == 0:
        sonkey.reverse()
    for key in sonkey:
        e_rn = des.e_expend(rn)
        s_input = int(key, base=2) ^ int(e_rn, base=2)
        s_sub = des.s_change(s_input)
        ln, rn = des.p_change(ln, rn, s_sub)
    ln, rn = rn, ln
    lstr = ln + rn
    cipher = des.ip_change(lstr, Matrix.IP_INVERSE_MATRIX)
    return cipher


def ECB(string, key, flag=1):
    if len(string) % 64 != 0:
        while (len(string) % 64 != 0):
            string += "0"
    time = int(len(string) / 64)
    cipher = ""
    start = 0
    for i in range(time):
        cipher += DES(string[start:start + 64], key, flag)
        start += 64
    return cipher


def CBC(string, key, iv):
    if len(string) % 64 != 0:
        while (len(string) % 64 != 0):
            string += "0"
    time = int(len(string) / 64)
    cipher = ""
    start = 0
    for i in range(time):
        ox = bin(int(iv, base=2) ^ int(string[start:start + 64], base=2))[2:]
        while (len(ox) % 64 != 0):
            ox = "0" + ox
        iv = DES(ox, key)
        cipher += iv
        start += 64
    return cipher


def de_CBC(string, key, iv):
    assert len(string) % 64 == 0
    assert len(iv) % 64 == 0
    time = int(len(string) / 64)
    end = len(string)
    plain = ""
    for i in range(time - 1):
        temp = bin(int(DES(string[end - 64:end], key, 0), base=2) ^ int(string[end - 64 - 64:end - 64], base=2))[2:]
        while (len(temp) % 64 != 0):
            temp = "0" + temp
        plain = temp + plain
        end = end - 64
    temp = bin(int(DES(string[end - 64:end], key, 0), base=2) ^ int(iv, base=2))[2:]
    while (len(temp) % 64 != 0):
        temp = "0" + temp
    plain = temp + plain
    return plain


def CFB(string, key, iv):
    if len(string) % 8 != 0:
        while (len(string) % 8 == 0):
            string += "0"
    time = int(len(string) / 8)
    cipher = ""
    start = 0
    for i in range(time):
        temp = bin(int(DES(iv, key)[:8], base=2) ^ int(string[start:start + 8], base=2))[2:]
        while (len(temp) % 8 != 0):
            temp = "0" + temp
        cipher += temp
        iv = iv[8:] + temp
        start += 8
    return cipher


def de_CFB(string, key, iv):
    if len(string) % 8 != 0:
        while (len(string) % 8 == 0):
            string += "0"
    time = int(len(string) / 8)
    plain = ""
    start = 0
    for i in range(time):
        temp = bin(int(DES(iv, key)[:8], base=2) ^ int(string[start:start + 8], base=2))[2:]
        while (len(temp) % 8 != 0):
            temp = "0" + temp
        plain += temp
        iv = iv[8:] + temp
        start += 8
    return plain


def OFB(string, key, iv):
    if len(string) % 8 != 0:
        while (len(string) % 8 == 0):
            string += "0"
    time = int(len(string) / 8)
    cipher = ""
    start = 0
    for i in range(time):
        add = DES(iv, key)[:8]
        temp = bin(int(add, base=2) ^ int(string[start:start + 8], base=2))[2:]
        while (len(temp) % 8 != 0):
            temp = "0" + temp
        cipher += temp
        iv = iv[8:] + add
        start += 8
    return cipher


def show(args):
    plain, key, iv = rw.read(args)
    mode = args.mode
    if mode == "all":
        ecb_cipher = ECB(plain, key)
        ecb_plain = ECB(ecb_cipher, key, 0)
        print(f"ecb_cipher is 0x {int(ecb_cipher, base=2):X}")

        Matrix.words.append(f"ecb_cipher is 0x {int(ecb_cipher, base=2):X}\n")

        cbc_cipher = CBC(plain, key, iv)
        cbc_plain = de_CBC(cbc_cipher, key, iv)
        print(f"cbc_cipher is 0x {int(cbc_cipher, base=2):X}")

        Matrix.words.append(f"cbc_cipher is 0x {int(cbc_cipher, base=2):X}\n")

        cfb_cipher = CFB(plain, key, iv)
        cfb_plain = CFB(cfb_cipher, key, iv)
        print(f"cfb_cipher is 0x {int(cfb_cipher, base=2):X}")

        Matrix.words.append(f"cfb_cipher is 0x {int(cfb_cipher, base=2):X}\n")

        ofb_cipher = OFB(plain, key, iv)
        ofb_plain = OFB(ofb_cipher, key, iv)
        print(f"ofb_cipher is 0x {int(ofb_cipher, base=2):X}")

        Matrix.words.append(f"ofb_cipher is 0x {int(ofb_cipher, base=2):X}\n")

    elif mode == "ECB":
        ecb_cipher = ECB(plain, key)
        ecb_plain = ECB(ecb_cipher, key, 0)

        ecb_cipher_formatted = "0x " + hex(int(ecb_cipher, base=2))[2:].upper()
        ecb_plain_formatted = "0x " + hex(int(ecb_plain, base=2))[2:].upper()

        print(f"ecb_cipher is {ecb_cipher_formatted}")
        Matrix.words.append(f"ecb_cipher is {ecb_cipher_formatted}\n")
        print(f"ecb_plain  is {ecb_plain_formatted}")

    elif mode == "CBC":
        cbc_cipher = CBC(plain, key)
        cbc_plain = CBC(cbc_cipher, key, 0)

        cbc_cipher_formatted = "0x " + hex(int(cbc_cipher, base=2))[2:].upper()
        cbc_plain_formatted = "0x " + hex(int(cbc_plain, base=2))[2:].upper()

        print(f"cbc_cipher is {cbc_cipher_formatted}")
        Matrix.words.append(f"ecb_cipher is {cbc_cipher_formatted}\n")
        print(f"cbc_plain  is {cbc_plain_formatted}")

    elif mode == "CFB":
        cfb_cipher = CFB(plain, key)
        cfb_plain = CFB(cfb_cipher, key, 0)

        cfb_cipher_formatted = "0x " + hex(int(cfb_cipher, base=2))[2:].upper()
        cfb_plain_formatted = "0x " + hex(int(cfb_plain, base=2))[2:].upper()

        print(f"cfb_cipher is {cfb_cipher_formatted}")
        Matrix.words.append(f"cfb_cipher is {cfb_cipher_formatted}\n")
        print(f"cfb_plain  is {cfb_plain_formatted}")

    elif mode == "OFB":
        ofb_cipher = OFB(plain, key)
        ofb_plain = OFB(ofb_cipher, key, 0)

        ofb_cipher_formatted = "0x " + hex(int(ofb_cipher, base=2))[2:].upper()
        ofb_plain_formatted = "0x " + hex(int(ofb_plain, base=2))[2:].upper()

        print(f"ofb_cipher is {ofb_cipher_formatted}")
        Matrix.words.append(f"ofb_cipher is {ofb_cipher_formatted}\n")
        print(f"ofb_plain  is {ofb_plain_formatted}")

    else:
        print("please input right modes")


def test_ECB(args):
    plain, key, iv = rw.read(args)
    readname = "b.txt"
    writename = "temp.txt"
    de_name = "detemp.txt"
    perplain = "1"
    start = time.time()
    with open(readname, 'r') as f1:
        with open(writename, 'w') as f2:
            while len(perplain) != 0:
                perplain = f1.read(64)
                if perplain == "":
                    break
                f2.write(ECB(perplain, key, flag=1))
    perplain = "1"
    with open(writename, 'r') as f3:
        with open(de_name, 'w') as f4:
            while len(perplain) != 0:
                perplain = f3.read(64)
                if perplain == "":
                    break
                f4.write(ECB(perplain, key, flag=0))
    end = time.time()

    total_data_processed = 5 * 20  # 5MB processed 20 times
    total_time_seconds = end - start
    speed_mbps = total_data_processed / total_time_seconds  # MB/s

    with open("recording.txt", "a") as f:
        f.write(f"5MB en_decode for 20 times by ECB costs {total_time_seconds * 1000:.2f} ms\n")
        f.write(f"Speed: {speed_mbps:.2f} MB/s\n")
    print("ECB test over")


def test_CBC(args):
    plain, key, iv = rw.read(args)
    readname = "b.txt"
    writename = "temp.txt"
    perplain = "1"
    start = time.time()
    with open(readname, 'r') as f1:
        with open(writename, "w") as f2:
            while (len(perplain) != 0):
                perplain = f1.read(64)
                if len(perplain) == 0:
                    break
                if len(perplain) != 64:
                    while (len(perplain) != 64):
                        perplain = "0" + perplain
                ox = bin(int(iv, 2) ^ int(perplain, 2))[2:]
                while (len(ox) != 64):
                    ox = "0" + ox
                iv = DES(ox, key)
                f2.write(iv)
    end = time.time()

    total_data_processed = 5 * 20  # 5MB processed 20 times
    total_time_seconds = end - start
    speed_mbps = total_data_processed / total_time_seconds  # MB/s

    with open("recording.txt", "a") as f:
        f.write(f"5MB en_decode for 20 times by CBC costs {total_time_seconds * 1000:.2f} ms\n")
        f.write(f"Speed: {speed_mbps:.2f} MB/s\n")
    print("CBC test over")


def test_CFB(args):
    plain, key, iv = rw.read(args)
    readname = "b.txt"
    writename = "temp.txt"
    perplain = "1"
    start = time.time()
    with open(readname, 'r') as f1:
        with open(writename, "w") as f2:
            while (len(perplain) != 0):
                perplain = f1.read(8)
                if len(perplain) == 0:
                    break
                if len(perplain) != 8:
                    while (len(perplain) != 8):
                        perplain = "0" + perplain
                ox = bin(int(DES(iv, key)[:8], 2) ^ int(perplain, 2))[2:]
                while (len(ox) != 8):
                    ox = "0" + ox
                iv = iv[8:] + ox
                f2.write(ox)
    end = time.time()

    total_data_processed = 5 * 20  # 5MB processed 20 times
    total_time_seconds = end - start
    speed_mbps = total_data_processed / total_time_seconds  # MB/s

    with open("recording.txt", "a") as f:
        f.write(f"5MB en_decode for 20 times by CFB costs {total_time_seconds * 1000:.2f} ms\n")
        f.write(f"Speed: {speed_mbps:.2f} MB/s\n")

    print("CFB test over")


def test_OFB(args):
    plain, key, iv = rw.read(args)
    readname = "b.txt"
    writename = "temp.txt"
    perplain = "1"
    start = time.time()
    with open(readname, 'r') as f1:
        with open(writename, "w") as f2:
            while (len(perplain) != 0):
                perplain = f1.read(8)
                if len(perplain) == 0:
                    break
                if len(perplain) != 8:
                    while (len(perplain) != 8):
                        perplain = "0" + perplain
                temp = DES(iv, key)[:8]
                ox = bin(int(temp, 2) ^ int(perplain, 2))[2:]
                while (len(ox) != 8):
                    ox = "0" + ox
                iv = iv[8:] + temp
                f2.write(ox)
    end = time.time()

    total_data_processed = 5 * 20  # 5MB processed 20 times
    total_time_seconds = end - start
    speed_mbps = total_data_processed / total_time_seconds  # MB/s

    with open("recording.txt", "a") as f:
        f.write(f"5MB en_decode for 20 times by OFB costs {total_time_seconds * 1000:.2f} ms\n")
        f.write(f"Speed: {speed_mbps:.2f} MB/s\n")
    print("OFB test over")


def test():
    args = rw.input_settings()
    test_ECB(args)
    test_CBC(args)
    test_CFB(args)
    test_OFB(args)


if __name__ == "__main__":
    args = rw.input_settings()
    show(args)
    # 删去注释即可跑测试实验
    # test()

