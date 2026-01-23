# encoding: utf-8
# @File  : CourseInfoPage.py
# @Author: 孔敬淳
# @Date  : 2026/01/17
# @Desc  : 课程信息页面对象类，封装课程信息相关的页面操作方法

from selenium.webdriver.common.by import By

from logs.log import log
from page.teacher_workbench.course_workbench.course_workbench_page import CourseWorkbenchPage


class CourseInfoPage(CourseWorkbenchPage):
    """课程信息页面类

    继承BasePage类，提供课程信息页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        super().__init__(driver)
    # ==================== 课程信息页面定位器=============================================================
    # 编辑按钮
    EDIT_BUTTON = (By.XPATH, "//span[contains(.,'编辑')]/parent::button")
    # 课程英文名称输入框
    COURSE_ENGLISH_NAME_INPUT = (By.XPATH, "//input[@placeholder='请输入课程英文名称']")
    # 课程中文简介输入框
    COURSE_CHINESE_INTRODUCTION_INPUT = (By.XPATH, "//textarea[@placeholder='请输入课程中文简介']")
    # 课程英文简介输入框
    COURSE_ENGLISH_INTRODUCTION_INPUT = (By.XPATH, "//textarea[@placeholder='请输入课程英文简介']")
    # 保存按钮
    SAVE_BUTTON = (By.XPATH, "//span[contains(.,'保存')]/parent::button")
    # 保存成功提示框
    SAVE_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='保存成功']")
    # ==================== 课程信息页面操作方法=============================================================

    def click_edit_button(self):
        """点击编辑按钮"""
        return self.click(self.EDIT_BUTTON)

    def input_course_english_name(self, english_name):
        """输入课程英文名称"""
        log.info(f"输入课程英文名称：{english_name}，定位器为：{self.COURSE_ENGLISH_NAME_INPUT[1]}")
        return self.input_text(self.COURSE_ENGLISH_NAME_INPUT, english_name)

    def input_course_chinese_introduction(self, chinese_introduction):
        """输入课程中文简介"""
        log.info(f"输入课程中文简介：{chinese_introduction}，定位器为：{self.COURSE_CHINESE_INTRODUCTION_INPUT[1]}")
        return self.input_text(self.COURSE_CHINESE_INTRODUCTION_INPUT, chinese_introduction)

    def input_course_english_introduction(self, english_introduction):
        """输入课程英文简介"""
        log.info(f"输入课程英文简介：{english_introduction}，定位器为：{self.COURSE_ENGLISH_INTRODUCTION_INPUT[1]}")
        return self.input_text(self.COURSE_ENGLISH_INTRODUCTION_INPUT, english_introduction)

    def click_save_button(self):
        """点击保存按钮"""
        log.info(f"点击保存按钮，定位器为：{self.SAVE_BUTTON[1]}")
        return self.click(self.SAVE_BUTTON)

    def assert_save_success(self):
        """断言保存成功"""
        log.info(f"断言保存成功，定位器为：{self.SAVE_SUCCESS_MESSAGE[1]}")
        return self.is_displayed(self.SAVE_SUCCESS_MESSAGE)

    # 编辑课程信息
    def edit_course_info(self, english_name, chinese_introduction, english_introduction):
        """编辑课程信息"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 点击编辑按钮
        self.click_edit_button()
        # 输入课程英文名称
        self.input_course_english_name(english_name)
        # 输入课程中文简介
        self.input_course_chinese_introduction(chinese_introduction)
        # 输入课程英文简介
        self.input_course_english_introduction(english_introduction)
        # 点击保存按钮
        self.click_save_button()
        # 断言保存成功
        result = self.assert_save_success()
        log.info(f"编辑课程信息结果：{result}")
        # 切出课程信息iframe
        self.switch_out_iframe()
        return result
