# encoding: utf-8
# @File  : cms_user_manage_page.py
# @Author: 孔敬淳
# @Date  : 2025/12/26
# @Desc  : CMS 用户管理页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
#         含 API 注册接口 register_cms_user，以及 UI 搜索、删除服务。
import time

import requests
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from common.yaml_config import GetConf
from logs.log import log


class CmsUserManagePage(BasePage):
    """CMS 用户管理页面类。

    对外只暴露“服务方法”：register_cms_user（API 注册）、search_cms_user（查用户 ID）、delete_cms_user_by_username（按用户名删除）。
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # CMS 用户管理 iframe
    CMS_USER_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2']")
    # 按用户名搜索的输入框
    SEARCH_INPUT = (By.XPATH, "//input[contains(@placeholder,'用户名')]")
    # 按用户名/昵称/手机号搜索的输入框
    SEARCH_KEYWORD_INPUT = (By.XPATH, "//input[contains(@placeholder,'用户名 ｜ 昵称 ｜ 手机号')]")
    # 列表行内删除用户按钮
    DELETE_BUTTON = (By.XPATH, "//button[contains(.,'删除用户')]")
    # 删除二次确认弹窗的确定按钮
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//div[contains(.,'警告')]//button[contains(.,'确定')]")
    # 删除成功 toast 文案
    DELETE_SUCCESS_ALERT = (By.XPATH, "//p[contains(.,'删除成功')]")

    # ==================== 动态定位器 getter ====================

    def get_user_id_locator(self, username):
        """用户名 → 该用户行中用户 ID 所在单元格定位器。"""
        return (By.XPATH, f"//span[text()='{username}']/ancestor::td/preceding-sibling::td//span")

    def get_edit_button_hover_locator(self, username):
        """用户名 → 该用户行编辑区域悬停触发定位器。"""
        return (By.XPATH, f"//tr[contains(.,'{username}')]//i[contains(@class,'action-icon')]")

    def get_edit_button_locator(self, username):
        """用户名 → 该用户行编辑/操作按钮定位器。"""
        return (By.XPATH, f"//tr[contains(.,'{username}')]//button")

    # ==================== 服务方法（页面对外能力） ====================

    def register_cms_user(self, user_info):
        """通过 API 注册 CMS 用户，user_info 需含 username、password。返回是否注册成功。"""
        username = user_info["username"]
        password = user_info["password"]
        log.info("api注册cms用户:用户名：" + username + "密码：" + password)
        data = {"username": str(username), "password": str(password)}
        url = GetConf().get_url()
        res = requests.post(url + "api/auth/register", json=data)
        response_data = res.json()
        if "注册成功" in str(response_data):
            log.info(f"用户 {username} 注册成功")
            return True
        error_msg = f"用户 {username} 注册失败，返回结果：{response_data}"
        log.error(error_msg)
        return False

    def search_cms_user(self, username):
        """在 CMS 用户列表中按用户名搜索，返回对应用户 ID；未找到则返回 None。"""
        self.switch_to_iframe(self.CMS_USER_MANAGE_IFRAME)  # 切入 CMS 用户管理 iframe
        self.input_text(self.SEARCH_INPUT, username)  # 输入用户名搜索
        time.sleep(1)  # 等待列表刷新
        user_id = self.get_text(self.get_user_id_locator(username))  # 取对应用户 ID 文本
        self.switch_out_iframe(to_root=True)  # 切回主文档
        return user_id

    def delete_cms_user_by_username(self, username):
        """按用户名搜索后悬停编辑、点击删除并确认，返回是否出现删除成功提示。"""
        self.switch_to_iframe(self.CMS_USER_MANAGE_IFRAME)  # 切入 CMS 用户管理 iframe
        self.input_text(self.SEARCH_KEYWORD_INPUT, username)  # 按用户名/昵称/手机号搜索
        self.hover(self.get_edit_button_hover_locator(username))  # 悬停该行编辑区域
        self.click(self.get_edit_button_locator(username), timeout=15)  # 点击编辑/操作
        self.click(self.DELETE_BUTTON, timeout=15)  # 点击删除用户
        self.click(self.DELETE_CONFIRM_BUTTON, timeout=15)  # 点击确认删除
        result = self.is_displayed(self.DELETE_SUCCESS_ALERT)  # 检查是否出现删除成功提示
        log.info(f"删除CMS用户结果：{result}")
        self.switch_out_iframe(to_root=True)  # 切回主文档
        return result
