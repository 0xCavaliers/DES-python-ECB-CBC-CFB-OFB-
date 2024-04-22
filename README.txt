川大密码学 DES(ECB,CBC,CFB,OFB)模式的python代码
本项目可以直接导入Colab或Jupyter NoteBook使用

1. 直接运行main.py文件可以得出四种DES加密方法结果。如果删去main.py结尾的test()注释即可实现对每种操作模式下加密及解密速度的测试。
!python main.py

2.如果要具体运行某种加密方法，则可以采取以下指令（以ECB模式为例）：
!python main.py -p des_plain.txt -k des_key.txt -v des_iv.txt -m ECB -c des_Cipher.txt

2024.4.22