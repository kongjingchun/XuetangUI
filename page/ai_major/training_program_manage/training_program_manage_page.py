# encoding: utf-8
# @File  : TrainingProgramManagePage.py
# @Author: 孔敬淳
# @Date  : 2025/12/31
# @Desc  : 培养方案管理页面对象类，封装培养方案管理相关的页面操作方法

from time import sleep
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class TrainingProgramManagePage(BasePage):
    """培养方案管理页面类

    继承BasePage类，提供培养方案管理页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化培养方案管理页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
    # 培养方案管理iframe
    TRAINING_PROGRAM_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2102']")
    # 导入培养方案按钮
    IMPORT_TRAINING_PROGRAM_BUTTON = (By.XPATH, "//button[contains(.,'导入培养方案')]")
    # 搜索关键词输入框
    SEARCH_KEYWORD_INPUT = (By.XPATH, "//input[@placeholder='培养方案名称']")
    # 新建培养方案按钮
    NEW_TRAINING_PROGRAM_BUTTON = (By.XPATH, "//button[contains(.,'新建培养方案')]")
    # 新建确定按钮
    NEW_TRAINING_PROGRAM_CONFIRM_BUTTON = (By.XPATH, "//div[@aria-label='新建培养方案']//button[contains(.,'创建')]")
    # 创建成功提示框
    CREATE_SUCCESS_ALERT = (By.XPATH, "//p[text()='创建培养方案成功']")
    # 删除培养方案按钮
    DELETE_TRAINING_PROGRAM_BUTTON = (By.XPATH, "//button[contains(.,'删除培养方案')]")
    # 删除确认按钮
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//button[contains(.,'确定')]")
    # 删除成功提示框
    DELETE_SUCCESS_ALERT = (By.XPATH, "//p[contains(.,'删除成功')]")

    # ==================== 动态定位器方法（需要参数的定位器）====================

    def get_new_training_program_input_locator(self, input_name):
        """获取新建培养方案输入框的定位器

        Args:
            input_name: 输入框名称，如 '方案名称'、'学分要求'、'版本年份'

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        if '方案名称' in input_name or '名称' in input_name:
            return (By.XPATH, "//div[@aria-label='新建培养方案']//input[contains(@placeholder,'请输入培养方案名称')]")
        elif '学分要求' in input_name or '学分' in input_name:
            return (By.XPATH, "//div[@aria-label='新建培养方案']//label[contains(.,'学分要求')]/following-sibling::div//input")
        elif '版本年份' in input_name or '年份' in input_name:
            return (By.XPATH, "//div[@aria-label='新建培养方案']//label[contains(.,'版本年份')]/following-sibling::div//input")
        else:
            return None

    def get_new_training_program_dropdown_locator(self, dropdown_name):
        """获取新建培养方案下拉框的定位器

        Args:
            dropdown_name: 下拉框名称，如 '关联专业'、'培养类型'、'培养层次'、'学制'、'授予学位'

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        if dropdown_name == '关联专业':
            return (By.XPATH, "//div[@aria-label='新建培养方案']//span[text()='请选择专业']/parent::div")
        elif dropdown_name == '培养类型':
            return (By.XPATH, "//div[@aria-label='新建培养方案']//span[text()='请选择培养类型']/parent::div")
        elif dropdown_name == '培养层次':
            return (By.XPATH, "//div[@aria-label='新建培养方案']//span[text()='请选择培养层次']/parent::div")
        elif dropdown_name == '学制':
            return (By.XPATH, "//div[@aria-label='新建培养方案']//span[text()='请选择学制']/parent::div")
        elif dropdown_name == '授予学位':
            return (By.XPATH, "//div[@aria-label='新建培养方案']//span[text()='请选择授予学位']/parent::div")
        else:
            return None

    def get_dropdown_option_locator(self, option_name):
        """获取下拉框选项的定位器

        Args:
            option_name: 选项名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//div[@aria-hidden='false']//span[contains(.,'{option_name}')]/parent::li")

    def get_revision_button_locator(self, program_name):
        """获取修订按钮的定位器

        Args:
            program_name: 培养方案名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//tr[.//td[contains(.,'{program_name}')]]//button[contains(.,'修订')]")

    def get_more_button_locator(self, program_name):
        """获取更多按钮的定位器

        Args:
            program_name: 培养方案名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//tr[.//td[contains(.,'{program_name}')]]//button[contains(.,'更多')]")

    # ==================== 页面操作方法 ====================

    def switch_out_training_program_manage_iframe(self):
        """从培养方案管理iframe切出

        Returns:
            切换操作结果
        """
        log.info("从培养方案管理iframe切出")
        return self.switch_out_iframe()

    def input_search_keyword(self, keyword):
        """输入搜索关键词

        Args:
            keyword: 搜索关键词

        Returns:
            输入操作结果
        """
        log.info(f"输入搜索关键词：{keyword}，定位器为：{self.SEARCH_KEYWORD_INPUT[1]}")
        return self.input_text(self.SEARCH_KEYWORD_INPUT, keyword)

    def click_import_training_program_button(self):
        """点击导入培养方案按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击导入培养方案按钮，定位器为：{self.IMPORT_TRAINING_PROGRAM_BUTTON[1]}")
        return self.click(self.IMPORT_TRAINING_PROGRAM_BUTTON)

    def click_new_training_program_button(self):
        """点击新建培养方案按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击新建培养方案按钮，定位器为：{self.NEW_TRAINING_PROGRAM_BUTTON[1]}")
        return self.click(self.NEW_TRAINING_PROGRAM_BUTTON)

    def input_new_training_program_input(self, input_name, value):
        """输入新建培养方案信息

        Args:
            input_name: 输入框名称（如：'方案名称'、'学分要求'、'版本年份'）
            value: 输入的值

        Returns:
            输入操作结果
        """
        locator = self.get_new_training_program_input_locator(input_name)
        if locator is None:
            log.error(f"未找到输入框：{input_name}")
            return False
        log.info(f"输入新建培养方案信息：{input_name}为：{value}，定位器为：{locator[1]}")
        return self.input_text(locator, value)

    def click_new_training_program_dropdown(self, dropdown_name):
        """点击新建培养方案下拉框

        Args:
            dropdown_name: 下拉框名称，如 '关联专业'、'培养类型'、'培养层次'、'学制'、'授予学位'

        Returns:
            点击操作结果
        """
        locator = self.get_new_training_program_dropdown_locator(dropdown_name)
        if locator is None:
            log.error(f"未找到下拉框：{dropdown_name}")
            return False
        log.info(f"点击{dropdown_name}下拉框，定位器为：{locator[1]}")
        return self.click(locator)

    def click_new_training_program_dropdown_option(self, option_name):
        """点击新建培养方案下拉框选项

        Args:
            option_name: 选项名称

        Returns:
            点击操作结果
        """
        locator = self.get_dropdown_option_locator(option_name)
        log.info(f"点击下拉框选项：{option_name}，定位器为：{locator[1]}")
        result = self.click(locator, timeout=15)
        # 点击后等待下拉菜单关闭
        sleep(0.5)
        return result

    def click_new_training_program_confirm_button(self):
        """点击新建培养方案确认按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击新建培养方案确认按钮，定位器为：{self.NEW_TRAINING_PROGRAM_CONFIRM_BUTTON[1]}")
        return self.click(self.NEW_TRAINING_PROGRAM_CONFIRM_BUTTON)

    def is_create_success_alert_display(self):
        """查看创建成功提示框是否出现

        Returns:
            bool: True表示创建成功提示框出现，False表示未出现
        """
        log.info(f"查看创建成功提示框是否出现，定位器为：{self.CREATE_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.CREATE_SUCCESS_ALERT)

    def click_revision_button_by_program_name(self, program_name):
        """根据方案名称点击修订按钮

        Args:
            program_name: 培养方案名称

        Returns:
            bool: True表示点击成功，False表示点击失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)

        # 根据方案名称点击修订按钮
        locator = self.get_revision_button_locator(program_name)
        log.info(f"点击方案名称'{program_name}'后的修订按钮，定位器为：{locator[1]}")
        result = self.click(locator, timeout=15, fluent=False)

        # 切出iframe
        self.switch_out_training_program_manage_iframe()

        log.info(f"点击方案名称'{program_name}'后的修订按钮成功")
        return result

    def click_more_button_by_program_name(self, program_name):
        """根据方案名称点击更多按钮

        Args:
            program_name: 培养方案名称

        Returns:
            点击操作结果
        """
        # 根据方案名称点击更多按钮
        locator = self.get_more_button_locator(program_name)
        log.info(f"点击方案名称'{program_name}'后的更多按钮，定位器为：{locator[1]}")
        return self.click(locator, timeout=15)

    def click_edit_property_button(self):
        """点击编辑属性按钮

        Returns:
            点击操作结果
        """
        edit_property_locator = (By.XPATH, "//div[@aria-hidden='false']//span[contains(.,'编辑属性')]/parent::li | //div[@aria-hidden='false']//li[contains(.,'编辑属性')]")
        log.info(f"点击编辑属性按钮，定位器为：{edit_property_locator[1]}")
        return self.click(edit_property_locator, timeout=15)

    def click_delete_training_program_button(self):
        """点击删除培养方案按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击删除培养方案按钮，定位器为：{self.DELETE_TRAINING_PROGRAM_BUTTON[1]}")
        return self.click(self.DELETE_TRAINING_PROGRAM_BUTTON, timeout=15)

    def click_delete_confirm_button(self):
        """点击删除确认按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击删除确认按钮，定位器为：{self.DELETE_CONFIRM_BUTTON[1]}")
        return self.click(self.DELETE_CONFIRM_BUTTON, timeout=15)

    def is_delete_success_alert_display(self):
        """断言删除成功提示框是否出现

        Returns:
            bool: True表示删除成功提示框出现，False表示未出现
        """
        log.info(f"断言删除成功提示框是否出现，定位器为：{self.DELETE_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.DELETE_SUCCESS_ALERT)

    def create_training_program(self, training_program_info):
        """创建培养方案

        Args:
            training_program_info: 培养方案信息

        Returns:
            bool: True表示创建成功，False表示创建失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)

        # 点击新建培养方案按钮
        self.click_new_training_program_button()
        sleep(0.5)

        # 从上到下设置新建信息
        # 1. 方案名称
        self.input_new_training_program_input("方案名称", training_program_info['方案名称'])

        # 2. 所属院系（不需要更改默认，跳过）

        # 3. 关联专业
        self.click_new_training_program_dropdown("关联专业")
        self.click_new_training_program_dropdown_option(training_program_info['关联专业'])

        # 4. 培养类型
        self.click_new_training_program_dropdown("培养类型")
        self.click_new_training_program_dropdown_option(training_program_info['培养类型'])

        # 5. 培养层次
        self.click_new_training_program_dropdown("培养层次")
        self.click_new_training_program_dropdown_option(training_program_info['培养层次'])

        # 6. 学制
        self.click_new_training_program_dropdown("学制")
        self.click_new_training_program_dropdown_option(training_program_info['学制'])

        # 7. 学分要求（不需要更改默认，跳过）

        # 8. 授予学位
        self.click_new_training_program_dropdown("授予学位")
        self.click_new_training_program_dropdown_option(training_program_info['授予学位'])

        # 9. 版本年份（不需要更改默认，跳过）

        # 点击创建按钮
        self.click_new_training_program_confirm_button()
        sleep(1)

        # 断言创建成功提示框是否出现
        result = self.is_create_success_alert_display()

        # 切出iframe
        self.switch_out_training_program_manage_iframe()

        log.info(f"创建培养方案结果：{result}")
        return result

    def delete_training_program_by_program_name(self, program_name):
        """根据方案名称删除培养方案

        Args:
            program_name: 培养方案名称

        Returns:
            bool: True表示删除成功，False表示删除失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)
        # 输入搜索关键词
        self.input_search_keyword(program_name)
        sleep(1)
        # 点击更多按钮
        self.click_more_button_by_program_name(program_name)
        # 点击编辑属性按钮
        self.click_edit_property_button()
        # 根据方案名称点击删除按钮
        self.click_delete_training_program_button()
        # 点击删除确认按钮
        self.click_delete_confirm_button()
        # 断言删除成功提示框是否出现
        result = self.is_delete_success_alert_display()
        # 切出iframe
        self.switch_out_training_program_manage_iframe()
        log.info(f"删除培养方案结果：{result}")
        return result
