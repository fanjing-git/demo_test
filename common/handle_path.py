# encoding: utf-8
# @File  : handle_path.py
# @Author: Fan Jing
# @Date  : 2026/08/13/16:18

# 所有项目路径的处理
from datetime import datetime
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 文件上传路径
upload_file_path = BASE_DIR / 'image' / 'Snipaste_2026-04-20_14-36-36.png'

# 日志路径
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = BASE_DIR / 'logs' / f'shop{timestamp}.log'

# 报告的路径
report_path = BASE_DIR / 'allure_reports'

# 截图路径
screenshot_path = BASE_DIR / 'data_png'

# 图片路径
image_path = BASE_DIR / 'image'