# encoding: utf-8
# @File  : test_010_course_info.py
# @Author: 孔敬淳
# @Date  : 2025/12/31
# @Desc  : 课程信息测试用例，符合Selenium官方Page Object Model和pytest框架规范

import allure
import pytest

from common.report_add_img import add_img_2_report
from page.course_workbench.course_construction.course_outline.course_team_page import CourseTeamPage
from testcases.helpers.test_context_helper import TestContextHelper
from common.yaml_config import GetConf
from page.teacher_workbench.my_teaching_courses_page import MyTeachingCoursesPage
from page.course_workbench.course_construction.course_outline.course_info_page import CourseInfoPage
from page.course_workbench.course_construction.course_outline.course_objective_page import CourseObjectivePage


class TestCourseOutline:
    """课程大纲测试类

    测试用例按照Selenium官方Page Object Model规范编写：
    1. 页面对象在测试用例中创建，driver通过pytest fixture注入
    2. 页面对象方法不包含driver参数
    3. 断言在测试用例中，不在页面对象中
    """

    @pytest.mark.run(order=220)
    @allure.story("编辑课程信息")
    def test_001_edit_course_info(self, driver):
        """
        测试编辑课程信息流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 专业管理员账号
        prof_cms_user_info = GetConf().get_user_info("prof_cms")
        # 课程信息
        course_info = GetConf().get_info("course")
        # 使用TestContextHelper封装公共操作
        helper = TestContextHelper(driver)

        with allure.step("登录、切换教师身份、导航到我教的课"):
            result = helper.setup_context(user_info=prof_cms_user_info, role_name="教师", menu_name="我教的课")
            assert result is True, "登录、切换教师身份、导航到我教的课失败"

        with allure.step("根据课程名称点击课程卡片"):
            my_teaching_courses_page = MyTeachingCoursesPage(driver)
            result = my_teaching_courses_page.click_course(course_info['课程名称'])
            add_img_2_report(driver, "根据课程名称点击课程卡片")
            assert result is True, "根据课程名称点击课程卡片失败"

        with allure.step("点击课程大纲菜单栏"):
            course_info_page = CourseInfoPage(driver)
            result = course_info_page.click_left_menu("课程大纲")
            add_img_2_report(driver, "点击课程大纲菜单栏")
            assert result is True, "点击课程大纲菜单栏失败"

        with allure.step("点击课程信息菜单栏"):
            course_info_page = CourseInfoPage(driver)
            result = course_info_page.click_left_menu("课程信息")
            add_img_2_report(driver, "点击课程信息菜单栏")
            assert result is True, "点击课程信息菜单栏失败"

        with allure.step("编辑课程信息"):
            course_info_page = CourseInfoPage(driver)
            chinese_introduction = f"这是{course_info['课程名称']}的中文简介"
            english_introduction = f"This is the English introduction for {course_info['课程名称']}"
            result = course_info_page.edit_course_info("auto_course_name", chinese_introduction, english_introduction)
            add_img_2_report(driver, "编辑课程信息")
            assert result is True, "编辑课程信息失败"

    @pytest.mark.run(order=230)
    @allure.story("编辑课程目标")
    def test_002_edit_course_objective(self, driver):
        """
        测试编辑课程目标流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 专业管理员账号
        prof_cms_user_info = GetConf().get_user_info("prof_cms")

        # 课程信息
        course_info = GetConf().get_info("course")
        # 使用TestContextHelper封装公共操作
        helper = TestContextHelper(driver)

        with allure.step("登录、切换教师身份、导航到我教的课"):
            result = helper.setup_context(user_info=prof_cms_user_info, role_name="教师", menu_name="我教的课")
            assert result is True, "登录、切换教师身份、导航到我教的课失败"

        with allure.step("根据课程名称点击课程卡片"):
            my_teaching_courses_page = MyTeachingCoursesPage(driver)
            result = my_teaching_courses_page.click_course(course_info['课程名称'])
            add_img_2_report(driver, "根据课程名称点击课程卡片")
            assert result is True, "根据课程名称点击课程卡片失败"

        with allure.step("点击课程大纲菜单栏"):
            course_info_page = CourseInfoPage(driver)
            result = course_info_page.click_left_menu("课程大纲")
            add_img_2_report(driver, "点击课程大纲菜单栏")
            assert result is True, "点击课程大纲菜单栏失败"

        with allure.step("点击课程目标菜单栏"):
            course_objective_page = CourseObjectivePage(driver)
            result = course_objective_page.click_left_menu("课程目标")
            add_img_2_report(driver, "点击课程目标菜单栏")
            assert result is True, "点击课程目标菜单栏失败"

        with allure.step("编辑课程目标"):
            course_objective_page = CourseObjectivePage(driver)
            result = course_objective_page.edit_course_objective_description("auto_course_objective_description")
            add_img_2_report(driver, "编辑课程目标")
            assert result is True, "编辑课程目标失败"

        with allure.step("添加目标"):
            course_objective_page = CourseObjectivePage(driver)
            result = course_objective_page.add_objective("auto_objective_title", "auto_objective_tag")
            add_img_2_report(driver, "添加目标")
            assert result is True, "添加目标失败"

        with allure.step("关联毕业要求"):
            course_objective_page = CourseObjectivePage(driver)
            result = course_objective_page.associate_graduation_requirements("分解指标点名称1.1")
            add_img_2_report(driver, "关联毕业要求")
            assert result is True, "关联毕业要求失败"

    @pytest.mark.run(order=270)
    @allure.story("添加课程负责人")
    def test_003_add_course_leader(self, driver):
        """
        测试添加课程负责人流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 专业管理员账号
        prof_cms_user_info = GetConf().get_user_info("prof_cms")
        # 课程信息
        course_info = GetConf().get_info("course")
        # 教师信息
        teacher_cms_user_info = GetConf().get_user_info("teacher_cms")
        # 使用TestContextHelper封装公共操作
        helper = TestContextHelper(driver)

        with allure.step("登录、切换教师身份、导航到我教的课"):
            result = helper.setup_context(user_info=prof_cms_user_info, role_name="教师", menu_name="我教的课")
            assert result is True, "登录、切换教师身份、导航到我教的课失败"

        with allure.step("根据课程名称点击课程卡片"):
            my_teaching_courses_page = MyTeachingCoursesPage(driver)
            result = my_teaching_courses_page.click_course(course_info['课程名称'])
            add_img_2_report(driver, "根据课程名称点击课程卡片")
            assert result is True, "根据课程名称点击课程卡片失败"

        with allure.step("点击课程大纲菜单栏"):
            course_info_page = CourseInfoPage(driver)
            result = course_info_page.click_left_menu("课程大纲")
            add_img_2_report(driver, "点击课程大纲菜单栏")
            assert result is True, "点击课程大纲菜单栏失败"

        with allure.step("点击课程团队菜单栏"):
            course_team_page = CourseTeamPage(driver)
            result = course_team_page.click_left_menu("课程团队")
            add_img_2_report(driver, "点击课程团队菜单栏")
            assert result is True, "点击课程团队菜单栏失败"

        with allure.step("添加课程负责人"):
            course_team_page = CourseTeamPage(driver)
            result = course_team_page.add_course_leader(teacher_cms_user_info["username"])
            add_img_2_report(driver, "添加课程负责人")
            assert result is True, "添加课程负责人失败"
