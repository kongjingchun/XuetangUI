# encoding: utf-8
# @File  : teaching_class_management_page.py
# @Author: 孔敬淳
# @Date  : 2025/01/21
# @Desc  : 教学班管理页面对象类，封装教学班管理相关的页面操作方法
from selenium.webdriver.common.by import By
from logs.log import log
from page.teacher_workbench.course_workbench.course_workbench_page import CourseWorkbenchPage


class TeachingClassManagementPage(CourseWorkbenchPage):
    """教学班管理页面类

    继承CourseWorkbenchPage基类，提供教学班管理页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化教学班管理页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
    # 创建教学班按钮
    CREATE_TEACHING_CLASS_BUTTON = (By.XPATH, "//button[contains(.,'创建教学班')]")
    # 教学班名称输入框
    TEACHING_CLASS_NAME_INPUT = (By.XPATH, "//div[@aria-label='创建教学班']//input[@placeholder = '请输入教学班名称']")
    # 教学班编号输入框
    TEACHING_CLASS_CODE_INPUT = (By.XPATH, "//div[@aria-label='创建教学班']//input[@placeholder = '请输入教学班编号']")
    # 开课时间输入框
    OPEN_COURSE_TIME_INPUT = (By.XPATH, "//div[@aria-label='创建教学班']//input[@placeholder = '开课时间']")
    # 结课时间输入框
    END_COURSE_TIME_INPUT = (By.XPATH, "//div[@aria-label='创建教学班']//input[@placeholder = '结课时间']")
    # 无结课时间按钮
    NO_END_COURSE_TIME_BUTTON = (By.XPATH, "//span[text()=' 无结课时间 ']/preceding-sibling::span")
    # 选课开始时间输入框
    SELECT_COURSE_START_TIME_INPUT = (By.XPATH, "//div[@aria-label='创建教学班']//input[@placeholder = '选课开始时间']")
    # 选课结束时间输入框
    SELECT_COURSE_END_TIME_INPUT = (By.XPATH, "//div[@aria-label='创建教学班']//input[@placeholder = '选课结束时间']")
    # 日期确定按钮
    DATE_CONFIRM_BUTTON = (By.XPATH, "//div[contains(@class,'el-picker__popper') and @aria-hidden='false']//button[contains(.,'确定')]")
    # 创建确定按钮
    CREATE_CONFIRM_BUTTON = (By.XPATH, "//div[@aria-label='创建教学班']//button[contains(.,'确定')]")
    # 设置（修改）主讲老师按钮
    SET_LECTURER_BUTTON = (By.XPATH, "//div[./div/span[contains(.,'主讲教师')] and @class='edit-teacher-card']")
    # 确认设置按钮
    CONFIRM_SET_LECTURER_BUTTON = (By.XPATH, "//div[@aria-label='确认设置']//button[contains(.,'确认')]")
    # 设置成功提示框
    SET_LECTURER_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='设置成功']")
    # ==================== 动态定位器方法（需要参数的定位器）====================

    def get_allow_student_select_switch_locator(self, boolean=True):
        """获取是否允许学生自选开关的定位器

        Args:
            boolean: 是否允许学生自选

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        if boolean:
            return (By.XPATH, "//div[./label[text()='是否允许学生自选']]//label[./span[text()='是']]")
        else:
            return (By.XPATH, "//div[./label[text()='是否允许学生自选']]//label[./span[text()='否']]")

    def get_allow_student_drop_switch_locator(self, boolean=True):
        """获取是否允许学生退课开关的定位器

        Args:
            boolean: 是否允许学生退课

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        if boolean:
            return (By.XPATH, "//div[./label[text()='是否允许学生退课']]//label[./span[text()='是']]")
        else:
            return (By.XPATH, "//div[./label[text()='是否允许学生退课']]//label[./span[text()='否']]")

    def get_teaching_class_locator(self, value):
        """
        根据教学班名称或教学班编号判断是否创建成功的定位器

        Args:
            value (str): 教学班名称或教学班编号

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        # 假设教学班列表页面中，教学班名称或编号直接展示在对应的单元格中
        return (By.XPATH, f"//td/div[contains(.,'{value}')]")

    def get_member_management_button_locator(self, value):
        """
        根据教学班名称或教学班编号返回成员管理的定位器

        Args:
            value (str): 教学班名称或教学班编号

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//tr[contains(.,'{value}')]//button[contains(.,'成员管理')]")

    def get_replace_to_main_teacher_button_locator(self, value):
        """
        根据教师姓名或者工号返回替换为主讲教师按钮的定位器

        Args:
            value (str): 教师姓名或工号

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        # 假设页面上有一行包含该教师的姓名或工号，并有“替换为主讲教师”按钮
        return (By.XPATH, f"//tr[contains(.,'{value}')]//span[text()=' 替换为主讲教师 ']")

    # ==================== 页面操作方法 ====================
    def click_create_teaching_class_button(self):
        """点击创建教学班按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击创建教学班按钮，定位器为：{self.CREATE_TEACHING_CLASS_BUTTON[1]}")
        return self.click(self.CREATE_TEACHING_CLASS_BUTTON)

    def input_teaching_class_name(self, value):
        """输入教学班名称

        Args:
            value (str): 教学班名称

        Returns:
            输入操作结果
        """
        log.info(f"输入教学班名称：{value}，定位器为：{self.TEACHING_CLASS_NAME_INPUT[1]}")
        return self.input_text(self.TEACHING_CLASS_NAME_INPUT, value)

    def input_teaching_class_code(self, value):
        """输入教学班编号

        Args:
            value (str): 教学班编号

        Returns:
            输入操作结果
        """
        log.info(f"输入教学班编号：{value}，定位器为：{self.TEACHING_CLASS_CODE_INPUT[1]}")
        return self.input_text(self.TEACHING_CLASS_CODE_INPUT, value)

    def input_open_course_time(self, value):
        """输入开课时间

        Args:
            value (str): 开课时间

        Returns:
            输入操作结果
        """
        log.info(f"输入开课时间：{value}，定位器为：{self.OPEN_COURSE_TIME_INPUT[1]}")
        return self.input_text(self.OPEN_COURSE_TIME_INPUT, value)

    def input_end_course_time(self, value):
        """输入结课时间

        Args:
            value (str): 结课时间

        Returns:
            输入操作结果
        """
        log.info(f"输入结课时间：{value}，定位器为：{self.END_COURSE_TIME_INPUT[1]}")
        return self.input_text(self.END_COURSE_TIME_INPUT, value)

    def click_no_end_course_time_button(self):
        """点击无结课时间按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击无结课时间按钮，定位器为：{self.NO_END_COURSE_TIME_BUTTON[1]}")
        return self.click(self.NO_END_COURSE_TIME_BUTTON)

    def click_allow_student_self_select_checkbox(self, allow_student_self_select=True):
        """点击是否允许学生自选开关

        Args:
            allow_student_self_select (bool): 是否允许学生自选

        Returns:
            点击操作结果
        """
        log.info(f"点击'是否允许学生自选'复选框，定位器为：{self.get_allow_student_select_switch_locator(allow_student_self_select)[1]}")
        return self.click(self.get_allow_student_select_switch_locator(boolean=allow_student_self_select))

    def input_select_course_start_time(self, value):
        """输入选课开始时间

        Args:
            value (str): 选课开始时间

        Returns:
            输入操作结果
        """
        log.info(f"输入选课开始时间：{value}，定位器为：{self.SELECT_COURSE_START_TIME_INPUT[1]}")
        return self.input_text(self.SELECT_COURSE_START_TIME_INPUT, value)

    def input_select_course_end_time(self, value):
        """输入选课结束时间

        Args:
            value (str): 选课结束时间

        Returns:
            输入操作结果
        """
        log.info(f"输入选课结束时间：{value}，定位器为：{self.SELECT_COURSE_END_TIME_INPUT[1]}")
        return self.input_text(self.SELECT_COURSE_END_TIME_INPUT, value)

    def click_allow_student_drop_checkbox(self, allow_student_drop=True):
        """点击是否允许学生退课复选框

        Returns:
            点击操作结果
        """
        log.info(f"点击'是否允许学生退课'复选框，定位器为：{self.get_allow_student_drop_switch_locator()[1]}")
        return self.click(self.get_allow_student_drop_switch_locator())

    def click_date_confirm_button(self):
        """点击日期确定按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击日期确定按钮，定位器为：{self.DATE_CONFIRM_BUTTON[1]}")
        return self.click(self.DATE_CONFIRM_BUTTON)

    def click_create_confirm_button(self):
        """点击创建教学班确定按钮

        Returns:
            点击操作结果，点击后等待创建成功提示框出现
        """
        log.info(f"点击创建教学班确定按钮，定位器为：{self.CREATE_CONFIRM_BUTTON[1]}")
        return self.click(self.CREATE_CONFIRM_BUTTON, timeout=15)

    def is_teaching_class_created_successfully(self, value):
        """判断教学班是否创建成功

        Args:
            value (str): 教学班名称或教学班编号

        Returns:
            bool: True表示创建成功，False表示创建失败
        """
        locator = self.get_teaching_class_locator(value)
        log.info(f"判断教学班是否创建成功，定位器为：{locator[1]}")
        return self.is_displayed(locator)

    def click_member_management_button(self, value):
        """
        根据值点击成员管理按钮

        Args:
            value (str): 教学班名称或教学班编号

        Returns:
            点击操作结果
        """
        locator = self.get_member_management_button_locator(value)
        log.info(f"点击成员管理按钮，定位器为：{locator[1]}")
        return self.click(locator)

    def click_set_lecturer_button(self):
        """点击设置（修改）主讲老师按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击设置（修改）主讲老师按钮，定位器为：{self.SET_LECTURER_BUTTON[1]}")
        return self.click(self.SET_LECTURER_BUTTON)

    def click_replace_to_main_teacher_button(self, value):
        """根据教师姓名或者工号点击替换为主讲教师按钮

        Args:
            value (str): 教师姓名或工号

        Returns:
            点击操作结果
        """
        locator = self.get_replace_to_main_teacher_button_locator(value)
        log.info(f"点击替换为主讲教师按钮，定位器为：{locator[1]}")
        return self.click(locator)

    def click_confirm_set_lecturer_button(self):
        """点击确认设置按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击确认设置按钮，定位器为：{self.CONFIRM_SET_LECTURER_BUTTON[1]}")
        return self.click(self.CONFIRM_SET_LECTURER_BUTTON)

    def is_set_lecturer_successfully(self):
        """判断设置主讲老师是否成功

        Returns:
            bool: True表示设置成功，False表示设置失败
        """
        return self.is_displayed(self.SET_LECTURER_SUCCESS_MESSAGE)

    def create_teaching_class(self, class_name, class_code, open_course_time, select_course_start_time, select_course_end_time, allow_student_self_select=True, allow_student_drop=True):
        """创建教学班

        Args:
            class_name (str): 教学班名称
            class_code (str): 教学班编号
            open_course_time (str): 开课时间
            select_course_start_time (str): 选课开始时间
            select_course_end_time (str): 选课结束时间
            allow_student_self_select (bool): 是否允许学生自选
            allow_student_drop (bool): 是否允许学生退课
        """

        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 点击创建教学班按钮
        self.click_create_teaching_class_button()
        # 输入教学班名称
        self.input_teaching_class_name(class_name)
        # 输入教学班编号
        self.input_teaching_class_code(class_code)
        # 输入开课时间
        self.input_open_course_time(open_course_time)
        # 点击日期确定按钮
        self.click_date_confirm_button()
        # 点击无结课时间按钮
        self.click_no_end_course_time_button()
        # 点击是否允许学生自选复选框
        self.click_allow_student_self_select_checkbox(allow_student_self_select)
        # 输入选课开始时间
        self.input_select_course_start_time(select_course_start_time)
        # 点击日期确定按钮
        self.click_date_confirm_button()
        # 输入选课结束时间
        self.input_select_course_end_time(select_course_end_time)
        # 点击日期确定按钮
        self.click_date_confirm_button()
        # 点击是否允许学生退课复选框
        self.click_allow_student_drop_checkbox(allow_student_drop)
        # 点击创建教学班确定按钮
        self.click_create_confirm_button()
        # 判断教学班是否创建成功
        result = self.is_teaching_class_created_successfully(class_code)
        # 切出iframe
        self.switch_out_iframe()
        return result

    # 设置主讲教师
    def set_lecturer(self, class_name_or_code, lecturer_name_or_code):
        """设置主讲教师

        Args:
            class_value (str): 教学班名称或教学班编号
            lecturer (str): 教师姓名或工号

        Returns:
            bool: True表示设置成功，False表示设置失败
        """
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 点击成员管理按钮
        self.click_member_management_button(class_name_or_code)
        # 点击设置（修改）主讲老师按钮
        self.click_set_lecturer_button()
        # 根据教师姓名或者工号点击替换为主讲教师按钮
        self.click_replace_to_main_teacher_button(lecturer_name_or_code)
        # 点击确认设置按钮
        self.click_confirm_set_lecturer_button()
        # 判断设置主讲老师是否成功
        result = self.is_set_lecturer_successfully()
        # 切出iframe
        self.switch_out_iframe()
        log.info(f"设置主讲教师结果：{result}")
        return result
