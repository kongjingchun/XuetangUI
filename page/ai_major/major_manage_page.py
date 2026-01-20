# encoding: utf-8
# @File  : MajorManagePage.py
# @Author: 孔敬淳
# @Date  : 2025/12/30/16:23
# @Desc  : 专业管理页面对象类，封装专业管理相关的页面操作方法
from time import sleep

from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class MajorManagePage(BasePage):
    """专业管理页面类

    继承BasePage类，提供专业管理页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化专业管理页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
    # 专业管理iframe
    MAJOR_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2101']")
    # 搜索关键词输入框
    SEARCH_KEYWORD_INPUT = (By.XPATH, "//input[@placeholder='专业名称 ｜ 专业代码']")
    # 新建专业按钮
    NEW_MAJOR_BUTTON = (By.XPATH, "//button[contains(.,'新建专业')]")
    # 所属院系下拉框
    NEW_MAJOR_BELONG_DEP_DROPDOWN = (By.XPATH, "//span[text()='请选择所属院系']/parent::div")
    # 专业负责人下拉框
    NEW_MAJOR_BELONG_PROF_DROPDOWN = (By.XPATH, "//span[text()='请选择专业负责人']/parent::div")
    # 关闭下拉框
    CLOSE_DROPDOWN = (By.XPATH, "//label[text()='专业负责人']/following-sibling ::div")
    # 新建专业确认按钮
    NEW_MAJOR_CONFIRM_BUTTON = (By.XPATH, "//span[text()='确定']/parent::button")
    # 创建成功提示框
    CREATE_SUCCESS_ALERT = (By.XPATH, "//p[text()='新建成功']")
    # 删除专业按钮
    DELETE_BUTTON = (By.XPATH, "//button[contains(.,'删除专业')]")
    # 删除确认按钮
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//div[contains(.,'警告')]//button[contains(.,'确定')]")
    # 删除成功提示框
    DELETE_SUCCESS_ALERT = (By.XPATH, "//p[contains(.,'删除成功')]")

    # ==================== 动态定位器方法（需要参数的定位器）====================

    def get_new_major_input_locator(self, input_name):
        """获取新建专业输入框的定位器

        Args:
            input_name: 输入框名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        if '名称' in input_name:
            return (By.XPATH, "//input[contains(@placeholder,'请输入专业名称')]")
        elif '代码' in input_name and '学校' in input_name:
            return (By.XPATH, "//input[contains(@placeholder,'请输入专业代码（学校）')]")
        elif '代码' in input_name and '国家' in input_name:
            return (By.XPATH, "//input[contains(@placeholder,'请输入专业代码（国家）')]")

    def get_new_major_belong_dep_dropdown_option_locator(self, dept_name):
        """获取所属院系下拉框选项的定位器

        Args:
            dept_name: 院系名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@aria-hidden='false']//span[text()='" + dept_name + "']/parent::li")

    def get_new_major_belong_prof_dropdown_option_locator(self, prof_name):
        """获取专业负责人下拉框选项的定位器

        Args:
            prof_name: 专业负责人名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//span[text()='" + prof_name + "']/parent::li")

    def get_new_major_build_level_radio_locator(self, level="国家一流本科专业"):
        """获取建设层次单选框的定位器

        Args:
            level: 建设层次

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        if "国" in level:
            return (By.XPATH, "//span[text()='国家一流本科专业']/preceding-sibling::span")
        elif "普" in level:
            return (By.XPATH, "//span[text()='普通专业']/preceding-sibling::span")
        elif "省" in level:
            return (By.XPATH, "//span[text()='省级一流本科专业']/preceding-sibling::span")
        elif "校" in level:
            return (By.XPATH, "//span[text()='校级重点专业']/preceding-sibling::span")

    def get_new_major_feature_checkbox_locator(self, feature="国家级特色专业"):
        """获取特色专业复选框的定位器

        Args:
            feature: 特色专业

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//span[text()='" + feature + "']/preceding-sibling::span")

    def get_edit_button_hover_location_locator(self, major_name):
        """获取编辑悬停位置定位器（根据专业名称）

        Args:
            major_name: 专业名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//tr[contains(.,'" + major_name + "')]//i[contains(@class,'action-icon')]")

    def get_edit_button_by_major_name_locator(self, major_name):
        """获取编辑按钮定位器（根据专业名称）

        Args:
            major_name: 专业名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//tr[contains(.,'" + major_name + "')]//button")

    # ==================== 页面操作方法 ====================

    def click_new_major_button(self):
        """点击新建专业按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击新建专业按钮，定位器为：{self.NEW_MAJOR_BUTTON[1]}")
        return self.click(self.NEW_MAJOR_BUTTON)

    def input_new_major_input(self, input_name, value):
        """输入新建专业信息

        Args:
            input_name: 输入框名称
            value: 输入的值

        Returns:
            输入操作结果
        """
        locator = self.get_new_major_input_locator(input_name)
        log.info(f"输入新建专业信息：{input_name}为：{value}，定位器为：{locator[1]}")
        return self.input_text(locator, value)

    def click_new_major_belong_dep_dropdown(self):
        """点击所属院系下拉框

        Returns:
            点击操作结果
        """
        log.info(f"点击所属院系下拉框，定位器为：{self.NEW_MAJOR_BELONG_DEP_DROPDOWN[1]}")
        return self.click(self.NEW_MAJOR_BELONG_DEP_DROPDOWN)

    def click_new_major_belong_dep_dropdown_option(self, dep_name):
        """点击所属院系下拉框选项

        Args:
            dep_name: 院系名称

        Returns:
            点击操作结果
        """
        locator = self.get_new_major_belong_dep_dropdown_option_locator(dep_name)
        log.info(f"点击所属院系下拉框选项：{dep_name}，定位器为：{locator[1]}")
        result = self.click(locator, timeout=15)
        # 点击后等待下拉菜单关闭
        sleep(0.5)
        return result

    def click_new_major_belong_prof_dropdown(self):
        """点击专业负责人下拉框

        Returns:
            点击操作结果
        """
        log.info(f"点击专业负责人下拉框，定位器为：{self.NEW_MAJOR_BELONG_PROF_DROPDOWN[1]}")
        return self.click(self.NEW_MAJOR_BELONG_PROF_DROPDOWN)

    def click_new_major_belong_prof_dropdown_option(self, prof_name):
        """点击专业负责人下拉框选项

        Args:
            prof_name: 专业负责人名称

        Returns:
            点击操作结果
        """
        locator = self.get_new_major_belong_prof_dropdown_option_locator(prof_name)
        log.info(f"点击专业负责人下拉框选项：{prof_name}，定位器为：{locator[1]}")
        result = self.click(locator, timeout=15)
        # 点击后等待下拉菜单关闭
        sleep(0.5)
        return result

    def click_close_dropdown(self):
        """点击关闭下拉框

        Returns:
            点击操作结果
        """
        log.info(f"点击关闭下拉框，定位器为：{self.CLOSE_DROPDOWN[1]}")
        return self.click(self.CLOSE_DROPDOWN)

    def click_new_major_build_level_radio(self, level):
        """点击建设层次单选框

        Args:
            level: 建设层次

        Returns:
            点击操作结果
        """
        locator = self.get_new_major_build_level_radio_locator(level)
        log.info(f"点击建设层次单选框：{level}，定位器为：{locator[1]}")
        return self.click(locator)

    def click_new_major_feature_checkbox(self, feature="国家级特色专业"):
        """点击特色专业复选框

        Args:
            feature: 特色专业

        Returns:
            点击操作结果
        """
        locator = self.get_new_major_feature_checkbox_locator(feature)
        log.info(f"点击特色专业复选框：{feature}，定位器为：{locator[1]}")
        return self.click(locator)

    def click_new_major_confirm_button(self):
        """点击新建专业确认按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击新建专业确认按钮，定位器为：{self.NEW_MAJOR_CONFIRM_BUTTON[1]}")
        return self.click(self.NEW_MAJOR_CONFIRM_BUTTON)

    def is_create_success_alert_display(self):
        """判断创建成功提示框是否出现

        Returns:
            bool: True表示创建成功，False表示失败
        """
        log.info(f"判断创建成功提示框是否出现，定位器为：{self.CREATE_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.CREATE_SUCCESS_ALERT)

    def create_major(self, major_info):
        """创建专业

        Args:
            major_info: 专业信息字典，key为字段名称，value为字段值
                      例如：{"专业名称": "计算机科学", "学校专业代码": "001", ...}

        Returns:
            bool: True表示创建成功，False表示创建失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.MAJOR_MANAGE_IFRAME)

        # 点击新建专业按钮
        self.click_new_major_button()

        # 从下到上依次设置新建信息

        # 1. 专业特色标签（循环选择多个特色标签）
        for feature in major_info['专业特色标签']:
            self.click_new_major_feature_checkbox(feature)

        # 2. 专业建设层次
        self.click_new_major_build_level_radio(major_info['专业建设层次'])

        # 3. 专业负责人
        self.click_new_major_belong_prof_dropdown()
        self.click_new_major_belong_prof_dropdown_option(major_info['专业负责人'])
        # 关闭下拉框
        self.click_close_dropdown()

        # 4. 所属院系
        self.click_new_major_belong_dep_dropdown()
        sleep(0.5)
        self.click_new_major_belong_dep_dropdown_option(major_info['所属院系'])

        # 5. 国家专业代码
        self.input_new_major_input("国家专业代码", major_info['国家专业代码'])

        # 6. 学校专业代码
        self.input_new_major_input("学校专业代码", major_info['学校专业代码'])

        # 7. 专业名称
        self.input_new_major_input("名称", major_info['专业名称'])

        # 点击确定按钮
        self.click_new_major_confirm_button()

        # 断言创建成功提示框是否出现
        result = self.is_create_success_alert_display()
        sleep(1)

        # 切出iframe
        self.switch_out_iframe()

        log.info(f"创建专业结果：{result}")
        return result

    def input_search_keyword(self, keyword):
        """输入搜索关键词

        Args:
            keyword: 搜索关键词（专业名称或专业代码）

        Returns:
            输入操作结果
        """
        log.info(f"输入搜索关键词：{keyword}，定位器为：{self.SEARCH_KEYWORD_INPUT[1]}")
        return self.input_text(self.SEARCH_KEYWORD_INPUT, keyword)

    def hover_edit_button(self, major_name):
        """鼠标悬停编辑按钮

        Args:
            major_name: 专业名称

        Returns:
            悬停操作结果
        """
        locator = self.get_edit_button_hover_location_locator(major_name)
        log.info(f"鼠标悬停编辑按钮，定位器为：{locator[1]}")
        return self.hover(locator)

    def click_edit_button_by_major_name(self, major_name):
        """根据专业名称点击编辑按钮

        Args:
            major_name: 专业名称

        Returns:
            点击操作结果
        """
        locator = self.get_edit_button_by_major_name_locator(major_name)
        log.info(f"根据专业名称'{major_name}'点击编辑按钮，定位器为：{locator[1]}")
        return self.click(locator, timeout=15)

    def click_delete_button(self):
        """点击删除专业按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击删除专业按钮，定位器为：{self.DELETE_BUTTON[1]}")
        return self.click(self.DELETE_BUTTON, timeout=15)

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

    def delete_major_by_major_name(self, major_name):
        """根据专业名称删除专业

        Args:
            major_name: 专业名称

        Returns:
            bool: True表示删除成功，False表示删除失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.MAJOR_MANAGE_IFRAME)
        # 输入搜索关键词
        self.input_search_keyword(major_name)
        sleep(1)
        # 鼠标悬停编辑按钮
        self.hover_edit_button(major_name)
        # 点击编辑按钮
        self.click_edit_button_by_major_name(major_name)
        # 点击删除按钮
        self.click_delete_button()
        # 点击删除确认按钮
        self.click_delete_confirm_button()
        # 断言删除成功提示框是否出现
        result = self.is_delete_success_alert_display()
        # 切出iframe
        self.switch_out_iframe()
        log.info(f"删除专业结果：{result}")
        return result
