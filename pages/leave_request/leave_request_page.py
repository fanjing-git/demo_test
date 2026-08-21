# encoding: utf-8
# @File  : leave_request_page.py
# @Author: Fan Jing
# @Date  : 2026/08/14/14:29

# 这是请假页面的页面逻辑
from base_object.base_page_object import BasePage
from locators.leave_request.leave_request_locator import LeaveRequestLocator
import allure

class LeaveRequestPage(BasePage):

    """新建请假页面"""
    @allure.step("进入请假页面")
    def enter_leave_request_page(self):
        self.click_element(LeaveRequestLocator.CLICK_LEAVE_BUTTON)
        self.click_element(LeaveRequestLocator.CLICK_NEW_LEAVE_BUTTON)
