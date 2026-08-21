# encoding: utf-8
# @File  : run.py
# @Author: Fan Jing
# @Date  : 2026/07/10/11:45

import os

import pytest
from allure_combine import combine_allure
from loguru import logger

from common.handle_path import *

# 配置日志
logger.add(sink=log_path,
           encoding='utf-8',
           level="INFO",
           rotation="1day",
           retention=3000)

if __name__ == '__main__':
    # 记录开始执行
    logger.info("=" * 60)
    logger.info("开始执行自动化测试")
    logger.info(f"项目根目录：{os.path.dirname(os.path.abspath(__file__))}")
    logger.info(f"allure 数据目录：allure-results")

    print("\n" + "=" * 60)
    print("🚀 开始执行测试用例...")
    print("=" * 60 + "\n")

    # 执行 pytest（保持原有参数不变）
    pytest_args = ['-v', '-s', '--capture=sys',
                   './test_case/',
                   '--clean-alluredir',
                   '--alluredir=allure-results'
                   ]

    logger.info(f"pytest 参数：{pytest_args}")
    result = pytest.main(pytest_args)

    # 记录执行结果
    if result == 0:
        logger.info("✅ 测试用例执行成功")
    else:
        logger.warning(f"⚠️ 测试用例执行完成，返回码：{result}")

    # 生成 allure 报告（保持原有命令不变）
    print("\n📊 正在生成 Allure 测试报告...")
    logger.info("开始生成 Allure 报告")

    generate_result = os.system('allure generate -c -o allure_report')

    if generate_result == 0:
        logger.info("✅ Allure 报告生成成功")
    else:
        logger.error("❌ Allure 报告生成失败")

    # 合并 allure 报告（保持原有调用不变）
    logger.info("开始合并 Allure 报告")
    combine_allure('allure_report')
    logger.info("✅ Allure 报告合并完成")

    # 记录报告信息
    report_abs = os.path.abspath('allure_report')
    index_html = os.path.join(report_abs, 'index.html')

    logger.info("=" * 60)
    logger.info("测试报告生成完成")
    logger.info(f"报告路径：{report_abs}")
    logger.info(f"报告文件：{index_html}")
    if os.path.exists(index_html):
        logger.info(f"文件大小：{os.path.getsize(index_html) / 1024:.2f} KB")
    logger.info("=" * 60)

    # 打印总结信息
    print("\n" + "=" * 60)
    print("✅ 测试报告生成完成！")
    print("=" * 60)
    print(f"\n📊 报告位置：{report_abs}")
    print(f"\n💡 使用说明：")
    print(f"   1. 本地查看：双击打开 {index_html}")
    print(f"   2. 分享给同事：打包整个 allure_report 文件夹")
    print(f"   3. 启动服务（可选）：allure serve allure-results --host 0.0.0.0 --port 7888")
    print(f"\n📝 日志文件位置：{log_path}")
    print("=" * 60 + "\n")

