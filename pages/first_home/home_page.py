# encoding: utf-8
# @File  : home_page.py
# @Author: Fan Jing
# @Date  : 2026/08/14/09:56
# 这是首页的页面逻辑
import allure

from base_object.base_page_object import BasePage
from locators.first_home.home_locator import HomeLocator


class HomePage(BasePage):

    @allure.step("获取退出登录按钮")
    def first_home(self):
        return self.page.locator(HomeLocator.LOGIN_OUT)