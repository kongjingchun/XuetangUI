# encoding: utf-8
# @File  : BasePage.py
# @Author: 孔敬淳
# @Date  : 2025/01/13
# @Desc  : 基础页面类，符合 Selenium 官方 Page Object Model 设计模式
"""
BasePage - Selenium Page Object Model 基础类

按照 Selenium 官方文档的最佳实践设计：
1. 封装页面元素和操作
2. 支持返回其他 Page 对象
3. 不包含断言（断言应在测试用例中）
4. 提供页面验证机制
"""

import datetime
import os.path
import time

from selenium.common.exceptions import ElementNotVisibleException, WebDriverException, NoSuchElementException, \
    StaleElementReferenceException, TimeoutException, InvalidSessionIdException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.yaml_config import GetConf
from common.tools import get_project_path, sep
from common.find_img import FindImg
from common.report_add_img import add_img_path_2_report
from logs.log import log


class BasePage:
    """
    BasePage - Selenium Page Object Model 基础类

    这是所有页面对象类的基类，提供通用的页面操作方法。
    符合 Selenium 官方 Page Object Model 设计模式。

    使用示例:
        class LoginPage(BasePage):
            def __init__(self, driver):
                super().__init__(driver)
                # 页面元素定位器
                self.username_locator = (By.ID, "username")
                self.password_locator = (By.ID, "password")
                self.login_button_locator = (By.ID, "login")

            def enter_username(self, username):
                self.input_text(*self.username_locator, username)

            def enter_password(self, password):
                self.input_text(*self.password_locator, password)

            def click_login(self):
                self.click(*self.login_button_locator)
                # 返回下一个页面对象
                return HomePage(self.driver)
    """

    # 类属性：基础URL
    BASE_URL = GetConf().get_url()
    # 类属性：缓存 headless 模式状态，避免重复读取配置
    _headless_mode_cache = None

    def __init__(self, driver):
        """
        初始化 BasePage

        Args:
            driver: WebDriver 实例
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # 默认等待时间10秒

        # 可选：在构造函数中验证页面
        # self._verify_page()

    def _verify_page(self):
        """
        验证当前页面是否正确

        子类可以重写此方法来验证页面是否加载正确。
        如果页面不正确，应该抛出异常。

        Raises:
            Exception: 如果页面验证失败
        """
        pass

    # ==================== 配置相关方法 ====================

    @classmethod
    def _is_headless_mode(cls):
        """
        检查是否使用Headless模式（带缓存机制，避免重复读取配置）

        Returns:
            bool: True表示使用Headless模式，False表示使用有界面模式
        """
        if cls._headless_mode_cache is None:
            try:
                deploy_config = GetConf().get_info("部署环境")
                cls._headless_mode_cache = deploy_config.get("是否Headless模式", False) if deploy_config else False
            except Exception:
                # 如果读取配置失败，默认根据操作系统判断
                import sys
                cls._headless_mode_cache = sys.platform.startswith("linux")
        return cls._headless_mode_cache

    def _wait_for_headless_render(self, wait_time=0.3):
        """
        Headless模式下等待页面元素渲染完成

        Args:
            wait_time: 等待时间(秒)，默认0.3秒
        """
        if self._is_headless_mode():
            time.sleep(wait_time)

    def _get_headless_wait_config(self, timeout, min_timeout=15, poll_frequency=0.1):
        """
        获取Headless模式下的等待配置

        Args:
            timeout: 原始超时时间(秒)
            min_timeout: Headless模式下的最小超时时间(秒)，默认15秒
            poll_frequency: 非Headless模式下的轮询频率(秒)，默认0.1秒

        Returns:
            tuple: (实际超时时间, 轮询频率)
        """
        is_headless = self._is_headless_mode()
        if is_headless:
            actual_timeout = max(timeout, min_timeout)
            actual_poll_frequency = 0.2
        else:
            actual_timeout = timeout
            actual_poll_frequency = poll_frequency
        return actual_timeout, actual_poll_frequency

    # ==================== 页面加载等待 ====================

    def wait_for_ready_state_complete(self, timeout=10):
        """
        等待页面完全加载（优化：减少轮询次数，提高响应速度）

        Args:
            timeout: 超时时间(秒)，默认10秒

        Returns:
            bool: True表示加载完成

        Raises:
            Exception: 如果页面在超时时间内未完全加载
        """
        start_time = time.time()
        check_interval = 0.05  # 减少轮询间隔，提高响应速度

        while time.time() - start_time < timeout:
            try:
                ready_state = self.driver.execute_script("return document.readyState")
                if ready_state == "complete":
                    return True
            except InvalidSessionIdException:
                log.error("浏览器会话已关闭，无法等待页面加载完成")
                raise InvalidSessionIdException("浏览器会话已关闭，无法继续操作")
            except WebDriverException as e:
                if "invalid session id" in str(e).lower() or "session deleted" in str(e).lower():
                    log.error("浏览器会话已关闭，无法等待页面加载完成")
                    raise InvalidSessionIdException("浏览器会话已关闭，无法继续操作")
                # 其他 WebDriverException 可能表示页面正在加载，继续等待
                pass

            time.sleep(check_interval)

        raise Exception(f"打开网页时，页面元素在{timeout}秒后仍然没有完全加载完")

    # ==================== 元素定位和等待 ====================

    def _wait_for_element(self, locator, condition_type="visible", timeout=10):
        """
        等待元素出现（内部方法）

        Args:
            locator: 定位器元组 (By.ID, "element_id") 或 (By.XPATH, "xpath")
            condition_type: 等待条件类型，"visible"（可见）、"clickable"（可点击）、"presence"（存在）
            timeout: 超时时间(秒)

        Returns:
            WebElement: 找到的元素

        Raises:
            TimeoutException: 如果元素在超时时间内未出现
        """
        locate_type, locator_expression = locator

        is_headless = self._is_headless_mode()
        actual_timeout, actual_poll_frequency = self._get_headless_wait_config(timeout)

        wait = WebDriverWait(self.driver, actual_timeout, poll_frequency=actual_poll_frequency)

        if is_headless:
            log.info(f"Headless模式：先等待元素存在于DOM中，定位表达式: {locator_expression}")
            element = wait.until(EC.presence_of_element_located((locate_type, locator_expression)))
            log.info(f"元素已存在于DOM中，继续等待元素{condition_type}")

            if condition_type == "visible":
                element = wait.until(EC.visibility_of_element_located((locate_type, locator_expression)))
            elif condition_type == "clickable":
                element = wait.until(EC.element_to_be_clickable((locate_type, locator_expression)))

            log.info(f"元素已{condition_type}，可以继续操作")
            return element
        else:
            if condition_type == "visible":
                return wait.until(EC.visibility_of_element_located((locate_type, locator_expression)))
            elif condition_type == "clickable":
                return wait.until(EC.element_to_be_clickable((locate_type, locator_expression)))
            else:  # presence
                return wait.until(EC.presence_of_element_located((locate_type, locator_expression)))

    def find_element(self, locator, timeout=10, must_be_visible=False):
        """
        查找单个元素（Selenium 官方标准方法，优化：减少不必要的等待）

        Args:
            locator: 定位器元组 (By.ID, "element_id") 或 (By.XPATH, "xpath")
            timeout: 超时时间(秒)，默认10秒
            must_be_visible: 元素是否必须可见，True是必须可见，False是默认值

        Returns:
            WebElement: 返回的元素

        Raises:
            ElementNotVisibleException: 如果元素定位失败
        """
        # 只在必要时等待页面加载（减少等待时间）
        self.wait_for_ready_state_complete(timeout=3)
        self._wait_for_headless_render(wait_time=0.1)  # 减少 headless 等待时间

        try:
            if must_be_visible:
                element = self._wait_for_element(locator, condition_type="visible", timeout=timeout)
            else:
                element = self._wait_for_element(locator, condition_type="presence", timeout=timeout)

            _, locator_expression = locator
            log.info(f"元素 {locator_expression} 已找到")
            return element
        except TimeoutException:
            _, locator_expression = locator
            raise ElementNotVisibleException(
                f"元素定位失败（超时{timeout}秒），定位表达式: {locator_expression}"
            )

    def find_elements(self, locator, timeout=10):
        """
        查找多个元素（优化：减少等待时间）

        Args:
            locator: 定位器元组
            timeout: 超时时间(秒)

        Returns:
            list: 元素列表
        """
        self.wait_for_ready_state_complete(timeout=3)
        locate_type, locator_expression = locator
        return self.driver.find_elements(locate_type, locator_expression)

    def wait_for_element_to_disappear(self, locator, timeout=10):
        """
        等待元素消失（优化：减少等待时间）

        Args:
            locator: 定位器元组
            timeout: 超时时间(秒)

        Returns:
            bool: 元素消失返回True

        Raises:
            Exception: 如果元素在超时时间内未消失
        """
        self.wait_for_ready_state_complete(timeout=3)
        locate_type, locator_expression = locator

        try:
            wait = WebDriverWait(self.driver, timeout, poll_frequency=0.1)
            wait.until(EC.invisibility_of_element_located((locate_type, locator_expression)))
            return True
        except TimeoutException:
            raise Exception(
                f"元素没有消失（超时{timeout}秒），定位表达式: {locator_expression}"
            )

    # ==================== 元素交互操作 ====================

    def click(self, locator, timeout=10, need_hover=False, fluent=False):
        """
        点击元素（Selenium 官方标准方法）

        Args:
            locator: 定位器元组
            timeout: 超时时间(秒)，默认10秒
            need_hover: 是否需要在点击前先hover，默认False
            fluent: 是否支持链式调用，默认False
                     True: 返回self，支持链式调用
                     False: 返回bool，True表示成功，False表示失败

        Returns:
            self 或 bool: 根据fluent参数决定返回值

        Raises:
            Exception: 如果点击失败（当fluent=True时）
        """
        self.wait_for_ready_state_complete(timeout=3)  # 减少等待时间
        self._wait_for_headless_render(wait_time=0.2)  # 减少 headless 等待时间

        locate_type, locator_expression = locator
        log.info(f"准备点击元素：{locator_expression}，定位方式：{locate_type}")

        for attempt in range(2):
            try:
                is_headless = self._is_headless_mode()
                element = None
                use_js_click_fallback = False

                # 尝试等待元素可点击
                try:
                    element = self._wait_for_element(locator, condition_type="clickable", timeout=timeout)
                    time.sleep(0.1)  # 减少等待时间
                except TimeoutException:
                    # 在无头模式下，如果clickable检查超时，尝试使用presence检查 + JavaScript点击
                    if is_headless:
                        log.warning(f"Headless模式：等待元素clickable超时，尝试使用presence检查 + JavaScript点击")
                        try:
                            element = self._wait_for_element(locator, condition_type="presence", timeout=timeout)
                            use_js_click_fallback = True
                            log.info(f"Headless模式：元素已存在于DOM中，将使用JavaScript点击")
                        except TimeoutException:
                            raise
                    else:
                        raise

                if element is None:
                    raise Exception(f"元素 {locator_expression} 定位失败：element为None")

                if need_hover:
                    try:
                        log.info(f"点击前先hover到元素：{locator_expression}")
                        self.hover(locator, timeout=timeout)
                    except Exception as hover_error:
                        log.warning(f"hover操作失败，继续尝试点击：{hover_error}")

                # 滚动元素到可视区域（优化：减少等待时间）
                try:
                    scroll_behavior = "smooth" if not is_headless else "auto"
                    self.driver.execute_script(
                        f"arguments[0].scrollIntoView({{block: 'center', behavior: '{scroll_behavior}'}});",
                        element
                    )
                    # 减少等待时间
                    wait_time = 0.2 if is_headless else 0.15
                    time.sleep(wait_time)
                except Exception as scroll_error:
                    log.warning(f"滚动元素失败，继续尝试点击：{scroll_error}")

                # 如果使用JavaScript点击回退，直接使用JavaScript点击
                if use_js_click_fallback:
                    try:
                        log.info(f"Headless模式：使用JavaScript点击元素 {locator_expression}")
                        self.driver.execute_script("arguments[0].click();", element)
                        time.sleep(0.1)  # 减少等待时间
                        self.wait_for_ready_state_complete(timeout=1)  # 减少等待时间
                        log.info(f"元素 {locator_expression} JavaScript点击成功")
                        return self if fluent else True
                    except Exception as js_error:
                        log.error(f"Headless模式：JavaScript点击失败：{js_error}")
                        raise Exception(f"元素 {locator_expression} JavaScript点击失败：{js_error}")

                # 尝试多种点击方式（优化：减少日志输出）
                element_ref = element
                click_methods = [
                    ("普通点击", lambda: element_ref.click()),
                    ("ActionChains点击", lambda: ActionChains(self.driver).move_to_element(element_ref).click().perform()),
                    ("JavaScript点击", lambda: self.driver.execute_script("arguments[0].click();", element_ref)),
                ]

                for method_name, click_func in click_methods:
                    try:
                        click_func()
                        time.sleep(0.05)  # 减少等待时间
                        log.info(f"{method_name}成功")
                        break
                    except Exception as click_error:
                        error_msg = str(click_error).lower()
                        is_last_method = method_name == click_methods[-1][0]
                        if is_last_method:
                            log.warning(f"{method_name}失败：{click_error}")

                        if any(keyword in error_msg for keyword in [
                            "click intercepted", "not clickable", "element not interactable",
                            "element click intercepted", "is not clickable"
                        ]):
                            if not is_last_method:
                                log.warning(f"{method_name}失败（元素被遮挡或不可点击），尝试下一种方法")
                            continue
                        else:
                            if not is_last_method:
                                log.warning(f"{method_name}失败：{click_error}，尝试下一种方法")
                            continue
                else:
                    raise Exception("所有点击方式都失败了")

                self.wait_for_ready_state_complete(timeout=1)  # 减少等待时间
                time.sleep(0.1)  # 减少等待时间

                log.info(f"元素 {locator_expression} 点击成功")
                return self if fluent else True

            except StaleElementReferenceException:
                if attempt < 1:
                    log.warning(f"元素 {locator_expression} 点击时发生stale element异常，等待页面刷新后重试1次")
                    self.wait_for_ready_state_complete(timeout=5)
                    time.sleep(0.3)
                    continue
                else:
                    raise Exception(f"元素 {locator_expression} 点击失败：页面元素过期（已重试1次）")
            except TimeoutException as e:
                if attempt < 1:
                    log.warning(f"元素点击超时（第{attempt + 1}次尝试）: 将重试1次")
                    time.sleep(0.3)
                    continue
                raise Exception(f"元素 {locator_expression} 点击失败：元素超时未出现或不可点击（已重试1次）")
            except Exception as e:
                if attempt < 1:
                    log.warning(f"元素点击失败（第{attempt + 1}次尝试）: {e}，将重试1次")
                    time.sleep(0.3)
                    continue
                raise Exception(f"元素 {locator_expression} 点击失败（已重试1次）: {e}")

        raise Exception(f"元素 {locator_expression} 点击失败：已重试1次均失败")

    def input_text(self, locator, text, timeout=10, clear_first=True, need_enter=False, fluent=False):
        """
        向元素输入文本（Selenium 官方标准方法）

        Args:
            locator: 定位器元组
            text: 要输入的文本
            timeout: 超时时间(秒)
            clear_first: 是否先清除原有内容，默认True
            need_enter: 是否需要回车，默认False
            fluent: 是否支持链式调用，默认False
                     True: 返回self，支持链式调用
                     False: 返回bool，True表示成功，False表示失败

        Returns:
            self 或 bool: 根据fluent参数决定返回值

        Raises:
            Exception: 如果输入失败（当fluent=True时）
        """
        # 确保页面完全加载完成
        self.wait_for_ready_state_complete(timeout=5)

        # Headless模式下等待元素渲染
        self._wait_for_headless_render(wait_time=0.5)

        # 将输入值转换为字符串
        fill_value = str(text) if isinstance(text, (int, float)) else text

        # 如果输入值以\n结尾，则自动设置need_enter为True（兼容旧代码）
        if fill_value.endswith("\n"):
            need_enter = True
            fill_value = fill_value[:-1]

        locate_type, locator_expression = locator
        log.info(f"向元素 {locator_expression} 输入值 {fill_value}")

        # 获取并操作元素，最多重试1次
        for attempt in range(2):
            try:
                # 等待元素出现并可见（支持Headless模式优化）
                try:
                    element = self._wait_for_element(locator, condition_type="visible", timeout=timeout)
                except TimeoutException as e:
                    # 如果超时，尝试检查页面状态
                    if self._is_headless_mode():
                        current_url = self.driver.current_url
                        page_source_length = len(self.driver.page_source)
                        log.error(f"等待元素超时，当前URL: {current_url}, 页面源码长度: {page_source_length}")
                        log.error(f"尝试在页面源码中搜索定位表达式: {locator_expression}")
                        # 检查元素是否在页面源码中
                        if locator_expression in self.driver.page_source:
                            log.warning(f"定位表达式在页面源码中找到，但元素可能不可见")
                    raise

                # 滚动元素到可视区域中心位置
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
                time.sleep(0.2)  # 等待滚动完成

                # 清除原有值
                if clear_first:
                    try:
                        element.clear()
                    except Exception:
                        pass  # 清除失败不影响后续操作

                # 尝试普通输入，如果失败则使用JavaScript输入
                try:
                    # 先尝试点击元素确保获得焦点
                    try:
                        element.click()
                        time.sleep(0.1)
                    except Exception:
                        pass  # 点击失败不影响后续操作

                    # 输入值
                    element.send_keys(fill_value)
                    if need_enter:
                        element.send_keys(Keys.RETURN)

                    # 等待页面就绪
                    self.wait_for_ready_state_complete()
                    return self if fluent else True

                except Exception as send_error:
                    # 普通输入失败，尝试使用JavaScript输入
                    log.info(f"元素 {locator_expression} 普通输入失败，尝试使用JavaScript输入")
                    try:
                        # 如果元素可能过期，重新定位元素
                        try:
                            # 尝试使用现有元素
                            self.driver.execute_script("arguments[0].value = arguments[1];", element, "")
                        except (StaleElementReferenceException, Exception):
                            # 元素过期，重新定位
                            log.info(f"元素 {locator_expression} 在JavaScript输入时过期，重新定位元素")
                            element = self._wait_for_element(locator, condition_type="presence", timeout=timeout)
                            self.driver.execute_script("arguments[0].value = arguments[1];", element, "")

                        # 触发input事件，确保页面响应
                        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)
                        # 触发change事件
                        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", element)
                        # 触发click事件
                        try:
                            # 确保页面完全加载完成后再点击
                            self.wait_for_ready_state_complete(timeout=5)
                            self.driver.execute_script("arguments[0].click();", element)
                            time.sleep(0.1)
                            # 使用send_keys输入值（关键：某些输入框需要键盘事件）
                            element.send_keys(fill_value)
                        except Exception:
                            pass  # click事件触发失败不影响后续操作

                        if need_enter:
                            # 如果元素过期，重新定位后再发送回车
                            try:
                                element.send_keys(Keys.RETURN)
                            except (StaleElementReferenceException, Exception):
                                element = self._wait_for_element(locator, condition_type="presence", timeout=timeout)
                                element.send_keys(Keys.RETURN)

                        # 等待页面就绪
                        self.wait_for_ready_state_complete()
                        log.info(f"元素 {locator_expression} 使用JavaScript输入成功")
                        return self if fluent else True
                    except Exception as js_error:
                        # JavaScript输入也失败
                        log.info(f"元素 {locator_expression} JavaScript输入也失败：{str(js_error)}")
                        raise Exception(f"元素 {locator_expression} JavaScript输入也失败：{str(js_error)}")

            except StaleElementReferenceException:
                if attempt == 0:
                    # 第一次失败，等待页面刷新后重试1次
                    log.warning(f"元素 {locator_expression} 输入时发生stale element异常，等待页面刷新后重试1次")
                    self.wait_for_ready_state_complete()
                    time.sleep(0.1)
                    continue
                else:
                    # 重试后仍然失败
                    raise Exception(f"元素 {locator_expression} 填值失败：页面元素过期（已重试1次）")
            except TimeoutException as e:
                # 超时失败，不重试
                raise Exception(f"元素 {locator_expression} 填值失败：元素超时未出现或不可交互 - {str(e)}")
            except Exception as e:
                if attempt == 0:
                    log.warning(f"元素 {locator_expression} 输入失败（第{attempt + 1}次尝试），将重试1次：{str(e)}")
                    time.sleep(0.2)
                    continue
                else:
                    # 重试后仍然失败
                    raise Exception(f"元素 {locator_expression} 填值失败（已重试1次）：{str(e)}")

    def hover(self, locator, timeout=10):
        """
        鼠标悬停到指定元素（优化：减少等待时间）

        Args:
            locator: 定位器元组
            timeout: 等待元素出现的超时时间(秒)，默认10秒

        Returns:
            self: 返回自身，支持链式调用
        """
        self.wait_for_ready_state_complete(timeout=3)
        self._wait_for_headless_render(wait_time=0.2)

        _, locator_expression = locator
        log.info(f"鼠标悬停到元素 {locator_expression}")

        actual_timeout, _ = self._get_headless_wait_config(timeout)
        element = self.find_element(locator, timeout=actual_timeout)

        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        time.sleep(0.2)  # 减少等待时间
        return self

    def double_click(self, locator, timeout=10):
        """
        双击元素（优化：减少等待时间）

        Args:
            locator: 定位器元组
            timeout: 超时时间(秒)，默认10秒

        Returns:
            self: 返回自身，支持链式调用
        """
        self.wait_for_ready_state_complete(timeout=3)
        self._wait_for_headless_render(wait_time=0.2)

        element = self._wait_for_element(locator, condition_type="clickable", timeout=timeout)
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        return self

    # ==================== 元素属性获取 ====================

    def get_text(self, locator, timeout=10):
        """
        获取元素的文本内容（Selenium 官方标准方法，优化：减少等待时间）

        Args:
            locator: 定位器元组
            timeout: 超时时间(秒)

        Returns:
            str: 元素的文本内容
        """
        self.wait_for_ready_state_complete(timeout=3)
        element = self.find_element(locator, timeout=timeout)
        text = element.text.strip()
        _, locator_expression = locator
        log.info(f"获取元素 {locator_expression} 的文本内容: {text}")
        return text

    def get_attribute(self, locator, attribute_name, timeout=10):
        """
        获取元素的指定属性值（Selenium 官方标准方法，优化：减少等待时间）

        Args:
            locator: 定位器元组
            attribute_name: 属性名（如 'class', 'id', 'value' 等）
            timeout: 超时时间(秒)

        Returns:
            str: 属性值
        """
        self.wait_for_ready_state_complete(timeout=3)
        element = self.find_element(locator, timeout=timeout)
        attr_value = element.get_attribute(attribute_name)
        _, locator_expression = locator
        log.info(f"获取元素 {locator_expression} 的属性 {attribute_name}: {attr_value}")
        return attr_value

    def get_value(self, locator, timeout=10):
        """
        获取表单元素的value属性值（适用于input、textarea等）

        Args:
            locator: 定位器元组
            timeout: 超时时间(秒)

        Returns:
            str: 元素的value属性值
        """
        return self.get_attribute(locator, "value", timeout=timeout)

    def is_displayed(self, locator, timeout=5):
        """
        检查元素是否显示（Selenium 官方标准方法，优化：减少等待时间）

        Args:
            locator: 定位器元组
            timeout: 超时时间(秒)，默认5秒

        Returns:
            bool: 元素存在且可见返回True，否则返回False
        """
        self.wait_for_ready_state_complete(timeout=3)
        try:
            element = self.find_element(locator, timeout=timeout, must_be_visible=True)
            return element is not None
        except (NoSuchElementException, TimeoutException):
            return False

    # ==================== 页面导航 ====================

    def navigate_to(self, url, wait_for_load=True):
        """
        导航到指定URL

        Args:
            url: 目标URL（相对路径或绝对路径）
            wait_for_load: 是否等待页面加载完成，默认True

        Returns:
            self: 返回自身，支持链式调用
        """
        full_url = self.BASE_URL + url if not url.startswith("http") else url
        self.driver.get(full_url)

        if wait_for_load:
            page_timeout = 12 if self._is_headless_mode() else 8  # 优化：减少等待时间
            self.wait_for_ready_state_complete(timeout=page_timeout)

            if self._is_headless_mode():
                time.sleep(0.5)  # 优化：减少等待时间
                log.info("Headless模式：页面跳转后额外等待0.5秒，确保元素完全渲染")

        return self

    def get_current_url(self):
        """
        获取当前页面URL

        Returns:
            str: 当前页面URL
        """
        return self.driver.current_url

    def get_page_title(self):
        """
        获取当前页面标题

        Returns:
            str: 页面标题
        """
        return self.driver.title

    def refresh(self):
        """
        刷新当前页面（优化：减少等待时间）

        Returns:
            self: 返回自身，支持链式调用
        """
        self.driver.refresh()
        self.wait_for_ready_state_complete(timeout=3)
        return self

    def back(self):
        """
        浏览器后退（优化：减少等待时间）

        Returns:
            self: 返回自身，支持链式调用
        """
        self.driver.back()
        self.wait_for_ready_state_complete(timeout=3)
        return self

    def forward(self):
        """
        浏览器前进（优化：减少等待时间）

        Returns:
            self: 返回自身，支持链式调用
        """
        self.driver.forward()
        self.wait_for_ready_state_complete(timeout=3)
        return self

    # ==================== iframe 操作 ====================

    def switch_to_iframe(self, locator, timeout=10):
        """
        切换到iframe（优化：减少等待时间）

        Args:
            locator: iframe定位器元组
            timeout: 超时时间(秒)，默认10秒

        Returns:
            self: 返回自身，支持链式调用

        Raises:
            Exception: 如果切换到iframe失败
        """
        try:
            self.wait_for_ready_state_complete(timeout=3)
            _, locator_expression = locator
            log.info(f"切换到iframe：{locator_expression}")

            iframe = self.find_element(locator, timeout=timeout)
            self.driver.switch_to.frame(iframe)

            self.wait_for_ready_state_complete(timeout=3)
            self._wait_for_headless_render(wait_time=0.2)

            log.info(f"成功切换到iframe：{locator_expression}")
            return self
        except TimeoutException as e:
            _, locator_expression = locator
            raise Exception(f"切换到iframe失败（超时{timeout}秒）：{locator_expression} - {str(e)}")
        except Exception as e:
            _, locator_expression = locator
            raise Exception(f"切换到iframe失败：{locator_expression} - {str(e)}")

    def switch_out_iframe(self, to_root=True):
        """
        从iframe切回主文档（优化：减少等待时间）

        Args:
            to_root: True切回顶层文档，False切回上一层

        Returns:
            self: 返回自身，支持链式调用
        """
        self.wait_for_ready_state_complete(timeout=3)
        log.info("从iframe切回主文档")
        if to_root:
            self.driver.switch_to.default_content()
        else:
            self.driver.switch_to.parent_frame()
        return self

    # ==================== 窗口操作 ====================

    def switch_to_new_window(self):
        """
        切换到最新打开的窗口（优化：减少等待时间）

        Returns:
            self: 返回自身，支持链式调用
        """
        self.wait_for_ready_state_complete(timeout=3)
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[-1])
        return self

    def close_current_window(self, switch_to_first=True):
        """
        关闭当前窗口（优化：减少等待时间）

        Args:
            switch_to_first: 关闭后是否切换到第一个窗口，True切换到第一个窗口，False切换到上一个窗口

        Returns:
            bool: True成功，False失败
        """
        self.wait_for_ready_state_complete(timeout=3)
        try:
            current_handle = self.driver.current_window_handle
            all_handles = self.driver.window_handles

            log.info(f"关闭当前窗口，当前窗口句柄：{current_handle}，总窗口数：{len(all_handles)}")

            if len(all_handles) <= 1:
                log.warning("只有一个窗口，无法关闭")
                return False

            self.driver.close()

            remaining_handles = [handle for handle in all_handles if handle != current_handle]
            if remaining_handles:
                if switch_to_first:
                    self.driver.switch_to.window(remaining_handles[0])
                    log.info(f"已切换到第一个窗口，窗口句柄：{remaining_handles[0]}")
                else:
                    self.driver.switch_to.window(remaining_handles[-1])
                    log.info(f"已切换到上一个窗口，窗口句柄：{remaining_handles[-1]}")

            return True
        except Exception as e:
            log.error(f"关闭窗口失败：{str(e)}")
            return False

    # ==================== 文件上传 ====================

    def upload_file(self, locator, file_path):
        """
        上传文件（优化：减少等待时间）

        Args:
            locator: 文件输入框定位器元组
            file_path: 文件路径

        Returns:
            self: 返回自身，支持链式调用
        """
        self.wait_for_ready_state_complete(timeout=3)
        element = self.find_element(locator)
        element.send_keys(file_path)
        return self

    # ==================== 页面内容检查 ====================

    def page_contains_text(self, text, case_sensitive=False):
        """
        判断当前页面是否包含指定文字（优化：减少等待时间）

        Args:
            text: 要查找的文字
            case_sensitive: 是否区分大小写，True区分大小写，False不区分（默认）

        Returns:
            bool: True表示页面包含该文字，False表示不包含
        """
        self.wait_for_ready_state_complete(timeout=3)
        try:
            page_source = self.driver.page_source

            if case_sensitive:
                contains = text in page_source
            else:
                contains = text.lower() in page_source.lower()

            log.info(f"检查页面是否包含文字'{text}'（区分大小写：{case_sensitive}）：{contains}")
            return contains
        except Exception as e:
            log.error(f"判断页面是否包含文字失败：{str(e)}")
            return False

    # ==================== 滚动操作 ====================

    def scroll_to_element(self, locator):
        """
        滚动页面至元素可见（优化：减少等待时间）

        Args:
            locator: 定位器元组

        Returns:
            self: 返回自身，支持链式调用
        """
        self.wait_for_ready_state_complete(timeout=3)
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView()", element)
        time.sleep(0.1)  # 确保滚动完成
        return self

    def scroll_to_top(self):
        """
        滚动到页面顶部（优化：减少等待时间）

        Returns:
            self: 返回自身，支持链式调用
        """
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.1)  # 确保滚动完成
        return self

    def scroll_to_bottom(self):
        """
        滚动到页面底部（优化：减少等待时间）

        Returns:
            self: 返回自身，支持链式调用
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.1)  # 确保滚动完成
        return self

    # ==================== 截图操作 ====================

    def take_screenshot(self, file_path=None):
        """
        对当前页面截图

        Args:
            file_path: 截图保存路径，如果为None则自动生成

        Returns:
            str: 截图文件路径
        """
        if file_path is None:
            ele_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
            ele_img_dir_path = get_project_path() + sep(["img", "ele_img"], add_sep_before=True, add_sep_after=True)
            if not os.path.exists(ele_img_dir_path):
                os.mkdir(ele_img_dir_path)
            file_path = ele_img_dir_path + ele_name

        self.driver.get_screenshot_as_file(file_path)
        return file_path

    def element_screenshot(self, locator, file_path=None):
        """
        对指定元素截图（优化：减少等待时间）

        Args:
            locator: 定位器元组
            file_path: 截图保存路径，如果为None则自动生成

        Returns:
            str: 截图文件路径
        """
        self.wait_for_ready_state_complete(timeout=3)
        element = self.find_element(locator)

        if file_path is None:
            ele_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
            ele_img_dir_path = get_project_path() + sep(["img", "ele_img"], add_sep_before=True, add_sep_after=True)
            if not os.path.exists(ele_img_dir_path):
                os.mkdir(ele_img_dir_path)
            file_path = ele_img_dir_path + ele_name

        element.screenshot(file_path)
        return file_path
