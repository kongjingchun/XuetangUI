# encoding: utf-8
# @File  : CourseWorkbenchPage.py
# @Author:
# @Date  :
# @Desc  : 课程工作台页面对象类，封装课程工作台相关的页面操作方法

from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class CourseWorkbenchPage(BasePage):
    """课程工作台页面类

    继承BasePage类，提供课程工作台页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化课程工作台页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
    # 课程工作台iframe
    COURSE_WORKBENCH_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-4002']")

    # ==================== 元素定位器（动态定位器）====================
    # 根据名称获取左侧菜单的定位器
    def get_left_menu_locator(self, menu_name):
        """获取根据名称获取左侧菜单的定位器

        Args:
            menu_name: 菜单名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//span[contains(.,'{menu_name}')]/parent::div")

    # ==================== 页面操作方法 ====================

    def click_left_menu(self, menu_name):
        """点击左侧菜单

        Args:
            menu_name: 菜单名称

        Returns:
            点击操作结果
        """
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 根据名称获取左侧菜单的定位器
        locator = self.get_left_menu_locator(menu_name)
        log.info("点击左侧菜单：" + menu_name + "，定位器为：" + locator[1])
        result = self.click(locator)
        # 切出课程工作台iframe
        self.switch_out_iframe()
        log.info(f"点击左侧菜单'{menu_name}'成功")
        return result
