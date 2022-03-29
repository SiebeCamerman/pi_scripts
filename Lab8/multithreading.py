import time
import threading

exit_event = threading.Event()

def task(name, delay):
    while True:
        time.sleep(delay)
        print ("%s: %s" % (name,time.time()))
        if exit_event.is_set():
            break

def test(name, delay):
    while True:
        time.sleep(delay)
        print(name, 'test')
        if exit_event.is_set():
            break

#create two new threads
t1 = threading.Thread(target=test, args=("fast-thread", 1))
t2 = threading.Thread(target=test, args=("slow-thread", 5))

#start the threads
t1.start()
t2.start()

n=0

try:
    while True:
        n+=1
        print ("Main thread: %s" % n)
        time.sleep(1)
except KeyboardInterrupt:
    exit_event.set()