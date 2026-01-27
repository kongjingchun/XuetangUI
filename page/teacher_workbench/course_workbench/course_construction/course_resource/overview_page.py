# encoding: utf-8
# @File  : overview_page.py
# @Author:
# @Date  :
# @Desc  : 概览页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.get_text(...)。
from selenium.webdriver.common.by import By

from logs.log import log
from page.teacher_workbench.course_workbench.course_construction.course_resource.course_resource_page import (
    CourseResourcePage,
)


class OverviewPage(CourseResourcePage):
    """概览页面类。

    继承 CourseResourcePage，提供概览页面的能力。
    对外只暴露“服务方法”（如获取资源数量），不暴露每个元素的 getter 封装。定位器集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 资源数量展示
    RESOURCE_COUNT_DISPLAY = (By.XPATH, "//div[./div[text()='资源数']]/div[@class='stat-number']")

    # ==================== 动态定位器 getter ====================
    # （本页无动态定位器）

    # ==================== 服务方法（页面对外能力） ====================

    def get_resource_count(self):
        """在课程资源 iframe 内获取资源数量，返回展示文案。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        log.info(f"获取资源数量，定位器为：{self.RESOURCE_COUNT_DISPLAY[1]}")
        resource_count_str = self.get_text(self.RESOURCE_COUNT_DISPLAY)  # 获取资源数量文案
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return resource_count_str
