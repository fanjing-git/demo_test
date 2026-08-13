# encoding: utf-8
# @File  : ui_assertions.py
# @Author: Fan Jing
# @Date  : 2026/08/13/16:14

# 这是断言的封装

import re
import time
from loguru import logger
from typing import Any, List, Dict, Optional, Union
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeout, expect
from common.handle_path import screenshot_path


class UIAssertions:
    """
    UI断言工具类 - 专门针对UI自动化项目（Playwright版本）

    设计原则：
    1. 使用 Playwright expect 实现自动轮询等待
    2. 支持 str 和 Locator 两种参数类型
    3. 失败时自动截图
    4. 支持数据库断言、Console 监控等扩展功能

    使用方式：在测试用例中调用，页面类中不做断言
    """

    def __init__(self, page: Page = None, timeout: int = 10):
        self.page = page
        self.timeout = timeout
        self._validation_errors = []
        self._validation_passed = True
        self._screenshot_path = None
        self._screenshot_on_fail = True
        # Console 错误收集列表（通过 page.on('console') 事件收集）
        self._console_messages: List[Dict] = []

    # ==================== 辅助方法 ====================

    def _get_locator(self, locator: Union[str, Locator], frame=None) -> Locator:
        """将 str 或 Locator 统一转为 Locator。
        传入 frame（FrameLocator）时，在该 frame 内部查找，而不是默认的顶层 page——
        用于断言目标在嵌套 iframe 里的场景（比如弹窗内的元素）。"""
        if isinstance(locator, str):
            target = frame if frame is not None else self.page
            return target.locator(locator)
        return locator

    def _get_timeout(self, timeout: int = None) -> int:
        """获取超时时间（毫秒）"""
        return (timeout if timeout is not None else self.timeout) * 1000

    def _assert_true(self, condition: bool, message: str):
        """内部断言：条件为 True"""
        if not condition:
            raise AssertionError(message)

    def _log_assert_result(self, passed: bool, expected, actual):
        """统一格式打断言结果日志：True/False + 预期结果 vs 实际结果，
        全部高亮，看日志/Allure报告时一眼就能扫出这条断言比对了什么、
        通没通过。expected/actual 要先转义 '<'——失败时 actual 常常是
        Playwright 异常信息，里面会带元素的原始HTML（比如 <div id="x">），
        不转义的话会被 loguru 的颜色标签解析器当成未闭合标签，直接抛
        ValueError 把真正的断言失败信息炸没。"""
        expected_safe = str(expected).replace("<", "\\<")
        actual_safe = str(actual).replace("<", "\\<")
        if passed:
            logger.opt(colors=True).info(
                f"断言结果为:<green>True</green>，预期结果：<yellow>{expected_safe}</yellow> vs "
                f"实际结果：<magenta>{actual_safe}</magenta>，<green>用例断言通过</green>"
            )
        else:
            logger.opt(colors=True).info(
                f"断言结果为:<red>False</red>，预期结果：<yellow>{expected_safe}</yellow> vs "
                f"实际结果：<magenta>{actual_safe}</magenta>，<red>用例断言失败</red>"
            )

    def _assert_equal(self, actual: Any, expected: Any, message: str):
        """内部断言：值相等"""
        if actual != expected:
            raise AssertionError(f"{message}：期望 {expected}，实际 {actual}")

    def _wait_until(self, condition_func, timeout: int = None):
        """等待条件满足"""
        end_time = time.time() + (timeout or self.timeout)
        while time.time() < end_time:
            if condition_func():
                return
            time.sleep(0.3)
        raise TimeoutError(f"等待条件超时（{timeout or self.timeout}秒）")

    # ==================== 一、元素存在/可见断言 ====================

    def assert_element_visible(self, selector: str, message: str = "", frame=None) -> bool:
        """断言元素可见。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            expect(locator).to_be_visible(timeout=self.timeout * 1000)
            self._log_assert_result(True, "可见", "可见")
            return True
        except Exception as e:
            error_msg = message or f"元素不可见: {selector} - {e}"
            self._log_assert_result(False, "可见", str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            self._take_screenshot("element_not_visible")
            return False

    def assert_element_not_visible(self, selector: str, message: str = "", frame=None) -> bool:
        """断言元素不可见（隐藏/消失）。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            expect(locator).to_be_hidden(timeout=5000)
            self._log_assert_result(True, "不可见", "不可见")
            return True
        except Exception as e:
            error_msg = message or f"元素仍然可见: {selector} - {e}"
            self._log_assert_result(False, "不可见", str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            self._take_screenshot("element_still_visible")
            return False

    def assert_element_exists(self, selector: str, message: str = "", frame=None) -> bool:
        """断言元素存在于DOM中（不一定可见）。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            expect(locator).to_be_attached(timeout=5000)
            self._log_assert_result(True, "存在于DOM", "存在于DOM")
            return True
        except Exception as e:
            error_msg = message or f"元素不存在: {selector} - {e}"
            self._log_assert_result(False, "存在于DOM", str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def assert_element_clickable(self, selector: str, message: str = "", frame=None) -> bool:
        """断言元素可点击（可见且启用）。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            expect(locator).to_be_visible(timeout=self.timeout * 1000)
            expect(locator).to_be_enabled(timeout=self.timeout * 1000)
            self._log_assert_result(True, "可点击", "可点击")
            return True
        except Exception as e:
            error_msg = message or f"元素不可点击: {selector} - {e}"
            self._log_assert_result(False, "可点击", str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            self._take_screenshot("element_not_clickable")
            return False

    def assert_element_enabled(self, selector: str, message: str = "", frame=None) -> bool:
        """断言元素已启用。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            expect(locator).to_be_enabled(timeout=self.timeout * 1000)
            self._log_assert_result(True, "已启用", "已启用")
            return True
        except Exception as e:
            error_msg = message or f"元素未启用: {selector} - {e}"
            self._log_assert_result(False, "已启用", str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def assert_element_disabled(self, selector: str, message: str = "", frame=None) -> bool:
        """断言元素已禁用。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            expect(locator).to_be_disabled(timeout=self.timeout * 1000)
            self._log_assert_result(True, "已禁用", "已禁用")
            return True
        except Exception as e:
            error_msg = message or f"元素未禁用: {selector} - {e}"
            self._log_assert_result(False, "已禁用", str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def assert_element_checked(self, selector: str, message: str = "", frame=None) -> bool:
        """断言复选框/单选框已选中。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            expect(locator).to_be_checked(timeout=self.timeout * 1000)
            self._log_assert_result(True, "已选中", "已选中")
            return True
        except Exception as e:
            error_msg = message or f"元素未选中: {selector} - {e}"
            self._log_assert_result(False, "已选中", str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def assert_element_unchecked(self, selector: str, message: str = "", frame=None) -> bool:
        """断言复选框/单选框未选中。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            expect(locator).not_to_be_checked(timeout=self.timeout * 1000)
            self._log_assert_result(True, "未选中", "未选中")
            return True
        except Exception as e:
            error_msg = message or f"元素已选中: {selector} - {e}"
            self._log_assert_result(False, "未选中", str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    # ==================== 二、文本断言 ====================

    def assert_text(self, selector: str, expected_text: str, message: str = "", frame=None) -> bool:
        """断言元素文本等于预期值。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            expect(locator).to_have_text(expected_text, timeout=self.timeout * 1000)
            self._log_assert_result(True, expected_text, locator.inner_text())
            return True
        except Exception as e:
            error_msg = message or f"文本不符: {e}"
            self._log_assert_result(False, expected_text, str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            self._take_screenshot("text_mismatch")
            return False

    def assert_text_contains(self, selector: str, expected_text: str, message: str = "", frame=None) -> bool:
        """断言元素文本包含预期值。frame 传入时在该嵌套 iframe 内查找（比如弹窗内的提示文案）"""
        try:
            locator = self._get_locator(selector, frame=frame)
            expect(locator).to_contain_text(expected_text, timeout=self.timeout * 1000)
            self._log_assert_result(True, expected_text, locator.inner_text())
            return True
        except Exception as e:
            error_msg = message or f"文本不包含: {e}"
            self._log_assert_result(False, expected_text, str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            self._take_screenshot("text_contains_fail")
            return False

    def assert_text_matches(self, selector: str, pattern: str, message: str = "", frame=None) -> bool:
        """断言元素文本匹配正则表达式。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            expect(locator).to_have_text(re.compile(pattern), timeout=self.timeout * 1000)
            self._log_assert_result(True, pattern, locator.inner_text())
            return True
        except Exception as e:
            error_msg = message or f"文本不匹配正则: {e}"
            self._log_assert_result(False, pattern, str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            self._take_screenshot("text_regex_fail")
            return False

    def assert_text_not_empty(self, selector: str, message: str = "", frame=None) -> bool:
        """断言元素文本不为空。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            expect(locator).not_to_have_text("", timeout=self.timeout * 1000)
            self._log_assert_result(True, "非空", locator.inner_text())
            return True
        except Exception as e:
            error_msg = message or f"文本为空: {e}"
            self._log_assert_result(False, "非空", str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            self._take_screenshot("text_empty")
            return False

    # ==================== 三、属性断言 ====================

    def assert_attribute(self, selector: str, attr_name: str, expected_value: str, message: str = "", frame=None) -> bool:
        """断言元素属性值。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            expect(locator).to_have_attribute(attr_name, expected_value, timeout=self.timeout * 1000)
            self._log_assert_result(True, expected_value, locator.get_attribute(attr_name))
            return True
        except Exception as e:
            error_msg = message or f"属性不符: {e}"
            self._log_assert_result(False, expected_value, str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            self._take_screenshot("attribute_mismatch")
            return False

    def assert_attribute_contains(self, selector: str, attr_name: str, expected_value: str, message: str = "", frame=None) -> bool:
        """断言元素属性包含值。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            actual_value = locator.get_attribute(attr_name) or ""
            self._assert_true(expected_value in actual_value, f"属性不包含: {attr_name}='{actual_value}'")
            self._log_assert_result(True, f"包含'{expected_value}'", actual_value)
            return True
        except Exception as e:
            error_msg = message or f"属性不包含: {e}"
            self._log_assert_result(False, f"包含'{expected_value}'", str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            self._take_screenshot("attribute_contains_fail")
            return False

    def assert_class(self, selector: str, expected_class: str, message: str = "", frame=None) -> bool:
        """断言元素包含某个class。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            expect(locator).to_have_class(expected_class, timeout=self.timeout * 1000)
            self._log_assert_result(True, expected_class, locator.get_attribute("class"))
            return True
        except Exception as e:
            error_msg = message or f"Class不包含: {e}"
            self._log_assert_result(False, expected_class, str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def assert_value(self, selector: str, expected_value: str, message: str = "", frame=None) -> bool:
        """断言输入框的值。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            expect(locator).to_have_value(expected_value, timeout=self.timeout * 1000)
            self._log_assert_result(True, expected_value, locator.input_value())
            return True
        except Exception as e:
            error_msg = message or f"输入框值不符: {e}"
            self._log_assert_result(False, expected_value, str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def assert_placeholder(self, selector: str, expected_text: str, message: str = "", frame=None) -> bool:
        """断言输入框的placeholder。frame 传入时在该嵌套 iframe 内查找"""
        return self.assert_attribute(selector, "placeholder", expected_text, message, frame=frame)

    # ==================== 四、URL/标题断言 ====================

    def assert_url(self, expected_url: str, message: str = "") -> bool:
        """断言当前URL"""
        try:
            expect(self.page).to_have_url(expected_url, timeout=self.timeout * 1000)
            self._log_assert_result(True, expected_url, self.page.url)
            return True
        except Exception as e:
            error_msg = message or f"URL不符: {e}"
            self._log_assert_result(False, expected_url, str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            self._take_screenshot("url_mismatch")
            return False

    def assert_url_contains(self, expected_text: str, message: str = "") -> bool:
        """断言当前URL包含文本"""
        try:
            self._wait_until(lambda: expected_text in self.page.url)
            self._log_assert_result(True, f"包含'{expected_text}'", self.page.url)
            return True
        except Exception as e:
            error_msg = message or f"URL不包含: {e}"
            self._log_assert_result(False, f"包含'{expected_text}'", str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def assert_url_matches(self, pattern: str, message: str = "") -> bool:
        """断言当前URL匹配正则"""
        try:
            expect(self.page).to_have_url(re.compile(pattern), timeout=self.timeout * 1000)
            self._log_assert_result(True, pattern, self.page.url)
            return True
        except Exception as e:
            error_msg = message or f"URL不匹配: {e}"
            self._log_assert_result(False, pattern, str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def assert_title(self, expected_title: str, message: str = "", wait_for_load: bool = True) -> bool:
        """断言页面标题"""
        try:
            expect(self.page).to_have_title(expected_title, timeout=self.timeout * 1000)
            self._log_assert_result(True, expected_title, self.page.title())
            return True
        except Exception as e:
            error_msg = message or f"标题不符: {e}"
            self._log_assert_result(False, expected_title, str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            self._take_screenshot("title_mismatch")
            return False

    def assert_title_contains(self, expected_text: str, message: str = "", wait_for_load: bool = True) -> bool:
        """断言页面标题包含文本"""
        try:
            self._wait_until(lambda: expected_text in self.page.title())
            self._log_assert_result(True, f"包含'{expected_text}'", self.page.title())
            return True
        except Exception as e:
            error_msg = message or f"标题不包含: {e}"
            self._log_assert_result(False, f"包含'{expected_text}'", str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    # ==================== 五、数量断言 ====================

    def assert_count(self, selector: str, expected_count: int, message: str = "", frame=None) -> bool:
        """断言元素数量。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            expect(locator).to_have_count(expected_count, timeout=self.timeout * 1000)
            self._log_assert_result(True, expected_count, locator.count())
            return True
        except Exception as e:
            error_msg = message or f"数量不符: {e}"
            self._log_assert_result(False, expected_count, str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def assert_count_greater(self, selector: str, expected_count: int, message: str = "", frame=None) -> bool:
        """断言元素数量大于某个值。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            actual_count = locator.count()
            self._assert_true(actual_count > expected_count, f"数量 {actual_count} 不大于 {expected_count}")
            self._log_assert_result(True, f"> {expected_count}", actual_count)
            return True
        except Exception as e:
            error_msg = message or f"数量不大于: {e}"
            self._log_assert_result(False, f"> {expected_count}", str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def assert_count_less(self, selector: str, expected_count: int, message: str = "", frame=None) -> bool:
        """断言元素数量小于某个值。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            actual_count = locator.count()
            self._assert_true(actual_count < expected_count, f"数量 {actual_count} 不小于 {expected_count}")
            self._log_assert_result(True, f"< {expected_count}", actual_count)
            return True
        except Exception as e:
            error_msg = message or f"数量不小于: {e}"
            self._log_assert_result(False, f"< {expected_count}", str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def assert_count_between(self, selector: str, min_count: int, max_count: int, message: str = "", frame=None) -> bool:
        """断言元素数量在区间内。frame 传入时在该嵌套 iframe 内查找"""
        try:
            locator = self._get_locator(selector, frame=frame)
            actual_count = locator.count()
            self._assert_true(min_count <= actual_count <= max_count,
                              f"数量 {actual_count} 不在 [{min_count}, {max_count}]")
            self._log_assert_result(True, f"[{min_count}, {max_count}]", actual_count)
            return True
        except Exception as e:
            error_msg = message or f"数量不在区间: {e}"
            self._log_assert_result(False, f"[{min_count}, {max_count}]", str(e))
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    # ==================== 六、弹窗/消息断言 ====================

    def assert_toast_message(self, expected_text: str, timeout: int = 5, message: str = "") -> bool:
        """
        断言Toast提示消息

        Args:
            expected_text: 期望的Toast文本
            timeout: 等待时间（秒）
        """
        toast_selectors = [
            ".toast",
            ".ant-message",
            ".el-message",
            ".toast-message",
            "[class*='message']",
        ]

        for selector in toast_selectors:
            try:
                locator = self.page.locator(selector)
                locator.wait_for(state="visible", timeout=timeout * 1000)
                actual_text = locator.text_content() or ""
                if expected_text in actual_text.strip():
                    logger.info(f"✅ Toast消息匹配: '{actual_text.strip()}'")
                    return True
            except:
                continue

        error_msg = message or f"Toast消息未找到: '{expected_text}'"
        logger.error(f"❌ {error_msg}")
        self._validation_errors.append(error_msg)
        self._validation_passed = False
        self._take_screenshot("toast_not_found")
        return False

    def assert_alert_text(self, expected_text: str, message: str = "") -> bool:
        """
        断言Alert弹窗文本

        注意：Playwright 中 dialog 是同步处理的，需要在触发 dialog 的操作之前注册监听。
        此方法适用于已经弹出的 dialog，通过 page 的 dialog 事件获取文本。
        """
        try:
            with self.page.expect_event("dialog", timeout=5000) as dialog_info:
                pass
            dialog = dialog_info.value
            actual_text = dialog.message
            if expected_text in actual_text:
                logger.info(f"✅ Alert匹配: '{actual_text}'")
                dialog.accept()
                return True
            else:
                dialog.accept()
                raise Exception(f"实际: '{actual_text}'")
        except Exception as e:
            error_msg = message or f"Alert不匹配: {e}"
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def assert_error_message(self, expected_text: str, message: str = "") -> bool:
        """
        断言错误提示信息

        Example:
            self.assert_error_message("用户名或密码错误")
        """
        error_selectors = [
            ".error",
            ".error-message",
            ".alert-danger",
            ".ant-message-error",
            ".el-message--error",
            ".error-text",
            "[class*='error']",
        ]

        for selector in error_selectors:
            try:
                locator = self.page.locator(selector)
                locator.wait_for(state="visible", timeout=3000)
                actual_text = locator.text_content() or ""
                if expected_text in actual_text.strip():
                    logger.info(f"✅ 错误消息匹配: '{actual_text.strip()}'")
                    return True
            except:
                continue

        error_msg = message or f"错误消息未找到: '{expected_text}'"
        logger.error(f"❌ {error_msg}")
        self._validation_errors.append(error_msg)
        self._validation_passed = False
        self._take_screenshot("error_not_found")
        return False

    # ==================== 七、表格/列表断言 ====================

    def assert_table_row_count(self, table_selector: str, expected_count: int, message: str = "") -> bool:
        """断言表格行数"""
        try:
            table_locator = self.page.locator(table_selector)
            table_locator.wait_for(state="visible", timeout=self.timeout * 1000)
            rows = table_locator.locator("tr").all()
            actual_count = len(rows) - 1  # 减去表头
            if actual_count == expected_count:
                logger.info(f"✅ 表格行数匹配: {actual_count}")
                return True
            else:
                raise Exception(f"实际: {actual_count}")
        except Exception as e:
            error_msg = message or f"表格行数不符: {e}"
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def assert_table_cell_text(self, table_selector: str, row: int, col: int,
                               expected_text: str, message: str = "") -> bool:
        """断言表格某个单元格的文本"""
        try:
            table_locator = self.page.locator(table_selector)
            table_locator.wait_for(state="visible", timeout=self.timeout * 1000)
            rows = table_locator.locator("tr").all()
            if row >= len(rows):
                raise Exception(f"行索引超出: {row} >= {len(rows)}")

            cells = rows[row].locator("td").all()
            if col >= len(cells):
                raise Exception(f"列索引超出: {col} >= {len(cells)}")

            actual_text = (cells[col].text_content() or "").strip()
            if actual_text == expected_text:
                logger.info(f"✅ 单元格文本匹配: [{row},{col}] '{actual_text}'")
                return True
            else:
                raise Exception(f"实际: '{actual_text}'")
        except Exception as e:
            error_msg = message or f"单元格文本不符: {e}"
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def assert_list_contains_text(self, item_selector: str, expected_text: str,
                                  message: str = "") -> bool:
        """
        断言列表中某个元素包含指定文本（自动等待元素出现）

        Args:
            item_selector: 列表项选择器字符串
            expected_text: 期望包含的文本

        Example:
            self.assert_list_contains_text(".product-name", "测试商品")
        """
        try:
            locator = self.page.locator(item_selector)
            locator.first.wait_for(state="attached", timeout=self.timeout * 1000)
            elements = locator.all()
            for element in elements:
                text = element.text_content() or ""
                if expected_text in text:
                    logger.info(f"✅ 列表包含: '{expected_text}'")
                    return True
            raise Exception(f"未找到包含 '{expected_text}' 的元素")
        except Exception as e:
            error_msg = message or f"列表不包含: {e}"
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def assert_list_not_contains_text(self, item_selector: str, expected_text: str,
                                      message: str = "") -> bool:
        """断言列表不包含指定文本（自动等待页面加载）"""
        try:
            self.page.wait_for_function("document.readyState === 'complete'", timeout=3000)
            elements = self.page.locator(item_selector).all()
            for element in elements:
                text = element.text_content() or ""
                if expected_text in text:
                    raise Exception(f"找到了包含 '{expected_text}' 的元素")
            logger.info(f"✅ 列表不包含: '{expected_text}'")
            return True
        except Exception as e:
            error_msg = message or f"列表包含: {e}"
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    # ==================== 八、页面状态断言 ====================

    def assert_page_loaded(self, timeout: int = 30, message: str = "") -> bool:
        """断言页面加载完成"""
        try:
            self.page.wait_for_function("document.readyState === 'complete'", timeout=timeout * 1000)
            logger.info("✅ 页面加载完成")
            return True
        except PlaywrightTimeout:
            error_msg = message or "页面加载超时"
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            self._take_screenshot("page_load_timeout")
            return False

    def assert_no_js_errors(self, message: str = "") -> bool:
        """
        断言没有JavaScript错误

        注意：需要先调用 enable_console_monitoring() 开启监听，
        否则无法获取到控制台错误信息。
        """
        errors = [msg for msg in self._console_messages if msg.get('level') == 'error']
        if errors:
            error_msg = f"发现 {len(errors)} 个JS错误: {errors[0].get('text', '')[:200]}"
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False
        logger.info("✅ 无JS错误")
        return True

    def assert_no_white_screen(self, message: str = "") -> bool:
        """断言页面没有白屏"""
        try:
            body = self.page.locator("body")
            if not body.is_visible():
                raise Exception("body不可见")

            body_text = (body.text_content() or "").strip()
            if not body_text:
                raise Exception("body文本为空")

            logger.info("✅ 页面非白屏")
            return True
        except Exception as e:
            error_msg = message or f"页面白屏: {e}"
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            self._take_screenshot("white_screen")
            return False

    # ==================== 九、数据库断言 ====================

    def assert_db_record(self, db, table: str, where: Dict = None, expected: Dict = None,
                         fetch_num: int = 1, message: str = "") -> bool:
        """
        数据库断言 - 验证数据库记录是否符合预期

        参照接口自动化的数据库断言方式，适配UI自动化场景。
        用于UI操作后验证数据是否真正写入/更新/删除到了数据库。

        Args:
            db: HandleDB 实例
            table: 表名
            where: 查询条件字典，如 {"phone": "123", "status": 1}
            expected: 期望的字段值字典，如 {"status": 1, "name": "test"}
            fetch_num: 1=返回一条(dict), 2=返回多条(list), 0=返回全部
            message: 自定义错误信息
        """
        try:
            logger.info("=" * 50)
            logger.info("📦 开始数据库断言")

            sql = db.build_sql(table, where)
            logger.info(f"自动生成SQL：{sql}")
            db_result = db.select_sql(sql, fetch_num=fetch_num)

            if db_result is None:
                error_msg = message or f"数据库查询结果为空，表：{table}，条件：{where}"
                logger.error(f"❌ {error_msg}")
                self._validation_errors.append(error_msg)
                self._validation_passed = False
                return False

            logger.info(f"数据库查询结果：{db_result}")

            if not expected:
                logger.info(f"✅ 验证通过：数据库中存在匹配数据（表：{table}）")
                return True

            if isinstance(db_result, dict):
                self._validate_db_row(db_result, expected, path="db_result")
            elif isinstance(db_result, list):
                logger.info(f"数据库返回 {len(db_result)} 条记录，逐条验证")
                for idx, row in enumerate(db_result):
                    self._validate_db_row(row, expected, path=f"db_result[{idx}]")

            logger.info("✅ 数据库断言验证通过")
            return True

        except AssertionError:
            raise
        except Exception as e:
            error_msg = message or f"数据库断言失败：{e}"
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            self._take_screenshot("db_assert_fail")
            return False

    def assert_db_exists(self, db, table: str, where: Dict = None, message: str = "") -> bool:
        """数据库断言 - 验证数据是否存在"""
        return self.assert_db_record(db, table, where, expected=None, fetch_num=1, message=message)

    def assert_db_not_exists(self, db, table: str, where: Dict = None, message: str = "") -> bool:
        """
        数据库断言 - 验证数据是否不存在
        用于UI删除操作后验证数据已从数据库删除
        """
        try:
            logger.info("=" * 50)
            logger.info("📦 数据库断言 - 验证数据不存在")

            sql = db.build_sql(table, where)
            logger.info(f"自动生成SQL：{sql}")
            db_result = db.select_sql(sql, fetch_num=1)

            if db_result is None:
                logger.info(f"✅ 验证通过：数据库中不存在匹配数据（表：{table}）")
                return True
            else:
                error_msg = message or f"数据库中仍存在匹配数据，表：{table}，条件：{where}"
                logger.error(f"❌ {error_msg}")
                self._validation_errors.append(error_msg)
                self._validation_passed = False
                self._take_screenshot("db_data_still_exists")
                return False

        except Exception as e:
            error_msg = message or f"数据库断言失败：{e}"
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def assert_db_field(self, db, table: str, where: Dict, field: str, expected_value=None,
                        message: str = "") -> bool:
        """数据库断言 - 验证某个字段的值"""
        return self.assert_db_record(db, table, where, expected={field: expected_value},
                                     fetch_num=1, message=message)

    def assert_db_count(self, db, table: str, where: Dict = None, expected_count: int = None,
                        min_count: int = None, max_count: int = None, message: str = "") -> bool:
        """数据库断言 - 验证记录数量"""
        try:
            logger.info("=" * 50)
            logger.info("📦 数据库断言 - 验证记录数量")

            sql = db.build_sql(table, where)
            count_sql = sql.replace("SELECT *", "SELECT COUNT(*) as cnt")
            if "LIMIT" in count_sql:
                count_sql = count_sql[:count_sql.index("LIMIT")]

            logger.info(f"统计SQL：{count_sql}")
            result = db.select_sql(count_sql, fetch_num=1)
            actual_count = result.get("cnt", 0) if result else 0

            if expected_count is not None:
                if actual_count == expected_count:
                    logger.info(f"✅ 数量匹配: {actual_count} == {expected_count}")
                    return True
                else:
                    raise Exception(f"实际: {actual_count}, 期望: {expected_count}")

            if min_count is not None and max_count is not None:
                if min_count <= actual_count <= max_count:
                    logger.info(f"✅ 数量在区间: {actual_count} in [{min_count}, {max_count}]")
                    return True
                else:
                    raise Exception(f"实际: {actual_count}, 期望区间: [{min_count}, {max_count}]")

            if min_count is not None:
                if actual_count >= min_count:
                    logger.info(f"✅ 数量 >= {min_count}: {actual_count}")
                    return True
                else:
                    raise Exception(f"实际: {actual_count}, 期望 >= {min_count}")

            logger.info(f"✅ 数据库记录数：{actual_count}")
            return True

        except AssertionError:
            raise
        except Exception as e:
            error_msg = message or f"数据库数量断言失败：{e}"
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            return False

    def _validate_db_row(self, row: Dict, expected: Dict, path: str = "db_result"):
        """验证单条数据库记录的字段值（内部方法）"""
        logger.info(f"开始验证数据库记录 {path} 包含 {len(row)} 个字段")

        for key, value in row.items():
            logger.info(f"  📋 {path}.{key} = {value}")

        for key, expected_value in expected.items():
            actual_value = row.get(key)

            if key not in row:
                error_msg = f"数据库记录中不存在字段：{key}"
                logger.error(f"❌ {error_msg}")
                self._validation_errors.append(error_msg)
                self._validation_passed = False
                raise AssertionError(error_msg)

            logger.info(f"检查数据库字段：{path}.{key} 期望={expected_value}, 实际={actual_value}")

            if actual_value != expected_value:
                try:
                    if str(actual_value) == str(expected_value):
                        logger.warning(f"字段 {key} 值匹配（字符串比较）：期望={expected_value}, 实际={actual_value}")
                        continue
                except Exception:
                    pass
                error_msg = f"数据库字段 {key} 不匹配：期望={expected_value}, 实际={actual_value}"
                logger.error(f"❌ {error_msg}")
                self._validation_errors.append(error_msg)
                self._validation_passed = False
                raise AssertionError(error_msg)

        logger.info(f"✅ 数据库记录 {path} 验证通过")

    # ==================== 十、Console 控制台监控 ====================

    def enable_console_monitoring(self, raise_on_error: bool = False) -> 'UIAssertions':
        """
        启用 Console 监控 - 开启后通过 page.on('console') 事件监听控制台消息

        Args:
            raise_on_error: 发现控制台错误时是否抛出异常（默认False，只记录不中断）
        """
        self._console_monitoring_enabled = True
        self._raise_on_console_error = raise_on_error
        self._console_messages = []
        self.page.on("console", lambda msg: self._collect_console_message(msg))
        logger.info("🔍 Console 监控已启用")
        return self

    def disable_console_monitoring(self) -> 'UIAssertions':
        """关闭 Console 监控"""
        self._console_monitoring_enabled = False
        logger.info("🔇 Console 监控已关闭")
        return self

    def _collect_console_message(self, msg):
        """收集 Console 消息（内部回调方法）"""
        self._console_messages.append({
            'level': msg.type,
            'text': msg.text,
        })
        if hasattr(self, '_raise_on_console_error') and self._raise_on_console_error and msg.type == 'error':
            raise Exception(f"Console 错误: {msg.text[:200]}")

    def _check_console_errors_after_action(self):
        """操作后自动检查 Console 错误（内部调用，由 click/input 触发）"""
        errors = [msg for msg in self._console_messages if msg.get('level') == 'error']

        if errors:
            logger.error(f"⚠️ 检测到 {len(errors)} 个 Console 错误")
            for error in errors[:5]:
                logger.error(f"   🔴 {error.get('text', '')[:300]}")
            self._take_screenshot("console_error_detected")
            if hasattr(self, '_raise_on_console_error') and self._raise_on_console_error:
                raise Exception(f"Console 错误: {errors[0].get('text', '')[:200]}")
            return False
        else:
            logger.debug("✅ 无 Console 错误")
            return True

    def get_console_errors(self) -> List:
        """获取所有 Console 错误"""
        return [msg for msg in self._console_messages if msg.get('level') == 'error']

    def get_console_warnings(self) -> List:
        """获取所有 Console 警告"""
        return [msg for msg in self._console_messages if msg.get('level') == 'warning']

    def clear_console_logs(self) -> 'UIAssertions':
        """清空已收集的 Console 消息"""
        self._console_messages = []
        logger.info("🧹 Console 日志已清空")
        return self

    def assert_no_console_errors(self, message: str = "") -> bool:
        """断言没有 Console 错误（增强版），会显示所有错误的详细信息"""
        errors = self.get_console_errors()
        if errors:
            error_details = []
            for i, error in enumerate(errors[:5], 1):
                error_details.append(f"  {i}. {error.get('text', '')[:200]}")
            error_msg = message or f"发现 {len(errors)} 个 Console 错误:\n" + "\n".join(error_details)
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            self._validation_passed = False
            self._take_screenshot("console_errors")
            return False
        else:
            logger.info("✅ 无 Console 错误")
            return True

    def assert_no_console_warnings(self, message: str = "") -> bool:
        """断言没有 Console 警告"""
        warnings = self.get_console_warnings()
        if warnings:
            error_msg = message or f"发现 {len(warnings)} 个 Console 警告"
            logger.warning(f"⚠️ {error_msg}")
            return False
        else:
            logger.info("✅ 无 Console 警告")
            return True

    def assert_console_contains_error(self, expected_text: str, message: str = "") -> bool:
        """断言 Console 中包含特定错误"""
        errors = self.get_console_errors()
        for error in errors:
            if expected_text in error.get('text', ''):
                logger.info(f"✅ 找到 Console 错误: {expected_text}")
                return True
        error_msg = message or f"Console 中未找到错误: {expected_text}"
        logger.error(f"❌ {error_msg}")
        self._validation_errors.append(error_msg)
        self._validation_passed = False
        return False

    def get_console_report(self) -> Dict:
        """获取完整的 Console 报告"""
        errors = self.get_console_errors()
        warnings = self.get_console_warnings()
        info_msgs = [msg for msg in self._console_messages if msg.get('level') == 'info']
        return {
            'total_logs': len(self._console_messages),
            'errors': len(errors),
            'warnings': len(warnings),
            'info': len(info_msgs),
            'error_details': errors[:10],
            'warning_details': warnings[:10]
        }

    # ==================== 十一、截图工具 ====================

    def _take_screenshot(self, name):
        """截图（内部使用），返回截图字节数据并附加到 Allure"""
        try:
            screenshot_bytes = self.page.screenshot(full_page=True)
            logger.info(f"📸 截图完成：{name}")
            try:
                import allure
                allure.attach(
                    screenshot_bytes,
                    name=name,
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass
            self._screenshot_path = name
            return screenshot_bytes
        except Exception as e:
            logger.error(f"截图失败：{e}")
            return None

    # ==================== 十二、断言结果管理 ====================

    def get_validation_results(self) -> Dict:
        """获取所有校验结果"""
        return {
            'passed': self._validation_passed,
            'total_errors': len(self._validation_errors),
            'errors': self._validation_errors,
            'screenshot': self._screenshot_path
        }

    def clear_validation_results(self):
        """清空校验结果"""
        self._validation_errors = []
        self._validation_passed = True
        self._screenshot_path = None
        logger.info("🧹 已清空校验结果")

    def raise_if_validation_failed(self):
        """如果校验失败，抛出异常"""
        if not self._validation_passed:
            error_msg = f"断言失败，共 {len(self._validation_errors)} 个错误:\n" + "\n".join(self._validation_errors)
            raise AssertionError(error_msg)

    def get_all_errors(self) -> List[str]:
        """获取所有错误信息"""
        return self._validation_errors

    def has_errors(self) -> bool:
        """是否有错误"""
        return len(self._validation_errors) > 0
