# encoding: utf-8
# @File  : my_classes_page.py
# @Author:
# @Date  :
# @Desc  : 我的班级页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class MyClassesPage(BasePage):
    """我的班级页面类。

    对外只暴露“服务方法”（如进入班级、编辑课程导读、引用课程内容、创建章节等），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 我的班级主内容区域 iframe
    MY_CLASSES_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-4009']")
    # 保存成功 toast 文案
    SAVE_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='保存成功']")

    # ======================课程导读======================
    # 课程导读区域的编辑按钮
    COURSE_INTRODUCTION_EDIT_BUTTON = (By.XPATH, "//button[contains(.,'编辑')]")
    # 课程导读区域的保存按钮
    COURSE_INTRODUCTION_SAVE_BUTTON = (By.XPATH, "//button[contains(.,'保存')]")

    # ======================教学内容 - 引用课程内容======================
    # 引用课程内容入口按钮
    REFERENCE_COURSE_CONTENT_BUTTON = (By.XPATH, "//button[contains(.,'引用课程内容')]")
    # 全选未引用版本复选框
    ALL_SELECT_UNREFERENCED_VERSION_CHECKBOX = (By.XPATH, "//label[contains(.,'全选未引用的版本')]/span[1]")
    # 确定引用按钮
    CONFIRM_REFERENCE_BUTTON = (By.XPATH, "//button[contains(.,'确定引用')]")
    # 引用成功 toast 文案
    SUCCESS_REFERENCE_MESSAGE = (By.XPATH, "//p[contains(.,'成功引用')]")

    # ======================教学内容 - 添加章======================
    # 添加章按钮
    ADD_CHAPTER_BUTTON = (By.XPATH, "//button[contains(.,'添加章')]")
    # 创建章节弹窗中的章节标题输入框
    CHAPTER_TITLE_INPUT = (By.XPATH, "//input[@placeholder='请输入章节标题']")
    # 创建章节弹窗的创建按钮
    CONFIRM_ADD_CHAPTER_BUTTON = (By.XPATH, "//div[@aria-label='创建章节']//button[contains(.,'创建')]")
    # 创建成功 toast 文案
    SUCCESS_CREATE_CHAPTER_MESSAGE = (By.XPATH, "//p[contains(.,'创建') and contains(.,'成功')]")

    # ======================教学内容 - 添加节======================
    # 章节更多菜单中的「添加节」项
    ADD_SECTION_DROPDOWN = (By.XPATH, "//div[@aria-hidden='false']//li[contains(.,'添加节')]")
    # 添加节弹窗中的子章节标题输入框
    SUB_CHAPTER_TITLE_INPUT = (By.XPATH, "//input[@placeholder='请输入子章节标题']")
    # 添加节弹窗的创建按钮
    CONFIRM_ADD_SECTION_BUTTON = (By.XPATH, "//div[@aria-label='添加节']//button[contains(.,'创建')]")

    # ======================教学内容 - 选择学习单元======================
    # 章节更多菜单中的「添加学习单元」项
    ADD_LEARNING_UNIT_DROPDOWN = (By.XPATH, "//div[@aria-hidden='false']//li[contains(.,'添加学习单元')]")
    # 选择学习单元弹窗中第一行的复选框
    FIRST_LEARNING_UNIT_CHECKBOX = (By.XPATH, "//div[@aria-label='选择学习单元']//tr[1]/td[1]/div/label")
    # 选择学习单元弹窗的确定按钮
    SELECT_LEARNING_UNIT_CONFIRM_BUTTON = (By.XPATH, "//div[@aria-label='选择学习单元']//button[contains(.,'确定')]")
    # 添加成功 toast 文案
    ADD_SUCCESS_MESSAGE = (By.XPATH, "//p[contains(.,'成功')]")

    # ======================教学内容 - 添加知识图谱======================
    # 章节更多菜单中的「添加知识图谱」项
    ADD_KNOWLEDGE_GRAPH_DROPDOWN = (By.XPATH, "//div[@aria-hidden='false']//li[contains(.,'添加知识图谱')]")
    # 知识点弹窗中第一行复选框
    FIRST_KNOWLEDGE_POINT_CHECKBOX = (By.XPATH, "//div[@aria-label='选择知识点']//label[1]/span[1]")
    # 选择知识点弹窗的确定按钮
    SELECT_KNOWLEDGE_CONFIRM_BUTTON = (By.XPATH, "//div[@aria-label='选择知识点']//button[contains(.,'确定')]")
    # ==================== 动态定位器 getter ====================

    def get_class_card_locator(self, class_value):
        """班级名称或编号 → 班级卡片定位器。"""
        return (By.XPATH, f"//div[@class='class-card-inner' and contains(.,'{class_value}')]")

    def get_top_menu_button_locator(self, button_name):
        """上方菜单名称（如：课程导读、教学内容、讨论区…）→ 菜单按钮定位器。"""
        return (By.XPATH, f"//div[text()='{button_name}']")

    def get_chapter_more_dropdown_by_name(self, chapter_name):
        """章节名称 → 该章节「更多」下拉按钮定位器。"""
        return (By.XPATH, f"//div[./div/span[text()='{chapter_name}']]/div[2]/div[1]/button")

    def get_expand_chapter_button_by_name(self, chapter_name):
        """章节名称 → 展开该章节的图标/按钮定位器。"""
        return (By.XPATH, f"//div[./div/div/div/span[text()='{chapter_name}']]/i")

    # ==================== 服务方法（页面对外能力） ====================

    def click_class_card_by_value(self, class_value):
        """进入指定班级（按班级名称或编号点击班级卡片）。"""
        self.switch_to_iframe(self.MY_CLASSES_IFRAME)  # 切入我的班级 iframe
        locator = self.get_class_card_locator(class_value)
        log.info(f"点击班级卡片，定位器为：{locator[1]}")
        result = self.click(locator)  # 点击对应班级卡片
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def click_top_menu_button_by_name(self, button_name):
        """切换到上方某菜单（如：课程导读、教学内容、讨论区、公告等）。"""
        self.switch_to_iframe(self.MY_CLASSES_IFRAME)  # 切入我的班级 iframe
        locator = self.get_top_menu_button_locator(button_name)
        log.info(f"点击上方菜单按钮，定位器为：{locator[1]}")
        result = self.click(locator)  # 点击指定菜单项
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def edit_course_introduction(self):
        """编辑课程导读并保存，返回是否出现保存成功提示。"""
        self.switch_to_iframe(self.MY_CLASSES_IFRAME)  # 切入我的班级 iframe
        self.click(self.COURSE_INTRODUCTION_EDIT_BUTTON)  # 点击编辑按钮进入编辑态
        self.click(self.COURSE_INTRODUCTION_SAVE_BUTTON)  # 点击保存
        result = self.is_displayed(self.SAVE_SUCCESS_MESSAGE)  # 检查是否出现保存成功提示
        log.info(f"编辑课程导读结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def reference_course_content(self):
        """引用课程内容：全选未引用版本并确定引用，返回是否出现成功引用提示。"""
        self.switch_to_iframe(self.MY_CLASSES_IFRAME)  # 切入我的班级 iframe
        self.click(self.REFERENCE_COURSE_CONTENT_BUTTON)  # 点击「引用课程内容」打开弹窗
        self.click(self.ALL_SELECT_UNREFERENCED_VERSION_CHECKBOX)  # 勾选全选未引用版本
        self.click(self.CONFIRM_REFERENCE_BUTTON)  # 点击确定引用
        result = self.is_displayed(self.SUCCESS_REFERENCE_MESSAGE)  # 检查是否出现成功引用提示
        log.info(f"引用课程内容结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def create_chapter(self, chapter_title):
        """创建章，返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.MY_CLASSES_IFRAME)  # 切入我的班级 iframe
        self.click(self.ADD_CHAPTER_BUTTON)  # 点击添加章，弹出创建弹窗
        self.input_text(self.CHAPTER_TITLE_INPUT, chapter_title)  # 输入章节标题
        self.click(self.CONFIRM_ADD_CHAPTER_BUTTON)  # 点击创建确认
        result = self.is_displayed(self.SUCCESS_CREATE_CHAPTER_MESSAGE)  # 检查是否出现创建成功提示
        log.info(f"创建章节结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def create_section_in_chapter(self, chapter_title, sub_chapter_title):
        """在指定章下创建节，返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.MY_CLASSES_IFRAME)  # 切入我的班级 iframe
        self.click(self.get_chapter_more_dropdown_by_name(chapter_title))  # 点击该章的「更多」展开下拉
        self.click(self.ADD_SECTION_DROPDOWN)  # 选择「添加节」
        self.input_text(self.SUB_CHAPTER_TITLE_INPUT, sub_chapter_title)  # 输入节标题
        self.click(self.CONFIRM_ADD_SECTION_BUTTON)  # 点击创建确认
        result = self.is_displayed(self.SUCCESS_CREATE_CHAPTER_MESSAGE)  # 检查是否出现创建成功提示
        log.info(f"在章下创建节结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def add_learning_unit(self, chapter_title, parent_chapter_title=None):
        """给指定章节添加学习单元（若传 parent_chapter_title 则先展开父章）。返回是否出现添加成功提示。"""
        self.switch_to_iframe(self.MY_CLASSES_IFRAME)  # 切入我的班级 iframe
        if parent_chapter_title:
            self.click(self.get_expand_chapter_button_by_name(parent_chapter_title))  # 若为子章节，先展开父章
        self.click(self.get_chapter_more_dropdown_by_name(chapter_title))  # 点击该章节的「更多」展开下拉
        self.click(self.ADD_LEARNING_UNIT_DROPDOWN)  # 选择「添加学习单元」
        self.click(self.FIRST_LEARNING_UNIT_CHECKBOX)  # 勾选第一个学习单元
        self.click(self.SELECT_LEARNING_UNIT_CONFIRM_BUTTON)  # 点击确定完成添加
        result = self.is_displayed(self.ADD_SUCCESS_MESSAGE)  # 检查是否出现添加成功提示
        log.info(f"添加学习单元结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def add_knowledge_graph(self, chapter_title, parent_chapter_title=None):
        """给指定章节添加知识图谱（若传 parent_chapter_title 则先展开父章），返回是否出现添加成功提示。"""
        self.switch_to_iframe(self.MY_CLASSES_IFRAME)  # 切入我的班级 iframe
        if parent_chapter_title:
            self.click(self.get_expand_chapter_button_by_name(parent_chapter_title))  # 若为子章节，先展开父章
        self.click(self.get_chapter_more_dropdown_by_name(chapter_title))  # 点击该章节的「更多」展开下拉
        self.click(self.ADD_KNOWLEDGE_GRAPH_DROPDOWN)  # 选择「添加知识图谱」
        self.click(self.FIRST_KNOWLEDGE_POINT_CHECKBOX)  # 勾选第一个知识点
        self.click(self.SELECT_KNOWLEDGE_CONFIRM_BUTTON)  # 点击确定完成添加
        result = self.is_displayed(self.ADD_SUCCESS_MESSAGE)  # 检查是否出现添加成功提示
        log.info(f"添加知识图谱结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result
