import threading
import time

f = open("Data_dumps/wyniki.txt", "r")

f1 = f.readlines()
for x in range(10):
    print(f1[x])
    # print(f.readline())

f.close()


class threadtester (threading.Thread):
    def __init__(self, id, name, i):
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.i = i

    def run(self):
        print("%s has finished execution " % self.name)


def thread_test(name, wait, i):
    while i:
        time.sleep(wait)
        print("Running %s \n" % name)
        i = i - 1
