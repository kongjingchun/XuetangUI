# encoding: utf-8
# @File  : CourseManagePage.py
# @Author: 孔敬淳
# @Date  : 2025/12/31
# @Desc  : 课程管理页面对象类，封装课程管理相关的页面操作方法

from time import sleep
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class CourseManagePage(BasePage):
    """课程管理页面类

    继承BasePage类，提供课程管理页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化课程管理页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
    # 课程管理iframe
    COURSE_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2001']")
    # 搜索关键词输入框
    SEARCH_KEYWORD_INPUT = (By.XPATH, "//input[@placeholder='课程代码 ｜ 课程名称']")
    # 新建课程按钮
    NEW_COURSE_BUTTON = (By.XPATH, "//button[contains(.,'新建课程')]")
    # 是否一流课程开关
    NEW_COURSE_FIRST_CLASS_SWITCH = (By.XPATH, "//div[./label[text()='是否一流课程']]/div/div")
    # 新建确定按钮
    NEW_COURSE_CONFIRM_BUTTON = (By.XPATH, "//button[contains(.,'确定')]")
    # 创建成功提示框
    CREATE_SUCCESS_ALERT = (By.XPATH, "//p[text()='新建成功']")
    # 删除课程按钮
    DELETE_BUTTON = (By.XPATH, "//button[contains(.,'删除课程')]")
    # 删除确认按钮
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//div[contains(.,'警告')]//button[contains(.,'确定')]")
    # 删除成功提示框
    DELETE_SUCCESS_ALERT = (By.XPATH, "//p[contains(.,'删除成功')]")
    # 所属学院下拉框
    NEW_COURSE_DEPT_DROPDOWN = (By.XPATH, "//div[@aria-label='新建课程']//span[text()='请选择学院']/parent::div")
    # 课程负责人下拉框
    NEW_COURSE_RESPONSIBLE_PERSON_DROPDOWN = (By.XPATH, "//div[@aria-label='新建课程']//span[text()='请选择课程负责人']/parent::div")
    # 课程负责人下拉框关闭
    NEW_COURSE_RESPONSIBLE_PERSON_DROPDOWN_CLOSE = (By.XPATH, "//div[@aria-label='新建课程']//label[text()='课程负责人']/following-sibling::div//div[@class='el-select__suffix']")

    # ==================== 动态定位器方法（需要参数的定位器）====================

    def get_new_course_input_locator(self, input_name):
        """获取新建课程输入框的定位器

        Args:
            input_name: 输入框名称，如 '名称'、'代码'、'描述'

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        if '代码' in input_name:
            return (By.XPATH, "//div[@aria-label='新建课程'] //input[contains(@placeholder,'课程代码')]")
        elif '名称' in input_name:
            return (By.XPATH, "//div[@aria-label='新建课程'] //input[contains(@placeholder,'课程名称')]")
        elif '描述' in input_name:
            return (By.XPATH, "//textarea[contains(@placeholder,'课程描述')]")
        else:
            return None

    def get_new_course_dept_dropdown_option_locator(self, dept_name):
        """获取所属学院下拉框选项的定位器

        Args:
            dept_name: 学院名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@aria-hidden='false']//span[contains(.,'" + dept_name + "')]/parent::li")

    def get_new_course_responsible_person_dropdown_option_locator(self, prof_name):
        """获取课程负责人下拉框选项的定位器

        Args:
            prof_name: 课程负责人名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//span[text()='" + prof_name + "']/parent::div")

    def get_edit_button_hover_location_locator(self, course_code):
        """获取编辑悬停位置的定位器

        Args:
            course_code: 课程代码

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//tr[contains(.,'" + course_code + "')]//i[contains(@class,'action-icon')]")

    def get_edit_button_by_course_code_locator(self, course_code):
        """获取根据课程代码定位编辑按钮的定位器

        Args:
            course_code: 课程代码

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//tr[contains(.,'" + course_code + "')]//button")

    # ==================== 页面操作方法 ====================

    def click_new_course_button(self):
        """点击新建课程按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击新建课程按钮，定位器为：{self.NEW_COURSE_BUTTON[1]}")
        return self.click(self.NEW_COURSE_BUTTON)

    def input_new_course_input(self, input_name, value):
        """输入新建课程信息

        Args:
            input_name: 输入框名称（如：'名称'、'代码'、'描述'）
            value: 输入的值

        Returns:
            输入操作结果
        """
        locator = self.get_new_course_input_locator(input_name)
        if locator is None:
            log.error(f"未找到输入框：{input_name}")
            return False
        log.info(f"输入新建课程信息：{input_name}为：{value}，定位器为：{locator[1]}")
        return self.input_text(locator, value)

    def click_new_course_dept_dropdown(self):
        """点击所属学院下拉框

        Returns:
            点击操作结果
        """
        log.info(f"点击所属学院下拉框，定位器为：{self.NEW_COURSE_DEPT_DROPDOWN[1]}")
        return self.click(self.NEW_COURSE_DEPT_DROPDOWN)

    def click_new_course_dept_dropdown_option(self, dept_name):
        """点击所属学院下拉框选项

        Args:
            dept_name: 学院名称

        Returns:
            点击操作结果
        """
        locator = self.get_new_course_dept_dropdown_option_locator(dept_name)
        log.info(f"点击所属学院下拉框选项：{dept_name}，定位器为：{locator[1]}")
        result = self.click(locator, timeout=15)
        # 点击后等待下拉菜单关闭
        sleep(0.5)
        return result

    def click_new_course_responsible_person_dropdown(self):
        """点击课程负责人下拉框

        Returns:
            点击操作结果
        """
        log.info(f"点击课程负责人下拉框，定位器为：{self.NEW_COURSE_RESPONSIBLE_PERSON_DROPDOWN[1]}")
        return self.click(self.NEW_COURSE_RESPONSIBLE_PERSON_DROPDOWN)

    def click_new_course_responsible_person_dropdown_option(self, prof_name):
        """点击课程负责人下拉框选项

        Args:
            prof_name: 课程负责人名称

        Returns:
            点击操作结果
        """
        locator = self.get_new_course_responsible_person_dropdown_option_locator(prof_name)
        log.info(f"点击课程负责人下拉框选项：{prof_name}，定位器为：{locator[1]}")
        result = self.click(locator, timeout=15)
        # 点击后等待下拉菜单关闭
        sleep(0.5)
        return result

    def click_new_course_responsible_person_dropdown_close(self):
        """点击课程负责人下拉框关闭

        Returns:
            点击操作结果
        """
        log.info(f"点击课程负责人下拉框关闭，定位器为：{self.NEW_COURSE_RESPONSIBLE_PERSON_DROPDOWN_CLOSE[1]}")
        result = self.click(self.NEW_COURSE_RESPONSIBLE_PERSON_DROPDOWN_CLOSE)
        # 点击后等待下拉菜单关闭
        sleep(0.5)
        return result

    def click_new_course_first_class_switch(self):
        """点击是否一流课程开关

        Returns:
            点击操作结果
        """
        log.info(f"点击是否一流课程开关，定位器为：{self.NEW_COURSE_FIRST_CLASS_SWITCH[1]}")
        return self.click(self.NEW_COURSE_FIRST_CLASS_SWITCH)

    def click_new_course_confirm_button(self):
        """点击新建课程确认按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击新建课程确认按钮，定位器为：{self.NEW_COURSE_CONFIRM_BUTTON[1]}")
        return self.click(self.NEW_COURSE_CONFIRM_BUTTON)

    def is_create_success_alert_display(self):
        """查看创建成功提示框是否出现

        Returns:
            bool: True表示创建成功提示框出现，False表示未出现
        """
        log.info(f"查看创建成功提示框是否出现，定位器为：{self.CREATE_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.CREATE_SUCCESS_ALERT)

    def input_search_keyword(self, keyword):
        """输入搜索关键词

        Args:
            keyword: 搜索关键词（课程代码或课程名称）

        Returns:
            输入操作结果
        """
        log.info(f"输入搜索关键词：{keyword}，定位器为：{self.SEARCH_KEYWORD_INPUT[1]}")
        return self.input_text(self.SEARCH_KEYWORD_INPUT, keyword)

    def hover_edit_button(self, course_code):
        """鼠标悬停编辑按钮

        Args:
            course_code: 课程代码

        Returns:
            悬停操作结果
        """
        locator = self.get_edit_button_hover_location_locator(course_code)
        log.info(f"鼠标悬停编辑按钮，定位器为：{locator[1]}")
        return self.hover(locator)

    def click_edit_button_by_course_code(self, course_code):
        """根据课程代码点击编辑按钮

        Args:
            course_code: 课程代码

        Returns:
            点击操作结果
        """
        locator = self.get_edit_button_by_course_code_locator(course_code)
        log.info(f"根据课程代码'{course_code}'点击编辑按钮，定位器为：{locator[1]}")
        return self.click(locator, timeout=15)

    def click_delete_button(self):
        """点击删除课程按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击删除课程按钮，定位器为：{self.DELETE_BUTTON[1]}")
        return self.click(self.DELETE_BUTTON, timeout=15)

    def click_delete_confirm_button(self):
        """点击删除确认按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击删除确认按钮，定位器为：{self.DELETE_CONFIRM_BUTTON[1]}")
        return self.click(self.DELETE_CONFIRM_BUTTON, timeout=15)

    def is_delete_success_alert_display(self):
        """查看删除成功提示框是否出现

        Returns:
            bool: True表示删除成功提示框出现，False表示未出现
        """
        log.info(f"查看删除成功提示框是否出现，定位器为：{self.DELETE_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.DELETE_SUCCESS_ALERT)

    def create_course(self, course_info):
        """创建课程

        Args:
            course_info: 课程信息

        Returns:
            bool: True表示创建成功，False表示创建失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.COURSE_MANAGE_IFRAME)

        # 点击新建课程按钮
        self.click_new_course_button()

        # 从1到7从上到下设置新建信息
        # 1. 课程名称
        self.input_new_course_input("名称", course_info['课程名称'])

        # 2. 课程代码
        self.input_new_course_input("代码", course_info['课程代码'])

        # 3. 课程描述（如果存在则输入）
        if course_info.get('课程描述'):
            self.input_new_course_input("描述", course_info['课程描述'])

        # 4. 所属学院
        self.click_new_course_dept_dropdown()
        self.click_new_course_dept_dropdown_option(course_info['所属学院'])

        # 5. 是否一流课程（如果为true，则打开开关）
        if course_info.get('是否一流课程', False):
            self.click_new_course_first_class_switch()

        # 6. 课程负责人
        self.click_new_course_responsible_person_dropdown()
        self.click_new_course_responsible_person_dropdown_option(course_info['课程负责人'])
        self.click_new_course_responsible_person_dropdown_close()

        # 7. 课程图片不上传，跳过

        # 点击确定按钮
        self.click_new_course_confirm_button()
        sleep(1)

        # 断言创建成功提示框是否出现
        result = self.is_create_success_alert_display()

        # 切出iframe
        self.switch_out_iframe()

        log.info(f"创建课程结果：{result}")
        return result

    def delete_course_by_course_code(self, course_code):
        """根据课程代码删除课程

        Args:
            course_code: 课程代码

        Returns:
            bool: True表示删除成功，False表示删除失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.COURSE_MANAGE_IFRAME)
        # 输入搜索关键词
        self.input_search_keyword(course_code)
        sleep(1)
        # 鼠标悬停编辑按钮
        self.hover_edit_button(course_code)
        # 点击编辑按钮
        self.click_edit_button_by_course_code(course_code)
        # 点击删除按钮
        self.click_delete_button()
        # 点击删除确认按钮
        self.click_delete_confirm_button()
        # 断言删除成功提示框是否出现
        result = self.is_delete_success_alert_display()
        # 切出iframe
        self.switch_out_iframe()
        log.info(f"删除课程结果：{result}")
        return result
