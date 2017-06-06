import threading, time
class TimerDemo():

    def __init__(self):
        self.t = threading.interval
    def inputTime(self):
        now = time.strftime("%H:%M",time.localtime())
        print now
        self.t.cancel()
    def run(self):
         self.t.start()

if __name__ == '__main__':
    print 'after push failed,and pull failed, then i checkout first version ,then i updated this line try to push!AGAIN!'
    while(True):
        t.run()


