# encoding: utf-8
# @File  : link_page.py
# @Author: 孔敬淳
# @Date  : 2025/01/20
# @Desc  : 链接页面对象类，封装链接相关的页面操作方法
from selenium.webdriver.common.by import By

from logs.log import log
from page.course_workbench.course_construction.course_resource.course_resource_page import CourseResourcePage


class LinkPage(CourseResourcePage):
    """链接页面类

    继承CourseResourcePage基类，提供链接页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化链接页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
    # 新建链接按钮
    NEW_LINK_BUTTON = (By.XPATH, "//button[contains(.,' 新建链接 ')]")
    # 链接地址输入框
    LINK_ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='请输入链接地址（含 http/https）']")
    # 确定按钮
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(.,'确定')]")
    # 新建链接成功提示框
    NEW_LINK_SUCCESS_MESSAGE = (By.XPATH, "//p[contains(.,'链接创建成功')]")
    # ==================== 动态定位器方法（需要参数的定位器）====================

    # ==================== 页面操作方法 ====================
    def click_new_link_button(self):
        """点击新建链接按钮"""
        log.info(f"点击新建链接按钮，定位器为：{self.NEW_LINK_BUTTON[1]}")
        return self.click(self.NEW_LINK_BUTTON)

    def input_link_address(self, link_address):
        """输入链接地址"""
        log.info(f"输入链接地址：{link_address}，定位器为：{self.LINK_ADDRESS_INPUT[1]}")
        return self.input_text(self.LINK_ADDRESS_INPUT, link_address)

    def click_confirm_button(self):
        """点击确定按钮"""
        log.info(f"点击确定按钮，定位器为：{self.CONFIRM_BUTTON[1]}")
        return self.click(self.CONFIRM_BUTTON)

    def is_new_link_success_message_displayed(self):
        """查看新建链接成功提示框是否出现

        Returns:
            bool: True表示新建链接成功提示框出现，False表示未出现
        """
        log.info(f"查看新建链接成功提示框是否出现，定位器为：{self.NEW_LINK_SUCCESS_MESSAGE[1]}")
        return self.is_displayed(self.NEW_LINK_SUCCESS_MESSAGE)

    def new_link(self, link_address):
        """新建链接"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程资源iframe
        self.switch_to_iframe(self.COURSE_RESOURCE_IFRAME)
        # 点击新建链接按钮
        self.click_new_link_button()
        # 输入链接地址
        self.input_link_address(link_address)
        # 点击确定按钮
        self.click_confirm_button()
        # 断言新建链接成功提示框是否出现
        result = self.is_new_link_success_message_displayed()
        log.info(f"新建链接结果：{result}")
        # 切出课程资源iframe
        self.switch_out_iframe()
        return result
