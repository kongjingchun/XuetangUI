# encoding: utf-8
# @File  : RoleManagePage.py
# @Author: 孔敬淳
# @Date  : 2025/12/31
# @Desc  : 角色管理页面对象类，封装角色管理相关的页面操作方法

from time import sleep
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class RoleManagePage(BasePage):
    """角色管理页面类

    继承BasePage类，提供角色管理页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化角色管理页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
    # 角色管理iframe
    ROLE_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2008']")
    # 用户搜索输入框
    USER_SEARCH_INPUT = (By.XPATH, "//input[contains(@placeholder,'用户ID')]")
    # 分配角色确认按钮
    ASSIGN_ROLE_CONFIRM_BUTTON = (By.XPATH, "//button[.//span[contains(.,'确定分配')]]")
    # 分配角色成功提示框
    ASSIGN_ROLE_SUCCESS_ALERT = (By.XPATH, "//p[contains(text(),'成功')]")

    # ==================== 动态定位器方法（需要参数的定位器）====================

    def get_assign_role_button_locator(self, role_name):
        """获取分配角色按钮的定位器

        Args:
            role_name: 角色名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//tbody//tr[contains(.,'" + role_name + "')]//span[contains(.,'分配')]/parent::button")

    def get_user_checkbox_locator(self, user_name):
        """获取用户复选框的定位器

        Args:
            user_name: 用户名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//tr[contains(.,'" + user_name + "')]//span[@class='el-checkbox__inner']")

    # ==================== 页面操作方法 ====================

    def switch_into_role_manage_iframe(self):
        """切换到角色管理iframe

        Returns:
            切换操作结果
        """
        log.info(f"切换到角色管理iframe，定位器为：{self.ROLE_MANAGE_IFRAME[1]}")
        return self.switch_to_iframe(self.ROLE_MANAGE_IFRAME)

    def click_assign_role_button(self, role_name):
        """点击分配角色按钮

        Args:
            role_name: 角色名称

        Returns:
            点击操作结果
        """
        locator = self.get_assign_role_button_locator(role_name)
        log.info(f"点击分配角色按钮，角色名称：{role_name}，定位器为：{locator[1]}")
        return self.click(locator)

    def input_user_search(self, user_name):
        """输入用户搜索信息

        Args:
            user_name: 用户名称

        Returns:
            输入操作结果
        """
        log.info(f"输入用户搜索信息：{user_name}，定位器为：{self.USER_SEARCH_INPUT[1]}")
        return self.input_text(self.USER_SEARCH_INPUT, user_name)

    def click_user_checkbox(self, user_name):
        """勾选用户复选框

        Args:
            user_name: 用户名称

        Returns:
            点击操作结果
        """
        locator = self.get_user_checkbox_locator(user_name)
        log.info(f"勾选用户复选框，用户名称：{user_name}，定位器为：{locator[1]}")
        return self.click(locator)

    def click_assign_role_confirm_button(self):
        """点击分配角色确认按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击分配角色确认按钮，定位器为：{self.ASSIGN_ROLE_CONFIRM_BUTTON[1]}")
        return self.click(self.ASSIGN_ROLE_CONFIRM_BUTTON)

    def is_assign_role_success_alert_display(self):
        """判断分配角色成功提示框是否出现

        Returns:
            bool: True表示分配成功提示框出现，False表示未出现
        """
        log.info(f"判断分配角色成功提示框是否出现，定位器为：{self.ASSIGN_ROLE_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.ASSIGN_ROLE_SUCCESS_ALERT)

    def assign_role_to_user(self, role_name, user_name=None):
        """分配角色给用户

        Args:
            role_name: 角色名称
            user_name: 用户名称（必填，用于勾选用户）

        Returns:
            bool: True表示分配成功，False表示分配失败
        """
        # 切换到角色管理iframe
        self.switch_into_role_manage_iframe()
        # 点击分配角色按钮
        self.click_assign_role_button(role_name)
        # 输入用户名称进行搜索
        self.input_user_search(user_name)
        sleep(1)
        # 勾选用户复选框
        self.click_user_checkbox(user_name)
        # 点击分配角色确认按钮
        self.click_assign_role_confirm_button()
        # 判断分配角色成功提示框是否出现
        result = self.is_assign_role_success_alert_display()
        # 切换出iframe，回到主页面
        self.switch_out_iframe()
        log.info(f"分配角色 {role_name} 给用户 {user_name} 完成")
        return result
