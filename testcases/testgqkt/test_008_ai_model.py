# encoding: utf-8
# @File  : test_008_ai_model.py
# @Author: 孔敬淳
# @Date  : 2025/12/31
# @Desc  : 专业AI模型测试用例，符合Selenium官方Page Object Model和pytest框架规范

import allure
import pytest

from common.report_add_img import add_img_2_report
from testcases.helpers.test_context_helper import TestContextHelper
from common.yaml_config import GetConf
from page.ai_major.MajorAIModel.major_ai_model_page import MajorAIModelPage
from page.ai_major.MajorAIModel.major_graph_model_page import MajorGraphModelPage


class TestAIModel:
    """专业AI模型测试类

    测试用例按照Selenium官方Page Object Model规范编写：
    1. 页面对象在测试用例中创建，driver通过pytest fixture注入
    2. 页面对象方法不包含driver参数
    3. 断言在测试用例中，不在页面对象中
    """

    @pytest.mark.run(order=190)
    @allure.story("专业图谱概览")
    def test_001_major_graph_overview(self, driver):
        """
        测试专业图谱概览流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 专业管理员账号
        prof_cms_user_info = GetConf().get_user_info("prof_cms")

        # 使用TestContextHelper封装公共操作
        helper = TestContextHelper(driver)

        with allure.step("登录并进入专业AI模型"):
            result = helper.setup_context(
                user_info=prof_cms_user_info,
                menu_name="专业AI模型"
            )
            assert result is True, "登录或导航失败"

        with allure.step("创建专业图谱概览"):
            major_graph_page = MajorGraphModelPage(driver)
            result = major_graph_page.create_major_graph_overview()
            add_img_2_report(driver, "创建专业图谱概览")
            assert result is True, "创建专业图谱概览失败"

    @pytest.mark.run(order=210)
    @allure.story("专业课程群图谱")
    def test_002_major_course_group_graph(self, driver):
        """
        测试专业课程群图谱流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 专业管理员账号
        prof_cms_user_info = GetConf().get_user_info("prof_cms")

        # 专业图谱信息
        major_graph_info = GetConf().get_info("main_graph")

        # 使用TestContextHelper封装公共操作
        helper = TestContextHelper(driver)

        with allure.step("登录并进入专业AI模型"):
            result = helper.setup_context(
                user_info=prof_cms_user_info,
                role_name="专业管理员",
                menu_name="专业AI模型"
            )
            assert result is True, "登录或导航失败"

        with allure.step("点击专业课程群图谱"):
            major_graph_page = MajorAIModelPage(driver)
            result = major_graph_page.click_menu_by_name("专业课程群图谱")
            add_img_2_report(driver, "点击专业课程群图谱")
            assert result is True, "点击专业课程群图谱失败"

        with allure.step("关联图谱"):
            major_graph_page = MajorGraphModelPage(driver)
            result = major_graph_page.associate_graph(major_graph_info['图谱名称'])
            add_img_2_report(driver, "关联图谱")
            assert result is True, "关联图谱失败"
