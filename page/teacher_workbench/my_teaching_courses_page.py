# encoding: utf-8
# @File  : my_teaching_courses_page.py
# @Author:
# @Date  :
# @Desc  : 我教的课页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class MyTeachingCoursesPage(BasePage):
    """我教的课页面类。

    对外只暴露“服务方法”（如按课程名称进入课程等），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 我教的课主内容区域 iframe
    MY_TEACHING_COURSES_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-4003']")
    # 课程搜索输入框
    COURSE_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='搜索课程代码或名称']")

    # ==================== 动态定位器 getter ====================

    def get_course_card_locator(self, course_name):
        """课程名称 → 课程卡片（入口）定位器。"""
        return (By.XPATH, f"//span[text()='{course_name}']")

    # ==================== 服务方法（页面对外能力） ====================

    def click_course(self, course_name):
        """按课程名称搜索并点击课程卡片进入课程，返回是否点击成功。"""
        self.switch_to_iframe(self.MY_TEACHING_COURSES_IFRAME)  # 切入我教的课 iframe
        self.input_text(self.COURSE_SEARCH_INPUT, course_name)  # 输入课程名称搜索
        locator = self.get_course_card_locator(course_name)  # 获取课程卡片定位器
        log.info(f"根据课程名称'{course_name}'点击课程卡片，定位器为：{locator[1]}")
        result = self.click(locator, timeout=15, need_hover=True)  # 悬停并点击课程卡片
        self.switch_out_iframe()  # 切回默认上下文
        log.info(f"点击课程'{course_name}'成功")
        return result
