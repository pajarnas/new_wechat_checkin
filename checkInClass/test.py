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
    print 'fourth!'
    while(True):
        t.run()


