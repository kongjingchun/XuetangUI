# encoding: utf-8
# @File  : test_001_user.py
# @Author: 孔敬淳
# @Date  : 2025/12/24/21:27
# @Desc  : 用户管理测试用例，符合Selenium官方Page Object Model和pytest框架规范

import allure
import pytest

from common.report_add_img import add_img_2_report
from testcases.helpers.test_context_helper import TestContextHelper
from common.yaml_config import GetConf
from logs.log import log
from page.dean_manage.role_manage_page import RoleManagePage
from page.dean_manage.user_manage_page import UserManagePage
from page.cms.cms_user_manage_page import CmsUserManagePage


class TestUser:
    """用户管理测试类

    测试用例按照Selenium官方Page Object Model规范编写：
    1. 页面对象在测试用例中创建，driver通过pytest fixture注入
    2. 页面对象方法不包含driver参数
    3. 断言在测试用例中，不在页面对象中
    """

    @pytest.mark.skip_local  # 本地部署环境下跳过
    @pytest.mark.run(order=100)
    @allure.story("api注册cms账户")
    def test_001_register_cms_user(self, driver):
        """
        测试api注册cms账户流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 创建的CMS教务管理员信息
        dean_cms_user_info = GetConf().get_user_info("dean_cms")
        # 创建的CMS专业负责人信息
        prof_cms_user_info = GetConf().get_user_info("prof_cms")
        # 创建的CMS教师信息
        teacher_cms_user_info = GetConf().get_user_info("teacher_cms")

        with allure.step("api注册cms账户"):
            cms_user_page = CmsUserManagePage(driver)
            result = cms_user_page.register_cms_user(dean_cms_user_info)
            assert result is True, "api注册教务账户失败"
            result = cms_user_page.register_cms_user(prof_cms_user_info)
            assert result is True, "api注册专业负责人账户失败"
            result = cms_user_page.register_cms_user(teacher_cms_user_info)
            assert result is True, "api注册教师账户失败"

    @pytest.mark.run(order=110)
    @allure.story("创建用户")
    def test_002_create_user(self, driver):
        """
        测试创建用户流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 学校名称
        school_name = GetConf().get_school_name()
        # 初始管理员信息（账密）
        initial_admin = GetConf().get_user_info("initial_admin")
        # 教务管理员信息
        dean_user_info = GetConf().get_user_info("dean")
        # 专业负责人信息
        prof_user_info = GetConf().get_user_info("prof")

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

        with allure.step("创建用户"):
            user_page = UserManagePage(driver)
            result = user_page.create_user(role_name="创建教务管理员", user_info=dean_user_info)
            add_img_2_report(driver, "创建教务管理员")
            assert result is True, "创建教务管理员失败"
            result = user_page.create_user(role_name="创建专业负责人", user_info=prof_user_info)
            add_img_2_report(driver, "创建专业负责人")
            assert result is True, "创建专业负责人失败"

    @pytest.mark.skip_internet  # 网络部署环境下跳过
    @pytest.mark.run(order=115)
    @allure.story("初始化密码")
    def test_003_init_password(self, driver):
        """
        测试初始化密码流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # CMS教务管理员信息
        dean_cms_user_info = GetConf().get_user_info("dean_cms")
        # CMS专业负责人信息
        prof_cms_user_info = GetConf().get_user_info("prof_cms")
        # 教务管理员信息
        dean_user_info = GetConf().get_user_info("dean")
        # 专业负责人信息
        prof_user_info = GetConf().get_user_info("prof")

        # 使用TestContextHelper封装公共操作
        helper = TestContextHelper(driver)
        login_page = helper.login_page

        with allure.step("初始化教务管理员密码"):
            # 使用教务管理员工号作为账号，工号后6位作为密码
            dean_work_number = dean_user_info["工号"]
            dean_login_info = {
                "username": dean_work_number,
                "password": dean_work_number[-6:] if len(dean_work_number) >= 6 else dean_work_number
            }
            helper.login(dean_login_info, step_description="登录教务管理员（初始化密码）")
            result = login_page.init_password(dean_cms_user_info["password"])
            add_img_2_report(driver, "初始化教务管理员密码")
            assert result is True, "初始化教务管理员密码失败"

        with allure.step("初始化专业负责人密码"):
            # 使用专业负责人员工号作为账号，工号后6位作为密码
            prof_work_number = prof_user_info["工号"]
            prof_login_info = {
                "username": prof_work_number,
                "password": prof_work_number[-6:] if len(prof_work_number) >= 6 else prof_work_number
            }
            helper.login(prof_login_info, step_description="登录专业负责人（初始化密码）")
            result = login_page.init_password(prof_cms_user_info["password"])
            add_img_2_report(driver, "初始化专业负责人密码")
            assert result is True, "初始化专业负责人密码失败"

    @pytest.mark.skip_local  # 本地部署环境下跳过
    @pytest.mark.run(order=116)
    @allure.story("绑定用户")
    def test_003_bind_user(self, driver):
        """
        测试绑定用户流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 学校名称
        school_name = GetConf().get_school_name()
        # 初始管理员信息（账密）
        initial_admin = GetConf().get_user_info("initial_admin")
        # CMS教务管理员信息
        dean_cms_user_info = GetConf().get_user_info("dean_cms")
        # CMS专业负责人信息
        prof_cms_user_info = GetConf().get_user_info("prof_cms")
        # 教务管理员信息
        dean_user_info = GetConf().get_user_info("dean")
        # 专业负责人信息
        prof_user_info = GetConf().get_user_info("prof")

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
            dean_user_id = cms_user_page.search_cms_user(dean_cms_user_info["username"])
            add_img_2_report(driver, "查询教务管理员ID")
            assert dean_user_id is not None and dean_user_id != "", "查询教务管理员ID失败，未找到用户"
            log.info("教务管理员id为:" + dean_user_id)
            prof_user_id = cms_user_page.search_cms_user(prof_cms_user_info["username"])
            add_img_2_report(driver, "查询专业负责人ID")
            assert prof_user_id is not None and prof_user_id != "", "查询专业负责人ID失败，未找到用户"
            log.info("专业负责人id为:" + prof_user_id)

        with allure.step("切换学校并进入用户管理"):
            result = helper.switch_school(school_name)
            assert result is True, f"切换到{school_name}学校失败"
            result = helper.navigate_to_menu("用户管理")
            assert result is True, "点击用户管理失败"

        with allure.step("用户绑定"):
            user_page = UserManagePage(driver)
            result = user_page.bind_user(dean_user_info["工号"], dean_user_id)
            add_img_2_report(driver, "教务管理员绑定")
            assert result is True, "教务管理员绑定失败"
            result = user_page.bind_user(prof_user_info["工号"], prof_user_id)
            add_img_2_report(driver, "专业负责人绑定")
            assert result is True, "专业负责人绑定失败"

    @pytest.mark.run(order=117)
    @allure.story("分配角色")
    def test_004_assign_role(self, driver):
        """
        测试分配角色流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # CMS教务管理员信息
        dean_cms_user_info = GetConf().get_user_info("dean_cms")
        # 专业负责人信息
        prof_user_info = GetConf().get_user_info("prof")
        # 教务管理员信息
        dean_user_info = GetConf().get_user_info("dean")

        # 使用TestContextHelper封装公共操作
        helper = TestContextHelper(driver)

        with allure.step("登录并进入角色管理"):
            result = helper.setup_context(
                user_info=dean_cms_user_info,
                menu_name="角色管理"
            )
            assert result is True, "登录或导航失败"

        with allure.step("专业管理员分配教师角色"):
            role_page = RoleManagePage(driver)
            result = role_page.assign_role_to_user(role_name="教师", user_name=prof_user_info["姓名"])
            add_img_2_report(driver, "专业管理员分配教师角色")
            assert result is True, "专业管理员分配教师角色失败"
