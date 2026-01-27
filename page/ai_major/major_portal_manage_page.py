# encoding: utf-8
# @File  : major_portal_manage_page.py
# @Author:
# @Date  :
# @Desc  : 专业门户管理页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class MajorPortalManagePage(BasePage):
    """专业门户管理页面类。

    对外只暴露“服务方法”（如按专业名称进入编辑页、编辑门户并校验等），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 专业门户管理主内容区域 iframe
    MAJOR_PORTAL_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2104']")
    # 专业门户管理编辑页 iframe
    MAJOR_PORTAL_EDIT_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-3005']")
    # 搜索关键词输入框
    SEARCH_KEYWORD_INPUT = (By.XPATH, "//input[@placeholder='专业名称 ｜ 专业代码']")
    # 搜索按钮
    SEARCH_BUTTON = (By.XPATH, "//button[contains(.,'搜索')]")
    # 编辑页面按钮
    EDIT_PAGE_BUTTON = (By.XPATH, "//button[contains(.,'编辑页面')]")
    # 头部导航栏
    HEADER_NAVIGATION_BAR = (By.XPATH, "//div[@class='page-header']//h1")
    # 发布按钮
    PUBLISH_BUTTON = (By.XPATH, "//button[contains(.,'发布')]")
    # 发布确认弹窗中的确定按钮
    PUBLISH_CONFIRM_BUTTON = (By.XPATH, "//div[@aria-label='发布确认']//button[contains(.,'确定')]")
    # 编辑页中的「打开专业门户」链接
    OPEN_PORTAL_LINK_IN_EDIT_PAGE = (By.XPATH, "//a[contains(.,' 打开专业门户 ')]")

    # ==================== 动态定位器 getter ====================

    def get_open_portal_button_locator(self, major_name):
        """专业名称 → 该行「打开门户」按钮定位器。"""
        return (By.XPATH, f"//tr[.//td[contains(.,'{major_name}')]]//button[contains(.,'打开门户')]")

    def get_edit_button_locator(self, major_name):
        """专业名称 → 该行「编辑」按钮定位器。"""
        return (By.XPATH, f"//tr[.//td[contains(.,'{major_name}')]]//button[contains(.,'编辑')]")

    def get_tab_locator(self, index=1):
        """标签页索引（从 1 开始）→ 专业门户管理标签页定位器。"""
        return (By.XPATH, f"(//span[contains(.,'专业门户管理')])[{index}]")

    def get_navigation_name_input_locator(self, index=1):
        """导航索引（从 1 开始）→ 导航名称输入框定位器。"""
        return (By.XPATH, f"(//label[text()='名称'])[{index}]/following-sibling::div//input")

    # ==================== 服务方法（页面对外能力） ====================

    def click_edit_page_button_by_major_name(self, major_name):
        """按专业名称在列表页搜索并点击编辑，进入编辑页。返回是否点击成功。"""
        self.switch_to_iframe(self.MAJOR_PORTAL_MANAGE_IFRAME)  # 切入专业门户管理 iframe
        self.input_text(self.SEARCH_KEYWORD_INPUT, major_name)  # 输入专业名称搜索
        self.click(self.SEARCH_BUTTON)  # 点击搜索
        locator = self.get_edit_button_locator(major_name)  # 获取编辑按钮定位器
        log.info(f"根据专业名称'{major_name}'点击编辑按钮，定位器为：{locator[1]}")
        result = self.click(locator, timeout=15, fluent=False)  # 点击编辑按钮
        self.switch_out_iframe()  # 切回默认上下文
        log.info(f"根据专业名称'{major_name}'点击编辑按钮结果：{result}")
        return result

    def edit_portal(self, navigation_name=None, index=1):
        """在编辑页中修改导航名称、发布并打开专业门户，最后在新窗口校验是否包含 navigation_name。返回校验结果。"""
        self.switch_to_iframe(self.MAJOR_PORTAL_EDIT_IFRAME)  # 切入专业门户编辑页 iframe
        self.click(self.EDIT_PAGE_BUTTON, timeout=10)  # 点击编辑页面
        self.click(self.HEADER_NAVIGATION_BAR, timeout=10)  # 点击头部导航栏
        if navigation_name is not None:
            locator = self.get_navigation_name_input_locator(index)  # 获取导航名称输入框定位器
            self.click(locator, timeout=10)  # 聚焦导航名称输入框
            self.input_text(locator, navigation_name)  # 输入导航名称
        self.click(self.PUBLISH_BUTTON, timeout=10)  # 点击发布
        self.click(self.PUBLISH_CONFIRM_BUTTON, timeout=10)  # 点击发布确认
        self.click(self.OPEN_PORTAL_LINK_IN_EDIT_PAGE, timeout=10)  # 点击打开专业门户
        self.switch_out_iframe()  # 切回默认上下文
        self.switch_to_new_window()  # 切换到新打开的窗口
        self.wait_for_ready_state_complete(timeout=10)  # 等待页面加载完成
        result = self.page_contains_text(navigation_name)  # 检查是否包含导航名称
        log.info(f"编辑门户结果：{result}")
        return result
