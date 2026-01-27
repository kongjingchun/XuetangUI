# encoding: utf-8
# @File  : course_manage_page.py
# @Author:
# @Date  :
# @Desc  : 课程管理页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class CourseManagePage(BasePage):
    """课程管理页面类。

    对外只暴露“服务方法”（如创建课程、按课程代码删除课程等），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 课程管理主内容区域 iframe
    COURSE_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2001']")
    # 搜索关键词输入框
    SEARCH_KEYWORD_INPUT = (By.XPATH, "//input[@placeholder='课程代码 ｜ 课程名称']")
    # 新建课程按钮
    NEW_COURSE_BUTTON = (By.XPATH, "//button[contains(.,'新建课程')]")
    # 新建成功 toast 文案
    CREATE_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='新建成功']")
    # 删除成功 toast 文案
    DELETE_SUCCESS_MESSAGE = (By.XPATH, "//p[contains(.,'删除成功')]")

    # ======================新建课程弹窗======================
    # 是否一流课程开关
    NEW_COURSE_FIRST_CLASS_SWITCH = (By.XPATH, "//div[./label[text()='是否一流课程']]/div/div")
    # 新建确定按钮
    NEW_COURSE_CONFIRM_BUTTON = (By.XPATH, "//button[contains(.,'确定')]")
    # 删除课程按钮
    DELETE_BUTTON = (By.XPATH, "//button[contains(.,'删除课程')]")
    # 删除确认（警告弹窗中的确定）
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//div[contains(.,'警告')]//button[contains(.,'确定')]")
    # 所属学院下拉框
    NEW_COURSE_DEPT_DROPDOWN = (By.XPATH, "//div[@aria-label='新建课程']//span[text()='请选择学院']/parent::div")
    # 课程负责人下拉框
    NEW_COURSE_RESPONSIBLE_PERSON_DROPDOWN = (By.XPATH, "//div[@aria-label='新建课程']//span[text()='请选择课程负责人']/parent::div")
    # 课程负责人下拉框关闭
    NEW_COURSE_RESPONSIBLE_PERSON_DROPDOWN_CLOSE = (By.XPATH, "//div[@aria-label='新建课程']//label[text()='课程负责人']/following-sibling::div//div[@class='el-select__suffix']")

    # ==================== 动态定位器 getter ====================

    def get_new_course_input_locator(self, input_name):
        """输入框名称（如 '名称'、'代码'、'描述'）→ 新建课程对应输入框定位器。"""
        if '代码' in input_name:
            return (By.XPATH, "//div[@aria-label='新建课程'] //input[contains(@placeholder,'课程代码')]")
        elif '名称' in input_name:
            return (By.XPATH, "//div[@aria-label='新建课程'] //input[contains(@placeholder,'课程名称')]")
        elif '描述' in input_name:
            return (By.XPATH, "//textarea[contains(@placeholder,'课程描述')]")
        return None

    def get_new_course_dept_option_locator(self, dept_name):
        """学院名称 → 所属学院下拉选项定位器。"""
        return (By.XPATH, f"//div[@aria-hidden='false']//span[contains(.,'{dept_name}')]/parent::li")

    def get_new_course_responsible_person_option_locator(self, prof_name):
        """课程负责人名称 → 课程负责人下拉选项定位器。"""
        return (By.XPATH, f"//span[text()='{prof_name}']/parent::div")

    def get_edit_hover_locator(self, course_code):
        """课程代码 → 编辑悬停区域（操作图标）定位器。"""
        return (By.XPATH, f"//tr[contains(.,'{course_code}')]//i[contains(@class,'action-icon')]")

    def get_edit_button_locator(self, course_code):
        """课程代码 → 编辑按钮定位器。"""
        return (By.XPATH, f"//tr[contains(.,'{course_code}')]//button")

    # ==================== 服务方法（页面对外能力） ====================

    def create_course(self, course_info):
        """在课程管理页创建课程，返回是否出现新建成功提示。"""
        self.switch_to_iframe(self.COURSE_MANAGE_IFRAME)  # 切入课程管理 iframe

        self.click(self.NEW_COURSE_BUTTON)  # 打开新建课程弹窗

        locator_name = self.get_new_course_input_locator("名称")  # 获取课程名称输入框定位器
        if locator_name:
            self.input_text(locator_name, course_info['课程名称'])  # 输入课程名称
        locator_code = self.get_new_course_input_locator("代码")  # 获取课程代码输入框定位器
        if locator_code:
            self.input_text(locator_code, course_info['课程代码'])  # 输入课程代码
        if course_info.get('课程描述'):
            locator_desc = self.get_new_course_input_locator("描述")  # 获取课程描述输入框定位器
            if locator_desc:
                self.input_text(locator_desc, course_info['课程描述'])  # 输入课程描述

        self.click(self.NEW_COURSE_DEPT_DROPDOWN)  # 点击所属学院下拉框
        self.click(self.get_new_course_dept_option_locator(course_info['所属学院']))  # 选择学院

        if course_info.get('是否一流课程', False):
            self.click(self.NEW_COURSE_FIRST_CLASS_SWITCH)  # 开启是否一流课程

        self.click(self.NEW_COURSE_RESPONSIBLE_PERSON_DROPDOWN)  # 点击课程负责人下拉框
        self.click(self.get_new_course_responsible_person_option_locator(course_info['课程负责人']))  # 选择负责人
        self.click(self.NEW_COURSE_RESPONSIBLE_PERSON_DROPDOWN_CLOSE)  # 关闭负责人下拉

        self.click(self.NEW_COURSE_CONFIRM_BUTTON)  # 点击确定

        result = self.is_displayed(self.CREATE_SUCCESS_MESSAGE)  # 检查是否出现新建成功提示
        log.info(f"创建课程结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def delete_course_by_course_code(self, course_code):
        """按课程代码搜索并删除对应课程，返回是否出现删除成功提示。"""
        self.switch_to_iframe(self.COURSE_MANAGE_IFRAME)  # 切入课程管理 iframe

        self.input_text(self.SEARCH_KEYWORD_INPUT, course_code)  # 输入课程代码搜索
        self.hover(self.get_edit_hover_locator(course_code))  # 悬停到该行操作区
        self.click(self.get_edit_button_locator(course_code), timeout=15)  # 点击编辑按钮
        self.click(self.DELETE_BUTTON, timeout=15)  # 点击删除课程
        self.click(self.DELETE_CONFIRM_BUTTON, timeout=15)  # 点击删除确认

        result = self.is_displayed(self.DELETE_SUCCESS_MESSAGE)  # 检查是否出现删除成功提示
        log.info(f"删除课程结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result
