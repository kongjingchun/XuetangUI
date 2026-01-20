# encoding: utf-8
# @File  : MajorPortalManagePage.py
# @Author: 孔敬淳
# @Date  : 2025/12/31
# @Desc  : 专业门户管理页面对象类，封装专业门户管理相关的页面操作方法
from time import sleep
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class MajorPortalManagePage(BasePage):
    """专业门户管理页面类

    继承BasePage类，提供专业门户管理页面元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化专业门户管理页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
    # 专业门户管理iframe
    MAJOR_PORTAL_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2104']")
    # 搜索关键词输入框
    SEARCH_KEYWORD_INPUT = (By.XPATH, "//input[@placeholder='专业名称 ｜ 专业代码']")
    # 搜索按钮
    SEARCH_BUTTON = (By.XPATH, "//button[contains(.,'搜索')]")
    # 专业门户管理编辑页iframe
    MAJOR_PORTAL_EDIT_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-3005']")
    # 头部导航栏元素
    HEADER_NAVIGATION_BAR = (By.XPATH, "//div[@class='page-header']//h1")
    # 编辑页面按钮
    EDIT_PAGE_BUTTON = (By.XPATH, "//button[contains(.,'编辑页面')]")
    # 发布按钮
    PUBLISH_BUTTON = (By.XPATH, "//button[contains(.,'发布')]")
    # 发布确认按钮
    PUBLISH_CONFIRM_BUTTON = (By.XPATH, "//div[@aria-label='发布确认']//button[contains(.,'确定')]")
    # 编辑页打开专业门户链接
    OPEN_PORTAL_LINK_IN_EDIT_PAGE = (By.XPATH, "//a[contains(.,' 打开专业门户 ')]")

    # ==================== 动态定位器方法（需要参数的定位器）====================

    def get_open_portal_button_locator(self, major_name):
        """获取根据专业名称定位打开门户按钮的定位器

        Args:
            major_name: 专业名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//tr[.//td[contains(.,'{major_name}')]]//button[contains(.,'打开门户')]")

    def get_edit_button_locator(self, major_name):
        """获取根据专业名称定位编辑按钮的定位器

        Args:
            major_name: 专业名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//tr[.//td[contains(.,'{major_name}')]]//button[contains(.,'编辑')]")

    def get_tab_locator(self, index=1):
        """获取根据索引定位标签页的定位器

        Args:
            index: 标签页索引，从1开始，默认为1（第1个标签页）

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"(//span[contains(.,'专业门户管理')])[{index}]")

    def get_navigation_name_input_locator(self, index=1):
        """获取导航名称设置输入框的定位器

        Args:
            index: 导航索引，从1开始，默认为1（第1个导航）

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"(//label[text()='名称'])[{index}]/following-sibling::div//input")

    # ==================== 页面操作方法 ====================

    def switch_2_major_portal_manage_iframe(self):
        """切换到专业门户管理页面的iframe

        Returns:
            切换操作结果
        """
        log.info(f"切换到专业门户管理页面的iframe，定位器为：{self.MAJOR_PORTAL_MANAGE_IFRAME[1]}")
        return self.switch_to_iframe(self.MAJOR_PORTAL_MANAGE_IFRAME)

    def input_search_keyword(self, keyword):
        """输入搜索关键词

        Args:
            keyword: 搜索关键词（专业名称或专业代码）

        Returns:
            输入操作结果
        """
        log.info(f"输入搜索关键词：{keyword}，定位器为：{self.SEARCH_KEYWORD_INPUT[1]}")
        return self.input_text(self.SEARCH_KEYWORD_INPUT, keyword)

    def click_search_button(self):
        """点击搜索按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击搜索按钮，定位器为：{self.SEARCH_BUTTON[1]}")
        return self.click(self.SEARCH_BUTTON)

    def click_open_portal_button_by_major_name(self, major_name):
        """根据专业名称点击打开门户按钮

        Args:
            major_name: 专业名称

        Returns:
            点击操作结果
        """
        locator = self.get_open_portal_button_locator(major_name)
        log.info(f"根据专业名称'{major_name}'点击打开门户按钮，定位器为：{locator[1]}")
        return self.click(locator, timeout=15)

    def click_edit_button_by_major_name(self, major_name):
        """根据专业名称点击编辑按钮

        Args:
            major_name: 专业名称

        Returns:
            点击操作结果
        """
        locator = self.get_edit_button_locator(major_name)
        log.info(f"根据专业名称'{major_name}'点击编辑按钮，定位器为：{locator[1]}")
        return self.click(locator, timeout=15, fluent=False)

    def click_tab_by_index(self, index=1):
        """根据索引点击标签页

        Args:
            index: 标签页索引，从1开始，默认为1（第1个标签页）

        Returns:
            点击操作结果
        """
        locator = self.get_tab_locator(index)
        log.info(f"点击标签页（索引：{index}），定位器为：{locator[1]}")
        return self.click(locator, timeout=10)

    def click_edit_page_button_by_major_name(self, major_name):
        """根据专业名称点击编辑页面按钮

        Args:
            major_name: 专业名称

        Returns:
            点击操作结果
        """
        # 切换到专业门户管理iframe
        self.switch_2_major_portal_manage_iframe()
        # 输入搜索关键词
        self.input_search_keyword(major_name)
        # 点击搜索按钮
        self.click_search_button()
        sleep(1)
        # 根据专业名称点击编辑按钮
        result = self.click_edit_button_by_major_name(major_name)
        # 切出专业门户管理iframe
        self.switch_out_iframe()
        log.info(f"根据专业名称'{major_name}'点击编辑按钮结果：{result}")
        return result

    # ======================================= 编辑页面元素操作 ======================================

    def switch_2_major_portal_edit_iframe(self):
        """切换到专业门户管理编辑页iframe

        Returns:
            切换操作结果
        """
        log.info(f"切换到专业门户管理编辑页iframe，定位器为：{self.MAJOR_PORTAL_EDIT_IFRAME[1]}")
        return self.switch_to_iframe(self.MAJOR_PORTAL_EDIT_IFRAME)

    def click_edit_page_button(self):
        """点击编辑页面按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击编辑页面按钮，定位器为：{self.EDIT_PAGE_BUTTON[1]}")
        return self.click(self.EDIT_PAGE_BUTTON, timeout=10)

    def click_header_navigation_bar(self):
        """点击头部导航栏

        Returns:
            点击操作结果
        """
        log.info(f"点击头部导航栏，定位器为：{self.HEADER_NAVIGATION_BAR[1]}")
        return self.click(self.HEADER_NAVIGATION_BAR, timeout=10)

    def input_navigation_name(self, navigation_name, index=1):
        """输入导航名称

        Args:
            navigation_name: 导航名称
            index: 导航索引，从1开始，默认为1（第1个导航）

        Returns:
            输入操作结果
        """
        locator = self.get_navigation_name_input_locator(index)
        log.info(f"输入导航名称（索引：{index}）：{navigation_name}，定位器为：{locator[1]}")
        self.click(locator, timeout=10)
        result = self.input_text(locator, navigation_name)
        return result

    def click_publish_button(self):
        """点击发布按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击发布按钮，定位器为：{self.PUBLISH_BUTTON[1]}")
        return self.click(self.PUBLISH_BUTTON, timeout=10)

    def click_publish_confirm_button(self):
        """点击发布确认按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击发布确认按钮，定位器为：{self.PUBLISH_CONFIRM_BUTTON[1]}")
        return self.click(self.PUBLISH_CONFIRM_BUTTON, timeout=10)

    def click_open_portal_link_in_edit_page(self):
        """点击编辑页打开专业门户链接

        Returns:
            点击操作结果
        """
        log.info(f"点击编辑页打开专业门户链接，定位器为：{self.OPEN_PORTAL_LINK_IN_EDIT_PAGE[1]}")
        return self.click(self.OPEN_PORTAL_LINK_IN_EDIT_PAGE, timeout=10)

    def edit_portal(self, navigation_name=None, index=1):
        """编辑门户

        Args:
            navigation_name: 导航名称
            index: 导航索引，从1开始，默认为1（第1个导航）

        Returns:
            bool: True表示编辑成功，False表示编辑失败
        """
        # 切换到专业门户管理编辑页iframe
        self.switch_2_major_portal_edit_iframe()
        # 点击编辑页面按钮
        self.click_edit_page_button()
        # 点击头部导航栏
        self.click_header_navigation_bar()
        # 输入导航名称
        self.input_navigation_name(navigation_name, index=index)
        # 点击发布按钮
        self.click_publish_button()
        # 点击发布确认按钮
        self.click_publish_confirm_button()
        # 点击编辑页打开专业门户链接
        self.click_open_portal_link_in_edit_page()
        # 切出专业门户管理编辑页iframe
        self.switch_out_iframe()
        # 切换到最新打开的窗口
        self.switch_to_new_window()
        # 等待新页面加载完成
        self.wait_for_ready_state_complete(timeout=10)
        sleep(1)  # 额外等待1秒，确保页面内容完全加载
        result = self.page_contains_text(navigation_name)
        log.info(f"编辑门户结果：{result}")
        return result
