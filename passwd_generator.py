#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import string
import random
import secrets


passwords = []

def SetParser():
    parser = ArgumentParser(
        prog = "密码生成器",
        description = "这是一个简单的密码生成器，可以生成任意形式的密码"
    )

    parser.add_argument("-l","--lowercase",default=0,help="密码包含小写字符的位数",type=int)
    parser.add_argument("-u","--uppercase",default=0,help="密码包含大写字符的位数",type=int)
    parser.add_argument("-n","--numbers",default=0,help="密码包含数字的位数",type=int)
    parser.add_argument("-s","--special-chars",default=0,help="密码包含特殊字符",type=int)
    parser.add_argument("-t","--total-length",default=0,help="密码的总长度",type=int)
    parser.add_argument("-nu","--number",default=0,help="生成密码的数量",type=int)
    parser.add_argument("-a","--amount",default=0,help="控制长度",type=int)
    parser.add_argument("-o","--output-file")
    return parser.parse_args()

def CreateRandomPWD(args):

    for _ in range(args.amount):
            passwords.append("".join(
                [secrets.choice(string.digits+string.ascii_letters+string.punctuation)\
                 for _ in range(args.total_length)
            ]))
def CreateArgumentPWD(args):
    for _ in range(args.amount):
        password = []
        for _ in range(args.numbers):
            password.append(secrets.choice(string.digits))
        for _ in range(args.uppercase):
            password.append(secrets.choice(string.ascii_uppercase))
        for _ in range(args.lowercase):
            password.append(secrets.choice(string.ascii_lowercase))
        for _ in range(args.special_chars):
            password.append(secrets.choice(string.punctuation))
        random.shuffle(password)
        password = ''.join(password)
        passwords.append(password)

if __name__ == "__main__":
    args = SetParser()
    if args.total_length:
        CreateRandomPWD(args)
    else:
        CreateArgumentPWD(args)
    print('\n'.join(passwords))
    if args.output_file:
        with open(args.output_file,'w') as f:
            f.write('\n'.join(passwords))

'''
eg.:
python .\2.py -l 3 -n 3  -a 5 -o 2.txt
'''


