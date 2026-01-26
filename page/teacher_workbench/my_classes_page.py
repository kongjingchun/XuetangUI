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
    # 保存成功提示框
    SAVE_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='保存成功']")
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

    def get_top_menu_button_locator(self, button_name):
        """根据名称返回上方菜单按钮的定位器

        Args:
            button_name (str): 上方菜单按钮名称（如：课程导读、教学内容、讨论区、公告、考核方案、成绩单、成员管理、数据统计、设置、知识图谱）

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//div[text()='{button_name}']")

    # ======================================= 页面操作方法 =======================================
    def click_class_card_by_value(self, class_value):
        """根据信息点击班级的card

        Args:
            class_value (str): 班级名称或班级编号

        Returns:
            点击操作结果
        """
        # 切换到我的班级iframe
        self.switch_to_iframe(self.MY_CLASSES_IFRAME)   
        locator = self.get_class_card_locator(class_value)
        log.info(f"点击班级卡片，定位器为：{locator[1]}")
        result = self.click(locator)
        # 切出我的班级iframe
        self.switch_out_iframe()
        return result

    def click_top_menu_button_by_name(self, button_name):
        """根据名称点击上方菜单按钮

        Args:
            button_name (str): 上方菜单按钮名称（如：课程导读、教学内容、讨论区、公告、考核方案、成绩单、成员管理、数据统计、设置、知识图谱）

        Returns:
            点击操作结果
        """
        # 切换到我的班级iframe
        self.switch_to_iframe(self.MY_CLASSES_IFRAME)   
        locator = self.get_top_menu_button_locator(button_name)
        log.info(f"点击上方菜单按钮，定位器为：{locator[1]}")
        result = self.click(locator)
        # 切出我的班级iframe
        self.switch_out_iframe()
        return result

    def is_save_success_message_displayed(self):
        """查看保存成功提示框是否出现"""
        log.info(f"查看保存成功提示框是否出现，定位器为：{self.SAVE_SUCCESS_MESSAGE[1]}")
        return self.is_displayed(self.SAVE_SUCCESS_MESSAGE)
    # ======================================= 课程导读 =======================================
    # 课程导读编辑按钮
    COURSE_INTRODUCTION_EDIT_BUTTON = (By.XPATH, "//button[contains(.,'编辑')]")
    # 课程导读保存按钮
    COURSE_INTRODUCTION_SAVE_BUTTON = (By.XPATH, "//button[contains(.,'保存')]")

    def click_course_introduction_edit_button(self):
        """点击课程导读编辑按钮"""
        log.info(f"点击课程导读编辑按钮，定位器为：{self.COURSE_INTRODUCTION_EDIT_BUTTON[1]}")
        return self.click(self.COURSE_INTRODUCTION_EDIT_BUTTON)

    def click_course_introduction_save_button(self):
        """点击课程导读保存按钮"""
        log.info(f"点击课程导读保存按钮，定位器为：{self.COURSE_INTRODUCTION_SAVE_BUTTON[1]}")
        return self.click(self.COURSE_INTRODUCTION_SAVE_BUTTON)

    def edit_course_introduction(self):
        """编辑课程导读"""
        # 切换到我的班级iframe
        self.switch_to_iframe(self.MY_CLASSES_IFRAME)
        # 点击课程导读编辑按钮
        self.click_course_introduction_edit_button()
        # 点击课程导读保存按钮
        self.click_course_introduction_save_button()
        # 断言保存成功提示框是否出现
        result = self.is_save_success_message_displayed()
        log.info(f"编辑课程导读结果：{result}")
        # 切出我的班级iframe
        self.switch_out_iframe()
        return result
    # ======================================= 教学内容 =======================================
    # 引用课程内容按钮
    REFERENCE_COURSE_CONTENT_BUTTON = (By.XPATH, "//button[contains(.,'引用课程内容')]")
    # 全选未引用的版本复选框
    ALL_SELECT_UNREFERENCED_VERSION_CHECKBOX = (By.XPATH, "//label[contains(.,'全选未引用的版本')]/span[1]")
    # 确定引用按钮
    CONFIRM_REFERENCE_BUTTON = (By.XPATH, "//button[contains(.,'确定引用')]")
    # 成功引用提示框
    SUCCESS_REFERENCE_MESSAGE = (By.XPATH, "//p[contains(.,'成功引用')]")
    # 添加章按钮
    ADD_CHAPTER_BUTTON = (By.XPATH, "//button[contains(.,'添加章')]")
    # 章节标题输入框
    CHAPTER_TITLE_INPUT = (By.XPATH, "//input[@placeholder='请输入章节标题']")
    # 章节确认创建按钮
    CONFIRM_ADD_CHAPTER_BUTTON = (By.XPATH, "//div[@aria-label='创建章节']//button[contains(.,'创建')]")
    # 创建章节成功提示框
    SUCCESS_CREATE_CHAPTER_MESSAGE = (By.XPATH, "//p[contains(.,'创建') and contains(.,'成功')]")
    # 添加节下拉定位器
    ADD_SECTION_DROPDOWN = (By.XPATH, "//div[@aria-hidden='false']//li[contains(.,'添加节')]")
    # 子章节标题输入框
    SUB_CHAPTER_TITLE_INPUT = (By.XPATH, "//input[@placeholder='请输入子章节标题']")
    # 添加节创建按钮
    CONFIRM_ADD_SECTION_BUTTON = (By.XPATH, "//div[@aria-label='添加节']//button[contains(.,'创建')]")


    def get_chapter_more_dropdown_by_name(self, chapter_name):
        """
        根据章节名称返回对应章节的多功能下拉框定位器

        Args:
            chapter_name (str): 章节名称

        Returns:
            tuple: 用于Selenium的下拉框定位器
        """
        return (By.XPATH, f"//div[./div/span[text()='{chapter_name}']]/div[2]/div[1]/button")
    # ====================操作方法=============================
    def click_reference_course_content_button(self):
        """点击引用课程内容按钮"""
        log.info(f"点击引用课程内容按钮，定位器为：{self.REFERENCE_COURSE_CONTENT_BUTTON[1]}")
        return self.click(self.REFERENCE_COURSE_CONTENT_BUTTON)

    def click_all_select_unreferenced_version_checkbox(self):
        """点击全选未引用的版本复选框"""
        log.info(f"点击全选未引用的版本复选框，定位器为：{self.ALL_SELECT_UNREFERENCED_VERSION_CHECKBOX[1]}")
        return self.click(self.ALL_SELECT_UNREFERENCED_VERSION_CHECKBOX)

    def click_confirm_reference_button(self):
        """点击确定引用按钮"""
        log.info(f"点击确定引用按钮，定位器为：{self.CONFIRM_REFERENCE_BUTTON[1]}")
        return self.click(self.CONFIRM_REFERENCE_BUTTON)

    def is_success_reference_message_displayed(self):
        """查看成功引用提示框是否出现"""
        log.info(f"查看成功引用提示框是否出现，定位器为：{self.SUCCESS_REFERENCE_MESSAGE[1]}")
        return self.is_displayed(self.SUCCESS_REFERENCE_MESSAGE)
        
    def reference_course_content(self):
        """引用课程内容"""
        # 切换到我的班级iframe
        self.switch_to_iframe(self.MY_CLASSES_IFRAME)
        # 点击引用课程内容按钮
        self.click_reference_course_content_button()
        # 点击全选未引用的版本复选框
        self.click_all_select_unreferenced_version_checkbox()
        # 点击确定引用按钮
        self.click_confirm_reference_button()
        # 断言成功引用提示框是否出现
        result = self.is_success_reference_message_displayed()
        log.info(f"引用课程内容结果：{result}")
        # 切出我的班级iframe
        self.switch_out_iframe()
        return result

    def click_add_chapter_button(self):
        """点击添加章按钮"""
        log.info(f"点击添加章按钮，定位器为：{self.ADD_CHAPTER_BUTTON[1]}")
        return self.click(self.ADD_CHAPTER_BUTTON)

    def input_chapter_title(self, chapter_title):
        """输入章节标题"""
        log.info(f"输入章节标题：{chapter_title}，定位器为：{self.CHAPTER_TITLE_INPUT[1]}")
        return self.input_text(self.CHAPTER_TITLE_INPUT, chapter_title)

    def click_confirm_add_chapter_button(self):
        """点击章节确认创建按钮"""
        log.info(f"点击章节确认创建按钮，定位器为：{self.CONFIRM_ADD_CHAPTER_BUTTON[1]}")
        return self.click(self.CONFIRM_ADD_CHAPTER_BUTTON)
    
    def is_success_create_chapter_message_displayed(self):
        """查看创建章节成功提示框是否出现"""
        log.info(f"查看创建章节成功提示框是否出现，定位器为：{self.SUCCESS_CREATE_CHAPTER_MESSAGE[1]}")
        return self.is_displayed(self.SUCCESS_CREATE_CHAPTER_MESSAGE)
    
    def create_chapter(self, chapter_title):
        """创建章节"""
        # 切换到我的班级iframe
        self.switch_to_iframe(self.MY_CLASSES_IFRAME)
        # 点击添加章按钮
        self.click_add_chapter_button()
        # 输入章节标题
        self.input_chapter_title(chapter_title)
        # 点击章节确认创建按钮
        self.click_confirm_add_chapter_button()
        # 断言创建章节成功提示框是否出现
        result = self.is_success_create_chapter_message_displayed()
        log.info(f"创建章节结果：{result}")
        # 切出我的班级iframe
        self.switch_out_iframe()
        return result

    def click_chapter_more_dropdown_by_title(self, chapter_title):
        """
        根据章节名称点击对应章节的多功能下拉框

        Args:
            chapter_title (str): 章节名称

        Returns:
            bool: 点击操作结果
        """
        log.info(f"点击章节 [{chapter_title}] 的多功能下拉框, 定位器: {self.get_chapter_more_dropdown_by_name(chapter_title)[1]}")
        return self.click(self.get_chapter_more_dropdown_by_name(chapter_title))

    def click_add_section_dropdown(self):
        """
        点击添加节下拉框    

        Args:
            chapter_title (str): 章节名称

        Returns:
            bool: 点击操作结果
        """
        log.info(f"点击添加节下拉框, 定位器: {self.ADD_SECTION_DROPDOWN[1]}")
        return self.click(self.ADD_SECTION_DROPDOWN)
    
    def input_sub_chapter_title(self, sub_chapter_title):
        """输入子章节标题"""
        log.info(f"输入子章节标题：{sub_chapter_title}，定位器为：{self.SUB_CHAPTER_TITLE_INPUT[1]}")
        return self.input_text(self.SUB_CHAPTER_TITLE_INPUT, sub_chapter_title)
    
    def click_confirm_add_section_button(self):
        """点击确认添加节按钮"""
        log.info(f"点击确认添加节按钮，定位器为：{self.CONFIRM_ADD_SECTION_BUTTON[1]}")
        return self.click(self.CONFIRM_ADD_SECTION_BUTTON)
    
    def create_section_in_chapter(self, chapter_title, sub_chapter_title):
        """在指定章下创建节"""
        # 切换到我的班级iframe
        self.switch_to_iframe(self.MY_CLASSES_IFRAME)
        # 点击对应章节的多功能下拉框
        self.click_chapter_more_dropdown_by_title(chapter_title)
        # 点击添加节下拉框
        self.click_add_section_dropdown()
        # 输入子章节标题
        self.input_sub_chapter_title(sub_chapter_title)
        # 点击确认添加节按钮
        self.click_confirm_add_section_button()
        # 断言创建章节成功提示框是否出现
        result = self.is_success_create_chapter_message_displayed()
        log.info(f"创建章节结果：{result}")
        # 切出我的班级iframe
        self.switch_out_iframe()
        return result