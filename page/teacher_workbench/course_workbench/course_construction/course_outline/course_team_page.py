# encoding: utf-8
# @File  : CourseTeamPage.py
# @Author: 孔敬淳
# @Date  : 2026/01/17
# @Desc  : 课程团队页面对象类，封装课程团队相关的页面操作方法

from selenium.webdriver.common.by import By

from logs.log import log
from page.teacher_workbench.course_workbench.course_workbench_page import CourseWorkbenchPage


class CourseTeamPage(CourseWorkbenchPage):
    """课程团队页面类

    继承BasePage类，提供课程团队页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ==================== 课程团队定位器=============================================================
    # 课程负责人编辑按钮（退出编辑）
    COURSE_LEADER_EDIT_BUTTON = (By.XPATH, "//div[@class='section' and contains(.,'课程负责人')]//button")
    # 添加负责人按钮
    ADD_COURSE_LEADER_BUTTON = (By.XPATH, "//div[contains(@class,'add-card') and contains(.,'添加负责人')]")
    # 添加负责人搜索框
    ADD_COURSE_LEADER_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='请输入教师工号或姓名']")
    # 确认添加按钮
    CONFIRM_ADD_COURSE_LEADER_BUTTON = (By.XPATH, "//span[text()='确认']/parent::button")
    # 添加成功提示框
    ADD_COURSE_LEADER_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='添加成功']")

    # 添加教师按钮
    ADD_TEACHER_BUTTON = (By.XPATH, "//div[contains(@class,'add-card') and contains(.,'添加教师')]")
    # 添加教师搜索框
    ADD_TEACHER_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='请输入教师工号或姓名']")
    # 确认添加按钮
    CONFIRM_ADD_TEACHER_BUTTON = (By.XPATH, "//span[text()='确认']/parent::button")
    # 添加成功提示框
    ADD_TEACHER_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='添加成功']")

    # ==================== 动态定位器方法（需要参数的定位器）====================

    def get_add_course_leader_button_locator(self, search_text):
        """根据姓名工号返回添加按钮的定位器

        Args:
            search_text: 搜索文本

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//tr[contains(.,'{search_text}')]//span[text()=' 添加 ']/parent::button")

    # ==================== 课程团队操作方法=============================================================
    def click_course_leader_edit_button(self):
        """点击课程负责人编辑按钮"""
        log.info(f"点击课程负责人编辑按钮，定位器为：{self.COURSE_LEADER_EDIT_BUTTON[1]}")
        return self.click(self.COURSE_LEADER_EDIT_BUTTON)

    def click_add_course_leader_button(self):
        """点击添加负责人按钮"""
        log.info(f"点击添加负责人按钮，定位器为：{self.ADD_COURSE_LEADER_BUTTON[1]}")
        return self.click(self.ADD_COURSE_LEADER_BUTTON)

    def input_add_course_leader_search_input(self, search_text):
        """输入添加负责人搜索框"""
        log.info(f"输入添加负责人搜索框，定位器为：{self.ADD_COURSE_LEADER_SEARCH_INPUT[1]}")
        return self.input_text(self.ADD_COURSE_LEADER_SEARCH_INPUT, search_text)

    def click_add_course_leader_button_by_search_text(self, search_text):
        """根据姓名工号点击添加按钮"""
        locator = self.get_add_course_leader_button_locator(search_text)
        log.info(f"根据姓名工号点击添加按钮，定位器为：{locator[1]}")
        return self.click(locator)

    def click_confirm_add_course_leader_button(self):
        """点击确认添加按钮"""
        log.info(f"点击确认添加按钮，定位器为：{self.CONFIRM_ADD_COURSE_LEADER_BUTTON[1]}")
        return self.click(self.CONFIRM_ADD_COURSE_LEADER_BUTTON)

    def assert_add_course_leader_success(self):
        """断言添加负责人成功"""
        log.info(f"断言添加负责人成功，定位器为：{self.ADD_COURSE_LEADER_SUCCESS_MESSAGE[1]}")
        return self.is_displayed(self.ADD_COURSE_LEADER_SUCCESS_MESSAGE)

    # 添加课程负责人
    def add_course_leader(self, search_text):
        """添加课程负责人"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 点击课程负责人编辑按钮
        self.click_course_leader_edit_button()
        # 点击添加负责人按钮
        self.click_add_course_leader_button()
        # 输入添加负责人搜索框
        self.input_add_course_leader_search_input(search_text)
        # 根据姓名工号点击添加按钮
        self.click_add_course_leader_button_by_search_text(search_text)
        # 点击确认添加按钮
        self.click_confirm_add_course_leader_button()
        # 断言添加负责人成功
        result = self.assert_add_course_leader_success()
        log.info(f"添加课程负责人结果：{result}")
        # 切出iframe
        self.switch_out_iframe()
        return result
