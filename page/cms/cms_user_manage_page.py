# encoding: utf-8
# @File  : CmsUserManagePage.py
# @Author: 孔敬淳
# @Date  : 2025/12/26/14:11
# @Desc  : CMS用户管理页面对象类，封装CMS用户管理相关的页面操作方法
from time import sleep
import requests
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from common.yaml_config import GetConf
from logs.log import log


class CmsUserManagePage(BasePage):
    """CMS用户管理页面类

    继承BasePage类，提供CMS用户管理页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化CMS用户管理页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)  # 调用父类初始化，设置self.driver

    def register_cms_user(self, user_info):
        """通过API注册CMS用户

        Args:
            user_info: 用户信息字典，包含username和password键
                      例如：{"username": "test_user", "password": "test_password"}

        Returns:
            bool: True表示注册成功，False表示注册失败
        """
        username = user_info["username"]
        password = user_info["password"]
        log.info("api注册cms用户:用户名：" + username + "密码：" + password)
        data = {
            "username": str(username),
            "password": str(password)
        }
        url = GetConf().get_url()
        res = requests.post(url + "api/auth/register", json=data)
        response_data = res.json()

        # 判断返回结果中是否包含"注册成功"
        if "注册成功" in str(response_data):
            log.info(f"用户 {username} 注册成功")
            return True
        else:
            error_msg = f"用户 {username} 注册失败，返回结果：{response_data}"
            log.error(error_msg)
            return False

    # ==================== 元素定位器（静态定位器）====================
    # 用户管理iframe
    CMS_USER_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2']")
    # 搜索输入框
    SEARCH_INPUT = (By.XPATH, "//input[contains(@placeholder,'用户名')]")
    # 搜索关键词输入框
    SEARCH_KEYWORD_INPUT = (By.XPATH, "//input[contains(@placeholder,'用户名 ｜ 昵称 ｜ 手机号')]")
    # 删除按钮
    DELETE_BUTTON = (By.XPATH, "//button[contains(.,'删除用户')]")
    # 删除确认按钮
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//div[contains(.,'警告')]//button[contains(.,'确定')]")
    # 删除成功提示框
    DELETE_SUCCESS_ALERT = (By.XPATH, "//p[contains(.,'删除成功')]")

    # ==================== 动态定位器方法（需要参数的定位器）====================
    # 按照Selenium官方规范，动态定位器应该定义为方法

    def get_user_id_locator(self, username):
        """获取用户ID的定位器

        Args:
            username: 用户名

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//span[text()='{username}']/ancestor::td/preceding-sibling::td//span")

    def get_edit_button_hover_locator(self, username):
        """获取编辑按钮悬停位置的定位器

        Args:
            username: 用户名

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//tr[contains(.,'{username}')]//i[contains(@class,'action-icon')]")

    def get_edit_button_locator(self, username):
        """获取编辑按钮的定位器

        Args:
            username: 用户名

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//tr[contains(.,'{username}')]//button")

    def input_search_value(self, value):
        """在搜索输入框中输入内容

        Args:
            value: 要搜索的值

        Returns:
            输入操作结果
        """
        log.info(f"在搜索框中输入内容查询：{value}，xpath定位为：{self.SEARCH_INPUT}")
        return self.input_text(self.SEARCH_INPUT, value)

    def input_search_keyword(self, keyword):
        """输入搜索关键词

        Args:
            keyword: 搜索关键词（用户名、昵称或手机号）

        Returns:
            输入操作结果
        """
        log.info(f"输入搜索关键词：{keyword}，xpath定位为：{self.SEARCH_KEYWORD_INPUT}")
        return self.input_text(self.SEARCH_KEYWORD_INPUT, keyword)

    def switch_2_cms_user_manage_iframe(self):
        """切换到CMS用户管理iframe

        Returns:
            切换iframe操作结果
        """
        log.info(f"进入用户管理iframe，定位器为：{self.CMS_USER_MANAGE_IFRAME[1]}")
        return self.switch_to_iframe(self.CMS_USER_MANAGE_IFRAME)

    def switch_out_cms_iframe(self):
        """退出CMS用户管理iframe

        Returns:
            退出iframe操作结果
        """
        log.info("退出iframe")
        return super().switch_out_iframe(to_root=True)

    def search_cms_user(self, username):
        """搜索CMS用户并获取用户ID

        Args:
            username: 用户名

        Returns:
            str: 用户ID，如果未找到则返回None
        """
        log.info(f"搜索用户:{username}")
        self.switch_to_iframe(self.CMS_USER_MANAGE_IFRAME)
        self.input_search_value(username)
        sleep(1)
        # 使用动态定位器方法
        user_id_locator = self.get_user_id_locator(username)
        log.info(f"获取用户ID，xpath定位为：{user_id_locator[1]}")
        user_id = self.get_text(user_id_locator)
        self.switch_out_iframe(to_root=True)
        return user_id

    def hover_edit_button(self, username):
        """鼠标悬停编辑按钮

        Args:
            username: 用户名

        Returns:
            悬停操作结果
        """
        locator = self.get_edit_button_hover_locator(username)
        log.info(f"鼠标悬停编辑按钮，xpath定位为：{locator[1]}")
        return self.hover(locator)

    def click_edit_button_by_username(self, username):
        """根据用户名点击编辑按钮

        Args:
            username: 用户名

        Returns:
            点击操作结果
        """
        locator = self.get_edit_button_locator(username)
        log.info(f"根据用户名'{username}'点击编辑按钮，xpath定位为：{locator[1]}")
        return self.click(locator, timeout=15)

    def click_delete_button(self):
        """点击删除用户按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击删除用户按钮，定位器为：{self.DELETE_BUTTON[1]}")
        return self.click(self.DELETE_BUTTON, timeout=15)

    def click_delete_confirm_button(self):
        """点击删除确认按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击删除确认按钮，定位器为：{self.DELETE_CONFIRM_BUTTON[1]}")
        return self.click(self.DELETE_CONFIRM_BUTTON, timeout=15)

    def is_delete_success_alert_display(self):
        """查看删除成功提示框是否出现

        Returns:
            bool: True表示删除成功提示框出现，False表示未出现
        """
        log.info(f"查看删除成功提示框是否出现，定位器为：{self.DELETE_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.DELETE_SUCCESS_ALERT)

    def delete_cms_user_by_username(self, username):
        """根据用户名删除CMS用户

        Args:
            username: 用户名

        Returns:
            bool: True表示删除成功，False表示删除失败
        """
        # 切换到iframe
        self.switch_2_cms_user_manage_iframe()
        # 输入搜索关键词
        self.input_search_keyword(username)
        # 鼠标悬停编辑按钮
        self.hover_edit_button(username)
        # 点击编辑按钮
        self.click_edit_button_by_username(username)
        # 点击删除按钮
        self.click_delete_button()
        # 点击删除确认按钮
        self.click_delete_confirm_button()
        # 断言删除成功提示框是否出现
        result = self.is_delete_success_alert_display()
        # 切出iframe
        self.switch_out_cms_iframe()
        log.info(f"删除CMS用户结果：{result}")
        return result


if __name__ == '__main__':
    # 示例用法（需要传入driver实例）
    # driver = ...  # WebDriver实例
    # page = CmsUserManagePage(driver)
    # res = page.register_cms_user({"username": "test_user", "password": "test_password"})
    pass
