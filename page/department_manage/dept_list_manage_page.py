# encoding: utf-8
# @File  : DeptListManagePage.py
# @Author: 孔敬淳
# @Date  : 2025/12/29/16:27
# @Desc  : 院系列表管理页面对象类，封装院系列表管理相关的页面操作方法
from time import sleep
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class DeptListManagePage(BasePage):
    """院系列表管理页面类

    继承BasePage类，提供院系列表管理页面元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化院系列表管理页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
    # 院系管理iframe
    DEPT_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-3004']")
    # 新建院系按钮
    NEW_DEPT_BUTTON = (By.XPATH, "//button[contains(.,'新建院系')]")
    # 新建确定按钮
    NEW_DEPT_CONFIRM_BUTTON = (By.XPATH, "//span[text()='确定']/parent::button")
    # 创建成功提示框
    CREATE_SUCCESS_ALERT = (By.XPATH, "//p[text()='创建成功']")
    # 搜索关键词输入框
    SEARCH_KEYWORD_INPUT = (By.XPATH, "//input[@placeholder='院系名称 ｜ 院系代码']")
    # 删除院系按钮
    DELETE_BUTTON = (By.XPATH, "//button[contains(.,'删除院系')]")
    # 删除确认按钮
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//div[contains(.,'警告')]//button[contains(.,'确定')]")
    # 删除成功提示框
    DELETE_SUCCESS_ALERT = (By.XPATH, "//p[contains(.,'删除成功')]")

    # ==================== 动态定位器方法（需要参数的定位器）====================

    def get_new_dept_input_locator(self, input_name):
        """获取新建院系输入框的定位器

        Args:
            input_name: '代码' 或 '名称'

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        if '代码' in input_name:
            return (By.XPATH, "//input[contains(@placeholder,'请输入院系代码')]")
        elif '名称' in input_name:
            return (By.XPATH, "//input[contains(@placeholder,'请输入院系名称')]")
        else:
            return (By.XPATH, "//input[contains(@placeholder,'请输入院系代码')]")

    def get_edit_button_hover_locator(self, dept_code):
        """获取编辑悬停位置的定位器

        Args:
            dept_code: 院系代码

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//tr[contains(.,'{dept_code}')]//i[contains(@class,'action-icon')]")

    def get_edit_button_locator(self, dept_code):
        """获取编辑按钮的定位器

        Args:
            dept_code: 院系代码

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//tr[contains(.,'{dept_code}')]//button")

    # ==================== 页面操作方法 ====================

    def switch_2_dept_manage_iframe(self):
        """切换到院系列表管理页面的iframe

        Returns:
            切换操作结果
        """
        log.info(f"切换到院系列表管理页面的iframe，定位器为：{self.DEPT_MANAGE_IFRAME[1]}")
        return self.switch_to_iframe(self.DEPT_MANAGE_IFRAME)

    def click_new_dept_button(self):
        """点击新建院系按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击新建院系按钮，定位器为：{self.NEW_DEPT_BUTTON[1]}")
        return self.click(self.NEW_DEPT_BUTTON)

    def input_new_dept_input(self, input_name, value):
        """输入新建院系信息

        Args:
            input_name: 输入框名称
            value: 输入的值

        Returns:
            输入操作结果
        """
        locator = self.get_new_dept_input_locator(input_name)
        log.info(f"输入新建院系信息：{input_name}为：{value}，定位器为：{locator[1]}")
        return self.input_text(locator, value)

    def click_new_dept_confirm_button(self):
        """点击新建院系确认按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击新建院系确认按钮，定位器为：{self.NEW_DEPT_CONFIRM_BUTTON[1]}")
        return self.click(self.NEW_DEPT_CONFIRM_BUTTON)

    def is_create_success_alert_display(self):
        """查看创建成功提示框是否出现

        Returns:
            bool: True表示创建成功提示框出现，False表示未出现
        """
        log.info(f"查看创建成功提示框是否出现，定位器为：{self.CREATE_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.CREATE_SUCCESS_ALERT)

    def create_dept(self, dept_info):
        """创建院系

        Args:
            dept_info: 院系信息字典

        Returns:
            bool: True表示创建成功，False表示创建失败
        """
        self.switch_2_dept_manage_iframe()
        self.click_new_dept_button()
        for input_name, value in dept_info.items():
            self.input_new_dept_input(input_name, value)
        self.click_new_dept_confirm_button()
        result = self.is_create_success_alert_display()
        self.switch_out_iframe()
        log.info("创建院系结果：" + str(result))
        return result

    def input_search_keyword(self, keyword):
        """输入搜索关键词

        Args:
            keyword: 搜索关键词（院系名称或院系代码）

        Returns:
            输入操作结果
        """
        log.info(f"输入搜索关键词：{keyword}，定位器为：{self.SEARCH_KEYWORD_INPUT[1]}")
        return self.input_text(self.SEARCH_KEYWORD_INPUT, keyword)

    def hover_edit_button(self, dept_code):
        """鼠标悬停编辑按钮（根据院系代码）

        Args:
            dept_code: 院系代码

        Returns:
            悬停操作结果
        """
        locator = self.get_edit_button_hover_locator(dept_code)
        log.info(f"鼠标悬停编辑按钮（根据院系代码），定位器为：{locator[1]}")
        return self.hover(locator)

    def click_edit_button_by_dept_code(self, dept_code):
        """根据院系代码点击编辑按钮

        Args:
            dept_code: 院系代码

        Returns:
            点击操作结果
        """
        locator = self.get_edit_button_locator(dept_code)
        log.info(f"根据院系代码'{dept_code}'点击编辑按钮，定位器为：{locator[1]}")
        return self.click(locator, timeout=15)

    def click_delete_button(self):
        """点击删除院系按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击删除院系按钮，定位器为：{self.DELETE_BUTTON[1]}")
        return self.click(self.DELETE_BUTTON, timeout=15)

    def click_delete_confirm_button(self):
        """点击删除确认按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击删除确认按钮，定位器为：{self.DELETE_CONFIRM_BUTTON[1]}")
        return self.click(self.DELETE_CONFIRM_BUTTON, timeout=15)

    def is_delete_success_alert_display(self):
        """查看删除成功提示框是否出现

        Returns:
            bool: True表示删除成功提示框出现，False表示未出现
        """
        log.info(f"查看删除成功提示框是否出现，定位器为：{self.DELETE_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.DELETE_SUCCESS_ALERT)

    def delete_dept_by_dept_code(self, dept_code):
        """根据院系代码删除院系

        Args:
            dept_code: 院系代码

        Returns:
            bool: True表示删除成功，False表示删除失败
        """
        # 切换到iframe
        self.switch_2_dept_manage_iframe()
        # 输入搜索关键词
        self.input_search_keyword(dept_code)
        sleep(1)
        # 鼠标悬停编辑按钮
        self.hover_edit_button(dept_code)
        # 点击编辑按钮
        self.click_edit_button_by_dept_code(dept_code)
        # 点击删除按钮
        self.click_delete_button()
        # 点击删除确认按钮
        self.click_delete_confirm_button()
        # 断言删除成功提示框是否出现
        result = self.is_delete_success_alert_display()
        # 切出iframe
        self.switch_out_iframe()
        log.info(f"删除院系结果：{result}")
        return result
