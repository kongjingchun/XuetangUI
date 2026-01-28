# encoding: utf-8
# @File  : test_011_create_teacher.py
# @Author: 孔敬淳
# @Date  : 2025/12/24
# @Desc  : 创建/绑定/初始化教师相关测试用例，符合Selenium官方Page Object Model和pytest框架规范

import allure
import pytest

from common.report_add_img import add_img_2_report
from testcases.helpers.test_context_helper import TestContextHelper
from common.yaml_config import GetConf
from logs.log import log
from page.dean_manage.user_manage_page import UserManagePage
from page.cms.cms_user_manage_page import CmsUserManagePage


class TestCreateTeacher:
    """创建教师相关测试类

    测试用例按照Selenium官方Page Object Model规范编写：
    1. 页面对象在测试用例中创建，driver通过pytest fixture注入
    2. 页面对象方法不包含driver参数
    3. 断言在测试用例中，不在页面对象中
    """

    @pytest.mark.run(order=215)
    @allure.story("创建教师")
    def test_001_create_teacher(self, driver):
        """
        测试创建教师流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 学校名称
        school_name = GetConf().get_school_name()
        # 初始管理员信息（账密）
        initial_admin = GetConf().get_user_info("initial_admin")
        # 创建的教师信息
        teacher_user_info = GetConf().get_user_info("teacher")
        # 使用TestContextHelper封装公共操作
        helper = TestContextHelper(driver)

        with allure.step("登录、切换学校、切换角色并进入用户管理"):
            result = helper.setup_context(
                user_info=initial_admin,
                school_name=school_name,
                role_name="机构管理员",
                menu_name="用户管理"
            )
            assert result is True, "设置用户上下文失败"

        with allure.step("创建教师"):
            user_page = UserManagePage(driver)
            result = user_page.create_user(role_name="创建教师", user_info=teacher_user_info)
            add_img_2_report(driver, "创建教师")
            assert result is True, "创建教师失败"

    @pytest.mark.skip_local  # 本地部署环境下跳过
    @pytest.mark.run(order=216)
    @allure.story("绑定教师")
    def test_002_bind_teacher(self, driver):
        """
        测试绑定教师流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 学校名称
        school_name = GetConf().get_school_name()
        # 教师信息
        teacher_user_info = GetConf().get_user_info("teacher")
        # CMS教师信息
        teacher_cms_user_info = GetConf().get_user_info("teacher_cms")

        # 初始管理员信息（账密）
        initial_admin = GetConf().get_user_info("initial_admin")

        # 使用TestContextHelper封装公共操作
        helper = TestContextHelper(driver)

        with allure.step("登录并切换到CMS管理系统"):
            result = helper.setup_context(
                user_info=initial_admin,
                school_name="CMS管理系统",
                menu_name="全部用户管理"
            )
            assert result is True, "设置用户上下文失败"

        with allure.step("查询cms用户ID"):
            cms_user_page = CmsUserManagePage(driver)
            teacher_user_id = cms_user_page.search_cms_user(teacher_cms_user_info["username"])
            add_img_2_report(driver, "查询教师ID")
            assert teacher_user_id is not None and teacher_user_id != "", "查询教师ID失败，未找到用户"
            log.info("教师id为:" + teacher_user_id)

        with allure.step("切换学校并进入用户管理"):
            result = helper.switch_school(school_name)
            assert result is True, f"切换到{school_name}学校失败"
            result = helper.navigate_to_menu("用户管理")
            assert result is True, "点击用户管理失败"

        with allure.step("用户绑定"):
            user_page = UserManagePage(driver)
            result = user_page.bind_user(teacher_user_info["工号"], teacher_user_id)
            add_img_2_report(driver, "教师绑定")
            assert result is True, "教师绑定失败"

    @pytest.mark.skip_internet  # 网络部署环境下跳过
    @pytest.mark.run(order=217)
    @allure.story("初始化教师密码")
    def test_003_init_teacher_password(self, driver):
        """
        测试初始化密码流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 教师信息
        teacher_login_info = GetConf().get_user_info("teacher")
        # CMS教师信息
        teacher_cms_user_info = GetConf().get_user_info("teacher_cms")

        # 使用TestContextHelper封装公共操作
        helper = TestContextHelper(driver)
        login_page = helper.login_page

        with allure.step("初始化教师密码"):
            # 使用教务管理员工号作为账号，工号后6位作为密码
            teacher_work_number = teacher_cms_user_info["工号"]
            helper.login(teacher_login_info, step_description="登录教师（初始化密码）")
            result = login_page.init_password(teacher_cms_user_info["password"])
            add_img_2_report(driver, "初始化教师密码")
            assert result is True, "初始化教师密码失败"
