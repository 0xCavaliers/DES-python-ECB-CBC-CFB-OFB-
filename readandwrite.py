import os
import Matrix
import argparse
#明文路径\密钥路径\初始向量路径
def read(args):
    paths = []
    paths.append(args.plain)
    paths.append(args.key)
    paths.append(args.iv)
    context = []
    temp  = []
    for path in paths:
        with open(path) as f:
            context.append (f.read())
    for string in context:
        string = str(bin(int(string,16)))[2:]
        if not len(string)%4 == 0:
            for _ in range(4-len(string)%4):
                string = '0'+string
        temp.append(string)
    return temp

def write():
    path = "des_Cipher.txt"
    with open(path,'w') as f:
       for i in Matrix.words:
        f.write(i)

def read_data(filename):
    with open(filename,'b') as f:
        string = f.read()
    return string

def input_settings():
    parse = argparse.ArgumentParser()
    parse.add_argument("-p",type = str ,dest='plain',help= "- p plain.txt default des_plain.txt",default="des_plain.txt")
    parse.add_argument("-k", type = str ,dest= 'key', help = "-k key.txt default des_key.txt", default="des_key.txt")
    parse.add_argument("-v",type = str ,dest= 'iv', help= "- v iv.txt default des_plain.txt",default="des_iv.txt")
    parse.add_argument("-m", type = str , dest='mode',help = "-m mode yoeu want to encode default all mode", default="all")
    parse.add_argument("-c", type = str , dest = 'cipher',help = "-c where you want to store the secrect", default="des_Cipher.txt")
    args = parse.parse_args()
    return args

if __name__ == "__main__":
    args = input_settings()
    read(args)
