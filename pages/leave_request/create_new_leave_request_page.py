# encoding: utf-8
# @File  : create_new_leave_request_page.py
# @Author: Fan Jing
# @Date  : 2026/08/14/15:06

# 新建请假申请页面
from base_object.base_page_object import BasePage
import allure

from locators.leave_request.create_new_leave_application_locator import CreateNewLeaveApplicationLocator
from data.leave_request_data import LeaveRequestData


class CreateNewLeaveRequestPage(BasePage):

    @allure.step("新建请假申请")
    def create_new_leave_request(self, leave_request_data: LeaveRequestData):
        """根据 leave_request_data 中不为 None 的字段填写新建请假申请表单

        :param leave_request_data: 请假申请数据对象，字段均可选，只有不为 None 的字段才会被操作
        """
        if leave_request_data.student_no is not None:
            self.select_student(leave_request_data.student_no)
        if leave_request_data.leave_type is not None:
            self.select_dropdown(CreateNewLeaveApplicationLocator.LEAVE_TYPE_OPTION, leave_request_data.leave_type)
        if leave_request_data.start_time is not None:
            self.input_text(CreateNewLeaveApplicationLocator.START_TIME_INPUT, leave_request_data.start_time)
        if leave_request_data.end_time is not None:
            self.input_text(CreateNewLeaveApplicationLocator.END_TIME_INPUT, leave_request_data.end_time)
        if leave_request_data.text is not None:
            self.input_text(CreateNewLeaveApplicationLocator.LEAVE_REASON_INPUT, leave_request_data.text)

    # 选择学生下拉列表的封装
    @allure.step("按学号选择学生")
    def select_student(self,student_no: str):
        # <select> 收起时 <option> 包围盒为0，不满足可见性条件，不能走 find_element/get_element_attribute 的可见性等待，
        # 这里直接用 page.locator 取属性，绕开可见性检查
        option_locator = CreateNewLeaveApplicationLocator.STUDENT_OPTION_BY_NO.format(student_no = student_no)
        option_value = self.page.locator(option_locator).get_attribute("value")
        self.select_dropdown(CreateNewLeaveApplicationLocator.SELECT_STUDENT_TYPE,option_value)

    # 点击确认按钮
    @allure.step("点击确认按钮")
    def click_submit_button(self):
        self.click_element(CreateNewLeaveApplicationLocator.SUBMIT_BUTTON)

    # 点击取消按钮
    @allure.step("点击取消按钮")
    def click_cancel_button(self):
        self.click_element(CreateNewLeaveApplicationLocator.CANCEL_BUTTON)

    @allure.step("获取提交后的提示文本元素")
    def get_submit_text(self):
        """返回提交成功提示文本的 Locator，供用例断言，不在页面类内部取快照值"""
        return self.page.locator(CreateNewLeaveApplicationLocator.SUBMIT_TEXT)
