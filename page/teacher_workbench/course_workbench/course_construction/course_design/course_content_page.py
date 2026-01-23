# encoding: utf-8
# @File  : CourseContentPage.py
# @Author:
# @Date  :
# @Desc  : 课程内容页面对象类，封装课程内容相关的页面操作方法

from selenium.webdriver.common.by import By

from logs.log import log
from page.teacher_workbench.course_workbench.course_workbench_page import CourseWorkbenchPage


class CourseContentPage(CourseWorkbenchPage):
    """课程内容页面类

    继承CourseWorkbenchPage类，提供课程内容页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化课程内容页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)
    # ==================== 元素定位器（静态定位器）====================
    # 管理学习单元按钮
    MANAGE_LEARNING_UNIT_BUTTON = (By.XPATH, "//button[contains(.,'管理学习单元')]")
    # 创建学习单元按钮
    CREATE_LEARNING_UNIT_BUTTON = (By.XPATH, "//button[contains(.,'创建学习单元')]")
    # 创建章节按钮
    CREATE_CHAPTER_BUTTON = (By.XPATH, "//button[contains(.,'创建章节')]")
    # 章节标题输入框
    CHAPTER_TITLE_INPUT = (By.XPATH, "//div[@aria-label='创建章节']//input[@placeholder='请输入章节标题']")
    # 章节确认创建按钮
    CONFIRM_CREATE_CHAPTER_BUTTON = (By.XPATH, "//div[@aria-label='创建章节']//button[./span[text()=' 创建 ']]")
    # 子章节标题输入框
    SUB_CHAPTER_TITLE_INPUT = (By.XPATH, "//div[@aria-label='添加子章节']//input[@placeholder='请输入子章节标题']")
    # 子章节确认创建按钮
    CONFIRM_CREATE_SUB_CHAPTER_BUTTON = (By.XPATH, "//div[@aria-label='添加子章节']//button[./span[text()=' 创建 ']]")

    # ======新建学习单元定位器=======
    # 学习单元创建标题输入框
    LEARNING_UNIT_TITLE_INPUT = (By.XPATH, "//input[contains(@placeholder,'请输入') and contains(@placeholder,'标题')]")
    # 学习单元正文富文本输入框
    LEARNING_UNIT_CONTENT_INPUT = (By.XPATH, "//div[@contenteditable='true']")
    # 是否允许评论按钮
    ALLOW_COMMENT_SWITCH = (By.XPATH, "//div[./label[text()='是否允许评论']]//span[2]")
    # 是否计入成绩
    COUNT_GRADE_SWITCH = (By.XPATH, "//div[./label[text()='是否计入成绩']]//span[2]")
    # 确认创建学习单元按钮
    CONFIRM_CREATE_LEARNING_UNIT_BUTTON = (By.XPATH, "//span[text()='创建']/parent::button")
    # 创建成功提示框
    CREATE_LEARNING_UNIT_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='创建成功']")

    # 选择视频文件按钮
    SELECT_VIDEO_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择视频文件')]")
    # 选择第一个视频文件按钮
    SELECT_FIRST_VIDEO_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//tr/td[1]")
    # 确认选择视频文件按钮
    CONFIRM_SELECT_VIDEO_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//button[./span[text()='确定']]")

    # ====================元素定位器（动态定位器）====================

    def get_create_learning_unit_button_locator(self, learning_unit_type):
        """根据值返回创建学习单元类型新建按钮的定位器

        Args:
            learning_unit_type: 学习单元类型

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//li[text()='{learning_unit_type}']")

    def get_add_sub_chapter_button_locator(self, chapter_name):
        """根据章节名称返回新增子章节的按钮

        Args:
            chapter_name: 章节名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//div[contains(@class,'el-tree-node') and contains(.,'{chapter_name}')]/div/div/div/button[contains(.,'子章节')]")

    def get_add_learning_unit_button_locator(self, chapter_name):
        """根据章节名称返回添加学习单元的按钮

        Args:
            chapter_name: 章节名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        # 假设页面结构：某章节div下“添加学习单元”按钮有特定文本
        return (By.XPATH, f"//div[contains(@class,'el-tree-node') and contains(.,'{chapter_name}')]/div/div/div/button[contains(.,'学习单元')]")

    # ==================== 元素操作方法 ==============================

    def click_manage_learning_unit_button(self):
        """点击管理学习单元按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击管理学习单元按钮，定位器为：{self.MANAGE_LEARNING_UNIT_BUTTON[1]}")
        return self.click(self.MANAGE_LEARNING_UNIT_BUTTON)

    # ====================创建学习单元操作方法=================================
    def click_create_learning_unit_button(self, learning_unit_type):
        """点击创建学习单元按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击创建学习单元按钮，定位器为：{self.CREATE_LEARNING_UNIT_BUTTON[1]}")
        return self.click(self.CREATE_LEARNING_UNIT_BUTTON)

    def click_create_learning_unit_button_by_type(self, learning_unit_type):
        """根据单元类型点击新建学习单元类型

        Args:
            learning_unit_type: 学习单元类型

        Returns:
            点击操作结果
        """
        log.info(f"根据单元类型点击新建学习单元类型，定位器为：{self.get_create_learning_unit_button_locator(learning_unit_type)[1]}")
        return self.click(self.get_create_learning_unit_button_locator(learning_unit_type))

    def input_learning_unit_title(self, value):
        """输入学习单元标题

        Args:
            value: 学习单元标题

        Returns:
            输入操作结果
        """
        log.info(f"输入学习单元标题：{value}，定位器为：{self.LEARNING_UNIT_TITLE_INPUT[1]}")
        return self.input_text(self.LEARNING_UNIT_TITLE_INPUT, value)

    def input_learning_unit_content(self, value):
        """输入学习单元正文

        Args:
            value: 学习单元正文

        Returns:
            输入操作结果
        """
        log.info(f"输入学习单元正文：{value}，定位器为：{self.LEARNING_UNIT_CONTENT_INPUT[1]}")
        return self.input_rich_text(self.LEARNING_UNIT_CONTENT_INPUT, value)

    # ====================课程内容主页面操作方法=================================

    def click_create_chapter_button(self):
        """点击创建章节按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击创建章节按钮，定位器为：{self.CREATE_CHAPTER_BUTTON[1]}")
        return self.click(self.CREATE_CHAPTER_BUTTON)

    def input_chapter_title(self, value):
        """输入章节标题

        Args:
            value: 章节标题

        Returns:
            输入操作结果
        """
        log.info(f"输入章节标题：{value}，定位器为：{self.CHAPTER_TITLE_INPUT[1]}")
        return self.input_text(self.CHAPTER_TITLE_INPUT, value)

    def click_confirm_create_chapter_button(self):
        """点击确认创建章节按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击确认创建章节按钮，定位器为：{self.CONFIRM_CREATE_CHAPTER_BUTTON[1]}")
        return self.click(self.CONFIRM_CREATE_CHAPTER_BUTTON)

    def click_add_sub_chapter_button_by_chapter(self, chapter_name):
        """根据章节名称点击子章节创建按钮

        Args:
            chapter_name: 章节名称

        Returns:
            点击操作结果
        """
        locator = self.get_add_sub_chapter_button_locator(chapter_name)
        log.info(f"点击章节“{chapter_name}”的子章节创建按钮，定位器为：{locator[1]}")
        return self.click(locator)

    def input_sub_chapter_title(self, value):
        """输入子章节标题

        Args:
            value: 子章节标题

        Returns:
            输入操作结果
        """
        log.info(f"输入子章节标题：{value}，定位器为：{self.SUB_CHAPTER_TITLE_INPUT[1]}")
        return self.input_text(self.SUB_CHAPTER_TITLE_INPUT, value)

    def click_confirm_create_sub_chapter_button(self):
        """点击确认创建子章节按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击确认创建子章节按钮，定位器为：{self.CONFIRM_CREATE_SUB_CHAPTER_BUTTON[1]}")
        return self.click(self.CONFIRM_CREATE_SUB_CHAPTER_BUTTON)
