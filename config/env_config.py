# encoding: utf-8
# @File  : env_config.py
# @Author: Fan Jing
# @Date  : 2026/08/13/16:20

# 配置文件
LOGIN_URL = "http://localhost:5173/login"
LOGIN_USERNAME = "admin"
LOGIN_PASSWORD = "admin123"

# 默认等待超时时间（秒），用于 BasePage/UIAssertions 的默认等待
# 单个断言如需更长等待，调用时传 timeout 参数覆盖，不用改这里
DEFAULT_TIMEOUT = 8
