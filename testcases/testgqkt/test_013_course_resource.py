# encoding: utf-8
# @File  : test_013_course_resource.py
# @Author: 孔敬淳
# @Date  : 2025/01/20
# @Desc  : 课程资源测试用例，符合Selenium官方Page Object Model和pytest框架规范

import allure
import pytest

from common.report_add_img import add_img_2_report
from common.tools import get_project_path, sep
from testcases.helpers.test_context_helper import TestContextHelper
from common.yaml_config import GetConf
from logs.log import log
from page.teacher_workbench.course_workbench.course_construction.course_resource.exam_page import ExamPage
from page.teacher_workbench.course_workbench.course_construction.course_resource.homework_page import HomeworkPage
from page.teacher_workbench.course_workbench.course_construction.course_resource.link_page import LinkPage
from page.teacher_workbench.course_workbench.course_construction.course_resource.overview_page import OverviewPage
from page.teacher_workbench.course_workbench.course_construction.course_resource.question_bank_page import QuestionBankPage
from page.teacher_workbench.my_teaching_courses_page import MyTeachingCoursesPage
from page.teacher_workbench.course_workbench.course_construction.course_resource.course_resource_page import CourseResourcePage


class TestCourseResource:
    """课程资源测试类

    测试用例按照Selenium官方Page Object Model规范编写：
    1. 页面对象在测试用例中创建，driver通过pytest fixture注入
    2. 页面对象方法不包含driver参数
    3. 断言在测试用例中，不在页面对象中
    """

    @pytest.mark.run(order=230)
    @allure.story("测试课程资源")
    def test_001_upload_course_resource_file(self, driver):
        """
        测试课程资源流程

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

        with allure.step("点击课程资源菜单栏"):
            course_resource_page = CourseResourcePage(driver)
            result = course_resource_page.click_left_menu("课程资源")
            add_img_2_report(driver, "点击课程资源菜单栏")
            assert result is True, "点击课程资源菜单栏失败"

        with allure.step("上传教材文件"):
            course_resource_page.click_left_menu("教材")
            # 获取测试文件路径（使用相对路径）
            file_path = get_project_path() + sep(['file', 'test_files', 'test.docx'], add_sep_before=True)
            result = course_resource_page.upload_file_with_iframe(file_path)
            add_img_2_report(driver, "上传教材文件")
            assert result is True, "上传教材文件失败"

        with allure.step("上传课件文件"):
            course_resource_page.click_left_menu("课件")
            # 获取测试文件路径（使用相对路径）
            file_path = get_project_path() + sep(['file', 'test_files', 'test.pptx'], add_sep_before=True)
            result = course_resource_page.upload_file_with_iframe(file_path)
            add_img_2_report(driver, "上传课件文件")
            assert result is True, "上传课件文件失败"

        with allure.step("上传视频文件"):
            course_resource_page.click_left_menu("视频")
            # 获取测试文件路径（使用相对路径）
            file_path = get_project_path() + sep(['file', 'test_files', 'test.mp4'], add_sep_before=True)
            result = course_resource_page.upload_file_with_iframe(file_path)
            add_img_2_report(driver, "上传视频文件")
            assert result is True, "上传视频文件失败"

        with allure.step("上传音频文件"):
            course_resource_page.click_left_menu("音频")
            # 获取测试文件路径（使用相对路径）
            file_path = get_project_path() + sep(['file', 'test_files', 'test.mp3'], add_sep_before=True)
            result = course_resource_page.upload_file_with_iframe(file_path)
            add_img_2_report(driver, "上传音频文件")
            assert result is True, "上传音频文件失败"

        with allure.step("上传论文文件"):
            course_resource_page.click_left_menu("论文")
            # 获取测试文件路径（使用相对路径）
            file_path = get_project_path() + sep(['file', 'test_files', 'test.doc'], add_sep_before=True)
            result = course_resource_page.upload_file_with_iframe(file_path)
            add_img_2_report(driver, "上传论文文件")
            assert result is True, "上传论文文件失败"

        with allure.step("上传案例文件"):
            course_resource_page.click_left_menu("案例")
            # 获取测试文件路径（使用相对路径）
            file_path = get_project_path() + sep(['file', 'test_files', 'test.doc'], add_sep_before=True)
            result = course_resource_page.upload_file_with_iframe(file_path)
            add_img_2_report(driver, "上传案例文件")
            assert result is True, "上传案例文件失败"

        with allure.step("上传图片文件"):
            course_resource_page.click_left_menu("图片")
            # 获取测试文件路径（使用相对路径）
            file_path = get_project_path() + sep(['file', 'test_files', 'test.jpg'], add_sep_before=True)
            result = course_resource_page.upload_file_with_iframe(file_path)
            add_img_2_report(driver, "上传图片文件")
            assert result is True, "上传图片文件失败"

        with allure.step("上传其他资料文件"):
            course_resource_page.click_left_menu("其他资料")
            # 获取测试文件路径（使用相对路径）
            file_path = get_project_path() + sep(['file', 'test_files', 'test.docx'], add_sep_before=True)
            result = course_resource_page.upload_file_with_iframe(file_path)
            add_img_2_report(driver, "上传其他资料文件")
            assert result is True, "上传其他资料文件失败"

        with allure.step("新建链接"):
            link_page = LinkPage(driver)
            link_page.click_left_menu("链接")
            result = link_page.new_link("https://www.baidu.com")
            add_img_2_report(driver, "新建链接")
            assert result is True, "新建链接失败"

        with allure.step("题库：新建简答题"):
            question_bank_page = QuestionBankPage(driver)
            question_bank_page.click_left_menu("题库")
            # 获取主图谱信息
            main_graph_info = GetConf().get_info("main_graph")
            result = question_bank_page.new_question("简答题", "题目内容", "参考答案", "题目解析", main_graph_info['节点1'])
            add_img_2_report(driver, "新建简答题")
            assert result is True, "新建简答题失败"

        with allure.step("题库：导入题库"):
            # 获取测试文件路径（使用相对路径）
            file_path = get_project_path() + sep(['file', 'teacher_workbench', 'question.xlsx'], add_sep_before=True)
            result = question_bank_page.import_question_bank(file_path)
            add_img_2_report(driver, "导入题库")
            assert result is True, "导入题库失败"

        with allure.step("新建作业"):
            homework_page = HomeworkPage(driver)
            homework_page.click_left_menu("作业")
            result = homework_page.new_homework("作业标题")
            add_img_2_report(driver, "新建作业")
            assert result is True, "新建作业失败"

        with allure.step("试卷：新建试卷"):
            exam_page = ExamPage(driver)
            exam_page.click_left_menu("试卷")
            result = exam_page.new_exam("试卷标题")
            add_img_2_report(driver, "新建试卷")
            assert result is True, "新建试卷失败"

        with allure.step("概览：获取资源数量"):
            overview_page = OverviewPage(driver)
            overview_page.click_left_menu("概览")
            resource_count_str = overview_page.get_resource_count()
            add_img_2_report(driver, "获取资源数量")
            # 将字符串转换为整数并判断是否大于1，如果不大于1，说明子资源数异常
            resource_count = int(resource_count_str)
            assert resource_count > 1, f"子资源数异常，资源数量为：{resource_count}，应大于1"
