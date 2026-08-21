# encoding: utf-8
# @File  : common_page.py
# @Author: Fan Jing
# @Date  : 2026/08/13/16:53
# 这是公共页面的页面逻辑
import allure

from base_object.base_page_object import BasePage
from locators.leave_request.leave_request_locator import LeaveRequestLocator



# 进入请假页面的页面封装

class LeaveRequestCommonPage(BasePage):

    @allure.story("进入请假申请页面")
    def leave_request(self):
        self.click_element(LeaveRequestLocator.CLICK_LEAVE_BUTTON)