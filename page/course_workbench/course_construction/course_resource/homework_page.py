# encoding: utf-8
# @File  : homework_page.py
# @Author: 孔敬淳
# @Date  : 2025/01/21
# @Desc  : 作业页面对象类，封装作业相关的页面操作方法
from selenium.webdriver.common.by import By
from logs.log import log
from page.course_workbench.course_construction.course_resource.course_resource_page import CourseResourcePage


class HomeworkPage(CourseResourcePage):
    """作业页面类

    继承CourseResourcePage基类，提供作业页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化作业页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
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
    # ==================== 动态定位器方法（需要参数的定位器）====================

    # ==================== 页面操作方法 ====================
    def click_new_homework_button(self):
        """点击新建作业按钮"""
        log.info(f"点击新建作业按钮，定位器为：{self.NEW_HOMEWORK_BUTTON[1]}")
        return self.click(self.NEW_HOMEWORK_BUTTON)

    def input_homework_title(self, homework_title):
        """输入作业标题"""
        log.info(f"输入作业标题：{homework_title}，定位器为：{self.HOMEWORK_TITLE_INPUT[1]}")
        return self.input_text(self.HOMEWORK_TITLE_INPUT, homework_title)

    def click_create_and_edit_button(self):
        """点击创建并编辑按钮"""
        log.info(f"点击创建并编辑按钮，定位器为：{self.CREATE_AND_EDIT_BUTTON[1]}")
        return self.click(self.CREATE_AND_EDIT_BUTTON)

    def click_select_question_button(self):
        """点击选择题目按钮"""
        log.info(f"点击选择题目按钮，定位器为：{self.SELECT_QUESTION_BUTTON[1]}")
        return self.click(self.SELECT_QUESTION_BUTTON)

    def click_all_select_checkbox(self):
        """点击题目全选勾选框"""
        log.info(f"点击题目全选勾选框，定位器为：{self.ALL_SELECT_CHECKBOX[1]}")
        return self.click(self.ALL_SELECT_CHECKBOX)

    def click_confirm_select_button(self):
        """点击确定选择按钮"""
        log.info(f"点击确定选择按钮，定位器为：{self.CONFIRM_SELECT_BUTTON[1]}")
        return self.click(self.CONFIRM_SELECT_BUTTON)

    def is_added_success_message_displayed(self):
        """查看已添加提示框是否出现"""
        log.info(f"查看已添加提示框是否出现，定位器为：{self.ADDED_SUCCESS_MESSAGE[1]}")
        return self.is_displayed(self.ADDED_SUCCESS_MESSAGE)

    def click_save_button(self):
        """点击保存按钮"""
        log.info(f"点击保存按钮，定位器为：{self.SAVE_BUTTON[1]}")
        return self.click(self.SAVE_BUTTON)

    def is_save_success_message_displayed(self):
        """查看保存成功提示框是否出现"""
        log.info(f"查看保存成功提示框是否出现，定位器为：{self.SAVE_SUCCESS_MESSAGE[1]}")
        return self.is_displayed(self.SAVE_SUCCESS_MESSAGE)

    def new_homework(self, homework_title):
        """新建作业"""
        log.info(f"新建作业：{homework_title}")
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程资源iframe
        self.switch_to_iframe(self.COURSE_RESOURCE_IFRAME)
        # 点击新建作业按钮
        self.click_new_homework_button()
        # 输入作业标题
        self.input_homework_title(homework_title)
        # 点击创建并编辑按钮
        self.click_create_and_edit_button()
        # 点击选择题目按钮
        self.click_select_question_button()
        # 点击题目全选勾选框
        self.click_all_select_checkbox()
        # 点击确定选择按钮
        self.click_confirm_select_button()
        # 点击保存按钮
        self.click_save_button()
        # 断言保存成功提示框是否出现
        result = self.is_save_success_message_displayed()
        log.info(f"新建作业结果：{result}")
        # 切出课程资源iframe
        self.switch_out_iframe()
        # 切出课程工作台iframe
        self.switch_out_iframe()
        return result
