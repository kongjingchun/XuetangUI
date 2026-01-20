# encoding: utf-8
# @File  : TopMenuPage.py
# @Author: 孔敬淳
# @Date  : 2025/12/25/11:03
# @Desc  : 顶部菜单页面对象类，封装顶部菜单相关的页面操作方法
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class TopMenuPage(BasePage):
    """顶部菜单页面类

    继承BasePage类，提供顶部菜单页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化顶部菜单页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 动态定位器方法（需要参数的定位器）====================

    def get_school_switch_locator(self):
        """获取学校切换按钮的定位器

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@class='el-dropdown org-dropdown']")

    def get_school_switch_list_locator(self, school_name):
        """获取学校切换列表项的定位器

        Args:
            school_name: 学校名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//span[text()='{school_name}']/ancestor::li")

    def get_role_switch_locator(self):
        """获取角色切换按钮的定位器

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@class='role-tag']")

    def get_role_switch_list_locator(self, role_name):
        """获取角色切换列表项的定位器

        Args:
            role_name: 角色名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//span[text()='{role_name}']//ancestor::li")

    # ==================== 页面操作方法 ====================

    def click_school_switch(self):
        """点击学校切换按钮

        Returns:
            点击操作结果
        """
        locator = self.get_school_switch_locator()
        log.info("点击学校切换按钮，定位器为：" + locator[1])
        return self.click(locator)

    def click_school_switch_list(self, school_name):
        """选择切换的学校

        Args:
            school_name: 学校名称

        Returns:
            点击操作结果
        """
        locator = self.get_school_switch_list_locator(school_name)
        log.info("选择切换为" + school_name + "学校，定位器为：" + locator[1])
        return self.click(locator)

    def click_role_switch(self):
        """点击角色切换按钮

        Returns:
            点击操作结果
        """
        locator = self.get_role_switch_locator()
        log.info("点击角色切换按钮，定位器为：" + locator[1])
        return self.click(locator)

    def click_role_switch_list(self, role_name):
        """选择切换的角色

        Args:
            role_name: 角色名称

        Returns:
            点击操作结果
        """
        locator = self.get_role_switch_list_locator(role_name)
        log.info("选择切换为 [" + role_name + "] 角色，定位器为：" + locator[1])
        return self.click(locator)

    def switch_school(self, school_name):
        """切换学校

        Args:
            school_name: 学校名称

        Returns:
            切换操作结果
        """
        self.click_school_switch()
        return self.click_school_switch_list(school_name)

    def switch_role(self, role_name):
        """切换角色

        Args:
            role_name: 角色名称

        Returns:
            切换操作结果
        """
        self.click_role_switch()
        return self.click_role_switch_list(role_name)
