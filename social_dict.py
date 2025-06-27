#!/usr/bin/env python

import itertools
import string

dictionaryFile = open('passwd.txt', 'w')


def ReadInformationList():
    inforlist = []
    try:
        information = open("infor.txt", "r", encoding="utf-8")
        lines = information.readlines()
        for line in lines:
            # print(line.strip().split(':')[1])
            inforlist.append(line.strip().split(':')[1])
    except Exception as e:
        print(e + '\n')
        print("infor.txt文件读取错误")
    return inforlist


def CreateNumberList():
    numberList = []
    words = string.digits
    itertoolsNumberlist = itertools.product(words, repeat=3)
    for number in itertoolsNumberlist:
        numberList.append("".join(number))
    return numberList


def CreateSpecialList():
    specialList = []
    specialWords = string.punctuation
    for i in specialWords:
        specialList.append("".join(i))
    return specialList


def Combination():
    global dictionaryFile
    inforlist = ReadInformationList()
    # print(infolist)
    inforlen = len(inforlist)
    specialList = CreateSpecialList()
    for a in range(inforlen):
        #把个人信息大于等于8为的输出到文件
        if len(inforlist[a]) >= 8:
            # print(inforlist[a])
            dictionaryFile = open('passwd.txt', 'w')

        else:
            needWords = 8 - len(inforlist[a])
            #类似姓名+数字，共8位
            for b in itertools.permutations(string.digits, needWords):
                # print(infolist[a]+"".join(b))
                dictionaryFile.write(inforlist[a] + ''.join(b) + '\n')
        #类似姓名+生日
        for c in range(0, inforlen):
            if (len(inforlist[a] + inforlist[c]) >= 8):
                # print(inforlist[a]+inforlist[c])
                dictionaryFile.write(inforlist[a] + inforlist[c] + '\n')
        for d in range(0, inforlen):
            for e in range(0, len(specialList)):
                if (len(inforlist[a] + specialList[e] + inforlist[d]) >= 8):
                    #特殊字符加尾部
                    # print(infolist[a] + infolist[d] + specialList[e])
                    dictionaryFile.write(inforlist[a] + inforlist[d] + specialList[e] + '\n')
                    # 特殊字符加中间
                    # print(infolist[a] + specialList[e] + infolist[d])
                    dictionaryFile.write(inforlist[a] + specialList[e] + inforlist[d] + '\n')
                    # 特殊字符加前面
                    # print(specialList[e] + infolist[a] + infolist[d] )
                    dictionaryFile.write(specialList[e] + inforlist[a] + inforlist[d] + '\n')


if __name__ == '__main__':
    Combination()

