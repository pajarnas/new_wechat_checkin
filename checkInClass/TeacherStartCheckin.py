# encoding=utf-8

from TeacherCommonMethods import Method
from __init__ import ReadIni
from TimeWindow import Timer
import csv
import time
import os

# This program is show the teacher's operations
# This program is show teacher to start the checkIn

class TeacherStartCheckIn(Method):

    #对教师开始考勤类进行初始化
    def __init__(self):
        Method.__init__(self)
        pass

    # 获取该课程上课的班级
    def getClassByTeacherAndCourse(self,teacherID,courseID, classList):
        with open('InData/courseInfo.csv', 'rb') as courseInfo:
            reader = csv.reader(courseInfo)
            flag = 0  # 设置下边追加班级时的控制变量
            reader.next()
            for line in reader:
                if (line[0] == str(courseID)) & (line[2] == str(teacherID)):
                    classList.append(line[3])
                    flag = 1
                else:
                    pass
            if flag == 0:
                print '没有上课的班级！'
                return False

    # 教师进入队列。
    def entryList(self,teacherID,courseID):

        timerObj = Timer()    #建立一个Timer计时器的实例

        classList = []  # 获取当前课程上课的班级列表
        if self.getClassByTeacherAndCourse(teacherID,courseID, classList) == False:
            return

        nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
        messagelist = [teacherID, courseID, classList, nowtime]

        # 列表非空 需要进行判断！如果该班能合法进入考勤队列将排在考勤队列的末尾
        #如果列表为空则新建一个计时器 这个计时器只为列表首的考勤班服务
        #列表第二位即以后的班要等到第一个班用完计时器才能使用计时器
        #如果首位的班提前结束使用计时器 那么第二位的班将销毁之前的计时器
        #然后加上当前时间到下课时间的时间差为第二个班服务
        if ReadIni.List:
            for line in ReadIni.List:
                if (set(classList) & set(line[2])):
                    print "班级已存在"
                    tempObj = ReadIni()
                    time0 = tempObj.readIni()     #  从readIni中得到课程的开始时间和结束时间
                    nowtime0 = nowtime.split(" ")
                    nowtime1 = nowtime0[1].split(':')
                    nowtime2 = nowtime1[0] + nowtime1[1] + nowtime1[2]
                    #如果现在时间是下课时间 说明那个正在考勤的班级应该移出队列
                    if (time0[0] < nowtime2 < time0[1]) | \
                            (time0[2] < nowtime2 < time0[3]) | (time0[4] < nowtime2 < time0[5]):
                        ReadIni.List.remove(line)
                        ReadIni.List.append(messagelist)
                        print "移出前一个考勤结束的班成功，成功进入队列！"
                    else:
                        print "当前班级正在考勤！您无法开启考勤窗口"
                        return False
                else:#这个班合法的进入队列并排在后位
                    ReadIni.List.append(messagelist)
                    timerObj.stopCheckIn()
        else:#这个是队列首位 将新建一个计时器
            ReadIni.List.append(messagelist)
            timerObj.startCheckTime()

    # 生成考勤次序表+考勤详细表
    def creatSeq(self,teacherID, courseID):
        with open('OutData/seq.csv', 'r+') as csvfile:
            reader = csv.reader(csvfile)
            writer = csv.writer(csvfile)
            nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
            seqID = ''
            for line in reader:
                 if line[0] == teacherID:
                    seqID = line[2]
                 else:
                    pass
            if seqID == '':
                seqID = 1
            else:
                seqID = str(int(seqID) + 1)
            messageList = [teacherID, courseID, seqID, nowtime]
            writer.writerow(messageList)

        # 生成考勤详细表
        newFileName = 'OutData/' + str(teacherID) + '_' + str(courseID) + '_' + \
                      str(seqID) + '_' + 'checkinDetail.csv'
        with open(newFileName, 'a+') as filename:
           writer2 = csv.writer(filename)
           messageList2 = ['StuID', 'checkTime', 'ProofPath', 'checkinType', 'IsSucc', 'checkinResult']
           writer2.writerow(messageList2)

    # 生成sum表，在考勤时间窗口结束后汇总信息
    # 此时将学生ID全部加入
    def creatSum(self,teacherID, courseID):
        filename = 'OutData/' + str(teacherID) + '_' + str(courseID) + '_' + "sum.csv"
        if os.path.exists(filename) != True:
            with open(filename, 'a+') as csvfile:
                writer = csv.writer(csvfile)
                String2 = ['StuID', '']
                writer.writerow(String2)
                for line in ReadIni.List:
                    if (line[0] == teacherID) & (line[1] == courseID):
                        with open('InData/studentInfo.csv', 'r') as classFilename:
                            reader = csv.reader(classFilename)
                            reader.next()
                            for line1 in reader:
                                if line1[2] in line[2]:
                                    string = [line1[0], '']
                                    writer.writerow(string)

    #教师开始考勤
    def startCheckIn(self,teacherWechatID,courseID):
        teacherID = self.find_teacherid_by_wechatid(teacherWechatID)
        if (self.entryList(teacherID,courseID) != False):
            self.creatSeq(teacherID,courseID)
            self.creatSum(teacherID,courseID)


# if __name__ == "__main__":
#     ReadIni.List = [['2004633', '51610189', ['\xe8\xbd\xaf\xe4\xbb\xb6\xe5\xb7\xa5\xe7\xa8\x8b1401', '\xe8\xbd\xaf\xe4\xbb\xb6\xe5\xb7\xa5\xe7\xa8\x8b1402', '\xe8\xbd\xaf\xe4\xbb\xb6\xe5\xb7\xa5\xe7\xa8\x8b1403', '\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba\xe7\xa7\x91\xe5\xad\xa6\xe4\xb8\x8e\xe6\x8a\x80\xe6\x9c\xaf1401'], '2016-06-09 14:00:21']]
#     t = teacherStartCheckIn()
#     tc = '2004633'
#     co = '51610189'
#     # t.startCheckIn(tc,co)
#     t.creatSum(tc,co)



