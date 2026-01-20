# encoding: utf-8
# @File  : test_003_major.py
# @Author: 孔敬淳
# @Date  : 2025/12/30/16:21
# @Desc  : 专业管理测试用例，符合Selenium官方Page Object Model和pytest框架规范

import allure
import pytest

from common.report_add_img import add_img_2_report
from testcases.helpers.test_context_helper import TestContextHelper
from common.yaml_config import GetConf
from page.ai_major.major_manage_page import MajorManagePage


class TestMajor:
    """专业管理测试类

    测试用例按照Selenium官方Page Object Model规范编写：
    1. 页面对象在测试用例中创建，driver通过pytest fixture注入
    2. 页面对象方法不包含driver参数
    3. 断言在测试用例中，不在页面对象中
    """

    @pytest.mark.run(order=130)
    @allure.story("创建专业")
    def test_001_create_major(self, driver):
        """
        测试创建专业流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 教务管理员账号
        dean_cms_user_info = GetConf().get_user_info("dean_cms")
        # 新建的专业信息
        major_info = GetConf().get_info("major")

        # 使用TestContextHelper封装公共操作
        helper = TestContextHelper(driver)

        with allure.step("登录并进入专业管理"):
            result = helper.setup_context(
                user_info=dean_cms_user_info,
                menu_name="专业管理"
            )
            assert result is True, "登录或导航失败"

        with allure.step("创建专业"):
            major_page = MajorManagePage(driver)
            result = major_page.create_major(major_info)
            add_img_2_report(driver, "创建专业")
            assert result is True, "创建专业失败"
