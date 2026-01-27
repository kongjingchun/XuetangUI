# encoding: utf-8
# @File  : link_page.py
# @Author:
# @Date  :
# @Desc  : 链接页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from logs.log import log
from page.teacher_workbench.course_workbench.course_construction.course_resource.course_resource_page import (
    CourseResourcePage,
)


class LinkPage(CourseResourcePage):
    """链接页面类。

    继承 CourseResourcePage，提供链接页面的能力。
    对外只暴露“服务方法”（如新建链接），不暴露每个按钮/输入框的 click/input 封装。定位器集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 新建链接按钮
    NEW_LINK_BUTTON = (By.XPATH, "//button[contains(.,' 新建链接 ')]")
    # 链接地址输入框
    LINK_ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='请输入链接地址（含 http/https）']")
    # 确定按钮
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(.,'确定')]")
    # 新建链接成功提示框
    NEW_LINK_SUCCESS_MESSAGE = (By.XPATH, "//p[contains(.,'链接创建成功')]")

    # ==================== 动态定位器 getter ====================
    # （本页无动态定位器）

    # ==================== 服务方法（页面对外能力） ====================

    def new_link(self, link_address):
        """新建链接：输入链接地址并确定，返回是否出现链接创建成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.NEW_LINK_BUTTON)  # 点击新建链接
        self.input_text(self.LINK_ADDRESS_INPUT, link_address)  # 输入链接地址
        self.click(self.CONFIRM_BUTTON)  # 点击确定
        result = self.is_displayed(self.NEW_LINK_SUCCESS_MESSAGE)  # 检查是否出现链接创建成功提示
        log.info(f"新建链接结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result
