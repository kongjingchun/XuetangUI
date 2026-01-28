# encoding: utf-8
# @File  : test_015_course_content.py
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

    @pytest.mark.run(order=250)
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
            result = course_content_page.new_video_learning_unit(learning_unit_title, learning_unit_content, count_grade=True)
            add_img_2_report(driver, "创建视频学习单元")
            assert result is True, "创建视频学习单元失败"

        with allure.step("创建资料学习单元"):
            learning_unit_title = f"资料单元_{course_info['课程名称']}"
            learning_unit_content = f"这是{course_info['课程名称']}的资料学习单元内容"
            result = course_content_page.new_material_learning_unit(learning_unit_title, learning_unit_content, count_grade=True)
            add_img_2_report(driver, "创建资料学习单元")
            assert result is True, "创建资料学习单元失败"

        with allure.step("创建课件学习单元"):
            learning_unit_title = f"课件单元_{course_info['课程名称']}"
            learning_unit_content = f"这是{course_info['课程名称']}的课件学习单元内容"
            result = course_content_page.new_ppt_learning_unit(learning_unit_title, learning_unit_content, count_grade=True)
            add_img_2_report(driver, "创建课件学习单元")
            assert result is True, "创建课件学习单元失败"

        with allure.step("创建讨论学习单元"):
            learning_unit_title = f"讨论单元_{course_info['课程名称']}"
            learning_unit_content = f"这是{course_info['课程名称']}的讨论学习单元内容"
            result = course_content_page.new_discussion_learning_unit(learning_unit_title, learning_unit_content, count_grade=True, anonymous_comment=True)
            add_img_2_report(driver, "创建讨论学习单元")
            assert result is True, "创建讨论学习单元失败"

        with allure.step("创建作业学习单元"):
            learning_unit_title = f"作业单元_{course_info['课程名称']}"
            learning_unit_content = f"这是{course_info['课程名称']}的作业学习单元内容"
            result = course_content_page.new_homework_learning_unit(learning_unit_title, learning_unit_content, count_grade=True)
            add_img_2_report(driver, "创建作业学习单元")
            assert result is True, "创建作业学习单元失败"

        with allure.step("创建考试学习单元"):
            learning_unit_title = f"考试单元_{course_info['课程名称']}"
            learning_unit_content = f"这是{course_info['课程名称']}的考试学习单元内容"
            result = course_content_page.new_exam_learning_unit(learning_unit_title, learning_unit_content, count_grade=True)
            add_img_2_report(driver, "创建考试学习单元")
            assert result is True, "创建考试学习单元失败"

        with allure.step("创建链接学习单元"):
            learning_unit_title = f"链接单元_{course_info['课程名称']}"
            learning_unit_content = f"这是{course_info['课程名称']}的链接学习单元内容"
            result = course_content_page.new_link_learning_unit(learning_unit_title, learning_unit_content, count_grade=True)
            add_img_2_report(driver, "创建链接学习单元")
            assert result is True, "创建链接学习单元失败"

        with allure.step("创建音频学习单元"):
            learning_unit_title = f"音频单元_{course_info['课程名称']}"
            learning_unit_content = f"这是{course_info['课程名称']}的音频学习单元内容"
            result = course_content_page.new_audio_learning_unit(learning_unit_title, learning_unit_content, count_grade=True)
            add_img_2_report(driver, "创建音频学习单元")
            assert result is True, "创建音频学习单元失败"

        with allure.step("创建课堂学习单元"):
            learning_unit_title = f"课堂单元_{course_info['课程名称']}"
            learning_unit_content = f"这是{course_info['课程名称']}的课堂学习单元内容"
            result = course_content_page.new_classroom_learning_unit(learning_unit_title, learning_unit_content)
            add_img_2_report(driver, "创建课堂学习单元")
            assert result is True, "创建课堂学习单元失败"

        with allure.step("退出管理学习单元"):
            result = course_content_page.click_exit_manage_learning_unit_button()
            add_img_2_report(driver, "退出管理学习单元")
            assert result is True, "退出管理学习单元失败"

        with allure.step("创建章节"):
            chapter_title = f"章节_{course_info['课程名称']}"
            result = course_content_page.new_chapter(chapter_title)
            add_img_2_report(driver, "创建章节")
            assert result is True, "创建章节失败"

        with allure.step("在章节中新增子章节"):
            sub_chapter_title = f"子章节_{course_info['课程名称']}"
            result = course_content_page.new_sub_chapter_in_chapter(chapter_title, sub_chapter_title)
            add_img_2_report(driver, "在章节中新增子章节")
            assert result is True, "在章节中新增子章节失败"

        with allure.step("给章节批量添加学习单元"):
            result = course_content_page.add_learning_unit_by_chapter(sub_chapter_title)
            add_img_2_report(driver, "给章节批量添加学习单元")
            assert result is True, "给章节批量添加学习单元失败"

        with allure.step("从默认版本复制新版本"):
            new_version_name = f"新版本_{course_info['课程名称']}"
            result = course_content_page.copy_new_version_from_default(new_version_name)
            add_img_2_report(driver, "从默认版本复制新版本")
            assert result is True, "从默认版本复制新版本失败"

        with allure.step("根据章节名称关联第一个知识点"):
            result = course_content_page.relate_first_knowledge_by_chapter(chapter_title)
            add_img_2_report(driver, "根据章节名称关联第一个知识点")
            assert result is True, "根据章节名称关联第一个知识点失败"
