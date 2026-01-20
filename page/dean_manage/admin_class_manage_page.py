# encoding: utf-8
# @File  : AdminClassManagePage.py
# @Author: 孔敬淳
# @Date  : 2025/12/31
# @Desc  : 行政班管理页面对象类，封装行政班管理相关的页面操作方法
from time import sleep

from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class AdminClassManagePage(BasePage):
    """行政班管理页面类

    继承BasePage类，提供行政班管理页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化行政班管理页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
    # 行政班管理iframe
    ADMIN_CLASS_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2005']")
    # 搜索关键词输入框
    SEARCH_KEYWORD_INPUT = (By.XPATH, "//input[@placeholder='行政班名称 ｜ 行政班编号']")
    # 搜索按钮
    SEARCH_BUTTON = (By.XPATH, "//button[contains(.,'搜索')]")
    # 新建行政班按钮
    NEW_ADMIN_CLASS_BUTTON = (By.XPATH, "//button[contains(.,'新建行政班')]")
    # 所属学院下拉框
    NEW_ADMIN_CLASS_DEPT_DROPDOWN = (By.XPATH, "//div[contains(@aria-label,'新建行政班')]//span[text()='请选择学院']/parent::div")
    # 所属专业下拉框
    NEW_ADMIN_CLASS_MAJOR_DROPDOWN = (By.XPATH, "//span[text()='请先选择学院']/parent::div")
    # 年级下拉框
    NEW_ADMIN_CLASS_GRADE_DROPDOWN = (By.XPATH, "//div[contains(@aria-label,'新建行政班')]//span[text()='请选择年级']/parent::div")
    # 新建行政班确认按钮
    NEW_ADMIN_CLASS_CONFIRM_BUTTON = (By.XPATH, "//div[contains(@aria-label,'新建行政班')]//span[contains(.,'创建')]/parent::button")
    # 创建成功提示框
    CREATE_SUCCESS_ALERT = (By.XPATH, "//p[@class='el-message__content' and text()='创建成功']")
    # 删除下拉选项
    DELETE_LI = (By.XPATH, "//div[@aria-hidden='false']//li[contains(.,'删除')]")
    # 删除确认按钮
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//div[@aria-label='确认删除']//button[contains(.,'确定')]")
    # 删除成功提示框
    DELETE_SUCCESS_ALERT = (By.XPATH, "//p[contains(.,'删除成功')]")

    # ==================== 动态定位器方法（需要参数的定位器）====================

    def get_new_admin_class_input_locator(self, input_name):
        """获取新建行政班输入框的定位器

        Args:
            input_name: 输入框名称（如：'名称'、'编号'、'描述'）

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        if '名称' in input_name:
            return (By.XPATH, "//input[contains(@placeholder,'请输入行政班名称')]")
        elif '编号' in input_name:
            return (By.XPATH, "//input[contains(@placeholder,'请输入行政班编号')]")
        elif '描述' in input_name:
            return (By.XPATH, "//textarea[contains(@placeholder,'请输入行政班描述')]")
        else:
            return (By.XPATH, "//input[contains(@placeholder,'请输入行政班名称')]")

    def get_new_admin_class_dept_dropdown_option_locator(self, dept_name):
        """获取所属学院下拉框选项的定位器

        Args:
            dept_name: 学院名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@aria-hidden='false']//span[text()='" + dept_name + "']/parent::li")

    def get_new_admin_class_major_dropdown_option_locator(self, major_name):
        """获取所属专业下拉框选项的定位器

        Args:
            major_name: 专业名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@aria-hidden='false']//span[text()='" + major_name + "']/parent::li")

    def get_new_admin_class_grade_dropdown_option_locator(self, grade):
        """获取年级下拉框选项的定位器

        Args:
            grade: 年级（如：'2025级'）

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@aria-hidden='false']//span[text()='" + grade + "']/parent::li")

    def get_operation_button_by_admin_class_name_locator(self, admin_class_name):
        """获取根据行政班名称定位操作按钮的定位器

        Args:
            admin_class_name: 行政班名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//tr[.//td[contains(.,'" + admin_class_name + "')]]//button")

    # ==================== 页面操作方法 ====================

    def input_search_keyword(self, keyword):
        """输入搜索关键词

        Args:
            keyword: 搜索关键词（行政班名称或行政班编号）

        Returns:
            输入操作结果
        """
        log.info(f"输入搜索关键词：{keyword}，定位器为：{self.SEARCH_KEYWORD_INPUT[1]}")
        return self.input_text(self.SEARCH_KEYWORD_INPUT, keyword)

    def click_search_button(self):
        """点击搜索按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击搜索按钮，定位器为：{self.SEARCH_BUTTON[1]}")
        return self.click(self.SEARCH_BUTTON, timeout=15)

    def click_new_admin_class_button(self):
        """点击新建行政班按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击新建行政班按钮，定位器为：{self.NEW_ADMIN_CLASS_BUTTON[1]}")
        return self.click(self.NEW_ADMIN_CLASS_BUTTON)

    def input_new_admin_class_input(self, input_name, value):
        """输入新建行政班信息

        Args:
            input_name: 输入框名称（如：'名称'、'编号'、'描述'）
            value: 输入的值

        Returns:
            输入操作结果
        """
        locator = self.get_new_admin_class_input_locator(input_name)
        log.info(f"输入新建行政班信息：{input_name}为：{value}，定位器为：{locator[1]}")
        return self.input_text(locator, value, need_enter=True)

    def click_new_admin_class_dept_dropdown(self):
        """点击所属学院下拉框

        Returns:
            点击操作结果
        """
        log.info(f"点击所属学院下拉框，定位器为：{self.NEW_ADMIN_CLASS_DEPT_DROPDOWN[1]}")
        return self.click(self.NEW_ADMIN_CLASS_DEPT_DROPDOWN)

    def click_new_admin_class_dept_dropdown_option(self, dept_name):
        """点击所属学院下拉框选项

        Args:
            dept_name: 学院名称

        Returns:
            点击操作结果
        """
        locator = self.get_new_admin_class_dept_dropdown_option_locator(dept_name)
        log.info(f"点击所属学院下拉框选项：{dept_name}，定位器为：{locator[1]}")
        result = self.click(locator, timeout=15)
        # 点击后等待下拉菜单关闭
        sleep(0.5)
        return result

    def click_new_admin_class_major_dropdown(self):
        """点击所属专业下拉框

        Returns:
            点击操作结果
        """
        log.info(f"点击所属专业下拉框，定位器为：{self.NEW_ADMIN_CLASS_MAJOR_DROPDOWN[1]}")
        return self.click(self.NEW_ADMIN_CLASS_MAJOR_DROPDOWN)

    def click_new_admin_class_major_dropdown_option(self, major_name):
        """点击所属专业下拉框选项

        Args:
            major_name: 专业名称

        Returns:
            点击操作结果
        """
        locator = self.get_new_admin_class_major_dropdown_option_locator(major_name)
        log.info(f"点击所属专业下拉框选项：{major_name}，定位器为：{locator[1]}")
        result = self.click(locator, timeout=15)
        # 点击后等待下拉菜单关闭
        sleep(0.5)
        return result

    def click_new_admin_class_grade_dropdown(self):
        """点击年级下拉框

        Returns:
            点击操作结果
        """
        log.info(f"点击年级下拉框，定位器为：{self.NEW_ADMIN_CLASS_GRADE_DROPDOWN[1]}")
        return self.click(self.NEW_ADMIN_CLASS_GRADE_DROPDOWN)

    def click_new_admin_class_grade_dropdown_option(self, grade="2025级"):
        """点击年级下拉框选项

        Args:
            grade: 年级，默认为2025级（传入参数必须后面带级字，如2025级，2026级）

        Returns:
            点击操作结果
        """
        locator = self.get_new_admin_class_grade_dropdown_option_locator(grade)
        log.info(f"点击年级下拉框选项：{grade}，定位器为：{locator[1]}")
        result = self.click(locator, timeout=15)
        # 点击后等待下拉菜单关闭
        sleep(0.5)
        return result

    def click_new_admin_class_confirm_button(self):
        """点击新建行政班确认按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击新建行政班确认按钮，定位器为：{self.NEW_ADMIN_CLASS_CONFIRM_BUTTON[1]}")
        return self.click(self.NEW_ADMIN_CLASS_CONFIRM_BUTTON)

    def is_create_success_alert_display(self):
        """判断创建成功提示框是否出现

        Returns:
            bool: True表示创建成功，False表示失败
        """
        log.info(f"判断创建成功提示框是否出现，定位器为：{self.CREATE_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.CREATE_SUCCESS_ALERT)

    def click_operation_button_by_admin_class_name(self, admin_class_name):
        """根据行政班名称点击操作按钮

        Args:
            admin_class_name: 行政班名称

        Returns:
            点击操作结果
        """
        locator = self.get_operation_button_by_admin_class_name_locator(admin_class_name)
        log.info(f"根据行政班名称'{admin_class_name}'点击操作按钮，定位器为：{locator[1]}")
        return self.click(locator, timeout=15)

    def click_delete_li(self):
        """点击删除下拉选项

        Returns:
            点击操作结果
        """
        log.info(f"点击删除下拉选项，定位器为：{self.DELETE_LI[1]}")
        return self.click(self.DELETE_LI, timeout=15)

    def click_delete_confirm_button(self):
        """点击删除确认按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击删除确认按钮，定位器为：{self.DELETE_CONFIRM_BUTTON[1]}")
        return self.click(self.DELETE_CONFIRM_BUTTON, timeout=15)

    def is_delete_success_alert_display(self):
        """判断删除成功提示框是否出现

        Returns:
            bool: True表示删除成功，False表示失败
        """
        log.info(f"判断删除成功提示框是否出现，定位器为：{self.DELETE_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.DELETE_SUCCESS_ALERT)

    def create_admin_class(self, admin_class_info=None):
        """创建行政班

        Args:
            admin_class_info: 行政班信息字典，key为字段名称，value为字段值
                            例如：{"行政班名称": "计算机1班", "行政班编号": "001", ...}

        Returns:
            bool: True表示创建成功，False表示创建失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.ADMIN_CLASS_MANAGE_IFRAME)

        # 点击新建行政班按钮
        self.click_new_admin_class_button()

        # 从上到下设置新建信息
        # 1. 行政班名称
        self.input_new_admin_class_input("名称", admin_class_info['行政班名称'])

        # 2. 行政班编号
        self.input_new_admin_class_input("编号", admin_class_info['行政班编号'])

        # 3. 所属学院
        self.click_new_admin_class_dept_dropdown()
        self.click_new_admin_class_dept_dropdown_option(admin_class_info['所属学院'])

        # 4. 所属专业
        self.click_new_admin_class_major_dropdown()
        self.click_new_admin_class_major_dropdown_option(admin_class_info['所属专业'])

        # 5. 年级
        self.click_new_admin_class_grade_dropdown()
        self.click_new_admin_class_grade_dropdown_option(admin_class_info['年级'])

        # 6. 行政班描述
        self.input_new_admin_class_input("描述", admin_class_info['行政班描述'])

        # 点击确定按钮
        self.click_new_admin_class_confirm_button()

        # 断言创建成功提示框是否出现
        result = self.is_create_success_alert_display()

        # 切出iframe
        self.switch_out_iframe()

        log.info(f"创建行政班结果：{result}")
        return result

    def delete_admin_class_by_admin_class_name(self, admin_class_name):
        """根据行政班名称删除行政班

        Args:
            admin_class_name: 行政班名称

        Returns:
            bool: True表示删除成功，False表示删除失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.ADMIN_CLASS_MANAGE_IFRAME)
        # 输入搜索关键词
        self.input_search_keyword(admin_class_name)
        # 点击搜索按钮
        self.click_search_button()
        sleep(1)
        # 根据行政班名称点击操作按钮
        self.click_operation_button_by_admin_class_name(admin_class_name)
        # 点击删除下拉选项
        self.click_delete_li()
        # 点击删除确认按钮
        self.click_delete_confirm_button()
        # 断言删除成功提示框是否出现
        result = self.is_delete_success_alert_display()
        # 切出iframe
        self.switch_out_iframe()
        log.info(f"删除行政班结果：{result}")
        return result
