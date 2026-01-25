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
    # ====================元素定位器（静态定位器）====================
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

    # ====================操作方法=================================
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

    # ==================== 新建学习单元定位器====================
    # 管理学习单元按钮
    MANAGE_LEARNING_UNIT_BUTTON = (By.XPATH, "//button[contains(.,'管理学习单元')]")
    # 创建学习单元按钮
    CREATE_LEARNING_UNIT_BUTTON = (By.XPATH, "//button[contains(.,'创建学习单元')]")
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
    # 新建学习单元创建按钮
    NEW_LEARNING_UNIT_CREATE_BUTTON = (By.XPATH, "//div[contains(@aria-label,'学习单元')]//button[contains(.,'创建')]")
    # 新建学习单元创建成功提示框
    NEW_LEARNING_UNIT_CREATE_SUCCESS_ALERT = (By.XPATH, "//p[text()='创建成功']")
    # ====================元素定位器（动态定位器）====================

    def get_create_learning_unit_button_locator(self, learning_unit_type):
        """根据值返回创建学习单元类型新建按钮的定位器

        Args:
            learning_unit_type: 学习单元类型

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//li[text()='{learning_unit_type}']")

 # ====================创建学习单元通用操作方法=================================

    def click_manage_learning_unit_button(self):
        """点击管理学习单元按钮

        Returns:
            点击操作结果
        """
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        log.info(f"点击管理学习单元按钮，定位器为：{self.MANAGE_LEARNING_UNIT_BUTTON[1]}")
        result = self.click(self.MANAGE_LEARNING_UNIT_BUTTON)
        # 切出课程工作台iframe
        self.switch_out_iframe()
        return result

    def click_create_learning_unit_button(self):
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

    def click_allow_comment_switch(self):
        """点击是否允许评论开关

        Returns:
            点击操作结果
        """
        log.info(f"点击是否允许评论开关，定位器为：{self.ALLOW_COMMENT_SWITCH[1]}")
        return self.click(self.ALLOW_COMMENT_SWITCH)

    def click_count_grade_switch(self):
        """点击是否计入成绩开关

        Returns:
            点击操作结果
        """
        log.info(f"点击是否计入成绩开关，定位器为：{self.COUNT_GRADE_SWITCH[1]}")
        return self.click(self.COUNT_GRADE_SWITCH)

    def click_new_learning_unit_create_button(self):
        """点击新建学习单元创建按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击新建学习单元创建按钮，定位器为：{self.NEW_LEARNING_UNIT_CREATE_BUTTON[1]}")
        return self.click(self.NEW_LEARNING_UNIT_CREATE_BUTTON)

    def is_new_learning_unit_create_success_alert_displayed(self):
        """查看新建学习单元创建成功提示框是否出现

        Returns:
            bool: True表示新建学习单元创建成功提示框出现，False表示未出现
        """
        log.info(f"查看新建学习单元创建成功提示框是否出现，定位器为：{self.NEW_LEARNING_UNIT_CREATE_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.NEW_LEARNING_UNIT_CREATE_SUCCESS_ALERT)

    def create_learning_unit(self, learning_unit_type, learning_unit_title, learning_unit_content, count_grade=True):
        """创建学习单元

        Args:
            learning_unit_type: 学习单元类型
            learning_unit_title: 学习单元标题
            learning_unit_content: 学习单元正文
            count_grade: 是否计入成绩

        Returns:
            创建学习单元结果
        """
        # 点击创建学习单元按钮
        self.click_create_learning_unit_button()
        # 点击创建学习单元类型
        self.click_create_learning_unit_button_by_type(learning_unit_type)
        # 输入学习单元标题
        self.input_learning_unit_title(learning_unit_title)
        # 输入学习单元正文
        self.input_learning_unit_content(learning_unit_content)
        # 点击是否计入成绩开关
        if count_grade:
            self.click_count_grade_switch()

     # ====================新建视频学习单元定位器=================================
     # 选择视频文件按钮
    SELECT_VIDEO_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择视频文件')]")
    # 选择第一个视频文件按钮
    SELECT_FIRST_VIDEO_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//tr[1]/td[1]")
    # 确认选择视频文件按钮
    CONFIRM_SELECT_VIDEO_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//button[./span[text()='确定']]")

    # ====================新建视频学习单元操作方法=================================
    def click_select_video_file_button(self):
        """点击选择视频文件按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击选择视频文件按钮，定位器为：{self.SELECT_VIDEO_FILE_BUTTON[1]}")
        return self.click(self.SELECT_VIDEO_FILE_BUTTON)

    def click_select_first_video_file_button(self):
        """点击选择第一个视频文件按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击选择第一个视频文件按钮，定位器为：{self.SELECT_FIRST_VIDEO_FILE_BUTTON[1]}")
        return self.click(self.SELECT_FIRST_VIDEO_FILE_BUTTON)

    def click_confirm_select_video_file_button(self):
        """点击确认选择视频文件按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击确认选择视频文件按钮，定位器为：{self.CONFIRM_SELECT_VIDEO_FILE_BUTTON[1]}")
        return self.click(self.CONFIRM_SELECT_VIDEO_FILE_BUTTON)

    def new_video_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=True):
        """新建视频学习单元"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 新建视频学习单元
        self.create_learning_unit("视频", learning_unit_title, learning_unit_content, count_grade)
        # 选择视频文件
        self.click_select_video_file_button()
        # 点击选择第一个视频文件按钮
        self.click_select_first_video_file_button()
        # 点击确认选择视频文件按钮
        self.click_confirm_select_video_file_button()
        # 点击新建学习单元创建按钮
        self.click_new_learning_unit_create_button()
        # 断言新建学习单元创建成功提示框是否出现
        result = self.is_new_learning_unit_create_success_alert_displayed()
        log.info(f"新建视频学习单元结果：{result}")
        # 切出课程工作台iframe
        self.switch_out_iframe()
        return result

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
    # ====================新建资料学习单元定位器=================================
    # 选择资料文件按钮
    SELECT_MATERIAL_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择资料文件')]")
    # 选择第一个资料文件按钮
    SELECT_FIRST_MATERIAL_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//tr[1]/td[1]")
    # 确认选择资料文件按钮
    CONFIRM_SELECT_MATERIAL_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//button[./span[text()='确定']]")
    # ====================新建资料学习单元操作方法=================================
