# encoding: utf-8
# @File  : test_012_teaching.py
# @Author: 孔敬淳
# @Date  : 2025/01/23
# @Desc  : 课程教学测试用例，符合Selenium官方Page Object Model和pytest框架规范

import allure
import pytest

from common.report_add_img import add_img_2_report
from testcases.helpers.test_context_helper import TestContextHelper
from common.yaml_config import GetConf
from logs.log import log
from page.teacher_workbench.my_teaching_courses_page import MyTeachingCoursesPage
from page.teacher_workbench.course_workbench.course_workbench_page import CourseWorkbenchPage
from page.teacher_workbench.course_workbench.course_teaching.teaching_class_management_page import TeachingClassManagementPage


class TestTeaching:
    """课程教学测试类

    测试用例按照Selenium官方Page Object Model规范编写：
    1. 页面对象在测试用例中创建，driver通过pytest fixture注入
    2. 页面对象方法不包含driver参数
    3. 断言在测试用例中，不在页面对象中
    """

    @pytest.mark.run(order=300)
    @allure.story("测试课程教学")
    def test_001_create_teaching_class(self, driver):
        """
        测试创建教学班流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 专业管理员信息
        prof_user_info = GetConf().get_user_info("prof")
        # 专业管理员账号
        prof_cms_user_info = GetConf().get_user_info("prof_cms")
        # 课程信息
        course_info = GetConf().get_info("course")
        # 教学班信息
        teach_class_info = GetConf().get_info("teach_class")
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

        with allure.step("点击教学班管理菜单栏"):
            teaching_class_management_page = TeachingClassManagementPage(driver)
            result = teaching_class_management_page.click_left_menu("教学班管理")
            add_img_2_report(driver, "点击教学班管理菜单栏")
            assert result is True, "点击教学班管理菜单栏失败"

        with allure.step("创建教学班"):
            # 获取当前时间作为时间戳，用于生成唯一的教学班名称和编号
            class_name = f"{teach_class_info['教学班名称']}"
            class_code = f"{teach_class_info['教学班编号']}"
            result = teaching_class_management_page.create_teaching_class(
                class_name=class_name,
                class_code=class_code,
                open_course_time="2026-01-01 00:00:00",
                select_course_start_time="2026-01-01 00:00:00",
                select_course_end_time="2026-12-31 23:59:59",
                allow_student_self_select=True,
                allow_student_drop=True
            )
            add_img_2_report(driver, "创建教学班")
            assert result is True, f"创建教学班失败，教学班编号：{class_code}"
        # 设置主讲教师
        with allure.step("设置主讲教师"):
            result = teaching_class_management_page.set_lecturer(class_name_or_code=class_code, lecturer_name_or_code=prof_user_info["工号"])
            add_img_2_report(driver, "设置主讲教师")
            assert result is True, "设置主讲教师失败"
