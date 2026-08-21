# encoding: utf-8
# @File  : test_login_success.py
# @Author: Fan Jing
# @Date  : 2026/08/13/16:59

# 登录成功的测试用例

import sys
import os


import allure
import pytest

from pages.first_home.home_page import HomePage
from pages.login.login_page import LoginPage
from config.env_config import LOGIN_USERNAME, LOGIN_PASSWORD



@allure.feature("登录功能")
class TestLoginSuccess:

    @allure.story("登录成功")
    def test_login_success(self, page):
        login_page = LoginPage(page)
        home_page = HomePage(page)
        login_page.login(LOGIN_USERNAME, LOGIN_PASSWORD)
        logout_button = home_page.first_home()
        login_page.assert_text(logout_button, "退出登录")


if __name__ == '__main__':
    pytest.main(["test_login_success.py", "-v", "-s"])
