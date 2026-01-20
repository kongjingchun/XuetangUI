# encoding: utf-8
# @File  : test_002_dept.py
# @Author: 孔敬淳
# @Date  : 2025/12/29/16:34
# @Desc  : 院系管理测试用例，符合Selenium官方Page Object Model和pytest框架规范

import allure
import pytest

from common.report_add_img import add_img_2_report
from testcases.helpers.test_context_helper import TestContextHelper
from common.yaml_config import GetConf
from page.department_manage.dept_list_manage_page import DeptListManagePage


class TestDept:
    """院系管理测试类

    测试用例按照Selenium官方Page Object Model规范编写：
    1. 页面对象在测试用例中创建，driver通过pytest fixture注入
    2. 页面对象方法不包含driver参数
    3. 断言在测试用例中，不在页面对象中
    """

    @pytest.mark.run(order=120)
    @allure.story("创建院系")
    def test_001_create_dept(self, driver):
        """
        测试创建院系流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 教务管理员账号
        dean_cms_user_info = GetConf().get_user_info("dean_cms")
        # 新建的院系信息
        dept_info = GetConf().get_info("department")

        # 使用TestContextHelper封装公共操作
        helper = TestContextHelper(driver)

        with allure.step("登录并进入院系列表管理"):
            result = helper.setup_context(
                user_info=dean_cms_user_info,
                menu_name="院系列表管理"
            )
            assert result is True, "登录或导航失败"

        with allure.step("创建院系"):
            dept_page = DeptListManagePage(driver)
            result = dept_page.create_dept(dept_info)
            add_img_2_report(driver, "创建院系")
            assert result is True, "创建院系失败"
