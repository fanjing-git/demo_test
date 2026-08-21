# encoding: utf-8
# @File  : login_page.py
# @Author: Fan Jing
# @Date  : 2026/08/13/16:53

# 登录页面的页面逻辑

import allure
from base_object.base_page_object import BasePage
from locators.login.login_locator import LoginLocator
from config.env_config import LOGIN_URL

class LoginPage(BasePage):
    @allure.step("执行登录：用户名={username}, 密码={password}")
    def login(self, username, password):
        self.open_browser(LOGIN_URL)
        self.input_text(LoginLocator.USERNAM_INOUT, username)
        self.input_text(LoginLocator.PASSWORD_INOUT, password)
        self.click_element(LoginLocator.LOGIN_BUTTON)
