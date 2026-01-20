# encoding: utf-8
# @File  : MajorAIModelPage.py
# @Author: 孔敬淳
# @Date  : 2025/12/31
# @Desc  : 专业AI模型页面对象类，封装专业AI模型相关的页面操作方法
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class MajorAIModelPage(BasePage):
    """专业AI模型页面类

    继承BasePage类，提供专业AI模型页面元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化专业AI模型页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
    # 专业AI模型iframe
    MAJOR_AI_MODEL_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2110']")

    # ==================== 动态定位器方法（需要参数的定位器）====================

    def get_menu_locator(self, menu_name):
        """获取根据菜单名称定位菜单的定位器

        Args:
            menu_name: 菜单名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//span[text()='{menu_name}']/parent::li")

    # ==================== 页面操作方法 ====================

    def switch_2_major_ai_model_iframe(self):
        """切换到专业AI模型页面的iframe

        Returns:
            切换操作结果
        """
        log.info(f"切换到专业AI模型页面的iframe，定位器为：{self.MAJOR_AI_MODEL_IFRAME[1]}")
        return self.switch_to_iframe(self.MAJOR_AI_MODEL_IFRAME)

    def click_menu_by_name(self, menu_name):
        """根据菜单名称点击菜单

        Args:
            menu_name: 菜单名称

        Returns:
            点击操作结果
        """
        # 切换到专业AI模型iframe
        self.switch_2_major_ai_model_iframe()
        # 根据菜单名称点击菜单
        locator = self.get_menu_locator(menu_name)
        log.info(f"点击菜单：{menu_name}，定位器为：{locator[1]}")
        result = self.click(locator)
        # 切出专业AI模型iframe
        self.switch_out_iframe()
        return result
