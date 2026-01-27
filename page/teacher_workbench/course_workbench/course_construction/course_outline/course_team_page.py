# encoding: utf-8
# @File  : course_team_page.py
# @Author:
# @Date  :
# @Desc  : 课程团队页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from logs.log import log
from page.teacher_workbench.course_workbench.course_workbench_page import CourseWorkbenchPage


class CourseTeamPage(CourseWorkbenchPage):
    """课程团队页面类。

    对外只暴露“服务方法”（如添加课程负责人等），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # ======================课程负责人======================
    # 课程负责人区域的编辑按钮
    COURSE_LEADER_EDIT_BUTTON = (By.XPATH, "//div[@class='section' and contains(.,'课程负责人')]//button")
    # 添加负责人入口
    ADD_COURSE_LEADER_BUTTON = (By.XPATH, "//div[contains(@class,'add-card') and contains(.,'添加负责人')]")
    # 添加负责人搜索框
    ADD_COURSE_LEADER_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='请输入教师工号或姓名']")
    # 确认添加按钮（负责人弹窗）
    CONFIRM_ADD_COURSE_LEADER_BUTTON = (By.XPATH, "//span[text()='确认']/parent::button")
    # 添加成功 toast 文案
    ADD_COURSE_LEADER_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='添加成功']")

    # ==================== 动态定位器 getter ====================

    def get_add_course_leader_row_button_locator(self, search_text):
        """搜索文本（教师工号或姓名）→ 该行「添加」按钮定位器。"""
        return (By.XPATH, f"//tr[contains(.,'{search_text}')]//span[text()=' 添加 ']/parent::button")

    # ==================== 服务方法（页面对外能力） ====================

    def add_course_leader(self, search_text):
        """在课程团队页添加课程负责人：编辑负责人区域、添加负责人、按工号/姓名搜索并添加、确认。返回是否出现添加成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.COURSE_LEADER_EDIT_BUTTON)  # 点击课程负责人编辑按钮
        self.click(self.ADD_COURSE_LEADER_BUTTON)  # 点击添加负责人
        self.input_text(self.ADD_COURSE_LEADER_SEARCH_INPUT, search_text)  # 输入教师工号或姓名搜索
        self.click(self.get_add_course_leader_row_button_locator(search_text))  # 点击该行添加按钮
        self.click(self.CONFIRM_ADD_COURSE_LEADER_BUTTON)  # 点击确认添加
        result = self.is_displayed(self.ADD_COURSE_LEADER_SUCCESS_MESSAGE)  # 检查是否出现添加成功提示
        log.info(f"添加课程负责人结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result
