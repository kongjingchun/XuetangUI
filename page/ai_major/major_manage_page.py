# encoding: utf-8
# @File  : major_manage_page.py
# @Author: 孔敬淳
# @Date  : 2025/12/30
# @Desc  : 专业管理页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from time import sleep

from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class MajorManagePage(BasePage):
    """专业管理页面类。

    对外只暴露“服务方法”（创建专业、按专业名称删除专业），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 专业管理 iframe
    MAJOR_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2101']")
    # 列表上方专业名称/专业代码搜索输入框
    SEARCH_KEYWORD_INPUT = (By.XPATH, "//input[@placeholder='专业名称 ｜ 专业代码']")
    # 新建专业按钮
    NEW_MAJOR_BUTTON = (By.XPATH, "//button[contains(.,'新建专业')]")
    # 新建专业弹窗 - 所属院系下拉框
    NEW_MAJOR_BELONG_DEP_DROPDOWN = (By.XPATH, "//span[text()='请选择所属院系']/parent::div")
    # 新建专业弹窗 - 专业负责人下拉框
    NEW_MAJOR_BELONG_PROF_DROPDOWN = (By.XPATH, "//span[text()='请选择专业负责人']/parent::div")
    # 新建专业弹窗 - 收起专业负责人下拉后点击的空白区域（用于关闭下拉）
    CLOSE_DROPDOWN = (By.XPATH, "//label[text()='专业负责人']/following-sibling::div")
    # 新建专业弹窗的确定按钮
    NEW_MAJOR_CONFIRM_BUTTON = (By.XPATH, "//span[text()='确定']/parent::button")
    # 新建成功 toast 文案
    CREATE_SUCCESS_ALERT = (By.XPATH, "//p[text()='新建成功']")
    # 编辑弹窗中的删除专业按钮
    DELETE_BUTTON = (By.XPATH, "//button[contains(.,'删除专业')]")
    # 删除二次确认弹窗的确定按钮
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//div[contains(.,'警告')]//button[contains(.,'确定')]")
    # 删除成功 toast 文案
    DELETE_SUCCESS_ALERT = (By.XPATH, "//p[contains(.,'删除成功')]")

    # ==================== 动态定位器 getter ====================

    def get_new_major_input_locator(self, input_name):
        """新建专业表单字段名（'名称'/'学校专业代码'/'国家专业代码'）→ 对应输入框定位器。"""
        if '名称' in input_name:
            return (By.XPATH, "//input[contains(@placeholder,'请输入专业名称')]")
        if '代码' in input_name and '学校' in input_name:
            return (By.XPATH, "//input[contains(@placeholder,'请输入专业代码（学校）')]")
        if '代码' in input_name and '国家' in input_name:
            return (By.XPATH, "//input[contains(@placeholder,'请输入专业代码（国家）')]")
        return (By.XPATH, "//input[contains(@placeholder,'请输入专业名称')]")

    def get_new_major_belong_dep_dropdown_option_locator(self, dept_name):
        """院系名称 → 所属院系下拉选项中该院系项定位器。"""
        # 不依赖 aria-hidden，适配 Element Plus 下拉挂载到 body 的情况，只在当前可见下拉面板中找选项
        return (By.XPATH, f"//div[@aria-hidden='false']//li[.//span[text()='{dept_name}']]")

    def get_new_major_belong_prof_dropdown_option_locator(self, prof_name):
        """专业负责人姓名 → 专业负责人下拉选项中该项定位器。"""
        # 不直接在整页上找 span，避免命中其他下拉或隐藏的历史下拉；只在当前可见下拉面板中找负责人
        return (By.XPATH, f"//div[@aria-hidden='false']//li[.//span[text()='{prof_name}']]")

    def get_new_major_build_level_radio_locator(self, level="国家一流本科专业"):
        """建设层次（含'国'/'省'/'校'/'普'）→ 对应单选圆点定位器。"""
        if "国" in level:
            return (By.XPATH, "//span[text()='国家一流本科专业']/preceding-sibling::span")
        if "普" in level:
            return (By.XPATH, "//span[text()='普通专业']/preceding-sibling::span")
        if "省" in level:
            return (By.XPATH, "//span[text()='省级一流本科专业']/preceding-sibling::span")
        if "校" in level:
            return (By.XPATH, "//span[text()='校级重点专业']/preceding-sibling::span")
        return (By.XPATH, "//span[text()='国家一流本科专业']/preceding-sibling::span")

    def get_new_major_feature_checkbox_locator(self, feature="国家级特色专业"):
        """特色标签文案（如国家级特色专业）→ 对应复选框定位器。"""
        return (By.XPATH, f"//span[text()='{feature}']/preceding-sibling::span")

    def get_edit_button_hover_location_locator(self, major_name):
        """专业名称 → 该行编辑区域悬停触发定位器。"""
        return (By.XPATH, f"//tr[contains(.,'{major_name}')]//i[contains(@class,'action-icon')]")

    def get_edit_button_by_major_name_locator(self, major_name):
        """专业名称 → 该行编辑/操作按钮定位器。"""
        return (By.XPATH, f"//tr[contains(.,'{major_name}')]//button")

    # ==================== 服务方法（页面对外能力） ====================

    def create_major(self, major_info):
        """按 major_info 字典创建专业（从下到上填：专业特色标签、建设层次、负责人、所属院系、代码、名称），返回是否出现新建成功提示。"""
        self.switch_to_iframe(self.MAJOR_MANAGE_IFRAME)  # 切入专业管理 iframe
        self.click(self.NEW_MAJOR_BUTTON)  # 点击新建专业，弹出创建弹窗
        for feature in major_info.get('专业特色标签', []):
            self.click(self.get_new_major_feature_checkbox_locator(feature))  # 勾选专业特色标签
        self.click(self.get_new_major_build_level_radio_locator(major_info.get('专业建设层次', '国家一流本科专业')))  # 选择专业建设层次
        self.click(self.NEW_MAJOR_BELONG_PROF_DROPDOWN)  # 展开专业负责人下拉
        self.click(self.get_new_major_belong_prof_dropdown_option_locator(major_info['专业负责人']), timeout=15)  # 选择专业负责人
        sleep(0.5)
        self.click(self.CLOSE_DROPDOWN)  # 点击空白处关闭下拉
        self.click(self.NEW_MAJOR_BELONG_DEP_DROPDOWN)  # 展开所属院系下拉
        sleep(0.5)
        self.click(self.get_new_major_belong_dep_dropdown_option_locator(major_info['所属院系']), timeout=15)  # 选择所属院系
        loc_code_national = self.get_new_major_input_locator("国家专业代码")
        self.input_text(loc_code_national, str(major_info['国家专业代码']))  # 输入国家专业代码
        loc_code_school = self.get_new_major_input_locator("学校专业代码")
        self.input_text(loc_code_school, str(major_info['学校专业代码']))  # 输入学校专业代码
        loc_name = self.get_new_major_input_locator("名称")
        self.input_text(loc_name, str(major_info['专业名称']))  # 输入专业名称
        self.click(self.NEW_MAJOR_CONFIRM_BUTTON)  # 点击确定
        result = self.is_displayed(self.CREATE_SUCCESS_ALERT)  # 检查是否出现新建成功提示
        log.info(f"创建专业结果：{result}")
        sleep(1)
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def delete_major_by_major_name(self, major_name):
        """按专业名称搜索后进入编辑并删除该专业，返回是否出现删除成功提示。"""
        self.switch_to_iframe(self.MAJOR_MANAGE_IFRAME)  # 切入专业管理 iframe
        self.input_text(self.SEARCH_KEYWORD_INPUT, major_name)  # 输入专业名称搜索
        sleep(1)  # 等待列表刷新
        self.hover(self.get_edit_button_hover_location_locator(major_name))  # 悬停该行编辑区域
        self.click(self.get_edit_button_by_major_name_locator(major_name), timeout=15)  # 点击编辑/操作
        self.click(self.DELETE_BUTTON, timeout=15)  # 点击删除专业
        self.click(self.DELETE_CONFIRM_BUTTON, timeout=15)  # 点击确认删除
        result = self.is_displayed(self.DELETE_SUCCESS_ALERT)  # 检查是否出现删除成功提示
        log.info(f"删除专业结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result
