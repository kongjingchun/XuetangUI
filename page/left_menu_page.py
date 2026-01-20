# encoding: utf-8
# @File  : LeftMenuPage.py
# @Author: 孔敬淳
# @Date  : 2025/12/25/12:05
# @Desc  : 左侧菜单页面对象类，封装左侧菜单相关的页面操作方法
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class LeftMenuPage(BasePage):
    """左侧菜单页面类

    继承BasePage类，提供左侧菜单页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化左侧菜单页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 动态定位器方法（需要参数的定位器）====================

    def get_two_level_menu_locator(self, menu_name):
        """获取二级菜单的定位器

        Args:
            menu_name: 菜单名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//div[text()='{menu_name}']/parent::div")

    # ==================== 页面操作方法 ====================

    def click_two_level_menu(self, menu_name):
        """点击二级菜单

        Args:
            menu_name: 菜单名称

        Returns:
            点击操作结果
        """
        locator = self.get_two_level_menu_locator(menu_name)
        log.info("点击二级菜单：" + menu_name + "，定位器为：" + locator[1])
        return self.click(locator)
