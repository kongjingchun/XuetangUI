# encoding: utf-8
# @File  : dept_list_manage_page.py
# @Author: 孔敬淳
# @Date  : 2025/12/29
# @Desc  : 院系列表管理页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from time import sleep

from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class DeptListManagePage(BasePage):
    """院系列表管理页面类。

    对外只暴露“服务方法”（创建院系、按院系代码删除院系），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 院系列表管理 iframe
    DEPT_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-3004']")
    # 新建院系按钮
    NEW_DEPT_BUTTON = (By.XPATH, "//button[contains(.,'新建院系')]")
    # 新建院系弹窗的确定按钮
    NEW_DEPT_CONFIRM_BUTTON = (By.XPATH, "//span[text()='确定']/parent::button")
    # 创建成功 toast 文案
    CREATE_SUCCESS_ALERT = (By.XPATH, "//p[text()='创建成功']")

    # ======================搜索与删除======================
    # 列表上方院系名称/院系代码搜索输入框
    SEARCH_KEYWORD_INPUT = (By.XPATH, "//input[@placeholder='院系名称 ｜ 院系代码']")
    # 编辑弹窗中的删除院系按钮
    DELETE_BUTTON = (By.XPATH, "//button[contains(.,'删除院系')]")
    # 删除二次确认弹窗的确定按钮
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//div[contains(.,'警告')]//button[contains(.,'确定')]")
    # 删除成功 toast 文案
    DELETE_SUCCESS_ALERT = (By.XPATH, "//p[contains(.,'删除成功')]")

    # ==================== 动态定位器 getter ====================

    def get_new_dept_input_locator(self, input_name):
        """新建院系表单字段名（'代码' 或 '名称'）→ 对应输入框定位器。"""
        if '代码' in input_name:
            return (By.XPATH, "//input[contains(@placeholder,'请输入院系代码')]")
        elif '名称' in input_name:
            return (By.XPATH, "//input[contains(@placeholder,'请输入院系名称')]")
        return (By.XPATH, "//input[contains(@placeholder,'请输入院系代码')]")

    def get_edit_button_hover_locator(self, dept_code):
        """院系代码 → 该行编辑区域悬停触发定位器。"""
        return (By.XPATH, f"//tr[contains(.,'{dept_code}')]//i[contains(@class,'action-icon')]")

    def get_edit_button_locator(self, dept_code):
        """院系代码 → 该行编辑/操作按钮定位器。"""
        return (By.XPATH, f"//tr[contains(.,'{dept_code}')]//button")

    # ==================== 服务方法（页面对外能力） ====================

    def create_dept(self, dept_info):
        """按 dept_info 字典创建院系（键为字段名如院系名称、院系代码），返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.DEPT_MANAGE_IFRAME)  # 切入院系列表管理 iframe
        self.click(self.NEW_DEPT_BUTTON)  # 点击新建院系，弹出创建弹窗
        for input_name, value in dept_info.items():
            self.input_text(self.get_new_dept_input_locator(input_name), str(value))  # 按字段逐项填写
        self.click(self.NEW_DEPT_CONFIRM_BUTTON)  # 点击确定
        result = self.is_displayed(self.CREATE_SUCCESS_ALERT)  # 检查是否出现创建成功提示
        log.info("创建院系结果：" + str(result))
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def delete_dept_by_dept_code(self, dept_code):
        """按院系代码搜索后进入编辑并删除该院系，返回是否出现删除成功提示。"""
        self.switch_to_iframe(self.DEPT_MANAGE_IFRAME)  # 切入院系列表管理 iframe
        self.input_text(self.SEARCH_KEYWORD_INPUT, dept_code)  # 输入院系代码搜索
        sleep(1)  # 等待列表刷新
        self.hover(self.get_edit_button_hover_locator(dept_code))  # 悬停该行编辑区域
        self.click(self.get_edit_button_locator(dept_code), timeout=15)  # 点击编辑/操作
        self.click(self.DELETE_BUTTON, timeout=15)  # 点击删除院系
        self.click(self.DELETE_CONFIRM_BUTTON, timeout=15)  # 点击确认删除
        result = self.is_displayed(self.DELETE_SUCCESS_ALERT)  # 检查是否出现删除成功提示
        log.info(f"删除院系结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result
