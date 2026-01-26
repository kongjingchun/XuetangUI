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
    # 创建章节成功提示框
    CREATE_CHAPTER_SUCCESS_ALERT = (By.XPATH, "//p[text()='创建章节成功']")
    # 子章节标题输入框
    SUB_CHAPTER_TITLE_INPUT = (By.XPATH, "//div[@aria-label='添加子章节']//input[@placeholder='请输入子章节标题']")
    # 子章节确认创建按钮
    CONFIRM_CREATE_SUB_CHAPTER_BUTTON = (By.XPATH, "//div[@aria-label='添加子章节']//button[./span[text()=' 创建 ']]")
    # 创建子章节成功提示框
    CREATE_SUB_CHAPTER_SUCCESS_ALERT = (By.XPATH, "//p[text()='创建子章节成功']")
    # 添加学习单元全选复选框
    ADD_LEARNING_UNIT_ALL_SELECT_CHECKBOX = (By.XPATH, "//tr[contains(.,'标题') and contains(.,'创建时间')]/th[1]//label")
    # 选择学习单元确定按钮
    CONFIRM_SELECT_LEARNING_UNIT_BUTTON = (By.XPATH, "//div[@aria-label='选择学习单元']//button[contains(.,'确定')]")
    # 学习单元添加成功提示框
    LEARNING_UNIT_ADD_SUCCESS_ALERT = (By.XPATH, "//p[contains(.,'成功')]")
    # 版本管理按钮
    VERSION_MANAGEMENT_BUTTON = (By.XPATH, "//button[contains(.,'版本管理')]")
    # 从其他版本复制按钮
    COPY_FROM_OTHER_VERSION_BUTTON = (By.XPATH, "//li[contains(.,'从其他版本复制')]")
    # 版本选择下拉框
    VERSION_SELECT_DROPDOWN = (By.XPATH, "//div[@aria-label='从其他版本复制']//div[./span[text()='请选择要复制的版本']]")
    # 默认版本下拉框选项
    DEFAULT_VERSION_DROPDOWN_OPTION = (By.XPATH, "//div[@aria-hidden='false']//li[contains(.,'默认版本')]")
    # 新版本名称输入框
    NEW_VERSION_NAME_INPUT = (By.XPATH, "//div[@aria-label='从其他版本复制']//input[@placeholder='请输入新版本名称']")
    # 确定复制按钮
    CONFIRM_COPY_BUTTON = (By.XPATH, "//div[@aria-label='从其他版本复制']//button[contains(.,'确定')]")
    # 复制版本成功提示框
    COPY_VERSION_SUCCESS_ALERT = (By.XPATH, "//p[contains(.,'复制版本成功')]")
    # 知识点第一个复选框
    FIRST_KNOWLEDGE_CHECKBOX = (By.XPATH, "(//div[@aria-label='选择知识点']//label/span)[1]")
    # 选择知识点确定按钮
    CONFIRM_SELECT_KNOWLEDGE_BUTTON = (By.XPATH, "//div[@aria-label='选择知识点']//button[contains(.,'确定')]")
    #成功添加知识点提示框
    SUCCESS_ADD_KNOWLEDGE_ALERT = (By.XPATH, "//p[contains(.,'成功')]")
    # ===================元素定位器（动态定位器）====================

    def get_add_learning_unit_button_locator_by_chapter(self, chapter_title):
        """
        根据章节名称返回对应章节的“+增加学习单元”按钮定位器

        Args:
            chapter_title (str): 章节名称

        Returns:
            tuple: (By.XPATH, xpath字符串)
        """
        return (By.XPATH, f"//div[./div/span[text()='{chapter_title}']]//button[contains(.,'学习单元')]")
    def get_knowledge_graph_button_locator_by_chapter(self, chapter_title):
        """
        根据章节名称返回对应章节的“知识图谱”按钮定位器

        Args:
            chapter_title (str): 章节名称

        Returns:
            tuple: (By.XPATH, xpath字符串)
        """
        return (By.XPATH, f"//div[./div/span[text()='{chapter_title}']]//button[contains(.,'知识图谱')]")
     
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

    def is_create_chapter_success_alert_display(self):
        """查看创建章节成功提示框是否出现

        Returns:
            bool: True表示创建章节成功提示框出现，False表示未出现
        """
        log.info(f"查看创建章节成功提示框是否出现，定位器为：{self.CREATE_CHAPTER_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.CREATE_CHAPTER_SUCCESS_ALERT)

    def new_chapter(self, chapter_title):
        """新建章节"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 点击创建章节按钮
        self.click_create_chapter_button()
        # 输入章节标题
        self.input_chapter_title(chapter_title)
        # 点击确认创建章节按钮
        self.click_confirm_create_chapter_button()
        # 断言创建章节成功提示框是否出现
        result = self.is_create_chapter_success_alert_display()
        log.info(f"新建章节结果：{result}")
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

    def is_create_sub_chapter_success_alert_display(self):
        """查看创建子章节成功提示框是否出现

        Returns:
            bool: True表示创建子章节成功提示框出现，False表示未出现
        """
        log.info(f"查看创建子章节成功提示框是否出现，定位器为：{self.CREATE_SUB_CHAPTER_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.CREATE_SUB_CHAPTER_SUCCESS_ALERT)

    def new_sub_chapter_in_chapter(self, chapter_name, sub_chapter_title):
        """在章节中新增子章节"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 点击新增子章节按钮
        self.click_add_sub_chapter_button_by_chapter(chapter_name)
        # 输入子章节标题
        self.input_sub_chapter_title(sub_chapter_title)
        # 点击确认创建子章节按钮
        self.click_confirm_create_sub_chapter_button()
        # 断言创建子章节成功提示框是否出现
        result = self.is_create_sub_chapter_success_alert_display()
        log.info(f"在章节中新增子章节结果：{result}")
        # 切出课程工作台iframe
        self.switch_out_iframe()
        return result

    def click_add_learning_unit_button_by_chapter(self, chapter_name):
        """
        根据章节名称，点击添加学习单元按钮

        Args:
            chapter_name (str): 章节名称

        Returns:
            点击操作结果
        """
        chapter_add_learning_unit_button = self.get_add_learning_unit_button_locator_by_chapter(chapter_name)
        log.info(f"点击章节「{chapter_name}」下的添加学习单元按钮，定位器为：{chapter_add_learning_unit_button[1]}")
        return self.click(chapter_add_learning_unit_button)

    def click_add_learning_unit_all_select_button(self):
        """点击学习单元全选复选框

        Returns:
            点击操作结果
        """
        log.info(f"点击学习单元全选复选框，定位器为：{self.ADD_LEARNING_UNIT_ALL_SELECT_CHECKBOX[1]}")
        return self.click(self.ADD_LEARNING_UNIT_ALL_SELECT_CHECKBOX)

    def click_confirm_select_learning_unit_button(self):
        """点击选择学习单元确定按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击选择学习单元确定按钮，定位器为：{self.CONFIRM_SELECT_LEARNING_UNIT_BUTTON[1]}")
        return self.click(self.CONFIRM_SELECT_LEARNING_UNIT_BUTTON)

    def is_learning_unit_add_success_alert_display(self):
        """判断学习单元添加成功提示框是否出现

        Returns:
            bool: True表示学习单元添加成功提示框出现，False表示未出现
        """
        log.info(f"判断学习单元添加成功提示框是否出现，定位器为：{self.LEARNING_UNIT_ADD_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.LEARNING_UNIT_ADD_SUCCESS_ALERT)

    def is_learning_unit_add_success_alert_disappear(self, timeout=5):
        """
        判断学习单元添加成功提示框是否消失

        Args:
            timeout (int): 等待提示框消失的超时时间，单位为秒，默认5秒

        Returns:
            bool: True表示提示框已消失，False表示未消失
        """
        log.info(f"判断学习单元添加成功提示框是否消失，定位器为：{self.LEARNING_UNIT_ADD_SUCCESS_ALERT[1]}")
        return self.is_disappear(self.LEARNING_UNIT_ADD_SUCCESS_ALERT, timeout=timeout)

    def add_learning_unit_by_chapter(self, chapter_name):
        """
        给指定章节批量添加学习单元

        Args:
            chapter_name (str): 章节名称

        Returns:
            bool: True表示添加成功，False表示失败或未出现提示
        """
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 点击章节下添加学习单元按钮
        self.click_add_learning_unit_button_by_chapter(chapter_name)
        # 勾选全选复选框
        self.click_add_learning_unit_all_select_button()
        # 点击确定
        self.click_confirm_select_learning_unit_button()
        # 检查是否出现添加成功提示框
        result = self.is_learning_unit_add_success_alert_display()
        log.info(f"章节「{chapter_name}」添加学习单元结果：{result}")
        self.is_learning_unit_add_success_alert_disappear(timeout=7)
        # 切出iframe
        self.switch_out_iframe()
        return result

    def click_version_management_button(self):
        """点击版本管理按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击版本管理按钮，定位器为：{self.VERSION_MANAGEMENT_BUTTON[1]}")
        return self.click(self.VERSION_MANAGEMENT_BUTTON)

    def click_copy_from_other_version_button(self):
        """点击从其他版本复制按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击从其他版本复制按钮，定位器为：{self.COPY_FROM_OTHER_VERSION_BUTTON[1]}")
        return self.click(self.COPY_FROM_OTHER_VERSION_BUTTON)

    def click_version_select_dropdown(self):
        """点击版本选择下拉框

        Returns:
            点击操作结果
        """
        log.info(f"点击版本选择下拉框，定位器为：{self.VERSION_SELECT_DROPDOWN[1]}")
        return self.click(self.VERSION_SELECT_DROPDOWN)

    def click_default_version_dropdown_option(self):
        """点击默认版本下拉框选项

        Returns:
            点击操作结果
        """
        log.info(f"点击默认版本下拉框选项，定位器为：{self.DEFAULT_VERSION_DROPDOWN_OPTION[1]}")
        return self.click(self.DEFAULT_VERSION_DROPDOWN_OPTION)

    def input_new_version_name(self, new_version_name):
        """输入新版本名称

        Args:
            new_version_name (str): 新版本名称
        """
        log.info(f"输入新版本名称：{new_version_name}，定位器为：{self.NEW_VERSION_NAME_INPUT[1]}")
        return self.input_text(self.NEW_VERSION_NAME_INPUT, new_version_name)

    def click_confirm_copy_button(self):
        """点击确定复制按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击确定复制按钮，定位器为：{self.CONFIRM_COPY_BUTTON[1]}")
        return self.click(self.CONFIRM_COPY_BUTTON)

    def is_copy_version_success_alert_display(self):
        """判断复制版本成功提示框是否出现

        Returns:
            bool: True表示复制版本成功提示框出现，False表示未出现
        """
        log.info(f"判断复制版本成功提示框是否出现，定位器为：{self.COPY_VERSION_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.COPY_VERSION_SUCCESS_ALERT)

    def copy_new_version_from_default(self, new_version_name):
        """
        从默认版本复制新版本

        Args:
            new_version_name (str): 新版本的名称

        Returns:
            bool: True - 复制成功; False - 复制失败
        """
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 点击版本管理按钮
        self.click_version_management_button()
        # 点击从其他版本复制按钮
        self.click_copy_from_other_version_button()
        # 点击版本选择下拉框
        self.click_version_select_dropdown()
        # 选择默认版本
        self.click_default_version_dropdown_option()
        # 输入新版本名称
        self.input_new_version_name(new_version_name)
        # 点击确定复制按钮
        self.click_confirm_copy_button()
        # 判断复制版本成功提示框是否出现
        result = self.is_copy_version_success_alert_display()
        log.info(f"从默认版本复制新版本结果：{result}")
        # 切出课程工作台iframe
        self.switch_out_iframe()
        return result

    def click_add_knowledge_button_by_chapter(self, chapter_title):
        """根据章节名称点击增加知识点按钮

        Args:
            chapter_title (str): 章节名称
        """
        return self.click(self.get_knowledge_graph_button_locator_by_chapter(chapter_title))
    
    def click_first_knowledge_checkbox(self):
        """
        点击第一个知识点的复选框

        Returns:
            bool: 点击操作结果
        """
        log.info(f"点击第一个知识点的复选框，定位器为：{self.FIRST_KNOWLEDGE_CHECKBOX[1]}")
        return self.click(self.FIRST_KNOWLEDGE_CHECKBOX)

    def click_confirm_select_knowledge_button(self):
        """
        点击选择知识点确定按钮

        Returns:
            bool: 点击操作结果
        """
        return self.click(self.CONFIRM_SELECT_KNOWLEDGE_BUTTON)

    def is_success_add_knowledge_alert_display(self):
        """
        判断成功添加知识点提示框是否出现

        Returns:
            bool: 提示框是否出现
        """
        return self.is_displayed(self.SUCCESS_ADD_KNOWLEDGE_ALERT)

    def relate_first_knowledge_by_chapter(self, chapter_title):
        """
        根据章节名称关联第一个知识点

        Args:
            chapter_title (str): 章节名称

        Returns:
            bool: 操作是否成功
        """
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 点击本章节下“增加知识点”按钮
        self.click_add_knowledge_button_by_chapter(chapter_title)
        # 点击第一个知识点的复选框
        self.click_first_knowledge_checkbox()
        # 点击“确定”按钮
        self.click_confirm_select_knowledge_button()
        # 判断成功添加知识点提示框是否出现
        result = self.is_success_add_knowledge_alert_display()
        log.info(f"章节 [{chapter_title}] 关联第一个知识点结果: {result}")
        # 切出课程工作台iframe
        self.switch_out_iframe()
        return result

        
    # ==================== 新建学习单元定位器====================
    # 管理学习单元按钮
    MANAGE_LEARNING_UNIT_BUTTON = (By.XPATH, "//button[contains(.,'管理学习单元')]")
    # 退出管理学习单元的返回按钮
    EXIT_MANAGE_LEARNING_UNIT_BUTTON = (By.XPATH, "//button[./span[text()=' 返回 ']]")
    # 创建学习单元按钮
    CREATE_LEARNING_UNIT_BUTTON = (By.XPATH, "//button[contains(.,'创建学习单元')]")
    # 学习单元创建标题输入框
    LEARNING_UNIT_TITLE_INPUT = (By.XPATH, "//div[./label[contains(.,'学习单元标题')]]//input")
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

    def click_exit_manage_learning_unit_button(self):
        """点击退出管理学习单元按钮

        Returns:
            点击操作结果
        """
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        log.info(f"点击退出管理学习单元按钮，定位器为：{self.EXIT_MANAGE_LEARNING_UNIT_BUTTON[1]}")
        result = self.click(self.EXIT_MANAGE_LEARNING_UNIT_BUTTON)
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

    def create_learning_unit(self, learning_unit_type, learning_unit_title, learning_unit_content, count_grade=False, allow_comment=True):
        """创建学习单元

        Args:
            learning_unit_type: 学习单元类型
            learning_unit_title: 学习单元标题
            learning_unit_content: 学习单元正文
            count_grade: 是否计入成绩
            allow_comment: 是否允许评论

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
        # 是否允许评论，默认开启
        if not allow_comment:
            self.click_allow_comment_switch()
        # 点击是否计入成绩开关
        if count_grade:
            self.click_count_grade_switch()
        return True

    # ====================新建视频学习单元定位器=================================
     # 选择视频文件按钮
    SELECT_VIDEO_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择视频文件')]")
    # 选择第一个视频文件按钮
    SELECT_FIRST_VIDEO_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//tr[1]/td[1]/div")
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
        # 点击选择视频文件
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

    # ====================新建资料学习单元定位器=================================
    # 选择资料文件按钮
    SELECT_MATERIAL_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择资料文件')]")
    # 选择第一个资料文件按钮
    SELECT_FIRST_MATERIAL_FILE_BUTTON = (By.XPATH, "//div[contains(@aria-label,'选择文件')]//tr[1]/td[1]/div/label")
    # 确认选择资料文件按钮
    CONFIRM_SELECT_MATERIAL_FILE_BUTTON = (By.XPATH, "//div[contains(@aria-label,'选择文件')]//button[./span[text()='确定']]")
    # ====================新建资料学习单元操作方法=================================

    def click_select_material_file_button(self):
        """点击选择资料文件按钮"""
        log.info(f"点击选择资料文件按钮，定位器为：{self.SELECT_MATERIAL_FILE_BUTTON[1]}")
        return self.click(self.SELECT_MATERIAL_FILE_BUTTON)

    def click_select_first_material_file_button(self):
        """点击选择第一个资料文件按钮"""
        log.info(f"点击选择第一个资料文件按钮，定位器为：{self.SELECT_FIRST_MATERIAL_FILE_BUTTON[1]}")
        return self.click(self.SELECT_FIRST_MATERIAL_FILE_BUTTON)

    def click_confirm_select_material_file_button(self):
        """点击确认选择资料文件按钮"""
        log.info(f"点击确认选择资料文件按钮，定位器为：{self.CONFIRM_SELECT_MATERIAL_FILE_BUTTON[1]}")
        return self.click(self.CONFIRM_SELECT_MATERIAL_FILE_BUTTON)

    def new_material_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=False, allow_comment=True):
        """新建资料学习单元"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 新建资料学习单元
        self.create_learning_unit("资料", learning_unit_title, learning_unit_content, count_grade, allow_comment)
        # 选择资料文件
        self.click_select_material_file_button()
        # 点击选择第一个资料文件按钮
        self.click_select_first_material_file_button()
        # 点击确认选择资料文件按钮
        self.click_confirm_select_material_file_button()
        # 点击新建学习单元创建按钮
        self.click_new_learning_unit_create_button()
        # 断言新建学习单元创建成功提示框是否出现
        result = self.is_new_learning_unit_create_success_alert_displayed()
        log.info(f"新建资料学习单元结果：{result}")
        # 切出课程工作台iframe
        self.switch_out_iframe()
        return result
    # ====================新建课件学习单元定位器=================================
    # 选择课件文件按钮
    SELECT_PPT_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择课件文件')]")
    # 选择第一个课件文件按钮
    SELECT_FIRST_PPT_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//tr[1]/td[1]/div")
    # 确认选择课件文件按钮
    CONFIRM_SELECT_PPT_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//button[./span[text()='确定']]")
    # ====================新建课件学习单元操作方法=================================

    def click_select_ppt_file_button(self):
        """点击选择课件文件按钮"""
        log.info(f"点击选择课件文件按钮，定位器为：{self.SELECT_PPT_FILE_BUTTON[1]}")
        return self.click(self.SELECT_PPT_FILE_BUTTON)

    def click_select_first_ppt_file_button(self):
        """点击选择第一个课件文件按钮"""
        log.info(f"点击选择第一个课件文件按钮，定位器为：{self.SELECT_FIRST_PPT_FILE_BUTTON[1]}")
        return self.click(self.SELECT_FIRST_PPT_FILE_BUTTON)

    def click_confirm_select_ppt_file_button(self):
        """点击确认选择课件文件按钮"""
        log.info(f"点击确认选择课件文件按钮，定位器为：{self.CONFIRM_SELECT_PPT_FILE_BUTTON[1]}")
        return self.click(self.CONFIRM_SELECT_PPT_FILE_BUTTON)

    def new_ppt_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=False, allow_comment=True):
        """新建课件学习单元"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 新建课件学习单元
        self.create_learning_unit("课件", learning_unit_title, learning_unit_content, count_grade, allow_comment)
        # 选择课件文件
        self.click_select_ppt_file_button()
        # 点击选择第一个课件文件按钮
        self.click_select_first_ppt_file_button()
        # 点击确认选择课件文件按钮
        self.click_confirm_select_ppt_file_button()
        # 点击新建学习单元创建按钮
        self.click_new_learning_unit_create_button()
        # 断言新建学习单元创建成功提示框是否出现
        result = self.is_new_learning_unit_create_success_alert_displayed()
        log.info(f"新建课件学习单元结果：{result}")
        # 切出课程工作台iframe
        self.switch_out_iframe()
        return result

    # ====================新建讨论学习单元定位器=================================
    # 是否匿名评论开关
    ANONYMOUS_COMMENT_SWITCH = (By.XPATH, "//div[./label[text()='是否匿名评论']]//span[2]")
    # ====================新建讨论学习单元操作方法=================================

    def click_anonymous_comment_switch(self, anonymous_comment=False):
        """点击是否匿名评论开关

        Args:
            anonymous_comment: 是否匿名评论，默认不匿名

        Returns:
            点击操作结果
        """
        if anonymous_comment:
            log.info(f"点击是否匿名评论开关，定位器为：{self.ANONYMOUS_COMMENT_SWITCH[1]}")
            return self.click(self.ANONYMOUS_COMMENT_SWITCH)

    def new_discussion_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=False, allow_comment=True, anonymous_comment=False):
        """新建讨论学习单元"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 新建讨论学习单元
        self.create_learning_unit("讨论", learning_unit_title, learning_unit_content, count_grade, allow_comment)
        # 点击是否匿名评论开关
        self.click_anonymous_comment_switch(anonymous_comment)
        # 点击新建学习单元创建按钮
        self.click_new_learning_unit_create_button()
        # 断言新建学习单元创建成功提示框是否出现
        result = self.is_new_learning_unit_create_success_alert_displayed()
        log.info(f"新建讨论学习单元结果：{result}")
        # 切出课程工作台iframe
        self.switch_out_iframe()
        return result
    # ====================新建作业学习单元定位器=================================
    # 选择作业文件按钮
    SELECT_HOMEWORK_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择作业')]")
    # 选择第一个作业按钮
    SELECT_FIRST_HOMEWORK_BUTTON = (By.XPATH, "//div[@aria-label='选择作业']//tr[1]/td[1]/div/label")
    # 确认选择作业按钮
    CONFIRM_SELECT_HOMEWORK_BUTTON = (By.XPATH, "//div[@aria-label='选择作业']//button[./span[contains(.,'确定选择')]]")
    # ====================新建作业学习单元操作方法=================================

    def click_select_homework_file_button(self):
        """点击选择作业文件按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击选择作业按钮，定位器为：{self.SELECT_HOMEWORK_FILE_BUTTON[1]}")
        return self.click(self.SELECT_HOMEWORK_FILE_BUTTON)

    def click_select_first_homework_button(self):
        """点击选择第一个作业按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击选择第一个作业按钮，定位器为：{self.SELECT_FIRST_HOMEWORK_BUTTON[1]}")
        return self.click(self.SELECT_FIRST_HOMEWORK_BUTTON)

    def click_confirm_select_homework_button(self):
        """点击确认选择作业按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击确认选择作业按钮，定位器为：{self.CONFIRM_SELECT_HOMEWORK_BUTTON[1]}")
        return self.click(self.CONFIRM_SELECT_HOMEWORK_BUTTON)

    def new_homework_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=False, allow_comment=True):
        """新建作业学习单元"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 新建作业学习单元
        self.create_learning_unit("作业", learning_unit_title, learning_unit_content, count_grade, allow_comment)
        # 点击选择作业文件按钮
        self.click_select_homework_file_button()
        # 点击选择第一个作业按钮
        self.click_select_first_homework_button()
        # 点击确认选择作业按钮
        self.click_confirm_select_homework_button()
        # 点击新建学习单元创建按钮
        self.click_new_learning_unit_create_button()
        # 断言新建学习单元创建成功提示框是否出现
        result = self.is_new_learning_unit_create_success_alert_displayed()
        log.info(f"新建作业学习单元结果：{result}")
        # 切出课程工作台iframe
        self.switch_out_iframe()
        return result
    # ====================新建考试学习单元定位器=================================
    # 选择考试文件按钮
    SELECT_EXAM_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择试卷')]")
    # 选择第一个考试按钮
    SELECT_FIRST_EXAM_BUTTON = (By.XPATH, "//div[@aria-label='选择试卷']//tr[1]/td[1]/div/label")
    # 确认选择考试按钮
    CONFIRM_SELECT_EXAM_BUTTON = (By.XPATH, "//div[@aria-label='选择试卷']//button[./span[contains(.,'确定选择')]]")
    # ====================新建考试学习单元操作方法=================================

    def click_select_exam_file_button(self):
        """点击选择考试文件按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击选择考试文件按钮，定位器为：{self.SELECT_EXAM_FILE_BUTTON[1]}")
        return self.click(self.SELECT_EXAM_FILE_BUTTON)

    def click_select_first_exam_button(self):
        """点击选择第一个考试按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击选择第一个考试按钮，定位器为：{self.SELECT_FIRST_EXAM_BUTTON[1]}")
        return self.click(self.SELECT_FIRST_EXAM_BUTTON)

    def click_confirm_select_exam_button(self):
        """点击确认选择考试按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击确认选择考试按钮，定位器为：{self.CONFIRM_SELECT_EXAM_BUTTON[1]}")
        return self.click(self.CONFIRM_SELECT_EXAM_BUTTON)

    def new_exam_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=False, allow_comment=True):
        """新建考试学习单元"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 新建考试学习单元
        self.create_learning_unit("考试", learning_unit_title, learning_unit_content, count_grade, allow_comment)
        # 点击选择考试文件按钮
        self.click_select_exam_file_button()
        # 点击选择第一个考试按钮
        self.click_select_first_exam_button()
        # 点击确认选择考试按钮
        self.click_confirm_select_exam_button()
        # 点击新建学习单元创建按钮
        self.click_new_learning_unit_create_button()
        # 断言新建学习单元创建成功提示框是否出现
        result = self.is_new_learning_unit_create_success_alert_displayed()
        log.info(f"新建考试学习单元结果：{result}")
        # 切出课程工作台iframe
        self.switch_out_iframe()
        return result

     # ====================新建链接学习单元定位器=================================
     # 选择链接文件按钮
    SELECT_LINK_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择链接')]")
    # 选择第一个链接文件按钮
    SELECT_FIRST_LINK_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//tr[1]/td[1]/div")
    # 确认选择链接文件按钮
    CONFIRM_SELECT_LINK_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//button[./span[text()='确定']]")

    # ====================新建链接学习单元操作方法=================================
    def click_select_link_file_button(self):
        """点击选择链接文件按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击选择链接文件按钮，定位器为：{self.SELECT_LINK_FILE_BUTTON[1]}")
        return self.click(self.SELECT_LINK_FILE_BUTTON)

    def click_select_first_link_file_button(self):
        """点击选择第一个链接文件按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击选择第一个链接文件按钮，定位器为：{self.SELECT_FIRST_LINK_FILE_BUTTON[1]}")
        return self.click(self.SELECT_FIRST_LINK_FILE_BUTTON)

    def click_confirm_select_link_file_button(self):
        """点击确认选择链接文件按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击确认选择链接文件按钮，定位器为：{self.CONFIRM_SELECT_LINK_FILE_BUTTON[1]}")
        return self.click(self.CONFIRM_SELECT_LINK_FILE_BUTTON)

    def new_link_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=False, allow_comment=True):
        """新建链接学习单元"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 新建链接学习单元
        self.create_learning_unit("链接", learning_unit_title, learning_unit_content, count_grade, allow_comment)
        # 点击选择链接文件按钮
        self.click_select_link_file_button()
        # 点击选择第一个链接文件按钮
        self.click_select_first_link_file_button()
        # 点击确认选择链接文件按钮
        self.click_confirm_select_link_file_button()
        # 点击新建学习单元创建按钮
        self.click_new_learning_unit_create_button()
        # 断言新建学习单元创建成功提示框是否出现
        result = self.is_new_learning_unit_create_success_alert_displayed()
        log.info(f"新建链接学习单元结果：{result}")
        # 切出课程工作台iframe
        self.switch_out_iframe()
        return result

    # ====================新建音频学习单元定位器=================================
    # 选择音频文件按钮
    SELECT_AUDIO_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择音频文件')]")
    # 选择第一个音频文件按钮
    SELECT_FIRST_AUDIO_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//tr[1]/td[1]/div/label")
    # 确认选择音频文件按钮
    CONFIRM_SELECT_AUDIO_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//button[./span[text()='确定']]")

    # ====================新建音频学习单元操作方法=================================
    def click_select_audio_file_button(self):
        """点击选择音频文件按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击选择音频文件按钮，定位器为：{self.SELECT_AUDIO_FILE_BUTTON[1]}")
        return self.click(self.SELECT_AUDIO_FILE_BUTTON)

    def click_select_first_audio_file_button(self):
        """点击选择第一个音频文件按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击选择第一个音频文件按钮，定位器为：{self.SELECT_FIRST_AUDIO_FILE_BUTTON[1]}")
        return self.click(self.SELECT_FIRST_AUDIO_FILE_BUTTON)

    def click_confirm_select_audio_file_button(self):
        """点击确认选择音频文件按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击确认选择音频文件按钮，定位器为：{self.CONFIRM_SELECT_AUDIO_FILE_BUTTON[1]}")
        return self.click(self.CONFIRM_SELECT_AUDIO_FILE_BUTTON)

    def new_audio_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=False, allow_comment=True):
        """新建音频学习单元"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 新建音频学习单元
        self.create_learning_unit("音频", learning_unit_title, learning_unit_content, count_grade, allow_comment)
        # 点击选择音频文件按钮
        self.click_select_audio_file_button()
        # 点击选择第一个音频文件按钮
        self.click_select_first_audio_file_button()
        # 点击确认选择音频文件按钮
        self.click_confirm_select_audio_file_button()
        # 点击新建学习单元创建按钮
        self.click_new_learning_unit_create_button()
        # 断言新建学习单元创建成功提示框是否出现
        result = self.is_new_learning_unit_create_success_alert_displayed()
        log.info(f"新建音频学习单元结果：{result}")
        # 切出课程工作台iframe
        self.switch_out_iframe()
        return result

    # ====================新建课堂学习单元操作方法=================================
    def new_classroom_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=False, allow_comment=True):
        """新建课堂学习单元"""
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 新建课堂学习单元
        self.create_learning_unit("课堂", learning_unit_title, learning_unit_content, count_grade, allow_comment)
        # 点击新建学习单元创建按钮
        self.click_new_learning_unit_create_button()
        # 断言新建学习单元创建成功提示框是否出现
        result = self.is_new_learning_unit_create_success_alert_displayed()
        log.info(f"新建课堂学习单元结果：{result}")
        # 切出课程工作台iframe
        self.switch_out_iframe()
        return result
