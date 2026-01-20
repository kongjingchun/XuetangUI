# encoding: utf-8
# @File  : test_006_training_program.py
# @Author: 孔敬淳
# @Date  : 2025/12/31
# @Desc  : 培养方案管理测试用例，符合Selenium官方Page Object Model和pytest框架规范

import allure
import pytest

from common.report_add_img import add_img_2_report
from testcases.helpers.test_context_helper import TestContextHelper
from common.yaml_config import GetConf
from page.ai_major.training_program_revision_page import TrainingProgramRevisionPage
from page.ai_major.TrainingProgramManage.training_program_manage_page import TrainingProgramManagePage


class TestTrainingProgram:
    """培养方案管理测试类

    测试用例按照Selenium官方Page Object Model规范编写：
    1. 页面对象在测试用例中创建，driver通过pytest fixture注入
    2. 页面对象方法不包含driver参数
    3. 断言在测试用例中，不在页面对象中
    """
    @pytest.mark.run(order=160)
    @allure.story("创建培养方案")
    def test_001_create_training_program(self, driver):
        """
        测试创建培养方案流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 专业管理员账号
        prof_cms_user_info = GetConf().get_user_info("prof_cms")
        # 新建的培养方案信息
        training_program_info = GetConf().get_info("training_program")

        # 使用TestContextHelper封装公共操作
        helper = TestContextHelper(driver)

        with allure.step("登录并进入培养方案管理"):
            result = helper.setup_context(
                user_info=prof_cms_user_info,
                menu_name="培养方案管理"
            )
            assert result is True, "登录或导航失败"

        with allure.step("创建培养方案"):
            training_program_page = TrainingProgramManagePage(driver)
            result = training_program_page.create_training_program(training_program_info)
            add_img_2_report(driver, "创建培养方案")
            assert result is True, "创建培养方案失败"

    @pytest.mark.run(order=170)
    @allure.story("修订培养方案")
    def test_002_revision_training_program(self, driver):
        """
        测试修订培养方案流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 专业管理员账号
        prof_cms_user_info = GetConf().get_user_info("prof_cms")
        # 新建的培养方案信息
        training_program_info = GetConf().get_info("training_program")
        # 课程信息
        course_info = GetConf().get_info("course")

        # 使用TestContextHelper封装公共操作
        helper = TestContextHelper(driver)

        with allure.step("登录并进入培养方案管理"):
            result = helper.setup_context(
                user_info=prof_cms_user_info,
                menu_name="培养方案管理"
            )
            assert result is True, "登录或导航失败"

        with allure.step("根据方案名称点击修订按钮"):
            training_program_page = TrainingProgramManagePage(driver)
            result = training_program_page.click_revision_button_by_program_name(training_program_info['方案名称'])
            add_img_2_report(driver, "根据方案名称点击修订按钮")
            assert result is True, "根据方案名称点击修订按钮失败"

        with allure.step("更新专业信息"):
            revision_page = TrainingProgramRevisionPage(driver)
            result = revision_page.update_major_info(description="专业描述")
            add_img_2_report(driver, "更新专业信息")
            assert result is True, "更新专业信息失败"

        with allure.step("更新培养目标"):
            result1 = revision_page.update_training_objective("培养目标概述1", "培养目标描述1")
            assert result1 is True, "更新培养目标1失败"
            result2 = revision_page.update_training_objective("培养目标概述2", "培养目标描述2")
            assert result2 is True, "更新培养目标2失败"
            add_img_2_report(driver, "更新培养目标")

        with allure.step("更新毕业要求"):
            result1 = revision_page.update_graduation_requirement(
                description="毕业要求概述",
                indicator_index=1,
                indicator_name="指标点名称1",
                indicator_description="指标点描述1",
                decomposed_indicator_index=1,
                decomposed_indicator_name="分解指标点名称1.1",
                decomposed_indicator_description="分解指标点描述1.1")
            assert result1 is True, "更新毕业要求1失败"
            result2 = revision_page.update_graduation_requirement(
                description="毕业要求概述2",
                indicator_index=2,
                indicator_name="指标点名称2",
                indicator_description="指标点描述2",
                decomposed_indicator_index=1,
                decomposed_indicator_name="分解指标点名称2.1",
                decomposed_indicator_description="分解指标点描述2.1")
            assert result2 is True, "更新毕业要求2失败"
            add_img_2_report(driver, "更新毕业要求")

        with allure.step("更新目标支撑"):
            result1 = revision_page.update_target_support(index=1, level="高支撑")
            assert result1 is True, "更新目标支撑1失败"
            result2 = revision_page.update_target_support(index=1, level="中支撑")
            assert result2 is True, "更新目标支撑2失败"
            result3 = revision_page.update_target_support(index=1, level="低支撑")
            assert result3 is True, "更新目标支撑3失败"
            result4 = revision_page.update_target_support(index=1, level="中支撑")
            assert result4 is True, "更新目标支撑4失败"
            add_img_2_report(driver, "更新目标支撑")

        with allure.step("更新课程体系"):
            result = revision_page.update_course_system(course_name=course_info['课程名称'])
            add_img_2_report(driver, "更新课程体系")
            assert result is True, "更新课程体系失败"

        with allure.step("更新课程支撑"):
            result = revision_page.update_course_support(index=1, course_name=course_info['课程名称'], level="H")
            assert result is True, "更新课程支撑失败"
            result = revision_page.update_course_support(index=2, course_name=course_info['课程名称'], level="M")
            assert result is True, "更新课程支撑失败"
            add_img_2_report(driver, "更新课程支撑")
