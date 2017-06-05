# encoding: utf-8

import json
import sys
import __init__
from TeacherStartCheckin import *
from TeacherRandomCheckin import *
from TeacherManualCheckin import *
from StudentAutoCheckin import *
from StudentDelay import *
from ViewAtAnyTime import *


class SystemRun(object):
    def __init__(self):
        self.readIniMethodRef = __init__.ReadIni()
        self.teacherStartCheckInObj = TeacherStartCheckIn()  # 教师开始签到类实例
        self.teacherStartRandomCheckInObj = TeacherRandomCheckIn()  # 教师抽点类实例
        self.teacherManualCheckInObj = TeacherManualCheckin()  # 教师手动签到类实例
        self.studentAutoCheckInObj = StudentAutoCheckin()  # 学生自动签到类实例
        self.studentDelay = StudentDelay()  # 学生请假类实例
        self.viewAtAnyTimeObj = ViewAtAnyTime()  # 查看信息类

    def main_menu(self):
        print "****************欢迎进入模拟控制菜单******************"
        print "*******1.教师开始考勤********2.学生进行考勤************"
        print "*******3.教师抽点考勤********4.学生进行请假************"
        print "*******5.教师手工考勤********6.考勤信息显示************"
        print "*******7.学生抽点考勤********0.退出*******************"
        op_num = raw_input("请输入您想要的操作：")
        flag = 0  # 结束循环标识符
        while flag == 0:
            flag = 1
            if op_num == '1':  # 教师开启考勤
                teacher_wechat_id = raw_input("请输入您的微信号：（教师）")
                course_id = raw_input("请输入您的课程号：")
                self.teacherStartCheckinObj.startCheckIn(teacher_wechat_id, course_id)
                for line in self.readIniMethodRef.List:
                    print json.dumps(line, encoding="utf-8", ensure_ascii=False)

            elif op_num == '2':  # 学生正常考勤操作
                stu_wechat_id = raw_input("请输入您的微信号：（学生）")
                input_stream = raw_input("请输入您的考勤证据：")
                self.studentAutoCheckinObj.stuAutoCheckIn(stu_wechat_id, input_stream)

            elif op_num == '3':  # 教师开启抽点考勤
                teacher_wechat_id = raw_input("请输入您的微信号：（教师）")
                num = int(raw_input("请输入您抽取的人数：（教师）"))
                self.teacherStartRandomCheckinObj.randomCheckIn(teacher_wechat_id, num)
                print "您已经完成了抽取人数！"

            elif op_num == '4':  # 学生进行请假操作
                stu_wechat_id = raw_input("请输入您的微信号：（学生）")
                input_stream = raw_input("请输入您的请假证据：")
                self.studentDelay.stuLeave(stu_wechat_id, input_stream)

            elif op_num == '5':  # 教师进行手工考勤操作
                flag1 = 0
                self.teacher_manual_checkin_menu()
                while flag1 == 0:
                    operator = raw_input("您是否继续操作?y/n")
                    if operator == 'y':
                        self.teacher_manual_checkin_menu()
                    else:
                        exit(0)

            elif op_num == '6':  # 随堂信息显示
                flag2 = 0
                self.viewInfoMenu()
                while flag2 == 0:
                    operator = raw_input("您是否继续操作?y/n")
                    if operator == 'y':
                        self.viewInfoMenu()
                    else:
                        exit(0)

            elif op_num == '7':  # 学生进行抽点考勤
                stu_wechat_id = raw_input("请输入您的微信号：（学生）")
                input_stream = raw_input("请输入您的证据路径：（学生）")
                self.teacherStartRandomCheckinObj.stuRandomCheckIn(stu_wechat_id, input_stream)

            elif op_num == '0':  # 退出系统
                sys.exit(0)
            else:
                flag = 0
                op_num = raw_input("您的输入有误！请重新输入:")

    # 查看信息窗口
    def view_info_menu(self):
        print "*****欢迎进入考勤信息展示菜单********"
        print "*******1.查看当前考勤信息***********"
        print "*******2.查看课程考勤信息***********"
        print "*******0.返回上层主菜单*************"
        op_num = raw_input("请输入您想要的操作：")
        flag = 0
        while flag == 0:
            flag = 1
            if op_num == '1':  # 查看当前考勤信息
                teacher_wechat_id = raw_input("请输入您的微信号：（教师）")
                print "你的当前课程的考勤信息如下："
                self.viewAtAnyTimeObj.showRealTime(teacher_wechat_id)

            elif op_num == '2':  # 查看课程考勤信息
                teacher_wechat_id = raw_input("请输入您的微信号：（教师）")
                course_id = raw_input("请输入您要查看的课程号：（教师）")
                print "\n您的课程号为" + str(course_id) + "的课的考勤结果如下："
                self.viewAtAnyTimeObj.sumCheckIn(teacher_wechat_id, course_id)
            elif op_num == '0':  # 回到主菜单
                break


            else:
                flag = 0
                op_num = raw_input("您的输入有误！请重新输入:")
        self.main_menu()

    # 手工考勤窗口
    def teacher_manual_checkin_menu(self):
        print "****************欢迎进入手工考勤菜单******************"
        print "*******1.教师进行手工修改****2.教师进行手工增加*********"
        print "*******3.教师手工批准请假****0.返回上层主菜单***********"
        op_num = raw_input("请输入您想要的操作：")
        flag = 0
        while flag == 0:
            flag = 1
            if (op_num == '1'):  # 教师手工考勤修改
                teacher_wechat_id = raw_input("请输入您的微信号：（教师）")
                self.teacherManunualCheckinObj.manualCheckInAlter(teacher_wechat_id)

            elif (op_num == '2'):  # 教师手工考勤增加
                teacher_wechat_id = raw_input("请输入您的微信号：（教师）")
                self.teacherManunualCheckinObj.manualCheckInAdd(teacher_wechat_id)

            elif (op_num == '3'):  # 教师手工批准请假
                teacher_wechat_id = raw_input("请输入您的微信号：（教师）")
                self.teacherManunualCheckinObj.leaveCheckIn(teacher_wechat_id)

            elif (op_num == '0'):  # 回到主菜单
                break

            else:
                flag = 0
                op_num = raw_input("您的输入有误！请重新输入:")
        self.main_menu()


if __name__ == "__main__":

    test = SystemRun()
    s = test.readIniMethodRef.List
    print json.dumps(s, encoding="utf-8", ensure_ascii=False)

    flag = 0
    test.main_menu()
    while(flag == 0) :
        operator = raw_input("您是否继续操作?y/n")
        if operator == 'y':
            test.main_menu()
        elif operator == 'n':
            sys.exit(0)
        else:
            operator = raw_input("您的输入有误，请重新输入: (y/n)")


