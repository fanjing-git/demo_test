# encoding: utf-8
# @File  : leave_pass_and__refuse_locator.py
# @Author: Fan Jing
# @Date  : 2026/08/21/16:39
# 请假通过的定位器
class LeaveRequestPassAndRefuse:
    # 操作按钮（button 标签 + [1] 索引，确保只点击第一个匹配按钮）
    CLICK_PASS = "(//button[text() = '通过'])[1]"
    CLICK_REFUSE = "(//button[text() = '拒绝'])[1]"
    CLICK_CANCEL = "(//button[text() = '撤回'])[1]"
    # 状态结果（右上角 toast 提示，点击操作后立即弹出）
    # toast 结构：<div class="toast success">已通过</div>
    REFUSE_SUCCESS = "//div[contains(@class, 'toast') and text() = '已拒绝']"
    CANCEL_SUCCESS = "//div[contains(@class, 'toast') and text() = '已撤回']"
    PASS_SUCCESS = "//div[contains(@class, 'toast') and text() = '已通过']"