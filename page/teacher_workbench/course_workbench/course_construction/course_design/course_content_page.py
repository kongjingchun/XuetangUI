# encoding: utf-8
# @File  : CourseContentPage.py
# @Author:
# @Date  :
# @Desc  : 课程内容页面对象类，封装课程内容相关的页面操作方法

from selenium.webdriver.common.by import By

from logs.log import log
from page.teacher_workbench.course_workbench.course_workbench_page import CourseWorkbenchPage


class CourseContentPage(CourseWorkbenchPage):
    """课程内容页面类

    继承CourseWorkbenchPage类，提供课程内容页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化课程内容页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)
