# encoding: utf-8
# @File  : CourseTeamPage.py
# @Author: 孔敬淳
# @Date  : 2026/01/17
# @Desc  : 课程团队页面对象类，封装课程团队相关的页面操作方法

from selenium.webdriver.common.by import By
from base.BasePage import BasePage
from logs.log import log
from page.course_workbench.CourseWorkbenchPage import CourseWorkbenchPage


class CourseTeamPage(CourseWorkbenchPage, BasePage):
    """课程团队页面类

    继承BasePage类，提供课程团队页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ==================== 课程团队定位器=============================================================
    # 课程团队iframe
    COURSE_TEAM_IFRAME = (By.XPATH, "//iframe[@id='course-workspace-iframe']")
