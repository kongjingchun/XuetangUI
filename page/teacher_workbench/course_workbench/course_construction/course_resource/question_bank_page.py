# encoding: utf-8
# @File  : question_bank_page.py
# @Author:
# @Date  :
# @Desc  : 题库页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_rich_text(...)。
from selenium.webdriver.common.by import By

from logs.log import log
from page.teacher_workbench.course_workbench.course_construction.course_resource.course_resource_page import (
    CourseResourcePage,
)


class QuestionBankPage(CourseResourcePage):
    """题库页面类。

    继承 CourseResourcePage，提供题库页面的能力。
    对外只暴露“服务方法”（如新建题目、导入题库），不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 新建题目按钮
    NEW_QUESTION_BUTTON = (By.XPATH, "//button[contains(.,'新建题目')]")
    # 题目内容输入框
    QUESTION_CONTENT_INPUT = (By.XPATH, "//div[text()='题目内容']/following-sibling::div//div[@contenteditable='true']")
    # 参考答案输入框
    REFERENCE_ANSWER_INPUT = (By.XPATH, "//div[text()='参考答案']/following-sibling::div//div[@contenteditable='true']")
    # 题目解析输入框
    QUESTION_ANALYSIS_INPUT = (By.XPATH, "//div[text()='题目解析']/following-sibling::div//div[@contenteditable='true']")
    # 选择知识点按钮
    SELECT_KNOWLEDGE_BUTTON = (By.XPATH, "//button[contains(.,'选择知识点')]")
    # 关联知识点确定按钮
    CONFIRM_KNOWLEDGE_BUTTON = (By.XPATH, "//span[text()='确定']")
    # 开放给学生开关
    OPEN_TO_STUDENTS_SWITCH = (By.XPATH, "//div[@class='el-switch__action']/parent::span")
    # 创建习题按钮
    CREATE_QUESTION_BUTTON = (By.XPATH, "//span[text()='创建']/parent::button")
    # 创建习题成功提示框
    CREATE_QUESTION_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='题目创建成功']")
    # 导入题库按钮
    IMPORT_QUESTION_BANK_BUTTON = (By.XPATH, "//button[contains(.,'导入题库')]")
    # 确认导入按钮
    CONFIRM_IMPORT_BUTTON = (By.XPATH, "//button[contains(.,'确认导入')]")
    # 导入题库成功提示框
    IMPORT_QUESTION_BANK_SUCCESS_MESSAGE = (By.XPATH, "//p[contains(.,'成功导入')]")

    # ==================== 动态定位器 getter ====================

    def get_new_question_dropdown_option_locator(self, question_type):
        """题目类型 → 新建题目下拉选项定位器。"""
        return (By.XPATH, f"//li[text()='{question_type}']")

    def get_knowledge_locator_by_name(self, knowledge_name):
        """知识点名称 → 知识点展示区域定位器。"""
        return (By.XPATH, f"//span[text()='{knowledge_name}']/parent::div")

    def get_select_knowledge_locator_by_name(self, knowledge_name):
        """知识点名称 → 选择关联知识点按钮定位器。"""
        return (By.XPATH, f"//span[text()='{knowledge_name}']/parent::div/following-sibling::div/button")

    # ==================== 服务方法（页面对外能力） ====================

    def new_question(
        self,
        question_type,
        question_content,
        reference_answer,
        question_analysis,
        knowledge_name,
    ):
        """新建题目：选择题型、填写内容与解析、关联知识点、开放给学生、创建，返回是否出现题目创建成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.NEW_QUESTION_BUTTON)  # 点击新建题目
        self.click(self.get_new_question_dropdown_option_locator(question_type))  # 选择题目类型
        self.input_rich_text(self.QUESTION_CONTENT_INPUT, question_content)  # 输入题目内容
        self.input_rich_text(self.REFERENCE_ANSWER_INPUT, reference_answer)  # 输入参考答案
        self.input_rich_text(self.QUESTION_ANALYSIS_INPUT, question_analysis)  # 输入题目解析
        self.click(self.SELECT_KNOWLEDGE_BUTTON)  # 点击选择知识点
        self.hover(self.get_knowledge_locator_by_name(knowledge_name))  # 悬浮到指定知识点
        self.click(self.get_select_knowledge_locator_by_name(knowledge_name))  # 选择该知识点
        self.click(self.CONFIRM_KNOWLEDGE_BUTTON)  # 确定关联知识点
        self.click(self.OPEN_TO_STUDENTS_SWITCH)  # 开放给学生
        self.click(self.CREATE_QUESTION_BUTTON)  # 点击创建习题
        result = self.is_displayed(self.CREATE_QUESTION_SUCCESS_MESSAGE)  # 检查是否出现题目创建成功提示
        log.info(f"创建习题结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def import_question_bank(self, file_path):
        """导入题库：点击导入题库、上传文件、确认导入，返回是否出现成功导入提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.IMPORT_QUESTION_BANK_BUTTON)  # 点击导入题库
        self.upload_file(file_path)  # 上传题库文件（基类方法，需在 iframe 内、弹窗已打开时调用）
        self.click(self.CONFIRM_IMPORT_BUTTON)  # 点击确认导入
        result = self.is_displayed(self.IMPORT_QUESTION_BANK_SUCCESS_MESSAGE)  # 检查是否出现成功导入提示
        log.info(f"导入题库结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result
