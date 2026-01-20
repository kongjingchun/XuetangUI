# encoding: utf-8
# @File  : LoginPage.py
# @Author: 孔敬淳
# @Date  : 2025/12/24/21:17
# @Desc  : 登录页面对象类，封装登录相关的页面操作方法
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class LoginPage(BasePage):
    """登录页面类

    继承BasePage类，提供登录页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化登录页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 动态定位器方法（需要参数的定位器）====================

    def get_login_input_locator(self, input_name):
        """获取登录输入框的定位器

        Args:
            input_name: 输入框名称(账户、密码)

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//input[@placeholder='请输入您的{input_name}']")

    def get_login_button_locator(self):
        """获取登录按钮的定位器

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//span[text()='登录']/parent::button")

    def get_new_password_input_locator(self):
        """获取新密码输入框的定位器

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//input[@placeholder='请输入新密码（至少6位）']")

    def get_confirm_password_input_locator(self):
        """获取确认密码输入框的定位器

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//input[@placeholder='请再次输入新密码']")

    def get_new_password_confirm_button_locator(self):
        """获取确认修改按钮的定位器

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//span[text()=' 确认修改 ']/parent::button")

    # ==================== 页面操作方法 ====================

    def login_input_value(self, input_name, input_value):
        """在登录页面的输入框中输入内容

        Args:
            input_name: 输入框名称（账户、密码）
            input_value: 要输入的值

        Returns:
            元素操作结果
        """
        locator = self.get_login_input_locator(input_name)
        log.info(f"在登录页面输入{input_name}：{input_value}，定位器为：{locator[1]}")
        return self.input_text(locator, input_value)

    def click_login_button(self):
        """点击登录按钮

        Returns:
            点击操作结果
        """
        locator = self.get_login_button_locator()
        log.info(f"点击登录按钮，定位器为：{locator[1]}")
        return self.click(locator)

    def user_login(self, user_info):
        """用户登录操作

        Args:
            user_info: 用户信息字典，包含username和password键

        Returns:
            登录操作结果
        """
        username = user_info["username"]
        password = user_info["password"]
        log.info(f"用户登录：{username}")
        self.navigate_to("login")
        self.login_input_value('账户', username)
        self.login_input_value('密码', password)
        return self.click_login_button()

    # ==============================初始化密码==============================

    def new_password_input_value(self, password_value):
        """在新密码输入框中输入内容

        Args:
            password_value: 要输入的新密码值

        Returns:
            元素操作结果
        """
        locator = self.get_new_password_input_locator()
        log.info(f"输入新密码：{password_value}，定位器为：{locator[1]}")
        return self.input_text(locator, password_value)

    def confirm_password_input_value(self, password_value):
        """在确认密码输入框中输入内容

        Args:
            password_value: 要输入的确认密码值

        Returns:
            元素操作结果
        """
        locator = self.get_confirm_password_input_locator()
        log.info(f"输入确认密码：{password_value}，定位器为：{locator[1]}")
        return self.input_text(locator, password_value)

    def click_new_password_confirm_button(self):
        """点击确认修改按钮

        Returns:
            点击操作结果
        """
        locator = self.get_new_password_confirm_button_locator()
        log.info(f"点击确认修改按钮，定位器为：{locator[1]}")
        return self.click(locator)

    def init_password(self, new_password):
        """初始化密码操作

        Args:
            new_password: 新密码

        Returns:
            初始化密码操作结果
        """
        log.info(f"初始化密码：{new_password}")
        self.new_password_input_value(new_password)
        self.confirm_password_input_value(new_password)
        return self.click_new_password_confirm_button()
