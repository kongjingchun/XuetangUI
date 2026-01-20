# encoding: utf-8
# @File  : ConstructionHistoryPage.py
# @Author: 孔敬淳
# @Date  : 2026/01/20
# @Desc  : 建设历程页面对象类，封装建设历程相关的页面操作方法

from selenium.webdriver.common.by import By

from logs.log import log
from page.course_workbench.course_workbench_page import CourseWorkbenchPage


class ConstructionHistoryPage(CourseWorkbenchPage):
    """建设历程页面类

    继承BasePage类，提供建设历程页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        super().__init__(driver)
    # ==================== 建设历程定位器=============================================================
    # 建设历程iframe
    CONSTRUCTION_HISTORY_IFRAME = (By.XPATH, "//iframe[@id='course-workspace-iframe']")
    # 编辑按钮
    EDIT_BUTTON = (By.XPATH, "//span[text()=' 编辑']/parent::button")
    # 建设时间输入框
    CONSTRUCTION_TIME_INPUT = (By.XPATH, "//input[@placeholder='请选择建设时间']")
    # 建设内容输入框
    CONSTRUCTION_CONTENT_INPUT = (By.XPATH, "//textarea[@placeholder='请输入建设内容']")
    # 获得荣誉输入框
    GET_HONOR_INPUT = (By.XPATH, "//textarea[@placeholder='请输入获得荣誉']")
    # 建设团队输入框
    CONSTRUCTION_TEAM_INPUT = (By.XPATH, "//textarea[@placeholder='请输入建设团队']")
    # 保存按钮
    SAVE_BUTTON = (By.XPATH, "//span[text()=' 保存']/parent::button")
    # 保存成功提示框
    SAVE_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='保存成功']")

    # ==================== 建设历程操作方法=============================================================

    def click_edit_button(self):
        """点击编辑按钮"""
        log.info(f"点击编辑按钮，定位器为：{self.EDIT_BUTTON[1]}")
        return self.click(self.EDIT_BUTTON)

    def input_construction_time(self, construction_time="2026-01-01"):
        """输入建设时间"""
        log.info(f"输入建设时间：{construction_time}，定位器为：{self.CONSTRUCTION_TIME_INPUT[1]}")
        return self.input_text(self.CONSTRUCTION_TIME_INPUT, construction_time)

    def input_construction_content(self, construction_content):
        """输入建设内容"""
        log.info(f"输入建设内容：{construction_content}，定位器为：{self.CONSTRUCTION_CONTENT_INPUT[1]}")
        return self.input_text(self.CONSTRUCTION_CONTENT_INPUT, construction_content)

    def input_get_honor(self, get_honor):
        """输入获得荣誉"""
        log.info(f"输入获得荣誉：{get_honor}，定位器为：{self.GET_HONOR_INPUT[1]}")
        return self.input_text(self.GET_HONOR_INPUT, get_honor)

    def input_construction_team(self, construction_team):
        """输入建设团队"""
        log.info(f"输入建设团队：{construction_team}，定位器为：{self.CONSTRUCTION_TEAM_INPUT[1]}")
        return self.input_text(self.CONSTRUCTION_TEAM_INPUT, construction_team)

    def click_save_button(self):
        """点击保存按钮"""
        log.info(f"点击保存按钮，定位器为：{self.SAVE_BUTTON[1]}")
        return self.click(self.SAVE_BUTTON)

    def assert_save_success(self):
        """断言保存成功"""
        log.info(f"断言保存成功，定位器为：{self.SAVE_SUCCESS_MESSAGE[1]}")
        return self.is_displayed(self.SAVE_SUCCESS_MESSAGE)

    def edit_construction_history(self, construction_time, construction_content, get_honor, construction_team):
        """编辑建设历程"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到建设历程iframe
        self.switch_to_iframe(self.CONSTRUCTION_HISTORY_IFRAME)
        # 点击编辑按钮
        self.click_edit_button()
        # 输入建设时间
        self.input_construction_time(construction_time)
        # 输入建设内容
        self.input_construction_content(construction_content)
        # 输入获得荣誉
        self.input_get_honor(get_honor)
        # 输入建设团队
        self.input_construction_team(construction_team)
        # 点击保存按钮
        self.click_save_button()
        # 断言保存成功
        result = self.assert_save_success()
        log.info(f"编辑建设历程结果：{result}")
        # 切出建设历程iframe
        self.switch_out_iframe()
        return result
