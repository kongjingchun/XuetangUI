# encoding: utf-8
# @File  : course_objective_page.py
# @Author:
# @Date  :
# @Desc  : 课程目标页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from logs.log import log
from page.teacher_workbench.course_workbench.course_workbench_page import CourseWorkbenchPage


class CourseObjectivePage(CourseWorkbenchPage):
    """课程目标页面类。

    对外只暴露“服务方法”（如编辑课程目标描述、添加目标、关联毕业要求等），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # ======================课程目标概览======================
    # 编辑描述按钮
    EDIT_DESCRIPTION_BUTTON = (By.XPATH, "//span[text()='编辑描述']/parent::button")
    # 课程目标描述输入框
    COURSE_OBJECTIVE_DESCRIPTION_INPUT = (By.XPATH, "//textarea[@placeholder='请输入课程目标的整体描述...']")
    # 课程描述保存按钮
    COURSE_DESCRIPTION_SAVE_BUTTON = (By.XPATH, "//span[contains(.,'保存')]/parent::button")
    # 保存成功 toast 文案
    SAVE_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='保存成功']")

    # ======================课程目标管理======================
    # 添加目标按钮
    ADD_OBJECTIVE_BUTTON = (By.XPATH, "//span[contains(.,'添加目标')]/parent::button")
    # 目标标题输入框
    OBJECTIVE_TITLE_INPUT = (By.XPATH, "//textarea[@placeholder='请输入目标标题']")
    # 添加标签按钮
    ADD_TAG_BUTTON = (By.XPATH, "//span[contains(.,'添加标签')]/parent::button")
    # 标签输入框
    TAG_INPUT = (By.XPATH, "//input[@placeholder='输入标签后按回车键添加']")
    # 添加课程目标弹窗中的创建按钮
    CREATE_OBJECTIVE_BUTTON = (By.XPATH, "//div[@aria-label='添加课程目标']//span[contains(.,'创建')]/parent::button")
    # 创建课程目标成功 toast 文案
    CREATE_OBJECTIVE_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='创建课程目标成功']")
    # 关联毕业要求按钮
    ASSOCIATE_GRADUATION_REQUIREMENTS_BUTTON = (By.XPATH, "//span[text()=' 关联毕业要求 ']/parent::button")
    # 添加毕业要求按钮
    ADD_GRADUATION_REQUIREMENTS_BUTTON = (By.XPATH, "//span[text()=' 添加毕业要求 ']/parent::button")
    # 关联毕业要求确认按钮
    ASSOCIATE_GRADUATION_REQUIREMENTS_CONFIRM_BUTTON = (By.XPATH, "//span[text()=' 确定 ']/parent::button")
    # 添加毕业要求关联成功 toast 文案
    ASSOCIATE_GRADUATION_REQUIREMENTS_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='添加毕业要求关联成功']")

    # ==================== 动态定位器 getter ====================

    def get_graduation_requirement_checkbox_locator(self, requirement_name):
        """毕业要求名称 → 该毕业要求项（可点击区域）定位器。"""
        return (By.XPATH, f"//span[text() = '{requirement_name}']/ancestor::div[@class = 'requirement-info']")

    # ==================== 服务方法（页面对外能力） ====================

    def edit_course_objective_description(self, description):
        """在课程目标概览页编辑描述并保存，返回是否出现保存成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.EDIT_DESCRIPTION_BUTTON)  # 点击编辑描述按钮
        self.input_text(self.COURSE_OBJECTIVE_DESCRIPTION_INPUT, description)  # 输入课程目标描述
        self.click(self.COURSE_DESCRIPTION_SAVE_BUTTON)  # 点击保存
        result = self.is_displayed(self.SAVE_SUCCESS_MESSAGE)  # 检查是否出现保存成功提示
        log.info(f"编辑课程目标描述结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def add_objective(self, title, tag):
        """添加课程目标：填写目标标题、添加标签并创建，返回是否出现创建课程目标成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.ADD_OBJECTIVE_BUTTON)  # 点击添加目标按钮
        self.input_text(self.OBJECTIVE_TITLE_INPUT, title)  # 输入目标标题
        self.click(self.ADD_TAG_BUTTON)  # 点击添加标签按钮
        self.input_text(self.TAG_INPUT, tag, need_enter=True)  # 输入标签并回车
        self.click(self.CREATE_OBJECTIVE_BUTTON)  # 点击创建目标
        result = self.is_displayed(self.CREATE_OBJECTIVE_SUCCESS_MESSAGE)  # 检查是否出现创建成功提示
        log.info(f"添加目标结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def associate_graduation_requirements(self, requirement_name):
        """关联毕业要求：点击关联毕业要求、添加毕业要求、勾选指定毕业要求并确定，返回是否出现添加毕业要求关联成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.ASSOCIATE_GRADUATION_REQUIREMENTS_BUTTON)  # 点击关联毕业要求按钮
        self.click(self.ADD_GRADUATION_REQUIREMENTS_BUTTON)  # 点击添加毕业要求按钮
        self.click(self.get_graduation_requirement_checkbox_locator(requirement_name))  # 勾选指定毕业要求
        self.click(self.ASSOCIATE_GRADUATION_REQUIREMENTS_CONFIRM_BUTTON)  # 点击确定
        result = self.is_displayed(self.ASSOCIATE_GRADUATION_REQUIREMENTS_SUCCESS_MESSAGE)  # 检查是否出现关联成功提示
        log.info(f"关联毕业要求结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result
