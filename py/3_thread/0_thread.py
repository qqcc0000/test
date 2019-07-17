import threading

import time

def worker(number):
    print ("worker",i)
    time.sleep(number)
    return

for i in range(5):

    t = threading.Thread(target=worker,args=(i,))

    t.start()
