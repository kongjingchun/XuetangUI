# encoding: utf-8
# @File  : test_009_ai_vertical_model.py
# @Author: 孔敬淳
# @Date  : 2025/12/31
# @Desc  : AI垂直模型测试用例，符合Selenium官方Page Object Model和pytest框架规范

import allure
import pytest

from common.report_add_img import add_img_2_report
from page.course_workbench.ai_vertical_model.knowledge_graph_page import KnowledgeGraphPage
from testcases.helpers.test_context_helper import TestContextHelper
from common.yaml_config import GetConf
from page.teacher_workbench.my_teaching_courses_page import MyTeachingCoursesPage


class TestAiVerticalModel:
    """AI垂直模型测试类

    测试用例按照Selenium官方Page Object Model规范编写：
    1. 页面对象在测试用例中创建，driver通过pytest fixture注入
    2. 页面对象方法不包含driver参数
    3. 断言在测试用例中，不在页面对象中
    """

    @pytest.mark.run(order=200)
    @allure.story("添加知识图谱")
    def test_001_add_knowledge_graph(self, driver):
        """
        测试添加知识图谱

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 专业管理员账号
        prof_cms_user_info = GetConf().get_user_info("prof_cms")
        # 课程信息
        course_info = GetConf().get_info("course")
        # 主图谱信息
        main_graph_info = GetConf().get_info("main_graph")
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

        with allure.step("点击知识图谱菜单栏"):
            course_workbench_page = KnowledgeGraphPage(driver)
            course_workbench_page.click_left_menu("AI垂直模型")
            result = course_workbench_page.click_left_menu("知识图谱")
            add_img_2_report(driver, "点击知识图谱菜单栏")
            assert result is True, "点击知识图谱菜单栏失败"

        with allure.step("新建主图谱"):
            knowledge_graph_page = KnowledgeGraphPage(driver)
            result = knowledge_graph_page.create_main_graph(main_graph_info['图谱名称'], main_graph_info['图谱描述'], main_graph_info['图谱版本号'], title='第1级标题')
            add_img_2_report(driver, "新建主图谱")
            assert result is True, "新建主图谱失败"

        with allure.step("根据图谱名称点击编辑数据按钮"):
            knowledge_graph_page = KnowledgeGraphPage(driver)
            result = knowledge_graph_page.click_edit_data_button_by_name(main_graph_info['图谱名称'])
            add_img_2_report(driver, "根据图谱名称点击编辑数据按钮")
            assert result is True, "根据图谱名称点击编辑数据按钮失败"

        with allure.step("添加节点"):
            knowledge_graph_page = KnowledgeGraphPage(driver)
            result = knowledge_graph_page.add_node(main_graph_info['图谱名称'], main_graph_info['节点1'], main_graph_info['节点1描述'])
            add_img_2_report(driver, "添加节点")
            assert result is True, "添加节点失败"

        with allure.step("添加子级节点"):
            knowledge_graph_page = KnowledgeGraphPage(driver)
            result = knowledge_graph_page.add_sub_node_by_name(main_graph_info['节点1'], main_graph_info['节点1.1'], main_graph_info['节点1.1描述'])
            add_img_2_report(driver, "添加子级节点")
            assert result is True, "添加子级节点失败"
