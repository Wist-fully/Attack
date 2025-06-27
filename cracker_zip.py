#!/usr/bin/env python

from tqdm import tqdm
import zipfile
import pyzipper

passwordfile = "PasswordFile.txt"
zip_file = "zzipp.zip"

n_words = len(list(open(passwordfile,"rb")))
print("总密码共有: ",n_words)
with open(passwordfile,"rb") as wordlist:
    for word in tqdm(wordlist,total=n_words,unit="word"):
        pwd = str(word,'utf-8').replace('\n','')
        try:
            # zip_file.extractall(pwd=pwd)
            with pyzipper.AESZipFile(zip_file, 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as extracted_zip:
                extracted_zip.extractall(pwd=str.encode(pwd))
        except:
            continue
        else:
            print("[+] password found:",word.decode().strip())
            exit(0)
print("[!] password not found,try other wordlist")