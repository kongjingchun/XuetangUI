# encoding: utf-8
# @File  : training_program_manage_page.py
# @Author:
# @Date  :
# @Desc  : 培养方案管理页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class TrainingProgramManagePage(BasePage):
    """培养方案管理页面类。

    对外只暴露“服务方法”（如创建培养方案、按方案名称进入修订、按方案名称删除培养方案等），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 培养方案管理主内容区域 iframe
    TRAINING_PROGRAM_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2102']")
    # 搜索关键词输入框
    SEARCH_KEYWORD_INPUT = (By.XPATH, "//input[@placeholder='培养方案名称']")
    # 新建培养方案按钮
    NEW_TRAINING_PROGRAM_BUTTON = (By.XPATH, "//button[contains(.,'新建培养方案')]")
    # 新建弹窗创建按钮
    NEW_TRAINING_PROGRAM_CONFIRM_BUTTON = (By.XPATH, "//div[@aria-label='新建培养方案']//button[contains(.,'创建')]")
    # 创建成功 toast 文案
    CREATE_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='创建培养方案成功']")
    # 删除培养方案按钮
    DELETE_TRAINING_PROGRAM_BUTTON = (By.XPATH, "//button[contains(.,'删除培养方案')]")
    # 删除确认（弹窗中的确定）
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//button[contains(.,'确定')]")
    # 删除成功 toast 文案
    DELETE_SUCCESS_MESSAGE = (By.XPATH, "//p[contains(.,'删除成功')]")
    # 更多菜单中的「编辑属性」项
    EDIT_PROPERTY_MENU_ITEM = (By.XPATH, "//div[@aria-hidden='false']//span[contains(.,'编辑属性')]/parent::li | //div[@aria-hidden='false']//li[contains(.,'编辑属性')]")

    # ==================== 动态定位器 getter ====================

    def get_new_training_program_input_locator(self, input_name):
        """输入框名称（如 '方案名称'、'学分要求'、'版本年份'）→ 新建培养方案对应输入框定位器。"""
        if '方案名称' in input_name or '名称' in input_name:
            return (By.XPATH, "//div[@aria-label='新建培养方案']//input[contains(@placeholder,'请输入培养方案名称')]")
        if '学分要求' in input_name or '学分' in input_name:
            return (By.XPATH, "//div[@aria-label='新建培养方案']//label[contains(.,'学分要求')]/following-sibling::div//input")
        if '版本年份' in input_name or '年份' in input_name:
            return (By.XPATH, "//div[@aria-label='新建培养方案']//label[contains(.,'版本年份')]/following-sibling::div//input")
        return None

    def get_new_training_program_dropdown_locator(self, dropdown_name):
        """下拉框名称（如 '关联专业'、'培养类型'、'培养层次'、'学制'、'授予学位'）→ 新建培养方案下拉框定位器。"""
        mapping = {
            '关联专业': "//div[@aria-label='新建培养方案']//span[text()='请选择专业']/parent::div",
            '培养类型': "//div[@aria-label='新建培养方案']//span[text()='请选择培养类型']/parent::div",
            '培养层次': "//div[@aria-label='新建培养方案']//span[text()='请选择培养层次']/parent::div",
            '学制': "//div[@aria-label='新建培养方案']//span[text()='请选择学制']/parent::div",
            '授予学位': "//div[@aria-label='新建培养方案']//span[text()='请选择授予学位']/parent::div",
        }
        xpath = mapping.get(dropdown_name)
        return (By.XPATH, xpath) if xpath else None

    def get_dropdown_option_locator(self, option_name):
        """选项名称 → 下拉框选项定位器。"""
        return (By.XPATH, f"//div[@aria-hidden='false']//span[contains(.,'{option_name}')]/parent::li")

    def get_revision_button_locator(self, program_name):
        """培养方案名称 → 修订按钮定位器。"""
        return (By.XPATH, f"//tr[.//td[contains(.,'{program_name}')]]//button[contains(.,'修订')]")

    def get_more_button_locator(self, program_name):
        """培养方案名称 → 更多按钮定位器。"""
        return (By.XPATH, f"//tr[.//td[contains(.,'{program_name}')]]//button[contains(.,'更多')]")

    # ==================== 服务方法（页面对外能力） ====================

    def create_training_program(self, training_program_info):
        """在培养方案管理页创建培养方案，返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)  # 切入培养方案管理 iframe

        self.click(self.NEW_TRAINING_PROGRAM_BUTTON)  # 点击新建培养方案

        locator_name = self.get_new_training_program_input_locator("方案名称")  # 获取方案名称输入框定位器
        if locator_name:
            self.input_text(locator_name, training_program_info['方案名称'])  # 输入方案名称

        self.click(self.get_new_training_program_dropdown_locator("关联专业"))  # 点击关联专业下拉
        self.click(self.get_dropdown_option_locator(training_program_info['关联专业']))  # 选择专业

        self.click(self.get_new_training_program_dropdown_locator("培养类型"))  # 点击培养类型下拉
        self.click(self.get_dropdown_option_locator(training_program_info['培养类型']))  # 选择培养类型

        self.click(self.get_new_training_program_dropdown_locator("培养层次"))  # 点击培养层次下拉
        self.click(self.get_dropdown_option_locator(training_program_info['培养层次']))  # 选择培养层次

        self.click(self.get_new_training_program_dropdown_locator("学制"))  # 点击学制下拉
        self.click(self.get_dropdown_option_locator(training_program_info['学制']))  # 选择学制

        self.click(self.get_new_training_program_dropdown_locator("授予学位"))  # 点击授予学位下拉
        self.click(self.get_dropdown_option_locator(training_program_info['授予学位']))  # 选择授予学位

        self.click(self.NEW_TRAINING_PROGRAM_CONFIRM_BUTTON)  # 点击创建

        result = self.is_displayed(self.CREATE_SUCCESS_MESSAGE)  # 检查是否出现创建成功提示
        log.info(f"创建培养方案结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def click_revision_button_by_program_name(self, program_name):
        """按培养方案名称点击修订按钮进入修订页，返回是否点击成功。"""
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)  # 切入培养方案管理 iframe
        locator = self.get_revision_button_locator(program_name)  # 获取修订按钮定位器
        log.info(f"点击方案名称'{program_name}'后的修订按钮，定位器为：{locator[1]}")
        result = self.click(locator, timeout=15, fluent=False)  # 点击修订按钮
        self.switch_out_iframe()  # 切回默认上下文
        log.info(f"点击方案名称'{program_name}'后的修订按钮成功")
        return result

    def delete_training_program_by_program_name(self, program_name):
        """按培养方案名称搜索并通过更多→编辑属性→删除培养方案完成删除，返回是否出现删除成功提示。"""
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)  # 切入培养方案管理 iframe

        self.input_text(self.SEARCH_KEYWORD_INPUT, program_name)  # 输入方案名称搜索
        self.click(self.get_more_button_locator(program_name), timeout=15)  # 点击更多按钮
        self.click(self.EDIT_PROPERTY_MENU_ITEM, timeout=15)  # 点击编辑属性
        self.click(self.DELETE_TRAINING_PROGRAM_BUTTON, timeout=15)  # 点击删除培养方案
        self.click(self.DELETE_CONFIRM_BUTTON, timeout=15)  # 点击确定

        result = self.is_displayed(self.DELETE_SUCCESS_MESSAGE)  # 检查是否出现删除成功提示
        log.info(f"删除培养方案结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result
