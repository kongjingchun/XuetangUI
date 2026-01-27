# encoding: utf-8
# @File  : course_info_page.py
# @Author:
# @Date  :
# @Desc  : 课程信息页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from logs.log import log
from page.teacher_workbench.course_workbench.course_workbench_page import CourseWorkbenchPage


class CourseInfoPage(CourseWorkbenchPage):
    """课程信息页面类。

    对外只暴露“服务方法”（如编辑课程信息等），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
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
    # 保存成功 toast 文案
    SAVE_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='保存成功']")

    # ==================== 服务方法（页面对外能力） ====================

    def edit_course_info(self, english_name, chinese_introduction, english_introduction):
        """在课程信息页编辑英文名称、中文简介、英文简介并保存，返回是否出现保存成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.EDIT_BUTTON)  # 点击编辑按钮
        self.input_text(self.COURSE_ENGLISH_NAME_INPUT, english_name)  # 输入课程英文名称
        self.input_text(self.COURSE_CHINESE_INTRODUCTION_INPUT, chinese_introduction)  # 输入课程中文简介
        self.input_text(self.COURSE_ENGLISH_INTRODUCTION_INPUT, english_introduction)  # 输入课程英文简介
        self.click(self.SAVE_BUTTON)  # 点击保存
        result = self.is_displayed(self.SAVE_SUCCESS_MESSAGE)  # 检查是否出现保存成功提示
        log.info(f"编辑课程信息结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result
