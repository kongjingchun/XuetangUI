# encoding: utf-8
# @File  : overview_page.py
# @Author: 孔敬淳
# @Date  : 2025/01/21
# @Desc  : 概览页面对象类，封装概览相关的页面操作方法
from selenium.webdriver.common.by import By
from logs.log import log
from page.course_workbench.course_construction.course_resource.course_resource_page import CourseResourcePage


class OverviewPage(CourseResourcePage):
    """概览页面类

    继承CourseResourcePage基类，提供概览页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化概览页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
    # 资源数量展示
    RESOURCE_COUNT_DISPLAY = (By.XPATH, "//div[./div[text()='资源数']]/div[@class='stat-number']")
    # ==================== 动态定位器方法（需要参数的定位器）====================

    # ==================== 页面操作方法 ====================
    def get_resource_count(self):
        """获取资源数量"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程资源iframe
        self.switch_to_iframe(self.COURSE_RESOURCE_IFRAME)
        # 获取资源数量
        log.info(f"获取资源数量：{self.RESOURCE_COUNT_DISPLAY[1]}")
        resource_count_str = self.get_text(self.RESOURCE_COUNT_DISPLAY)
        # 切出iframe
        self.switch_out_iframe()
        return resource_count_str
