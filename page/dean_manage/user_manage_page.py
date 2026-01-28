# encoding: utf-8
# @File  : user_manage_page.py
# @Author: 孔敬淳
# @Date  : 2025/12/25
# @Desc  : 用户管理页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from time import sleep

from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class UserManagePage(BasePage):
    """用户管理页面类。

    对外只暴露“服务方法”（如创建用户、绑定用户、按工号删除用户），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 用户管理 iframe
    USER_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2006']")
    # 工号搜索输入框
    SEARCH_CODE_INPUT = (By.XPATH, "//div[./label[text()='工号筛选：']]//input")
    # 新增用户下拉入口（悬停后出现角色选项）
    ADD_USER_BUTTON = (By.XPATH, "//div[@class='el-dropdown toolbar-button']")
    # 创建用户弹窗的提交按钮
    SUBMIT_USER_BUTTON = (By.XPATH, "//div[@class = 'dialog-footer']/button[contains(.,'创建用户')]")
    # 创建成功 toast 文案
    CREATE_SUCCESS_ALERT = (By.XPATH, "//p[contains(text(),'创建成功')]")
    # 绑定弹窗中平台用户 ID 输入框
    USER_BIND_INPUT = (By.XPATH, "//input[@placeholder='请输入平台用户ID']")
    # 绑定弹窗的确认绑定按钮
    USER_BIND_CONFIRM_BUTTON = (By.XPATH, "//span[contains(.,'确认绑定')]/parent::button")
    # 绑定成功 toast 文案
    BIND_SUCCESS_ALERT = (By.XPATH, "//p[contains(text(),'绑定用户成功')]")
    # 编辑弹窗中的删除用户按钮
    DELETE_USER_BUTTON = (By.XPATH, "//button[contains(.,'删除用户')]")
    # 删除二次确认弹窗的删除按钮
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//div[contains(@aria-label,'确认删除') or contains(@aria-label,'删除')]//button[contains(.,'删除')]")
    # 删除成功 toast 文案
    DELETE_SUCCESS_ALERT = (By.XPATH, "//p[contains(text(),'删除成功')]")
    # 新建用户表单中关闭所属学院下拉的图标（用于收起下拉）
    NEW_USER_DEPT_DROPDOWN_CLOSE = (By.XPATH, "//label[text()='所属学院']//following-sibling::div//div[@class='el-select__suffix']")

    # ==================== 动态定位器 getter ====================

    def get_add_user_role_select_locator(self, role_name):
        """角色名称（如：创建教务管理员、创建教师）→ 下拉中该角色选项定位器。"""
        return (By.XPATH, f"//li[contains(.,'{role_name}')]")

    def get_create_user_input_locator(self, input_name):
        """创建用户表单字段名（如：姓名、工号、手机、邮箱）→ 对应输入框定位器。"""
        return (By.XPATH, f"//div[contains(@aria-label,'创建')]//input[contains(@placeholder,'{input_name}')]")

    def get_search_input_locator(self, input_name):
        """筛选方式名（如：工号）→ 列表上方对应搜索输入框定位器。"""
        return (By.XPATH, f"//input[contains(@placeholder,'{input_name}')]")

    def get_user_bind_button_locator(self, user_code):
        """用户工号 → 该行「绑定」按钮定位器。"""
        return (By.XPATH, f"//tr[contains(.,'{user_code}')]//button[contains(.,'绑定')]")

    def get_edit_button_by_code_locator(self, code):
        """工号/学号 → 该行「编辑」按钮定位器。"""
        return (By.XPATH, f"//tr[.//td[contains(.,'{code}')]]//button[contains(.,'编辑')]")

    def get_new_user_dept_dropdown_locator(self, role_name):
        """新建用户弹窗按角色（如：创建教务管理员）→ 所属学院下拉框定位器。"""
        return (By.XPATH, f"//div[contains(@aria-label,'{role_name}')]//span[text()='请选择学院']")

    def get_new_user_dept_dropdown_option_locator(self, dept_name):
        """学院名称 → 所属学院下拉选项中该学院项定位器。"""
        return (By.XPATH, f"(//li/span[text()='{dept_name}'])[2]")

    # ==================== 服务方法（页面对外能力） ====================

    def create_user(self, role_name, user_info):
        """按角色创建用户并填写 user_info 中各字段，返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.USER_MANAGE_IFRAME)  # 切入用户管理 iframe
        self.hover(self.ADD_USER_BUTTON)  # 悬停「创建」展开角色下拉
        self.click(self.get_add_user_role_select_locator(role_name))  # 选择角色（如：创建教务管理员）
        for input_name, value in user_info.items():  # 按字段逐项填写
            if input_name == '学院':
                self.click(self.get_new_user_dept_dropdown_locator(role_name))  # 点击所属学院下拉
                self.click(self.get_new_user_dept_dropdown_option_locator(str(value)))  # 选择学院
            else:
                self.input_text(self.get_create_user_input_locator(input_name), str(value))  # 填写姓名/工号/手机/邮箱等
        self.click(self.SUBMIT_USER_BUTTON)  # 点击创建用户
        result = self.is_displayed(self.CREATE_SUCCESS_ALERT)  # 检查是否出现创建成功提示
        log.info("创建用户结果：" + str(result))
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def bind_user(self, user, user_id):
        """按用户标识搜索后，将平台用户 ID 绑定到对应用户，返回是否出现绑定成功提示。"""
        self.switch_to_iframe(self.USER_MANAGE_IFRAME)  # 切入用户管理 iframe
        self.input_text(self.SEARCH_CODE_INPUT, user)  # 按工号搜索
        sleep(1)  # 等待列表刷新
        self.click(self.get_user_bind_button_locator(user))  # 点击该用户的绑定按钮
        self.input_text(self.USER_BIND_INPUT, user_id)  # 输入平台用户 ID
        self.click(self.USER_BIND_CONFIRM_BUTTON)  # 点击确认绑定
        result = self.is_displayed(self.BIND_SUCCESS_ALERT)  # 检查是否出现绑定成功提示
        log.info("绑定用户结果：" + str(result))
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def delete_user_by_code(self, code):
        """按工号搜索后进入编辑并删除该用户，返回是否出现删除成功提示。"""
        self.switch_to_iframe(self.USER_MANAGE_IFRAME)  # 切入用户管理 iframe
        self.input_text(self.SEARCH_CODE_INPUT, code)  # 按工号搜索
        sleep(1)  # 等待列表刷新
        self.click(self.get_edit_button_by_code_locator(code), timeout=15)  # 点击该用户的编辑按钮
        self.click(self.DELETE_USER_BUTTON, timeout=15)  # 点击删除用户
        self.click(self.DELETE_CONFIRM_BUTTON, timeout=15)  # 点击删除确认
        result = self.is_displayed(self.DELETE_SUCCESS_ALERT)  # 检查是否出现删除成功提示
        log.info(f"删除用户结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result
