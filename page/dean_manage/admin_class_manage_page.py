# encoding: utf-8
# @File  : admin_class_manage_page.py
# @Author: 孔敬淳
# @Date  : 2025/12/31
# @Desc  : 行政班管理页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from time import sleep

from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class AdminClassManagePage(BasePage):
    """行政班管理页面类。

    对外只暴露“服务方法”（创建行政班、按行政班名称删除行政班），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 行政班管理 iframe
    ADMIN_CLASS_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2005']")
    # 列表上方行政班名称/编号搜索输入框
    SEARCH_KEYWORD_INPUT = (By.XPATH, "//input[@placeholder='行政班名称 ｜ 行政班编号']")
    # 搜索按钮
    SEARCH_BUTTON = (By.XPATH, "//button[contains(.,'搜索')]")
    # 新建行政班按钮
    NEW_ADMIN_CLASS_BUTTON = (By.XPATH, "//button[contains(.,'新建行政班')]")
    # 新建行政班弹窗 - 所属学院下拉框
    NEW_ADMIN_CLASS_DEPT_DROPDOWN = (By.XPATH, "//div[contains(@aria-label,'新建行政班')]//span[text()='请选择学院']/parent::div")
    # 新建行政班弹窗 - 所属专业下拉框（需先选学院）
    NEW_ADMIN_CLASS_MAJOR_DROPDOWN = (By.XPATH, "//span[text()='请先选择学院']/parent::div")
    # 新建行政班弹窗 - 年级下拉框
    NEW_ADMIN_CLASS_GRADE_DROPDOWN = (By.XPATH, "//div[contains(@aria-label,'新建行政班')]//span[text()='请选择年级']/parent::div")
    # 新建行政班弹窗的创建按钮
    NEW_ADMIN_CLASS_CONFIRM_BUTTON = (By.XPATH, "//div[contains(@aria-label,'新建行政班')]//span[contains(.,'创建')]/parent::button")
    # 新建成功 toast 文案
    CREATE_SUCCESS_ALERT = (By.XPATH, "//p[@class='el-message__content' and text()='创建成功']")
    # 操作菜单中的「删除」项
    DELETE_LI = (By.XPATH, "//div[@aria-hidden='false']//li[contains(.,'删除')]")
    # 删除二次确认弹窗的确定按钮
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//div[@aria-label='确认删除']//button[contains(.,'确定')]")
    # 删除成功 toast 文案
    DELETE_SUCCESS_ALERT = (By.XPATH, "//p[contains(.,'删除成功')]")

    # ==================== 动态定位器 getter ====================

    def get_new_admin_class_input_locator(self, input_name):
        """新建行政班表单字段名（'名称'/'编号'/'描述'）→ 对应输入框/文本域定位器。"""
        if '名称' in input_name:
            return (By.XPATH, "//input[contains(@placeholder,'请输入行政班名称')]")
        if '编号' in input_name:
            return (By.XPATH, "//input[contains(@placeholder,'请输入行政班编号')]")
        if '描述' in input_name:
            return (By.XPATH, "//textarea[contains(@placeholder,'请输入行政班描述')]")
        return (By.XPATH, "//input[contains(@placeholder,'请输入行政班名称')]")

    def get_new_admin_class_dept_dropdown_option_locator(self, dept_name):
        """学院名称 → 所属学院下拉选项中该项定位器。"""
        return (By.XPATH, f"//div[@aria-hidden='false']//span[text()='{dept_name}']/parent::li")

    def get_new_admin_class_major_dropdown_option_locator(self, major_name):
        """专业名称 → 所属专业下拉选项中该项定位器。"""
        return (By.XPATH, f"//div[@aria-hidden='false']//span[text()='{major_name}']/parent::li")

    def get_new_admin_class_grade_dropdown_option_locator(self, grade):
        """年级（如 2025级）→ 年级下拉选项中该项定位器。"""
        return (By.XPATH, f"//div[@aria-hidden='false']//span[text()='{grade}']/parent::li")

    def get_operation_button_by_admin_class_name_locator(self, admin_class_name):
        """行政班名称 → 该行操作按钮定位器。"""
        return (By.XPATH, f"//tr[.//td[contains(.,'{admin_class_name}')]]//button")

    # ==================== 服务方法（页面对外能力） ====================

    def create_admin_class(self, admin_class_info):
        """按 admin_class_info 字典创建行政班（名称、编号、所属学院、所属专业、年级、描述），返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.ADMIN_CLASS_MANAGE_IFRAME)  # 切入行政班管理 iframe
        self.click(self.NEW_ADMIN_CLASS_BUTTON)  # 点击新建行政班，弹出创建弹窗
        self.input_text(
            self.get_new_admin_class_input_locator("名称"),
            str(admin_class_info['行政班名称']),
            need_enter=True
        )  # 输入行政班名称
        self.input_text(
            self.get_new_admin_class_input_locator("编号"),
            str(admin_class_info['行政班编号']),
            need_enter=True
        )  # 输入行政班编号
        self.click(self.NEW_ADMIN_CLASS_DEPT_DROPDOWN)  # 展开所属学院下拉
        self.click(self.get_new_admin_class_dept_dropdown_option_locator(admin_class_info['所属学院']), timeout=15)  # 选择所属学院
        sleep(0.5)
        self.click(self.NEW_ADMIN_CLASS_MAJOR_DROPDOWN)  # 展开所属专业下拉
        self.click(self.get_new_admin_class_major_dropdown_option_locator(admin_class_info['所属专业']), timeout=15)  # 选择所属专业
        sleep(0.5)
        self.click(self.NEW_ADMIN_CLASS_GRADE_DROPDOWN)  # 展开年级下拉
        self.click(self.get_new_admin_class_grade_dropdown_option_locator(admin_class_info.get('年级', '2025级')), timeout=15)  # 选择年级
        sleep(0.5)
        self.input_text(
            self.get_new_admin_class_input_locator("描述"),
            str(admin_class_info['行政班描述']),
            need_enter=True
        )  # 输入行政班描述
        self.click(self.NEW_ADMIN_CLASS_CONFIRM_BUTTON)  # 点击创建
        result = self.is_displayed(self.CREATE_SUCCESS_ALERT)  # 检查是否出现创建成功提示
        log.info(f"创建行政班结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def delete_admin_class_by_admin_class_name(self, admin_class_name):
        """按行政班名称搜索后点操作→删除→确认，返回是否出现删除成功提示。"""
        self.switch_to_iframe(self.ADMIN_CLASS_MANAGE_IFRAME)  # 切入行政班管理 iframe
        self.input_text(self.SEARCH_KEYWORD_INPUT, admin_class_name)  # 输入行政班名称搜索
        self.click(self.SEARCH_BUTTON, timeout=15)  # 点击搜索
        sleep(1)  # 等待列表刷新
        self.click(self.get_operation_button_by_admin_class_name_locator(admin_class_name), timeout=15)  # 点击该行操作按钮
        self.click(self.DELETE_LI, timeout=15)  # 选择删除
        self.click(self.DELETE_CONFIRM_BUTTON, timeout=15)  # 点击确认删除
        result = self.is_displayed(self.DELETE_SUCCESS_ALERT)  # 检查是否出现删除成功提示
        log.info(f"删除行政班结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result
