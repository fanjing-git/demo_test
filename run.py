# encoding: utf-8
# @File  : run.py
# @Author: Fan Jing
# @Date  : 2026/07/10/11:45

import os
import shutil

import pytest
from allure_combine import combine_allure
from loguru import logger

from common.handle_path import *
from report_dashboard.build import build as build_dashboard

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
    logger.info(f"allure 报告目录：{report_path}")

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

    # 把上一次报告的 history 拷贝回 allure-results，这样即使每次都清空
    # allure-results，趋势图（通过率随时间变化）依然能跨多次运行累积。
    # allure-results 本身的清空（--clean-alluredir）不受影响，测试结果照常是全新的。
    prev_history = report_path / 'history'
    if prev_history.is_dir():
        dest_history = os.path.join('allure-results', 'history')
        shutil.copytree(prev_history, dest_history, dirs_exist_ok=True)
        logger.info("已拷贝上一次报告的 history 目录，趋势数据将继续累积")

    # 生成 allure 报告（保持原有命令不变）
    print("\n📊 正在生成 Allure 测试报告...")
    logger.info("开始生成 Allure 报告")

    generate_result = os.system(f'allure generate -c -o {report_path}')

    if generate_result == 0:
        logger.info("✅ Allure 报告生成成功")
    else:
        logger.error("❌ Allure 报告生成失败")

    # 合并 allure 报告（保持原有调用不变）。必须在生成自定义仪表盘之前合并：
    # combine_allure 要读原始的 index.html/app.js/styles.css 拼出 complete.html，
    # 仪表盘接下来会直接覆盖 index.html，晚了 combine_allure 就读不到原始内容了。
    logger.info("开始合并 Allure 报告")
    combine_allure(str(report_path))
    logger.info("✅ Allure 报告合并完成")

    # 生成自定义仪表盘首页（概览 + 模块树 + 失败详情，含失败截图预览），
    # 直接覆盖 index.html，这样打开报告文件夹默认看到的就是这个仪表盘；
    # 原生报告仍可通过 complete.html 查看（仪表盘左下角也有跳转链接）。
    print("\n🎨 正在生成自定义测试报告仪表盘...")
    logger.info("开始生成自定义仪表盘")
    try:
        dashboard_file = build_dashboard(report_path)
        logger.info(f"✅ 仪表盘生成成功：{dashboard_file}")
    except Exception as e:
        dashboard_file = None
        logger.error(f"❌ 仪表盘生成失败：{e}")

    # 记录报告信息
    report_abs = str(report_path.resolve())
    index_html = os.path.join(report_abs, 'index.html')
    complete_html = os.path.join(report_abs, 'complete.html')

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
    print(f"   2. 需要看原生 Allure 报告（时间轴/分类等更多页面）：打开 {complete_html}")
    print(f"   3. 分享给同事：打包整个 allure_reports 文件夹")
    print(f"   4. 启动服务（可选）：allure serve allure-results --host 0.0.0.0 --port 7888")
    print(f"\n📝 日志文件位置：{log_path}")
    print("=" * 60 + "\n")


