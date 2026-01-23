# encoding: utf-8
# @File  : MyClassesPage.py
# @Author:
# @Date  :
# @Desc  : 我的班级页面对象类，封装我的班级相关的页面操作方法
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class MyClassesPage(BasePage):
    """我的班级页面类

    继承BasePage类，提供我的班级页面元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化我的班级页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)
    # ==================== 元素定位器（静态定位器）====================
    # 我的班级iframe
    MY_CLASSES_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-4009']")

    # ==================== 动态定位器方法（需要参数的定位器）====================
    # 根据信息返回班级的card的定位器
    def get_class_card_locator(self, class_value):
        """根据信息返回班级的card的定位器

        Args:
            class_value (str): 班级名称或班级编号

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//div[@class='class-card-inner' and contains(.,'{class_value}')]")

    # ======================================= 页面操作方法 =======================================
    def click_class_card_by_value(self, class_value):
        """根据信息点击班级的card

        Args:
            class_value (str): 班级名称或班级编号

        Returns:
            点击操作结果
        """
        locator = self.get_class_card_locator(class_value)
        log.info(f"点击班级卡片，定位器为：{locator[1]}")
        return self.click(locator)

    def get_top_menu_button_locator(self, button_name):
        """根据名称返回上方菜单按钮的定位器

        Args:
            button_name (str): 上方菜单按钮名称（如：课程导读、教学内容、讨论区、公告、考核方案、成绩单、成员管理、数据统计、设置、知识图谱）

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//div[text()='{button_name}']")

    # ======================================= 课程导读 =======================================
    # 课程导读编辑按钮
    COURSE_INTRODUCTION_EDIT_BUTTON = (By.XPATH, "//button[contains(.,'编辑')]")
    # 课程导读保存按钮
    COURSE_INTRODUCTION_SAVE_BUTTON = (By.XPATH, "//button[contains(.,'保存')]")
    # ======================================= 教学内容 =======================================
