# encoding: utf-8
# @File  : construction_history_page.py
# @Author:
# @Date  :
# @Desc  : 建设历程页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from logs.log import log
from page.teacher_workbench.course_workbench.course_workbench_page import CourseWorkbenchPage


class ConstructionHistoryPage(CourseWorkbenchPage):
    """建设历程页面类。

    对外只暴露“服务方法”（如编辑建设历程等），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
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
    # 保存成功 toast 文案
    SAVE_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='保存成功']")

    # ==================== 服务方法（页面对外能力） ====================

    def edit_construction_history(self, construction_time, construction_content, get_honor, construction_team):
        """在建设历程页编辑建设时间、建设内容、获得荣誉、建设团队并保存，返回是否出现保存成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.EDIT_BUTTON)  # 点击编辑按钮
        self.input_text(self.CONSTRUCTION_TIME_INPUT, construction_time)  # 输入建设时间
        self.input_text(self.CONSTRUCTION_CONTENT_INPUT, construction_content)  # 输入建设内容
        self.input_text(self.GET_HONOR_INPUT, get_honor)  # 输入获得荣誉
        self.input_text(self.CONSTRUCTION_TEAM_INPUT, construction_team)  # 输入建设团队
        self.click(self.SAVE_BUTTON)  # 点击保存
        result = self.is_displayed(self.SAVE_SUCCESS_MESSAGE)  # 检查是否出现保存成功提示
        log.info(f"编辑建设历程结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result
