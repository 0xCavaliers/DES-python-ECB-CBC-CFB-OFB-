# SCU_DES-in-python-4-methods
# 川大密码学 DES(ECB,CBC,CFB,OFB)模式的python代码
本项目可以直接导入Colab或Jupyter NoteBook使用

## 1. main.py文件
直接运行main.py文件可以得出四种DES加密方法结果。删去main.py结尾的test()注释即可实现对每种操作模式下加密及解密速度的测试。
!python main.py

## 2.如果要具体运行某种加密方法，则可以采取以下指令（以ECB模式为例）
!python main.py -p des_plain.txt -k des_key.txt -v des_iv.txt -m ECB -c des_Cipher.txt


## 3.相关文件说明
Matrix.py存放算法常量如ip置换矩阵等
des.py des算法部件模块
readandwrite.py 控制密钥，明文，密文，iv文件读写
main.py主体文件
recording.txt 测试结果保存
des_key.txt 存放密钥
des_iv.txt 存放iv
des_plain.txt 存放明文
des_Cipher.txt 存放show()结果

2024.4.22
