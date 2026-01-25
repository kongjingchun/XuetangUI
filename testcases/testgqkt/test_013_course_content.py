# encoding: utf-8
# @File  : test_013_course_content.py
# @Author: 孔敬淳
# @Date  : 2026/01/25
# @Desc  : 课程内容测试用例，符合Selenium官方Page Object Model和pytest框架规范

import allure
import pytest

from common.report_add_img import add_img_2_report
from testcases.helpers.test_context_helper import TestContextHelper
from common.yaml_config import GetConf
from logs.log import log
from page.teacher_workbench.my_teaching_courses_page import MyTeachingCoursesPage
from page.teacher_workbench.course_workbench.course_construction.course_design.course_content_page import CourseContentPage


class TestCourseContent:
    """课程内容测试类

    测试用例按照Selenium官方Page Object Model规范编写：
    1. 页面对象在测试用例中创建，driver通过pytest fixture注入
    2. 页面对象方法不包含driver参数
    3. 断言在测试用例中，不在页面对象中
    """

    @pytest.mark.run(order=310)
    @allure.story("测试课程内容")
    def test_001_create_chapter(self, driver):
        """
        测试创建章节流程

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

        with allure.step("点击课程设计菜单栏"):
            course_content_page = CourseContentPage(driver)
            result = course_content_page.click_left_menu("课程设计")
            add_img_2_report(driver, "点击课程设计菜单栏")
            assert result is True, "点击课程设计菜单栏失败"

        with allure.step("点击课程内容菜单栏"):
            course_content_page = CourseContentPage(driver)
            result = course_content_page.click_left_menu("课程内容")
            add_img_2_report(driver, "点击课程内容菜单栏")
            assert result is True, "点击课程内容菜单栏失败"

        with allure.step("点击管理学习单元"):
            result = course_content_page.click_manage_learning_unit_button()
            add_img_2_report(driver, "点击管理学习单元")
            assert result is True, "点击管理学习单元失败"

        with allure.step("创建视频学习单元"):
            learning_unit_title = f"视频单元_{course_info['课程名称']}"
            learning_unit_content = f"这是{course_info['课程名称']}的视频学习单元内容"
            result = course_content_page.new_video_learning_unit(learning_unit_title, learning_unit_content)
            add_img_2_report(driver, "创建视频学习单元")
            assert result is True, "创建视频学习单元失败"
