# encoding: utf-8
# @File  : test_login_success.py
# @Author: Fan Jing
# @Date  : 2026/08/13/16:59

# 登录成功的测试用例

import sys
import os
# 添加项目根目录到 sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import allure
from pytest import main
import pytest
from pages.login.login_page import LoginPage
from config.env_config import LOGIN_USERNAME, LOGIN_PASSWORD


@allure.feature("登录功能")
class TestLoginSuccess:

    @allure.story("登录成功")
    def test_login_success(self, page):
        login_page = LoginPage(page)
        login_page.login(LOGIN_USERNAME, LOGIN_PASSWORD)
        login_page.assert_url_contains("home", message="登录后应跳转到首页")


if __name__ == '__main__':
    pytest.main(["test_login_success.py", "-v", "-s"])
