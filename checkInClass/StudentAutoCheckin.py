# encoding=utf-8

# This program show the student's operations

from StudentCommonMethods import StuMethod
import csv
import time
import random


class StudentAutoCheckin(StuMethod):

    # 对学生正常考勤类进行初始化
    def __init__(self):
        StuMethod.__init__(self)
        pass

    # 学生进行正常的自主考勤
    def stu_auto_checkin(self, stu_wechat_id, input_stream):
        stu_id = self.findStudentByWechatID(stu_wechat_id)[0]
        file_name = self.checkfileName(stu_wechat_id)
        checkin_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        proof_path = input_stream
        checkin_type = 'Auto'
        IsSucc = bool(random.randrange(0, 2))
        checkinResult = None

        if file_name=='':
            print '打开详细表失败，或许是考勤窗口已经关闭'
            return
        else:
            with open(file_name, 'a+') as checkfile:
                writer = csv.writer(checkfile)
                message0 = [stu_id, checkin_time, proof_path, checkin_type, IsSucc, checkinResult]
                writer.writerow(message0)
                print '你已进行了正常考勤的操作'


