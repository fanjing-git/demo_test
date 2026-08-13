# encoding: utf-8
# @File  : conftest.py
# @Author: Fan Jing
# @Date  : 2026/08/13/16:23

import time
import allure
import os
import pytest
from playwright.sync_api import sync_playwright
from loguru import logger
from pages.login.login_page import LoginPage
from config.env_config import LOGIN_URL, LOGIN_USERNAME, LOGIN_PASSWORD

# ==================== 页面级别 fixture（支持多浏览器） ====================
BROWSER_DEBUG = os.getenv("PW_BROWSER", "chromium")


@pytest.fixture(
    scope="function",
    params=[
        {"browser_name": "chromium", "headless": False},
        {"browser_name": "firefox", "headless": False},
        {"browser_name": "webkit", "headless": False}
    ] if not BROWSER_DEBUG else [{"browser_name": BROWSER_DEBUG, "headless": False}],
    ids=["Chromium", "Firefox", "WebKit"] if not BROWSER_DEBUG else [BROWSER_DEBUG]
)
def page(request):
    browser_config = request.param
    browser_name = browser_config["browser_name"]
    headless = browser_config.get("headless", False)

    logger.info(f"🚀 正在启动 {browser_name} 浏览器...")

    pw = sync_playwright().start()

    if browser_name == "chromium":
        browser = pw.chromium.launch(
            headless=headless,
            slow_mo=100,
            args=["--start-maximized"]
        )
    elif browser_name == "firefox":
        browser = pw.firefox.launch(
            headless=headless,
            slow_mo=100,
            args=["--start-maximized"]
        )
    elif browser_name == "webkit":
        browser = pw.webkit.launch(
            headless=headless,
            slow_mo=100
        )
    else:
        raise ValueError(f"不支持的浏览器: {browser_name}")

    context = browser.new_context(
        no_viewport=True,
        ignore_https_errors=True
    )
    page = context.new_page()
    logger.info(f"✅ {browser_name} 浏览器已启动，页面已创建")

    yield page

    # ==================== teardown：测试用例结束后执行 ====================
    logger.info(f"🧹 [teardown 开始] 测试用例结束，开始清理...")
    try:
        if not page.is_closed():
            page.close()
            logger.info("📄 页面已关闭")
    except Exception as e:
        logger.warning(f"关闭页面异常: {e}")

    try:
        context.close()
        logger.info("📦 上下文已关闭")
    except Exception as e:
        logger.warning(f"关闭上下文异常: {e}")

    try:
        browser.close()
        logger.info("🌐 浏览器已关闭")
    except Exception as e:
        logger.warning(f"关闭浏览器异常: {e}")

    try:
        pw.stop()
        logger.info(f"🔒 [teardown 完成] {browser_name} 所有资源已释放")
    except Exception as e:
        logger.warning(f"停止 playwright 异常: {e}")


# ==================== 测试失败自动截图并附加到 Allure 报告 ====================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试用例执行结果钩子
    作用：测试失败时自动截图，并把截图附加到 Allure 报告中
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        try:
            page = item.funcargs.get("page")
            if page and not page.is_closed():
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                browser_name = item.funcargs.get("browser_name", "unknown")
                screenshot_name = f"fail_{item.name}_{browser_name}_{timestamp}"

                screenshot_bytes = page.screenshot(full_page=True)

                allure.attach(
                    screenshot_bytes,
                    name=f"失败截图_{screenshot_name}",
                    attachment_type=allure.attachment_type.PNG
                )
                logger.info(f"📸 测试失败截图已附加到 Allure 报告")
        except Exception as e:
            logger.error(f"截图失败: {e}")


@pytest.fixture(scope="function")
def logged_in_page(page):
    """登录成功的 page，供后续所有用例使用"""
    login_page = LoginPage(page)
    login_page.login(LOGIN_URL, LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_SECURITY_CODE)
    assert "login.html" not in page.url
    yield page
    logger.info("登录fixture teardown完成，测试结束")
