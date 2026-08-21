# encoding: utf-8
# @File  : leave_request_pass_and_refuse_page.py
# @Author: Fan Jing
# @Date  : 2026/08/21/17:02
# 这是请假通过和拒绝以及撤回的页面逻辑
import allure
from loguru import logger

from base_object.base_page_object import BasePage
from locators.leave_request.leave_pass_and__refuse_locator import LeaveRequestPassAndRefuse


class PassRefuseCancel(BasePage):

    @allure.story("点击请假通过")
    def click_pass(self, comment="同意"):
        handler = self.handle_multi_dialog(confirm_accept=True, prompt_text=comment)
        self.click_element(LeaveRequestPassAndRefuse.CLICK_PASS)
        self.page.remove_listener("dialog", handler)

    @allure.story("点击请假拒绝")
    def click_refuse(self, comment="拒绝"):
        handler = self.handle_multi_dialog(confirm_accept=False, prompt_text=comment)
        self.click_element(LeaveRequestPassAndRefuse.CLICK_REFUSE)
        self.page.remove_listener("dialog", handler)

    @allure.story("点击请假撤回")
    def click_cancel(self, comment="撤回"):
        handler = self.handle_multi_dialog(confirm_accept=True, prompt_text=comment)
        self.click_element(LeaveRequestPassAndRefuse.CLICK_CANCEL)
        self.page.remove_listener("dialog", handler)

    def get_text(self, timeout=3):
        """获取右上角 toast 提示文本（瞬态提示，需立即检查）"""
        return self.get_toast_text(selector="div.toast", timeout=timeout)