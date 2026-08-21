# encoding: utf-8
# @File  : base_page_object.py
# @Author: Fan Jing
# @Date  : 2026/08/13/15:30

# 这是该项目的基类文件，用于定义一些公共的方法

from loguru import logger
from playwright.sync_api import Page

from common.ui_assertions import UIAssertions
from config.env_config import DEFAULT_TIMEOUT


class BasePage(UIAssertions):
    def __init__(self, page: Page):
        super().__init__(page=page, timeout=DEFAULT_TIMEOUT)
        logger.info("初始化BasePage类")
        self.page.set_default_timeout(self.timeout * 1000)
        self.page.set_default_navigation_timeout(self.timeout * 1000)

    # 封装元素的查找方法
    def find_element(self, locator, timeout=None):
        logger.info(f"查找元素：{locator}")
        element = self.page.locator(locator)
        wait_timeout = (timeout or self.timeout) * 1000
        element.wait_for(state='visible', timeout=wait_timeout)
        logger.info(f"元素可见：{locator}")
        self.locator_station(element)
        return element

    # 封装查找多个元素的方法（返回 Locator 列表）
    def find_elements(self, locator, timeout=None):
        logger.info(f"查找多个元素：{locator}")
        elements = self.page.locator(locator)
        wait_timeout = (timeout or self.timeout) * 1000
        elements.first.wait_for(state='visible', timeout=wait_timeout)
        logger.info(f"元素可见：{locator}")
        return elements

    # 封装元素高亮的显示
    def locator_station(self, locator):
        """
        高亮显示元素边框（绿色）
        Playwright 用 locator.evaluate() 直接操作
        """
        try:
            locator.evaluate(
                "el => el.style.border = '2px solid green'"
            )
        except Exception as e:
            logger.warning(f"元素高亮失败：{e}")

    # 封装打开浏览器的方法
    def open_browser(self, url):
        self.page.goto(url)
        logger.info(f"打开浏览器：{url}")

    # 获取当前页面 URL
    def get_current_url(self):
        return self.page.url

    # 封装元素输入的方法
    def input_text(self, locator, text):
        self.find_element(locator).fill(text)
        logger.info(f"输入文本：{text}")

    # 封装元素点击的方法
    def click_element(self, locator):
        self.find_element(locator).click()
        logger.info(f"点击元素：{locator}")

    # 封装获取元素属性的方法
    def get_element_attribute(self, locator, attribute):
        logger.info(f"获取元素属性：{attribute}")
        return self.find_element(locator).get_attribute(attribute)

    # 封装滚动到元素的方法
    def scroll_to_element(self, locator):
        self.find_element(locator).scroll_into_view_if_needed()
        logger.info(f"滚动到元素：{locator}")

    # 封装获取元素文本的方法
    def get_element_text(self, locator):
        logger.info(f"获取元素文本：{locator}")
        return self.find_element(locator).text_content()

    # 封装切换新窗口/标签页的方法（基于 Playwright expect_popup）
    def switch_to_new_window(self, locator):
        logger.info(f"点击元素并等待新窗口：{locator}")
        with self.page.expect_popup() as popup_info:
            self.find_element(locator).click()
        new_page = popup_info.value
        logger.info(f"已切换到新窗口：{new_page.url}")
        return new_page

    # 封装多层iframe嵌套的方法（基于 Playwright frame_locator）
    def switch_to_frame(self, locator):
        logger.info(f"切换到iframe：{locator}")
        frame = self.page.frame_locator(locator)
        return frame

    # 封装文件上传的方法
    def upload_file(self, locator, file_path):
        logger.info(f"上传文件：{file_path}")
        with self.page.expect_file_chooser() as file_chooser_info:
            self.find_element(locator).click()
        file_chooser = file_chooser_info.value
        file_chooser.set_files(file_path)

    # 封装下拉框的方法
    def select_dropdown(self, locator, option):
        logger.info(f"选择下拉框选项：{option}")
        self.find_element(locator).select_option(option)

    # 封装截图方法（失败时调用，自动 attach 到 Allure 报告）
    def take_screenshot(self, name="error"):
        import time
        from common.handle_path import screenshot_path
        import os
        os.makedirs(screenshot_path, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(screenshot_path, f"{name}_{timestamp}.png")
        self.page.screenshot(path=file_path, full_page=True)
        logger.info(f"截图保存：{file_path}")
        # attach 到 Allure 报告
        try:
            import allure
            allure.attach(
                self.page.screenshot(),
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass
        return file_path

    # 封装原生弹窗点击确认的方法
    def handle_dialog(self,accept: bool = True):
        """
       注册一次性弹窗处理器，用于处理点击后触发的浏览器原生 confirm/alert 弹窗
       :param accept: True=点确定(accept)，False=点取消(dismiss)
       :注意: 必须在触发弹窗的点击动作之前调用，因为这是"预先注册下一次弹窗怎么处理"，
             弹窗是浏览器原生UI，不在页面DOM里，无法用 locator 找到"确定/取消"按钮
       """
        if accept:
            self.page.once("dialog",lambda djalog: djalog.accept())
            logger.info("已注册弹窗处理：下一次弹窗将自动点击确认")
        else:
            self.page.once("dialog" , lambda  dialog: dialog.dismiss())
            logger.info("已注册弹窗处理：下一次弹窗将自动点击取消")