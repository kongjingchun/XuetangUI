# encoding: utf-8
# @File  : question_bank_page.py
# @Author: 孔敬淳
# @Date  : 2025/01/20
# @Desc  : 题库页面对象类，封装题库相关的页面操作方法
from selenium.webdriver.common.by import By

from logs.log import log
from page.course_workbench.course_construction.course_resource.course_resource_page import CourseResourcePage


class QuestionBankPage(CourseResourcePage):
    """题库页面类

    继承CourseResourcePage基类，提供题库页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化题库页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
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
    # ==================== 动态定位器方法（需要参数的定位器）====================
    # 根据题目类型返回新建的下啦选项

    def get_new_question_dropdown_option_locator(self, question_type):
        """获取新建题目下拉选项的定位器

        Args:
            question_type: 题目类型

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//li[text()='" + question_type + "']")

    def get_knowledge_locator_by_name(self, knowledge_name):
        """根据知识点名称返回知识点定位器

        Args:
            knowledge_name: 知识点名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//span[text()='" + knowledge_name + "']/parent::div")

    def get_select_knowledge_locator_by_name(self, knowledge_name):
        """根据知识点名称返回选择关联知识点定位器

        Args:
            knowledge_name: 知识点名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//span[text()='" + knowledge_name + "']/parent::div/following-sibling::div/button")

    # ==================== 页面操作方法 ====================
    def click_new_question_button(self):
        """点击新建题目按钮"""
        log.info(f"点击新建题目按钮，定位器为：{self.NEW_QUESTION_BUTTON[1]}")
        return self.click(self.NEW_QUESTION_BUTTON)

    def click_new_question_dropdown_option(self, question_type):
        """点击新建题目下拉选项"""
        log.info(f"点击新建题目下拉选项：{question_type}，定位器为：{self.get_new_question_dropdown_option_locator(question_type)[1]}")
        return self.click(self.get_new_question_dropdown_option_locator(question_type))

    def input_question_content(self, question_content):
        """输入题目内容（使用富文本输入方法）"""
        log.info(f"输入题目内容：{question_content}，定位器为：{self.QUESTION_CONTENT_INPUT[1]}")
        return self.input_rich_text(self.QUESTION_CONTENT_INPUT, question_content)

    def input_reference_answer(self, reference_answer):
        """输入参考答案（使用富文本输入方法）"""
        log.info(f"输入参考答案：{reference_answer}，定位器为：{self.REFERENCE_ANSWER_INPUT[1]}")
        return self.input_rich_text(self.REFERENCE_ANSWER_INPUT, reference_answer)

    def input_question_analysis(self, question_analysis):
        """输入题目解析（使用富文本输入方法）"""
        log.info(f"输入题目解析：{question_analysis}，定位器为：{self.QUESTION_ANALYSIS_INPUT[1]}")
        return self.input_rich_text(self.QUESTION_ANALYSIS_INPUT, question_analysis)

    def click_select_knowledge_button(self):
        """点击选择知识点按钮"""
        log.info(f"点击选择知识点按钮，定位器为：{self.SELECT_KNOWLEDGE_BUTTON[1]}")
        return self.click(self.SELECT_KNOWLEDGE_BUTTON)

    def hover_knowledge_by_name(self, knowledge_name):
        """悬浮到知识点"""
        log.info(f"悬浮到知识点：{knowledge_name}，定位器为：{self.get_knowledge_locator_by_name(knowledge_name)[1]}")
        return self.hover(self.get_knowledge_locator_by_name(knowledge_name))

    def click_knowledge_by_name(self, knowledge_name):
        """点击知识点"""
        log.info(f"点击知识点：{knowledge_name}，定位器为：{self.get_knowledge_locator_by_name(knowledge_name)[1]}")
        return self.click(self.get_knowledge_locator_by_name(knowledge_name))

    def select_knowledge_by_name(self, knowledge_name):
        """选择知识点"""
        log.info(f"选择知识点：{knowledge_name}，定位器为：{self.get_select_knowledge_locator_by_name(knowledge_name)[1]}")
        return self.click(self.get_select_knowledge_locator_by_name(knowledge_name))

    def click_confirm_knowledge_button(self):
        """点击关联知识点确定按钮"""
        log.info(f"点击关联知识点确定按钮，定位器为：{self.CONFIRM_KNOWLEDGE_BUTTON[1]}")
        return self.click(self.CONFIRM_KNOWLEDGE_BUTTON)

    def click_open_to_students_switch(self):
        """点击开放给学生开关"""
        log.info(f"点击开放给学生开关，定位器为：{self.OPEN_TO_STUDENTS_SWITCH[1]}")
        return self.click(self.OPEN_TO_STUDENTS_SWITCH)

    def click_create_question_button(self):
        """点击创建习题按钮"""
        log.info(f"点击创建习题按钮，定位器为：{self.CREATE_QUESTION_BUTTON[1]}")
        return self.click(self.CREATE_QUESTION_BUTTON)

    def is_create_question_success_message_displayed(self):
        """查看创建习题成功提示框是否出现"""
        log.info(f"查看创建习题成功提示框是否出现，定位器为：{self.CREATE_QUESTION_SUCCESS_MESSAGE[1]}")
        return self.is_displayed(self.CREATE_QUESTION_SUCCESS_MESSAGE)

    def new_question(self, question_type, question_content, reference_answer, question_analysis, knowledge_name):
        """新建题目"""
        log.info(f"新建题目：{question_type}，题目内容为：{question_content}，参考答案为：{reference_answer}，题目解析为：{question_analysis}")
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程资源iframe
        self.switch_to_iframe(self.COURSE_RESOURCE_IFRAME)
        # 点击新建题目按钮
        self.click_new_question_button()
        # 点击新建题目下拉选项
        self.click_new_question_dropdown_option(question_type)
        # 输入题目内容
        self.input_question_content(question_content)
        # 输入参考答案
        self.input_reference_answer(reference_answer)
        # 输入题目解析
        self.input_question_analysis(question_analysis)
        # 点击选择知识点按钮
        self.click_select_knowledge_button()
        # 悬浮到知识点
        self.hover_knowledge_by_name(knowledge_name)
        # 选择知识点
        self.select_knowledge_by_name(knowledge_name)
        # 点击关联知识点确定按钮
        self.click_confirm_knowledge_button()
        # 点击开放给学生开关
        self.click_open_to_students_switch()
        # 点击创建习题按钮
        self.click_create_question_button()
        # 断言创建习题成功提示框是否出现
        result = self.is_create_question_success_message_displayed()
        log.info(f"创建习题结果：{result}")
        # 切出课程资源iframe
        self.switch_out_iframe()
        # 切出课程工作台iframe
        self.switch_out_iframe()
        return result
