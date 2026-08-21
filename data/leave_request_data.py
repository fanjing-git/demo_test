# encoding: utf-8
# @File  : leave_request_data.py

# 新建请假申请数据模型
from dataclasses import dataclass
from typing import Optional


@dataclass
class LeaveRequestData:
    """新建请假申请数据模型，只装值，不涉及定位器"""
    student_no: Optional[str] = None
    leave_type: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    text: Optional[str] = None
