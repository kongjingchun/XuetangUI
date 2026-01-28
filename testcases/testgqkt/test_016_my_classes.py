# encoding: utf-8
# @File  : test_016_my_classes.py
# @Author: 孔敬淳
# @Date  : 2026/01/27
# @Desc  : 我的班级测试用例，符合Selenium官方Page Object Model和pytest框架规范

import allure
import pytest

from common.report_add_img import add_img_2_report
from testcases.helpers.test_context_helper import TestContextHelper
from common.yaml_config import GetConf
from logs.log import log
from page.teacher_workbench.my_classes_page import MyClassesPage


class TestMyClasses:
    """我的班级测试类

    测试用例按照Selenium官方Page Object Model规范编写：
    1. 页面对象在测试用例中创建，driver通过pytest fixture注入
    2. 页面对象方法不包含driver参数
    3. 断言在测试用例中，不在页面对象中
    """

    @pytest.mark.run(order=260)
    @allure.story("测试我的班级")
    def test_001_my_classes_operations(self, driver):
        """
        测试我的班级相关操作流程

        Args:
            driver: WebDriver实例（通过pytest fixture注入）

        Returns:
            None
        """
        # 专业管理员账号
        prof_cms_user_info = GetConf().get_user_info("prof_cms")
        # 教学班信息
        teach_class_info = GetConf().get_info("teach_class")
        # 使用TestContextHelper封装公共操作
        helper = TestContextHelper(driver)

        with allure.step("登录、切换教师身份、导航到我的班级"):
            result = helper.setup_context(user_info=prof_cms_user_info, role_name="教师", menu_name="我的班级")
            assert result is True, "登录、切换教师身份、导航到我的班级失败"

        with allure.step("根据教学班名称点击班级卡片"):
            my_classes_page = MyClassesPage(driver)
            result = my_classes_page.click_class_card_by_value(teach_class_info['教学班名称'])
            add_img_2_report(driver, "根据教学班名称点击班级卡片")
            assert result is True, "根据教学班名称点击班级卡片失败"

        with allure.step("编辑课程导读"):
            result = my_classes_page.edit_course_introduction()
            add_img_2_report(driver, "编辑课程导读")
            assert result is True, "编辑课程导读失败"

        with allure.step("点击教学内容菜单栏"):
            result = my_classes_page.click_top_menu_button_by_name("教学内容")
            add_img_2_report(driver, "点击教学内容菜单栏")
            assert result is True, "点击教学内容菜单栏失败"

        with allure.step("引用课程内容"):
            result = my_classes_page.reference_course_content()
            add_img_2_report(driver, "引用课程内容")
            assert result is True, "引用课程内容失败"

        with allure.step("创建章"):
            chapter_title = f"章节_{teach_class_info['教学班名称']}"
            result = my_classes_page.create_chapter(chapter_title)
            add_img_2_report(driver, "创建章")
            assert result is True, "创建章失败"

        with allure.step("在章下创建节"):
            sub_chapter_title = f"子章节_{teach_class_info['教学班名称']}"
            result = my_classes_page.create_section_in_chapter(chapter_title, sub_chapter_title)
            add_img_2_report(driver, "在章下创建节")
            assert result is True, "在章下创建节失败"

        with allure.step("给章节添加学习单元"):
            result = my_classes_page.add_learning_unit(sub_chapter_title, chapter_title)
            add_img_2_report(driver, "给章节添加学习单元")
            assert result is True, "给章节添加学习单元失败"

        with allure.step("给章节添加知识图谱"):
            result = my_classes_page.add_knowledge_graph(sub_chapter_title)
            add_img_2_report(driver, "给章节添加知识图谱")
            assert result is True, "给章节添加知识图谱失败"
