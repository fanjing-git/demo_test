# encoding: utf-8
# @File  : test_click_pass_refuse_cancel.py
# @Author: Fan Jing
# @Date  : 2026/08/21/16:35
# 这是测试请假申请通过/拒绝/撤回的用例


import allure
import pytest
from loguru import logger

from pages.common.common_page import LeaveRequestCommonPage
from pages.leave_request.leave_request_pass_and_refuse_page import PassRefuseCancel
from pages.leave_request.create_new_leave_request_page import CreateNewLeaveRequestPage
from pages.leave_request.leave_request_page import LeaveRequestPage
from data.leave_request_data import LeaveRequestData
from locators.common.handle_data import get_random_date_range


@allure.feature("请假申请功能")
class TestLeavePass:

    def _init_page(self, logged_in_page):
        self.leave_common_page = LeaveRequestCommonPage(logged_in_page)
        self.pass_refuse_cancel = PassRefuseCancel(logged_in_page)
        self.create_new_leave_page = CreateNewLeaveRequestPage(logged_in_page)
        self.leave_request_page = LeaveRequestPage(logged_in_page)

    def _create_leave_request(self):
        """前置步骤：新建一条请假申请，确保列表中有“待审批”记录"""
        self.leave_request_page.enter_leave_request_page()
        start_time, end_time = get_random_date_range()
        leave_request_data = LeaveRequestData(
            student_no="2024001",
            leave_type="病假",
            start_time=start_time,
            end_time=end_time,
            text="审批测试",
        )
        self.create_new_leave_page.create_new_leave_request(leave_request_data)
        self.create_new_leave_page.click_submit_button()

    @allure.story("请假申请通过")
    def test_leave_pass(self, logged_in_page):
        logger.info("测试请假申请通过")
        self._init_page(logged_in_page)
        self._create_leave_request()
        self.leave_common_page.leave_request()
        self.pass_refuse_cancel.click_pass()
        # toast 是瞬态提示，点击后立即出现，需要立刻检查
        text = self.pass_refuse_cancel.get_text(timeout=3)
        assert text == "已通过", f"期望状态为'已通过'，实际为'{text}'"


if __name__ == '__main__':
    pytest.main(["-v", "-s"])





