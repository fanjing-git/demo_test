# encoding: utf-8
# @File  : test_create_new_leave_application.py
# @Author: Fan Jing
# @Date  : 2026/08/14/17:24
# 新建请假申请的测试用例


import allure
import pytest

from locators.common.handle_data import get_random_date_range
from pages.leave_request.create_new_leave_request_page import CreateNewLeaveRequestPage
from pages.leave_request.leave_request_page import LeaveRequestPage
from data.leave_request_data import LeaveRequestData

START_TIME, END_TIME = get_random_date_range()


@allure.feature("请假申请功能")
class TestCreateNewLeaveApplication:

    def _init_page(self, logged_in_page):
        self.create_new_leave_page = CreateNewLeaveRequestPage(logged_in_page)
        self.leave_request_page = LeaveRequestPage(logged_in_page)

    @allure.story("请假申请功能")
    @allure.title("填写请假内容并且点击确认")
    def test_create_new_leave_application_submit(self, logged_in_page):
        """填写请假内容并提交，断言提交成功提示文本"""
        self._init_page(logged_in_page)
        self.leave_request_page.enter_leave_request_page()
        leave_request_data = LeaveRequestData(
            student_no="2024001",
            leave_type="病假",
            start_time=START_TIME,
            end_time=END_TIME,
            text="测试",
        )
        self.create_new_leave_page.create_new_leave_request(leave_request_data)
        self.create_new_leave_page.click_submit_button()
        submit_text_locator = self.create_new_leave_page.get_submit_text()
        self.create_new_leave_page.assert_text(submit_text_locator, "请假申请已提交")

    @allure.story("请假申请功能")
    @allure.title("创建请假申请并且点击取消")
    def test_create_new_leave_application_cancel(self, logged_in_page):
        """创建请假申请后取消"""
        self._init_page(logged_in_page)
        self.create_new_leave_page = CreateNewLeaveRequestPage(logged_in_page)
        self.leave_request_page = LeaveRequestPage(logged_in_page)
        leave_request_data = LeaveRequestData(
            student_no="2024001",
            leave_type="病假",
            start_time=START_TIME,
            end_time=END_TIME,
            text="测试"
        )
        self.create_new_leave_page.create_new_leave_request(leave_request_data)
        self.create_new_leave_page.click_cancel_button()


if __name__ == '__main__':
    pytest.main(["-v", "-s"])
