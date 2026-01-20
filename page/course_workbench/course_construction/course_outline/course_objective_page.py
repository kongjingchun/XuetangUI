# encoding: utf-8
# @File  : CourseObjectivePage.py
# @Author: 孔敬淳
# @Date  : 2026/01/17
# @Desc  : 课程目标页面对象类，封装课程目标相关的页面操作方法

from selenium.webdriver.common.by import By

from logs.log import log
from page.course_workbench.course_workbench_page import CourseWorkbenchPage


class CourseObjectivePage(CourseWorkbenchPage):
    """课程目标页面类
    继承BasePage类，提供课程目标页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ==================== 课程目标定位器=============================================================
    # 课程目标iframe
    COURSE_OBJECTIVE_IFRAME = (By.XPATH, "//iframe[@id='course-workspace-iframe']")

    # ==================== 课程目标概览定位器=============================================================
    # 编辑描述按钮
    EDIT_DESCRIPTION_BUTTON = (By.XPATH, "//span[text()='编辑描述']/parent::button")
    # 课程目标描述输入框
    COURSE_OBJECTIVE_DESCRIPTION_INPUT = (By.XPATH, "//textarea[@placeholder='请输入课程目标的整体描述...']")
    # 课程描述保存按钮
    COURSE_DESCRIPTION_SAVE_BUTTON = (By.XPATH, "//span[contains(.,'保存')]/parent::button")
    # 保存成功提示框
    SAVE_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='保存成功']")

    # ==================== 课程目标概览操作方法=============================================================
    def click_edit_description_button(self):
        """点击编辑描述按钮"""
        log.info(f"点击编辑描述按钮，定位器为：{self.EDIT_DESCRIPTION_BUTTON[1]}")
        return self.click(self.EDIT_DESCRIPTION_BUTTON)

    def input_course_objective_description(self, description):
        """输入课程目标描述"""
        log.info(f"输入课程目标描述：{description}，定位器为：{self.COURSE_OBJECTIVE_DESCRIPTION_INPUT[1]}")
        return self.input_text(self.COURSE_OBJECTIVE_DESCRIPTION_INPUT, description)

    def click_course_description_save_button(self):
        """点击课程描述保存按钮"""
        log.info(f"点击课程描述保存按钮，定位器为：{self.COURSE_DESCRIPTION_SAVE_BUTTON[1]}")
        return self.click(self.COURSE_DESCRIPTION_SAVE_BUTTON)

    def assert_save_success(self):
        """断言保存成功"""
        log.info(f"断言保存成功，定位器为：{self.SAVE_SUCCESS_MESSAGE[1]}")
        return self.is_displayed(self.SAVE_SUCCESS_MESSAGE)

    def edit_course_objective_description(self, description):
        """编辑课程目标描述"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程目标iframe
        self.switch_to_iframe(self.COURSE_OBJECTIVE_IFRAME)
        # 点击编辑描述按钮
        self.click_edit_description_button()
        # 输入课程目标描述
        self.input_course_objective_description(description)
        # 点击课程描述保存按钮
        self.click_course_description_save_button()
        # 断言保存成功
        result = self.assert_save_success()
        log.info(f"编辑课程目标描述结果：{result}")
        # 切出课程目标iframe
        self.switch_out_iframe()
        return result

    # ==================== 课程目标管理定位器=============================================================
    # 添加目标按钮
    ADD_OBJECTIVE_BUTTON = (By.XPATH, "//span[contains(.,'添加目标')]/parent::button")
    # 目标标题输入框
    OBJECTIVE_TITLE_INPUT = (By.XPATH, "//textarea[@placeholder='请输入目标标题']")
    # 添加标签按钮
    ADD_TAG_BUTTON = (By.XPATH, "//span[contains(.,'添加标签')]/parent::button")
    # 标签输入框
    TAG_INPUT = (By.XPATH, "//input[@placeholder='输入标签后按回车键添加']")
    # 创建目标按钮
    CREATE_OBJECTIVE_BUTTON = (By.XPATH, "//div[@aria-label='添加课程目标']//span[contains(.,'创建')]/parent::button")
    # 创建课程目标成功提示框
    CREATE_OBJECTIVE_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='创建课程目标成功']")
    # 关联毕业要求按钮
    ASSOCIATE_GRADUATION_REQUIREMENTS_BUTTON = (By.XPATH, "//span[text()=' 关联毕业要求 ']/parent::button")
    # 添加毕业要求按钮
    ADD_GRADUATION_REQUIREMENTS_BUTTON = (By.XPATH, "//span[text()=' 添加毕业要求 ']/parent::button")
    # 关联毕业要求确认按钮
    ASSOCIATE_GRADUATION_REQUIREMENTS_CONFIRM_BUTTON = (By.XPATH, "//span[text()=' 确定 ']/parent::button")
    # 关联毕业要求成功提示框
    ASSOCIATE_GRADUATION_REQUIREMENTS_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='添加毕业要求关联成功']")

    # ==================== 课程目标管理动态定位器方法（需要参数的定位器）=============================================================
    def get_graduation_requirement_checkbox_locator(self, requirement_name):
        """
        根据名称，返回对应毕业要求的复选框定位器

        Args:
            requirement_name: 毕业要求名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//span[text() = '{requirement_name}']/ancestor::div[@class = 'requirement-info']")

    # ==================== 课程目标管理操作方法=============================================================

    def click_add_objective_button(self):
        """点击添加目标按钮"""
        log.info(f"点击添加目标按钮，定位器为：{self.ADD_OBJECTIVE_BUTTON[1]}")
        return self.click(self.ADD_OBJECTIVE_BUTTON)

    def input_objective_title(self, title):
        """输入目标标题"""
        log.info(f"输入目标标题：{title}，定位器为：{self.OBJECTIVE_TITLE_INPUT[1]}")
        return self.input_text(self.OBJECTIVE_TITLE_INPUT, title)

    def click_add_tag_button(self):
        """点击添加标签按钮"""
        log.info(f"点击添加标签按钮，定位器为：{self.ADD_TAG_BUTTON[1]}")
        return self.click(self.ADD_TAG_BUTTON)

    def input_tag(self, tag):
        """输入标签"""
        log.info(f"输入标签：{tag}，定位器为：{self.TAG_INPUT[1]}")
        return self.input_text(self.TAG_INPUT, tag, need_enter=True)

    def click_create_objective_button(self):
        """点击创建目标按钮"""
        log.info(f"创建目标按钮，定位器为：{self.CREATE_OBJECTIVE_BUTTON[1]}")
        return self.click(self.CREATE_OBJECTIVE_BUTTON)

    def assert_create_objective_success(self):
        """断言创建目标成功"""
        log.info(f"断言创建目标成功，定位器为：{self.CREATE_OBJECTIVE_SUCCESS_MESSAGE[1]}")
        return self.is_displayed(self.CREATE_OBJECTIVE_SUCCESS_MESSAGE)

    # 添加目标
    def add_objective(self, title, tag):
        """添加目标"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程目标iframe
        self.switch_to_iframe(self.COURSE_OBJECTIVE_IFRAME)
        # 点击添加目标按钮
        self.click_add_objective_button()
        # 输入目标标题
        self.input_objective_title(title)
        # 点击添加标签按钮
        self.click_add_tag_button()
        # 输入标签
        self.input_tag(tag)
        # 点击创建目标按钮
        self.click_create_objective_button()
        # 断言创建目标成功
        result = self.assert_create_objective_success()
        log.info(f"添加目标结果：{result}")
        # 切出课程目标iframe
        self.switch_out_iframe()
        return result

    def click_associate_graduation_requirements_button(self):
        """点击关联毕业要求按钮"""
        log.info(f"点击关联毕业要求按钮，定位器为：{self.ASSOCIATE_GRADUATION_REQUIREMENTS_BUTTON[1]}")
        return self.click(self.ASSOCIATE_GRADUATION_REQUIREMENTS_BUTTON)

    def click_add_graduation_requirements_button(self):
        """点击添加毕业要求按钮"""
        log.info(f"点击添加毕业要求按钮，定位器为：{self.ADD_GRADUATION_REQUIREMENTS_BUTTON[1]}")
        return self.click(self.ADD_GRADUATION_REQUIREMENTS_BUTTON)

    def click_graduation_requirement_checkbox(self, requirement_name):
        """点击毕业要求复选框

        Args:
            requirement_name: 毕业要求名称

        Returns:
            点击操作结果
        """
        locator = self.get_graduation_requirement_checkbox_locator(requirement_name)
        log.info(f"点击毕业要求复选框，毕业要求名称：{requirement_name}，定位器为：{locator[1]}")
        return self.click(locator)

    def click_associate_graduation_requirements_confirm_button(self):
        """点击关联毕业要求确认按钮"""
        log.info(f"点击关联毕业要求确认按钮，定位器为：{self.ASSOCIATE_GRADUATION_REQUIREMENTS_CONFIRM_BUTTON[1]}")
        return self.click(self.ASSOCIATE_GRADUATION_REQUIREMENTS_CONFIRM_BUTTON)

    def assert_associate_graduation_requirements_success(self):
        """断言关联毕业要求成功"""
        log.info(f"断言关联毕业要求成功，定位器为：{self.ASSOCIATE_GRADUATION_REQUIREMENTS_SUCCESS_MESSAGE[1]}")
        return self.is_displayed(self.ASSOCIATE_GRADUATION_REQUIREMENTS_SUCCESS_MESSAGE)

    # 关联毕业要求
    def associate_graduation_requirements(self, requirement_name):
        """关联毕业要求"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程目标iframe
        self.switch_to_iframe(self.COURSE_OBJECTIVE_IFRAME)
        # 点击关联毕业要求按钮
        self.click_associate_graduation_requirements_button()
        # 点击添加毕业要求按钮
        self.click_add_graduation_requirements_button()
        # 点击毕业要求复选框
        self.click_graduation_requirement_checkbox(requirement_name)
        # 点击关联毕业要求确认按钮
        self.click_associate_graduation_requirements_confirm_button()
        # 断言关联毕业要求成功
        result = self.assert_associate_graduation_requirements_success()
        log.info(f"关联毕业要求结果：{result}")
        # 切出课程目标iframe
        self.switch_out_iframe()
        return result
