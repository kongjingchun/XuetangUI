# encoding: utf-8
# @File  : major_ai_model_page.py
# @Author:
# @Date  :
# @Desc  : 专业AI模型页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class MajorAIModelPage(BasePage):
    """专业AI模型页面类。

    对外只暴露“服务方法”（如按菜单名称点击进入子页等），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 专业AI模型主内容区域 iframe
    MAJOR_AI_MODEL_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2110']")

    # ==================== 动态定位器 getter ====================

    def get_menu_locator(self, menu_name):
        """菜单名称（如专业图谱概览、专业课程群图谱）→ 左侧菜单项定位器。"""
        return (By.XPATH, f"//span[text()='{menu_name}']/parent::li")

    # ==================== 服务方法（页面对外能力） ====================

    def click_menu_by_name(self, menu_name):
        """按菜单名称点击左侧菜单项进入对应子页，返回是否点击成功。"""
        self.switch_to_iframe(self.MAJOR_AI_MODEL_IFRAME)  # 切入专业AI模型 iframe
        locator = self.get_menu_locator(menu_name)  # 获取菜单项定位器
        log.info(f"点击菜单：{menu_name}，定位器为：{locator[1]}")
        result = self.click(locator)  # 点击菜单项
        self.switch_out_iframe()  # 切回默认上下文
        return result
