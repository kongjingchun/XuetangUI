# encoding: utf-8
# @File  : homework_page.py
# @Author:
# @Date  :
# @Desc  : 作业页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from logs.log import log
from page.teacher_workbench.course_workbench.course_construction.course_resource.course_resource_page import (
    CourseResourcePage,
)


class HomeworkPage(CourseResourcePage):
    """作业页面类。

    继承 CourseResourcePage，提供作业页面的能力。
    对外只暴露“服务方法”（如新建作业），不暴露每个按钮/输入框的 click/input 封装。定位器集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 新建作业按钮
    NEW_HOMEWORK_BUTTON = (By.XPATH, "//button[contains(.,'新建作业')]")
    # 作业标题输入框
    HOMEWORK_TITLE_INPUT = (By.XPATH, "//input[@placeholder='请输入作业标题']")
    # 创建并编辑按钮
    CREATE_AND_EDIT_BUTTON = (By.XPATH, "//button[contains(.,'创建并编辑')]")
    # 作业创建成功提示框
    HOMEWORK_CREATED_SUCCESS_MESSAGE = (By.XPATH, "//p[contains(.,'作业创建成功')]")
    # 选择题目按钮
    SELECT_QUESTION_BUTTON = (By.XPATH, "//button[contains(.,'选择题目')]")
    # 题目全选勾选框
    ALL_SELECT_CHECKBOX = (By.XPATH, "//tr[contains(.,'最后修改时间')]/th[1]//label")
    # 确定选择按钮
    CONFIRM_SELECT_BUTTON = (By.XPATH, "//button[contains(.,'确定选择')]")
    # 已添加提示框
    ADDED_SUCCESS_MESSAGE = (By.XPATH, "//p[contains(.,'已添加')]")
    # 保存按钮
    SAVE_BUTTON = (By.XPATH, "//button[contains(.,'保存')]")
    # 保存成功提示框
    SAVE_SUCCESS_MESSAGE = (By.XPATH, "//p[contains(.,'保存成功')]")

    # ==================== 动态定位器 getter ====================
    # （本页无动态定位器）

    # ==================== 服务方法（页面对外能力） ====================

    def new_homework(self, homework_title):
        """新建作业：填写标题、创建并编辑、选择题目、保存，返回是否出现保存成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.NEW_HOMEWORK_BUTTON)  # 点击新建作业
        self.input_text(self.HOMEWORK_TITLE_INPUT, homework_title)  # 输入作业标题
        self.click(self.CREATE_AND_EDIT_BUTTON)  # 点击创建并编辑
        self.click(self.SELECT_QUESTION_BUTTON)  # 点击选择题目
        self.click(self.ALL_SELECT_CHECKBOX)  # 全选题目
        self.click(self.CONFIRM_SELECT_BUTTON)  # 确定选择
        self.click(self.SAVE_BUTTON)  # 点击保存
        result = self.is_displayed(self.SAVE_SUCCESS_MESSAGE)  # 检查是否出现保存成功提示
        log.info(f"新建作业结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result
