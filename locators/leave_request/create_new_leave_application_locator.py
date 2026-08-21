# encoding: utf-8
# @File  : create_new_leave_application_locator.py
# @Author: Fan Jing
# @Date  : 2026/08/14/13:56

# 新建请假申请页面元素定位
class CreateNewLeaveApplicationLocator:

    # 选择学生下拉框
    SELECT_STUDENT_TYPE = "//label[text()='学生']/following-sibling::select"
    # 按学号匹配学生下拉框中的选项（姓名可能重复，需用学号唯一定位），{student_no} 需在页面方法中用 .format() 替换
    STUDENT_OPTION_BY_NO = "//label[text()='学生']/following-sibling::select/option[contains(text(), '{student_no}')]"
    # 选择请假类型下拉框
    SELECT_LEAVE_TYPE = "//*[@class = 'form-group']/select"
    # 请假类型选择的元素定位
    LEAVE_TYPE_OPTION = "//label[text()='请假类型']/following-sibling::select"
    # 开始时间输入框的元素定位
    START_TIME_INPUT = "//label[text()='开始日期']/following-sibling::input"
    # 结束时间输入框的元素定位
    END_TIME_INPUT = "//label[text()='结束日期']/following-sibling::input"
    # 请假原因输入框的元素定位
    LEAVE_REASON_INPUT = "//*[@class ='form-group']//textarea"
    # 提交按钮的元素定位
    SUBMIT_BUTTON = "//*[text() ='提交']"
    # 取消按钮的元素定位
    CANCEL_BUTTON = "//*[text() ='取消']"
    # 提交后的文本信息
    SUBMIT_TEXT = "//*[text() ='请假申请已提交']"
    

