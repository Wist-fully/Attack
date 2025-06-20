from collections.abc import Callable,Iterable,Mapping
from multiprocessing import Queue
from typing import Any
import requests
import threading
from fake_useragent import UserAgent

rua = UserAgent()

class DirScan(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            url = self.queue.get()
            try:
                headers = {
                    "User-Agent":rua.random
                }
                r = requests.get(url=url,headers=headers,timeout=2)
                if r.status_code == 200:
                    print('[*] %s\n',url)
                else:
                    print("This path does not exist")

            except:
                pass


def start(url,ext,count):
    queue = Queue()

    f = open('%s.txt'%ext,'r')
    #print(f.readlines)
    for i in f:
        #print(url+i.rstrip('\n'))
        queue.put(url+i.rstrip('\n'))

    '''多线程'''
    threads = []
    thread_count = int(count)
    for i in range(thread_count):
        threads.append(DirScan(queue))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    url = input('Please enter the url:')
    ext = 'asp'
    count = input('Please enter the number of threads:')
    start(url,ext,count)