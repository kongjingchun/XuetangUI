# encoding: utf-8
# @File  : MyTeachingCoursesPage.py
# @Author:
# @Date  :
# @Desc  : 我教的课页面对象类，封装我教的课相关的页面操作方法
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class MyTeachingCoursesPage(BasePage):
    """我教的课页面类

    继承BasePage类，提供我教的课页面元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化我教的课页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
    # 我教的课iframe
    MY_TEACHING_COURSES_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-4003']")
    # 课程搜索输入框
    COURSE_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='搜索课程代码或名称']")

    # ==================== 动态定位器方法（需要参数的定位器）====================

    def get_course_card_locator(self, course_name):
        """获取根据课程名称定位课程卡片的定位器

        Args:
            course_name: 课程名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//span[text()='{course_name}']")

    # ==================== 页面操作方法 ====================

    def switch_2_my_teaching_courses_iframe(self):
        """切换到我教的课页面的iframe

        Returns:
            切换操作结果
        """
        log.info(f"切换到我教的课页面的iframe，定位器为：{self.MY_TEACHING_COURSES_IFRAME[1]}")
        return self.switch_to_iframe(self.MY_TEACHING_COURSES_IFRAME)

    def input_course_search(self, course_name):
        """输入课程搜索关键词

        Args:
            course_name: 搜索关键词（课程代码或课程名称）

        Returns:
            输入操作结果
        """
        log.info(f"输入课程搜索关键词：{course_name}，定位器为：{self.COURSE_SEARCH_INPUT[1]}")
        return self.input_text(self.COURSE_SEARCH_INPUT, course_name)

    def click_course_card_by_name(self, course_name, need_hover=False):
        """根据课程名称点击课程卡片

        Args:
            course_name: 课程名称
            need_hover: 是否需要在点击前先hover，默认False

        Returns:
            点击操作结果
        """
        locator = self.get_course_card_locator(course_name)
        log.info(f"根据课程名称'{course_name}'点击课程卡片，定位器为：{locator[1]}")
        return self.click(locator, timeout=15, need_hover=need_hover)

    def click_course(self, course_name):
        """点击课程

        Args:
            course_name: 课程名称

        Returns:
            bool: True表示点击成功
        """
        # 切换到我教的课iframe
        self.switch_2_my_teaching_courses_iframe()
        # 输入课程搜索关键词
        self.input_course_search(course_name)
        # 根据课程名称点击课程卡片
        self.click_course_card_by_name(course_name, need_hover=True)
        # 切出我教的课iframe
        self.switch_out_iframe()
        log.info(f"点击课程'{course_name}'成功")
        return True
