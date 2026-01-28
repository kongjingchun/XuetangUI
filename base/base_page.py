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
import sys
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
        wait = WebDriverWait(self.driver, timeout, poll_frequency=0.1)
        if condition_type == "visible":
            return wait.until(EC.visibility_of_element_located((locate_type, locator_expression)))
        if condition_type == "clickable":
            return wait.until(EC.element_to_be_clickable((locate_type, locator_expression)))
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
        self.wait_for_ready_state_complete(timeout=3)
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

    def is_disappear(self, locator, timeout=10):
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

    def _get_click_diagnostic(self, locator_expression, attempt, error, element=None):
        """收集 click 失败时的诊断信息，便于定位问题。不抛异常。"""
        parts = [f"locator={locator_expression}", f"attempt={attempt + 1}", f"error={type(error).__name__}: {error}"]
        try:
            if element is not None:
                tag = element.tag_name
                disp = element.is_displayed()
                ena = element.is_enabled()
                rect = element.rect
                r = f"x={rect.get('x')},y={rect.get('y')},w={rect.get('width')},h={rect.get('height')}"
                aid = element.get_attribute("id") or ""
                txt = (element.text or "")[:80]
                cls = (element.get_attribute("class") or "")[:80]
                parts.append(f"element: tag={tag} displayed={disp} enabled={ena} rect=({r}) id={aid!r} text={txt!r} class={cls!r}")
            else:
                parts.append("element=(未获取到)")
        except Exception:
            parts.append("element=(无法获取或已过期)")
        try:
            ae = self.driver.execute_script(
                "var e = document.activeElement; if (!e) return 'null'; return e.tagName + (e.id ? '#'+e.id : '') + ' ' + (e.className || '').slice(0,40);"
            )
            parts.append(f"activeElement={ae}")
        except Exception:
            parts.append("activeElement=(无法获取)")
        try:
            url = self.driver.current_url
            parts.append(f"url={url[:100]}")
        except Exception:
            pass
        return " | ".join(parts)

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
        self.wait_for_ready_state_complete(timeout=3)
        locate_type, locator_expression = locator
        log.info(f"准备点击元素：{locator_expression}，定位方式：{locate_type}")

        for attempt in range(2):
            try:
                element = None
                use_js_click_fallback = False
                try:
                    element = self._wait_for_element(locator, condition_type="clickable", timeout=timeout)
                except TimeoutException:
                    # 兜底：部分环境（如 Linux Headless、iframe 内表格按钮）下元素已在 DOM 但未满足 clickable，改用 presence + JS 点击
                    log.warning(f"等待元素可点击超时，尝试等待元素存在后使用 JavaScript 点击：{locator_expression}")
                    element = self._wait_for_element(locator, condition_type="presence", timeout=timeout)
                    use_js_click_fallback = True
                time.sleep(0.1)

                if need_hover:
                    try:
                        log.info(f"点击前先hover到元素：{locator_expression}")
                        self.hover(locator, timeout=timeout)
                    except Exception as hover_error:
                        log.warning(f"hover操作失败，继续尝试点击：{hover_error}")

                try:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                        element
                    )
                    time.sleep(0.15)
                except Exception as scroll_error:
                    log.warning(f"滚动元素失败，继续尝试点击：{scroll_error}")

                if use_js_click_fallback:
                    try:
                        self.driver.execute_script("arguments[0].click();", element)
                        time.sleep(0.1)
                        self.wait_for_ready_state_complete(timeout=1)
                        log.info(f"元素 {locator_expression} JavaScript 点击成功")
                        return self if fluent else True
                    except Exception as js_error:
                        log.warning(f"[click] 失败 详细: {self._get_click_diagnostic(locator_expression, attempt, js_error, element)}")
                        raise Exception(f"元素 {locator_expression} JavaScript 点击失败：{js_error}")

                # 尝试多种点击方式
                element_ref = element
                last_click_error = None
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
                        last_click_error = click_error
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
                    err = last_click_error or Exception("所有点击方式均未成功")
                    log.warning(f"[click] 失败 详细: {self._get_click_diagnostic(locator_expression, attempt, err, element)}")
                    raise Exception("所有点击方式都失败了")

                self.wait_for_ready_state_complete(timeout=1)  # 减少等待时间
                time.sleep(0.1)  # 减少等待时间

                log.info(f"元素 {locator_expression} 点击成功")
                return self if fluent else True

            except StaleElementReferenceException as e:
                if attempt < 1:
                    log.warning(f"元素 {locator_expression} 点击时发生stale element异常，等待页面刷新后重试1次")
                    self.wait_for_ready_state_complete(timeout=5)
                    time.sleep(0.3)
                    continue
                else:
                    log.warning(f"[click] 失败 详细: {self._get_click_diagnostic(locator_expression, attempt, e, element)}")
                    raise Exception(f"元素 {locator_expression} 点击失败：页面元素过期（已重试1次）")
            except TimeoutException as e:
                if attempt < 1:
                    log.warning(f"元素点击超时（第{attempt + 1}次尝试）: 将重试1次")
                    time.sleep(0.3)
                    continue
                log.warning(f"[click] 失败 详细: {self._get_click_diagnostic(locator_expression, attempt, e, None)}")
                raise Exception(f"元素 {locator_expression} 点击失败：元素超时未出现或不可点击（已重试1次）")
            except Exception as e:
                if attempt < 1:
                    log.warning(f"元素点击失败（第{attempt + 1}次尝试）: {e}，将重试1次")
                    time.sleep(0.3)
                    continue
                log.warning(f"[click] 失败 详细: {self._get_click_diagnostic(locator_expression, attempt, e, element)}")
                raise Exception(f"元素 {locator_expression} 点击失败（已重试1次）: {e}")

        log.warning(f"[click] 失败 详细: locator={locator_expression} attempt=2 已重试1次均失败")
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
        self.wait_for_ready_state_complete(timeout=5)
        fill_value = str(text) if isinstance(text, (int, float)) else text
        if fill_value.endswith("\n"):
            need_enter = True
            fill_value = fill_value[:-1]

        locate_type, locator_expression = locator
        log.info(f"向元素 {locator_expression} 输入值 {fill_value}")

        for attempt in range(2):
            try:
                log.info(
                    f"[input_text] attempt={attempt + 1}/2 locator={locator_expression} "
                    f"timeout={timeout} clear_first={clear_first} need_enter={need_enter}"
                )
                # 对输入框来说，只要求“存在”即可，后续我们会主动滚动并聚焦；
                # 避免因为 y 为负值等原因被 Selenium 认为不可见而超时。
                element = self._wait_for_element(locator, condition_type="presence", timeout=timeout)

                # 滚动元素到可视区域中心位置
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
                time.sleep(0.2)  # 等待滚动完成

                # 记录元素关键属性，便于判断是否命中错元素/被遮挡/不可输入
                try:
                    rect = element.rect
                    tag = element.tag_name
                    displayed = element.is_displayed()
                    enabled = element.is_enabled()
                    placeholder = element.get_attribute("placeholder")
                    name = element.get_attribute("name")
                    element_id = element.get_attribute("id")
                    cls = element.get_attribute("class")
                    before_value = element.get_attribute("value")
                    active_tag = self.driver.execute_script("return document.activeElement && document.activeElement.tagName;")
                    active_id = self.driver.execute_script("return document.activeElement && document.activeElement.id;")
                    active_cls = self.driver.execute_script("return document.activeElement && document.activeElement.className;")
                    log.info(
                        "[input_text] element_info "
                        f"tag={tag} displayed={displayed} enabled={enabled} rect={rect} "
                        f"id={element_id} name={name} placeholder={placeholder} class={cls} value_before={before_value} "
                        f"active=({active_tag}#{active_id}.{active_cls})"
                    )
                except Exception as info_err:
                    log.warning(f"[input_text] 获取元素信息失败：{info_err}")

                # 先尝试点击元素确保获得焦点（很多组件化输入框不聚焦时 clear/send_keys 容易失败）
                try:
                    element.click()
                    time.sleep(0.05)
                    try:
                        active_tag = self.driver.execute_script("return document.activeElement && document.activeElement.tagName;")
                        active_id = self.driver.execute_script("return document.activeElement && document.activeElement.id;")
                        log.info(f"[input_text] click聚焦后 active=({active_tag}#{active_id})")
                    except Exception:
                        pass
                except Exception:
                    pass  # 点击失败不影响后续兜底

                # 清除原有值（更鲁棒：clear + 全选删除 兜底）
                if clear_first:
                    try:
                        log.info(f"[input_text] clear前 value={element.get_attribute('value')}")
                    except Exception:
                        pass
                    try:
                        element.clear()
                        time.sleep(0.02)
                    except Exception:
                        # element.clear() 在部分组件输入框会失败，继续走兜底
                        pass
                    try:
                        mod_key = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL
                        element.send_keys(mod_key, "a")
                        element.send_keys(Keys.BACKSPACE)
                        time.sleep(0.02)
                    except Exception:
                        pass
                    try:
                        log.info(f"[input_text] clear后 value={element.get_attribute('value')}")
                    except Exception:
                        pass

                # 尝试普通输入，如果失败则使用JavaScript输入
                try:
                    # 输入值
                    element.send_keys(fill_value)
                    if need_enter:
                        element.send_keys(Keys.RETURN)

                    # 轻量校验：防止 clear 失败导致“追加输入”或输入被拦截
                    try:
                        current_value = element.get_attribute("value") or ""
                        if fill_value and fill_value not in current_value:
                            raise Exception(f"value 校验失败，当前值: {current_value}")
                    except Exception:
                        raise
                    log.info(f"[input_text] send_keys后 value={element.get_attribute('value')}")

                    # 等待页面就绪
                    self.wait_for_ready_state_complete()
                    log.info("普通方式输入成功")
                    return self if fluent else True

                except Exception as send_error:
                    # 普通输入失败，尝试使用JavaScript输入
                    log.warning(f"[input_text] 普通输入失败：{type(send_error).__name__}: {send_error}，尝试使用JavaScript输入")
                    try:
                        # 如果元素可能过期，重新定位元素
                        try:
                            # 尝试使用现有元素
                            self.driver.execute_script("arguments[0].value = arguments[1];", element, fill_value)
                        except (StaleElementReferenceException, Exception):
                            # 元素过期，重新定位
                            log.info(f"元素 {locator_expression} 在JavaScript输入时过期，重新定位元素")
                            element = self._wait_for_element(locator, condition_type="presence", timeout=timeout)
                            self.driver.execute_script("arguments[0].value = arguments[1];", element, fill_value)

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
                            # 补一个轻量键盘事件（部分输入框依赖焦点/键盘事件触发联动）
                            element.send_keys(Keys.END)
                        except Exception:
                            pass  # click事件触发失败不影响后续操作

                        if need_enter:
                            # 如果元素过期，重新定位后再发送回车
                            try:
                                element.send_keys(Keys.RETURN)
                            except (StaleElementReferenceException, Exception):
                                element = self._wait_for_element(locator, condition_type="presence", timeout=timeout)
                                element.send_keys(Keys.RETURN)

                        try:
                            log.info(f"[input_text] JS设值后 value={element.get_attribute('value')}")
                        except Exception:
                            pass

                        # 等待页面就绪
                        self.wait_for_ready_state_complete()
                        log.info(f"使用JavaScript输入成功")
                        return self if fluent else True
                    except Exception as js_error:
                        # JavaScript输入也失败
                        log.warning(f"[input_text] JavaScript输入也失败：{type(js_error).__name__}: {js_error}")
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

    def input_rich_text(self, locator, text, timeout=10, clear_first=True, fluent=False):
        """
        向富文本编辑器输入内容（适用于contenteditable元素）

        富文本编辑器通常使用contenteditable="true"的div元素，需要特殊处理：
        1. 先点击元素获得焦点
        2. 清除原有内容
        3. 使用多种方式输入内容（普通输入、JavaScript设置等）
        4. 触发必要的事件（input、change等）让编辑器识别内容变化

        Args:
            locator: 定位器元组
            text: 要输入的文本内容
            timeout: 超时时间(秒)，默认10秒
            clear_first: 是否先清除原有内容，默认True
            fluent: 是否支持链式调用，默认False
                     True: 返回self，支持链式调用
                     False: 返回bool，True表示成功，False表示失败

        Returns:
            self 或 bool: 根据fluent参数决定返回值

        Raises:
            Exception: 如果输入失败（当fluent=True时）
        """
        self.wait_for_ready_state_complete(timeout=5)
        fill_value = str(text) if isinstance(text, (int, float)) else text
        locate_type, locator_expression = locator
        log.info(f"向富文本编辑器 {locator_expression} 输入值 {fill_value}")

        for attempt in range(2):
            try:
                element = self._wait_for_element(locator, condition_type="visible", timeout=timeout)

                # 滚动元素到可视区域中心位置
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
                time.sleep(0.2)  # 等待滚动完成

                # 先点击元素获得焦点
                try:
                    element.click()
                    time.sleep(0.2)  # 等待焦点获得
                except Exception as click_error:
                    log.warning(f"点击富文本编辑器失败，尝试使用JavaScript点击：{click_error}")
                    try:
                        self.driver.execute_script("arguments[0].click();", element)
                        time.sleep(0.2)
                    except Exception:
                        pass  # 点击失败不影响后续操作

                # 清除原有内容
                if clear_first:
                    try:
                        # 方法1: 使用Ctrl+A选中所有内容，然后删除
                        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                        time.sleep(0.1)
                        element.send_keys(Keys.DELETE)
                        time.sleep(0.1)
                    except Exception as clear_error:
                        log.warning(f"使用键盘快捷键清除内容失败，尝试使用JavaScript清除：{clear_error}")
                        try:
                            # 方法2: 使用JavaScript清除内容
                            self.driver.execute_script("arguments[0].innerHTML = '';", element)
                            self.driver.execute_script("arguments[0].textContent = '';", element)
                            time.sleep(0.1)
                        except Exception:
                            pass  # 清除失败不影响后续操作

                # 尝试多种方式输入内容
                input_success = False
                input_methods = [
                    # 方法1: 普通send_keys输入（适用于简单的富文本编辑器）
                    ("普通输入", lambda: element.send_keys(fill_value)),
                    # 方法2: 使用JavaScript设置textContent（纯文本）
                    ("JavaScript textContent", lambda: self.driver.execute_script(
                        "arguments[0].textContent = arguments[1];", element, fill_value
                    )),
                    # 方法3: 使用JavaScript设置innerHTML（支持HTML格式）
                    ("JavaScript innerHTML", lambda: self.driver.execute_script(
                        "arguments[0].innerHTML = arguments[1];", element, fill_value
                    )),
                ]

                for method_name, input_func in input_methods:
                    try:
                        input_func()
                        time.sleep(0.2)  # 等待输入完成

                        # 触发input事件，确保富文本编辑器识别内容变化
                        try:
                            self.driver.execute_script(
                                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element
                            )
                        except Exception:
                            pass

                        # 触发change事件
                        try:
                            self.driver.execute_script(
                                "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", element
                            )
                        except Exception:
                            pass

                        # 验证内容是否成功输入
                        try:
                            # 等待一下让内容更新
                            time.sleep(0.2)
                            # 获取元素内容进行验证
                            actual_content = self.driver.execute_script("return arguments[0].textContent || arguments[0].innerText;", element)
                            if fill_value in actual_content or actual_content.strip() == fill_value.strip():
                                log.info(f"富文本编辑器 {locator_expression} 使用{method_name}输入成功")
                                input_success = True
                                break
                            else:
                                log.warning(f"富文本编辑器内容验证失败，期望: {fill_value}, 实际: {actual_content}")
                        except Exception as verify_error:
                            log.warning(f"验证富文本编辑器内容失败：{verify_error}，假设输入成功")
                            input_success = True
                            break

                    except Exception as method_error:
                        log.warning(f"富文本编辑器 {locator_expression} 使用{method_name}输入失败：{method_error}")
                        if method_name == input_methods[-1][0]:
                            # 最后一种方法也失败，抛出异常
                            raise
                        continue

                if not input_success:
                    raise Exception(f"富文本编辑器 {locator_expression} 所有输入方法都失败")

                # 等待页面就绪
                self.wait_for_ready_state_complete()
                log.info(f"富文本编辑器 {locator_expression} 输入成功")
                return self if fluent else True

            except StaleElementReferenceException:
                if attempt == 0:
                    # 第一次失败，等待页面刷新后重试1次
                    log.warning(f"富文本编辑器 {locator_expression} 输入时发生stale element异常，等待页面刷新后重试1次")
                    self.wait_for_ready_state_complete()
                    time.sleep(0.2)
                    continue
                else:
                    # 重试后仍然失败
                    raise Exception(f"富文本编辑器 {locator_expression} 填值失败：页面元素过期（已重试1次）")
            except TimeoutException as e:
                # 超时失败，不重试
                raise Exception(f"富文本编辑器 {locator_expression} 填值失败：元素超时未出现或不可交互 - {str(e)}")
            except Exception as e:
                if attempt == 0:
                    log.warning(f"富文本编辑器 {locator_expression} 输入失败（第{attempt + 1}次尝试），将重试1次：{str(e)}")
                    time.sleep(0.3)
                    continue
                else:
                    # 重试后仍然失败
                    raise Exception(f"富文本编辑器 {locator_expression} 填值失败（已重试1次）：{str(e)}")

        raise Exception(f"富文本编辑器 {locator_expression} 填值失败：已重试1次均失败")

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
        _, locator_expression = locator
        log.info(f"鼠标悬停到元素 {locator_expression}")
        element = self.find_element(locator, timeout=timeout)

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
        time.sleep(1)
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
            self.wait_for_ready_state_complete(timeout=8)
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

    def page_contains_text(self, text, case_sensitive=False, retry_timeout=5):
        """
        判断当前页面是否包含指定文字（未找到时在 retry_timeout 秒内重复查询）

        Args:
            text: 要查找的文字
            case_sensitive: 是否区分大小写，True区分大小写，False不区分（默认）
            retry_timeout: 未找到时重复查询的总时长（秒），默认 5 秒，0 表示不重试

        Returns:
            bool: True表示页面包含该文字，False表示不包含
        """
        self.wait_for_ready_state_complete(timeout=3)
        poll_interval = 0.5
        deadline = time.time() + retry_timeout if retry_timeout > 0 else time.time()

        def _check():
            try:
                page_source = self.driver.page_source
                if case_sensitive:
                    return text in page_source
                return text.lower() in page_source.lower()
            except Exception as e:
                log.error(f"判断页面是否包含文字失败：{str(e)}")
                return False

        while True:
            contains = _check()
            if contains:
                log.info(f"检查页面是否包含文字'{text}'（区分大小写：{case_sensitive}）：True")
                return True
            if time.time() >= deadline:
                log.info(f"检查页面是否包含文字'{text}'（区分大小写：{case_sensitive}）：False（{retry_timeout}s 内未找到）")
                return False
            time.sleep(poll_interval)

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
