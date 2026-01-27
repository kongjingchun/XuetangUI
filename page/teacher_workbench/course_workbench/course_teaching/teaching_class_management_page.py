# encoding: utf-8
# @File  : teaching_class_management_page.py
# @Author:
# @Date  :
# @Desc  : 教学班管理页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from logs.log import log
from page.teacher_workbench.course_workbench.course_workbench_page import CourseWorkbenchPage


class TeachingClassManagementPage(CourseWorkbenchPage):
    """教学班管理页面类。

    继承 CourseWorkbenchPage，提供教学班管理页面的能力。
    对外只暴露“服务方法”（如创建教学班、设置主讲教师），不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 创建教学班按钮
    CREATE_TEACHING_CLASS_BUTTON = (By.XPATH, "//button[contains(.,'创建教学班')]")
    # 创建教学班弹窗 - 教学班名称输入框
    TEACHING_CLASS_NAME_INPUT = (By.XPATH, "//div[@aria-label='创建教学班']//input[@placeholder = '请输入教学班名称']")
    # 创建教学班弹窗 - 教学班编号输入框
    TEACHING_CLASS_CODE_INPUT = (By.XPATH, "//div[@aria-label='创建教学班']//input[@placeholder = '请输入教学班编号']")
    # 创建教学班弹窗 - 开课时间输入框
    OPEN_COURSE_TIME_INPUT = (By.XPATH, "//div[@aria-label='创建教学班']//input[@placeholder = '开课时间']")
    # 创建教学班弹窗 - 结课时间输入框
    END_COURSE_TIME_INPUT = (By.XPATH, "//div[@aria-label='创建教学班']//input[@placeholder = '结课时间']")
    # 无结课时间按钮
    NO_END_COURSE_TIME_BUTTON = (By.XPATH, "//span[text()=' 无结课时间 ']/preceding-sibling::span")
    # 创建教学班弹窗 - 选课开始时间输入框
    SELECT_COURSE_START_TIME_INPUT = (By.XPATH, "//div[@aria-label='创建教学班']//input[@placeholder = '选课开始时间']")
    # 创建教学班弹窗 - 选课结束时间输入框
    SELECT_COURSE_END_TIME_INPUT = (By.XPATH, "//div[@aria-label='创建教学班']//input[@placeholder = '选课结束时间']")
    # 日期选择器弹窗 - 确定按钮
    DATE_CONFIRM_BUTTON = (By.XPATH, "//div[contains(@class,'el-picker__popper') and @aria-hidden='false']//button[contains(.,'确定')]")
    # 创建教学班弹窗 - 确定按钮
    CREATE_CONFIRM_BUTTON = (By.XPATH, "//div[@aria-label='创建教学班']//button[contains(.,'确定')]")
    # 设置（修改）主讲老师按钮
    SET_LECTURER_BUTTON = (By.XPATH, "//div[./div/span[contains(.,'主讲教师')] and @class='edit-teacher-card']")
    # 确认设置弹窗 - 确认按钮
    CONFIRM_SET_LECTURER_BUTTON = (By.XPATH, "//div[@aria-label='确认设置']//button[contains(.,'确认')]")
    # 设置成功提示文案
    SET_LECTURER_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='设置成功']")

    # ==================== 动态定位器 getter ====================

    def get_allow_student_select_switch_locator(self, boolean=True):
        """是否允许学生自选（True/False）→ 对应开关定位器。"""
        if boolean:
            return (By.XPATH, "//div[./label[text()='是否允许学生自选']]//label[./span[text()='是']]")
        return (By.XPATH, "//div[./label[text()='是否允许学生自选']]//label[./span[text()='否']]")

    def get_allow_student_drop_switch_locator(self, boolean=True):
        """是否允许学生退课（True/False）→ 对应开关定位器。"""
        if boolean:
            return (By.XPATH, "//div[./label[text()='是否允许学生退课']]//label[./span[text()='是']]")
        return (By.XPATH, "//div[./label[text()='是否允许学生退课']]//label[./span[text()='否']]")

    def get_teaching_class_locator(self, value):
        """教学班名称或编号 → 列表中该教学班单元格/行定位器（用于校验是否创建成功）。"""
        return (By.XPATH, f"//td/div[contains(.,'{value}')]")

    def get_member_management_button_locator(self, value):
        """教学班名称或编号 → 该行「成员管理」按钮定位器。"""
        return (By.XPATH, f"//tr[contains(.,'{value}')]//button[contains(.,'成员管理')]")

    def get_replace_to_main_teacher_button_locator(self, value):
        """教师姓名或工号 → 该行「替换为主讲教师」按钮定位器。"""
        return (By.XPATH, f"//tr[contains(.,'{value}')]//span[text()=' 替换为主讲教师 ']")

    # ==================== 服务方法（页面对外能力） ====================

    def create_teaching_class(
        self,
        class_name,
        class_code,
        open_course_time,
        select_course_start_time,
        select_course_end_time,
        allow_student_self_select=True,
        allow_student_drop=True,
    ):
        """创建教学班：填写名称、编号、开课/选课时间，是否允许自选与退课，提交创建，返回列表中是否出现该教学班（以 class_code 校验）。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.CREATE_TEACHING_CLASS_BUTTON)  # 点击创建教学班，打开弹窗
        self.input_text(self.TEACHING_CLASS_NAME_INPUT, class_name)  # 输入教学班名称
        self.input_text(self.TEACHING_CLASS_CODE_INPUT, class_code)  # 输入教学班编号
        self.input_text(self.OPEN_COURSE_TIME_INPUT, open_course_time)  # 输入开课时间
        self.click(self.DATE_CONFIRM_BUTTON)  # 日期弹窗中点击确定
        self.click(self.NO_END_COURSE_TIME_BUTTON)  # 点击无结课时间
        self.click(self.get_allow_student_select_switch_locator(allow_student_self_select))  # 是否允许学生自选
        self.input_text(self.SELECT_COURSE_START_TIME_INPUT, select_course_start_time)  # 输入选课开始时间
        self.click(self.DATE_CONFIRM_BUTTON)  # 日期弹窗中点击确定
        self.input_text(self.SELECT_COURSE_END_TIME_INPUT, select_course_end_time)  # 输入选课结束时间
        self.click(self.DATE_CONFIRM_BUTTON)  # 日期弹窗中点击确定
        self.click(self.get_allow_student_drop_switch_locator(allow_student_drop))  # 是否允许学生退课
        self.click(self.CREATE_CONFIRM_BUTTON, timeout=15)  # 点击创建确定（创建耗时较长，延长等待）
        result = self.is_displayed(self.get_teaching_class_locator(class_code))  # 列表中是否出现该教学班（以编号校验）
        log.info(f"创建教学班结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def set_lecturer(self, class_name_or_code, lecturer_name_or_code):
        """设置主讲教师：按教学班进入成员管理，设置主讲老师，选择指定教师替换为主讲并确认，返回是否出现设置成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.get_member_management_button_locator(class_name_or_code))  # 点击该教学班的成员管理
        self.click(self.SET_LECTURER_BUTTON)  # 点击设置（修改）主讲老师
        self.click(self.get_replace_to_main_teacher_button_locator(lecturer_name_or_code))  # 点击该教师的「替换为主讲教师」
        self.click(self.CONFIRM_SET_LECTURER_BUTTON)  # 点击确认设置
        result = self.is_displayed(self.SET_LECTURER_SUCCESS_MESSAGE)  # 检查是否出现设置成功提示
        log.info(f"设置主讲教师结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result
