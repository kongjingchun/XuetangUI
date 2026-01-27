# encoding: utf-8
# @File  : role_manage_page.py
# @Author: 孔敬淳
# @Date  : 2025/12/31
# @Desc  : 角色管理页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from time import sleep

from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class RoleManagePage(BasePage):
    """角色管理页面类。

    对外只暴露“服务方法”（如分配角色给用户），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 角色管理 iframe
    ROLE_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2008']")
    # 用户搜索输入框（按用户ID/姓名等搜索）
    USER_SEARCH_INPUT = (By.XPATH, "//input[contains(@placeholder,'用户ID')]")
    # 分配角色弹窗的确定分配按钮
    ASSIGN_ROLE_CONFIRM_BUTTON = (By.XPATH, "//button[.//span[contains(.,'确定分配')]]")
    # 分配成功 toast 文案
    ASSIGN_ROLE_SUCCESS_ALERT = (By.XPATH, "//p[contains(text(),'成功')]")

    # ==================== 动态定位器 getter ====================

    def get_assign_role_button_locator(self, role_name):
        """角色名称 → 该角色行的「分配」按钮定位器。"""
        return (By.XPATH, f"//tbody//tr[contains(.,'{role_name}')]//span[contains(.,'分配')]/parent::button")

    def get_user_checkbox_locator(self, user_name):
        """用户名称 → 该用户行的复选框定位器。"""
        return (By.XPATH, f"//tr[contains(.,'{user_name}')]//span[@class='el-checkbox__inner']")

    # ==================== 服务方法（页面对外能力） ====================

    def assign_role_to_user(self, role_name, user_name=None):
        """将指定角色分配给指定用户，返回是否出现分配成功提示。"""
        self.switch_to_iframe(self.ROLE_MANAGE_IFRAME)  # 切入角色管理 iframe
        self.click(self.get_assign_role_button_locator(role_name))  # 点击该角色的分配按钮
        self.input_text(self.USER_SEARCH_INPUT, user_name)  # 输入用户名称搜索
        sleep(1)  # 等待搜索结果
        self.click(self.get_user_checkbox_locator(user_name))  # 勾选对应用户
        self.click(self.ASSIGN_ROLE_CONFIRM_BUTTON)  # 点击确定分配
        result = self.is_displayed(self.ASSIGN_ROLE_SUCCESS_ALERT)  # 检查是否出现分配成功提示
        log.info(f"分配角色 {role_name} 给用户 {user_name} 结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result
