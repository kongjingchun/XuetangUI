# encoding: utf-8
# @File  : MajorCourseGroupGraphPage.py
# @Author: 孔敬淳
# @Date  : 2026/01/14
# @Desc  : 专业课程群图谱页面对象类，封装专业课程群图谱相关的页面操作方法
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class MajorCourseGroupGraphPage(BasePage):
    """专业课程群图谱页面类

    继承BasePage类，提供专业课程群图谱页面元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化专业课程群图谱页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)
