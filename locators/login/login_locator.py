# encoding: utf-8
# @File  : login_locator.py
# @Author: Fan Jing
# @Date  : 2026/08/13/16:46

# 登录页面的元素定位

class LoginLocator:
    username_input = "//input[@placeholder = '请输入用户名']"
    password_input = "//input[@placeholder = '请输入密码']"
    login_button = "//*[contains(text(), '登录')]"
