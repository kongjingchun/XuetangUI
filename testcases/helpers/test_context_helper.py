# encoding: utf-8
# @File  : test_context_helper.py
# @Author: Auto
# @Date  : 2025/01/08
# @Desc  : 测试上下文辅助工具类，封装登录、切换身份、切换学校等公共操作

from common.report_add_img import add_img_2_report
from logs.log import log
from page.left_menu_page import LeftMenuPage
from page.top_menu_page import TopMenuPage
from page.login.login_page import LoginPage


class TestContextHelper:
    """测试上下文辅助工具类

    封装测试用例中常用的公共操作，如登录、切换角色、切换学校、导航菜单等
    简化测试用例代码，减少重复代码
    主要用于设置测试的上下文环境（用户登录、学校切换、角色切换、菜单导航）
    """

    def __init__(self, driver):
        """
        初始化测试上下文辅助类

        Args:
            driver: WebDriver实例
        """
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.top_menu = TopMenuPage(driver)
        self.left_menu = LeftMenuPage(driver)

    def _execute_operation(self, operation_func, description, take_screenshot=True):
        """
        执行操作的通用方法，统一处理日志、截图和异常

        Args:
            operation_func: 要执行的操作函数（无参数）
            description: 操作描述
            take_screenshot: 是否截图，默认True

        Returns:
            bool: 操作是否成功
        """
        log.info(description)
        try:
            result = operation_func()
            if not result:
                log.error(f"{description}失败")
                return False

            if take_screenshot:
                add_img_2_report(self.driver, description)

            log.info(f"{description}成功")
            return True
        except Exception as e:
            log.error(f"{description}失败，异常信息: {str(e)}")
            if take_screenshot:
                add_img_2_report(self.driver, f"{description}失败截图")
            return False

    def login(self, user_info, take_screenshot=True, step_description=None):
        """
        登录操作

        Args:
            user_info: 用户信息字典，包含username和password
            take_screenshot: 是否截图，默认True
            step_description: 步骤描述，用于截图和日志，如果为None则使用默认描述

        Returns:
            bool: 登录是否成功
        """
        username = user_info.get("username", "unknown")
        description = step_description or f"登录用户: {username}"

        return self._execute_operation(
            operation_func=lambda: self.login_page.user_login(user_info),
            description=description,
            take_screenshot=take_screenshot
        )

    def switch_school(self, school_name, take_screenshot=True, step_description=None):
        """
        切换学校

        Args:
            school_name: 学校名称
            take_screenshot: 是否截图，默认True
            step_description: 步骤描述，用于截图和日志，如果为None则使用默认描述

        Returns:
            bool: 切换是否成功
        """
        description = step_description or f"切换到学校: {school_name}"

        return self._execute_operation(
            operation_func=lambda: self.top_menu.switch_school(school_name),
            description=description,
            take_screenshot=take_screenshot
        )

    def switch_role(self, role_name, take_screenshot=True, step_description=None):
        """
        切换角色

        Args:
            role_name: 角色名称
            take_screenshot: 是否截图，默认True
            step_description: 步骤描述，用于截图和日志，如果为None则使用默认描述

        Returns:
            bool: 切换是否成功
        """
        description = step_description or f"切换到角色: {role_name}"

        return self._execute_operation(
            operation_func=lambda: self.top_menu.switch_role(role_name),
            description=description,
            take_screenshot=take_screenshot
        )

    def navigate_to_menu(self, menu_name, take_screenshot=True, step_description=None):
        """
        导航到指定菜单

        Args:
            menu_name: 菜单名称
            take_screenshot: 是否截图，默认True
            step_description: 步骤描述，用于截图和日志，如果为None则使用默认描述

        Returns:
            bool: 导航是否成功
        """
        description = step_description or f"导航到菜单: {menu_name}"

        return self._execute_operation(
            operation_func=lambda: self.left_menu.click_two_level_menu(menu_name),
            description=description,
            take_screenshot=take_screenshot
        )

    def setup_context(self, user_info, school_name=None, role_name=None, menu_name=None, take_screenshot=True):
        """
        设置完整的用户上下文（登录+切换学校+切换角色+导航菜单）

        Args:
            user_info: 用户信息
            school_name: 学校名称，可选
            role_name: 角色名称，可选
            menu_name: 菜单名称，可选
            take_screenshot: 是否截图，默认True

        Returns:
            bool: 所有操作是否成功
        """
        # 登录
        if not self.login(user_info, take_screenshot=take_screenshot):
            return False

        # 切换学校（如果提供）
        if school_name:
            if not self.switch_school(school_name, take_screenshot=take_screenshot):
                return False

        # 切换角色（如果提供）
        if role_name:
            if not self.switch_role(role_name, take_screenshot=take_screenshot):
                return False

        # 导航到菜单（如果提供）
        if menu_name:
            if not self.navigate_to_menu(menu_name, take_screenshot=take_screenshot):
                return False

        return True
