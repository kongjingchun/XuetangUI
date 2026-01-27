# encoding: utf-8
# @File  : course_content_page.py
# @Author:
# @Date  :
# @Desc  : 课程内容页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from logs.log import log
from page.teacher_workbench.course_workbench.course_workbench_page import CourseWorkbenchPage


class CourseContentPage(CourseWorkbenchPage):
    """课程内容页面类。

    继承 CourseWorkbenchPage，提供课程内容页面的能力。
    对外只暴露“服务方法”（如创建章节、子章节、各类学习单元、版本复制、关联知识点等），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # ======================创建章节======================
    # 创建章节按钮
    CREATE_CHAPTER_BUTTON = (By.XPATH, "//button[contains(.,'创建章节')]")
    # 创建章节弹窗 - 章节标题输入框
    CHAPTER_TITLE_INPUT = (By.XPATH, "//div[@aria-label='创建章节']//input[@placeholder='请输入章节标题']")
    # 创建章节弹窗 - 确认创建按钮
    CONFIRM_CREATE_CHAPTER_BUTTON = (By.XPATH, "//div[@aria-label='创建章节']//button[./span[text()=' 创建 ']]")
    # 创建章节成功提示文案
    CREATE_CHAPTER_SUCCESS_ALERT = (By.XPATH, "//p[text()='创建章节成功']")

    # ======================添加子章节======================
    # 添加子章节弹窗 - 子章节标题输入框
    SUB_CHAPTER_TITLE_INPUT = (By.XPATH, "//div[@aria-label='添加子章节']//input[@placeholder='请输入子章节标题']")
    # 添加子章节弹窗 - 确认创建按钮
    CONFIRM_CREATE_SUB_CHAPTER_BUTTON = (By.XPATH, "//div[@aria-label='添加子章节']//button[./span[text()=' 创建 ']]")
    # 创建子章节成功提示文案
    CREATE_SUB_CHAPTER_SUCCESS_ALERT = (By.XPATH, "//p[text()='创建子章节成功']")

    # ======================选择学习单元======================
    # 添加学习单元全选复选框
    ADD_LEARNING_UNIT_ALL_SELECT_CHECKBOX = (By.XPATH, "//tr[contains(.,'标题') and contains(.,'创建时间')]/th[1]//label")
    # 选择学习单元弹窗 - 确定按钮
    CONFIRM_SELECT_LEARNING_UNIT_BUTTON = (By.XPATH, "//div[@aria-label='选择学习单元']//button[contains(.,'确定')]")
    # 学习单元添加成功提示文案
    LEARNING_UNIT_ADD_SUCCESS_ALERT = (By.XPATH, "//p[contains(.,'成功')]")

    # ======================版本管理 - 从其他版本复制======================
    # 版本管理按钮
    VERSION_MANAGEMENT_BUTTON = (By.XPATH, "//button[contains(.,'版本管理')]")
    # 从其他版本复制菜单项
    COPY_FROM_OTHER_VERSION_BUTTON = (By.XPATH, "//li[contains(.,'从其他版本复制')]")
    # 从其他版本复制弹窗 - 版本选择下拉框
    VERSION_SELECT_DROPDOWN = (By.XPATH, "//div[@aria-label='从其他版本复制']//div[./span[text()='请选择要复制的版本']]")
    # 默认版本下拉选项
    DEFAULT_VERSION_DROPDOWN_OPTION = (By.XPATH, "//div[@aria-hidden='false']//li[contains(.,'默认版本')]")
    # 从其他版本复制弹窗 - 新版本名称输入框
    NEW_VERSION_NAME_INPUT = (By.XPATH, "//div[@aria-label='从其他版本复制']//input[@placeholder='请输入新版本名称']")
    # 从其他版本复制弹窗 - 确定复制按钮
    CONFIRM_COPY_BUTTON = (By.XPATH, "//div[@aria-label='从其他版本复制']//button[contains(.,'确定')]")
    # 复制版本成功提示文案
    COPY_VERSION_SUCCESS_ALERT = (By.XPATH, "//p[contains(.,'复制版本成功')]")

    # ======================选择知识点======================
    # 选择知识点弹窗 - 第一个知识点复选框
    FIRST_KNOWLEDGE_CHECKBOX = (By.XPATH, "(//div[@aria-label='选择知识点']//label/span)[1]")
    # 选择知识点弹窗 - 确定按钮
    CONFIRM_SELECT_KNOWLEDGE_BUTTON = (By.XPATH, "//div[@aria-label='选择知识点']//button[contains(.,'确定')]")
    # 成功添加知识点提示文案
    SUCCESS_ADD_KNOWLEDGE_ALERT = (By.XPATH, "//p[contains(.,'成功')]")

    # ======================管理学习单元======================
    # 管理学习单元按钮
    MANAGE_LEARNING_UNIT_BUTTON = (By.XPATH, "//button[contains(.,'管理学习单元')]")
    # 退出管理学习单元的返回按钮
    EXIT_MANAGE_LEARNING_UNIT_BUTTON = (By.XPATH, "//button[./span[text()=' 返回 ']]")
    # 创建学习单元按钮
    CREATE_LEARNING_UNIT_BUTTON = (By.XPATH, "//button[contains(.,'创建学习单元')]")
    # 学习单元标题输入框
    LEARNING_UNIT_TITLE_INPUT = (By.XPATH, "//div[./label[contains(.,'学习单元标题')]]//input")
    # 学习单元正文富文本输入框
    LEARNING_UNIT_CONTENT_INPUT = (By.XPATH, "//div[@contenteditable='true']")
    # 是否允许评论开关
    ALLOW_COMMENT_SWITCH = (By.XPATH, "//div[./label[text()='是否允许评论']]//span[2]")
    # 是否计入成绩开关
    COUNT_GRADE_SWITCH = (By.XPATH, "//div[./label[text()='是否计入成绩']]//span[2]")
    # 新建学习单元弹窗 - 创建按钮
    NEW_LEARNING_UNIT_CREATE_BUTTON = (By.XPATH, "//div[contains(@aria-label,'学习单元')]//button[contains(.,'创建')]")
    # 新建学习单元创建成功提示文案
    NEW_LEARNING_UNIT_CREATE_SUCCESS_ALERT = (By.XPATH, "//p[text()='创建成功']")

    # ======================新建视频学习单元======================
    # 请选择视频文件按钮
    SELECT_VIDEO_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择视频文件')]")
    # 选择文件弹窗 - 第一行（视频）
    SELECT_FIRST_VIDEO_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//tr[1]/td[1]/div")
    # 选择文件弹窗 - 确定按钮（视频）
    CONFIRM_SELECT_VIDEO_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//button[./span[text()='确定']]")

    # ======================新建资料学习单元======================
    # 请选择资料文件按钮
    SELECT_MATERIAL_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择资料文件')]")
    # 选择文件弹窗 - 第一行复选框（资料）
    SELECT_FIRST_MATERIAL_FILE_BUTTON = (By.XPATH, "//div[contains(@aria-label,'选择文件')]//tr[1]/td[1]/div/label")
    # 选择文件弹窗 - 确定按钮（资料）
    CONFIRM_SELECT_MATERIAL_FILE_BUTTON = (By.XPATH, "//div[contains(@aria-label,'选择文件')]//button[./span[text()='确定']]")

    # ======================新建课件学习单元======================
    # 请选择课件文件按钮
    SELECT_PPT_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择课件文件')]")
    # 选择文件弹窗 - 第一行（课件）
    SELECT_FIRST_PPT_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//tr[1]/td[1]/div")
    # 选择文件弹窗 - 确定按钮（课件）
    CONFIRM_SELECT_PPT_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//button[./span[text()='确定']]")

    # ======================新建讨论学习单元======================
    # 是否匿名评论开关
    ANONYMOUS_COMMENT_SWITCH = (By.XPATH, "//div[./label[text()='是否匿名评论']]//span[2]")

    # ======================新建作业学习单元======================
    # 请选择作业按钮
    SELECT_HOMEWORK_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择作业')]")
    # 选择作业弹窗 - 第一行复选框
    SELECT_FIRST_HOMEWORK_BUTTON = (By.XPATH, "//div[@aria-label='选择作业']//tr[1]/td[1]/div/label")
    # 选择作业弹窗 - 确定选择按钮
    CONFIRM_SELECT_HOMEWORK_BUTTON = (By.XPATH, "//div[@aria-label='选择作业']//button[./span[contains(.,'确定选择')]]")

    # ======================新建考试学习单元======================
    # 请选择试卷按钮
    SELECT_EXAM_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择试卷')]")
    # 选择试卷弹窗 - 第一行复选框
    SELECT_FIRST_EXAM_BUTTON = (By.XPATH, "//div[@aria-label='选择试卷']//tr[1]/td[1]/div/label")
    # 选择试卷弹窗 - 确定选择按钮
    CONFIRM_SELECT_EXAM_BUTTON = (By.XPATH, "//div[@aria-label='选择试卷']//button[./span[contains(.,'确定选择')]]")

    # ======================新建链接学习单元======================
    # 请选择链接按钮
    SELECT_LINK_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择链接')]")
    # 选择文件弹窗 - 第一行（链接）
    SELECT_FIRST_LINK_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//tr[1]/td[1]/div")
    # 选择文件弹窗 - 确定按钮（链接）
    CONFIRM_SELECT_LINK_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//button[./span[text()='确定']]")

    # ======================新建音频学习单元======================
    # 请选择音频文件按钮
    SELECT_AUDIO_FILE_BUTTON = (By.XPATH, "//button[contains(.,'请选择音频文件')]")
    # 选择文件弹窗 - 第一行复选框（音频）
    SELECT_FIRST_AUDIO_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//tr[1]/td[1]/div/label")
    # 选择文件弹窗 - 确定按钮（音频）
    CONFIRM_SELECT_AUDIO_FILE_BUTTON = (By.XPATH, "//div[@aria-label='选择文件']//button[./span[text()='确定']]")

    # ==================== 动态定位器 getter ====================

    def get_add_learning_unit_button_locator_by_chapter(self, chapter_title):
        """章节名称 → 该章节「学习单元」按钮定位器（div+span 结构）。"""
        return (By.XPATH, f"//div[./div/span[text()='{chapter_title}']]//button[contains(.,'学习单元')]")

    def get_knowledge_graph_button_locator_by_chapter(self, chapter_title):
        """章节名称 → 该章节「知识图谱」按钮定位器。"""
        return (By.XPATH, f"//div[./div/span[text()='{chapter_title}']]//button[contains(.,'知识图谱')]")

    def get_add_sub_chapter_button_locator(self, chapter_name):
        """章节名称 → 该章节「子章节」按钮定位器。"""
        return (By.XPATH, f"//div[contains(@class,'el-tree-node') and contains(.,'{chapter_name}')]/div/div/div/button[contains(.,'子章节')]")

    def get_add_learning_unit_button_locator(self, chapter_name):
        """章节名称 → 该章节「学习单元」按钮定位器（树节点结构）。"""
        return (By.XPATH, f"//div[contains(@class,'el-tree-node') and contains(.,'{chapter_name}')]/div/div/div/button[contains(.,'学习单元')]")

    def get_create_learning_unit_button_locator(self, learning_unit_type):
        """学习单元类型（如视频、资料、课件）→ 创建该类型学习单元菜单项定位器。"""
        return (By.XPATH, f"//li[text()='{learning_unit_type}']")

    # ==================== 服务方法（页面对外能力） ====================

    def _fill_learning_unit_form(self, learning_unit_type, learning_unit_title, learning_unit_content, count_grade=False, allow_comment=True):
        """内部：填写学习单元类型、标题、正文及是否允许评论/计入成绩。调用前需已处于课程工作空间 iframe 内。"""
        self.click(self.CREATE_LEARNING_UNIT_BUTTON)  # 点击创建学习单元
        self.click(self.get_create_learning_unit_button_locator(learning_unit_type))  # 选择类型
        self.input_text(self.LEARNING_UNIT_TITLE_INPUT, learning_unit_title)  # 输入标题
        self.input_rich_text(self.LEARNING_UNIT_CONTENT_INPUT, learning_unit_content)  # 输入正文
        if not allow_comment:
            self.click(self.ALLOW_COMMENT_SWITCH)  # 关闭允许评论
        if count_grade:
            self.click(self.COUNT_GRADE_SWITCH)  # 开启计入成绩

    def click_manage_learning_unit_button(self):
        """点击管理学习单元按钮，进入管理学习单元页面。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        log.info(f"点击管理学习单元按钮，定位器为：{self.MANAGE_LEARNING_UNIT_BUTTON[1]}")
        result = self.click(self.MANAGE_LEARNING_UNIT_BUTTON)
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def click_exit_manage_learning_unit_button(self):
        """点击退出管理学习单元（返回）按钮。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        log.info(f"点击退出管理学习单元按钮，定位器为：{self.EXIT_MANAGE_LEARNING_UNIT_BUTTON[1]}")
        result = self.click(self.EXIT_MANAGE_LEARNING_UNIT_BUTTON)
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def new_chapter(self, chapter_title):
        """创建章节：输入标题并确认创建，返回是否出现创建章节成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.CREATE_CHAPTER_BUTTON)  # 点击创建章节
        self.input_text(self.CHAPTER_TITLE_INPUT, chapter_title)  # 输入章节标题
        self.click(self.CONFIRM_CREATE_CHAPTER_BUTTON)  # 点击确认创建
        result = self.is_displayed(self.CREATE_CHAPTER_SUCCESS_ALERT)  # 检查是否出现创建章节成功提示
        log.info(f"新建章节结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def new_sub_chapter_in_chapter(self, chapter_name, sub_chapter_title):
        """在指定章节下新建子章节：点击该章节的子章节按钮、输入子章节标题并确认，返回是否出现创建子章节成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.get_add_sub_chapter_button_locator(chapter_name))  # 点击该章节的子章节按钮
        self.input_text(self.SUB_CHAPTER_TITLE_INPUT, sub_chapter_title)  # 输入子章节标题
        self.click(self.CONFIRM_CREATE_SUB_CHAPTER_BUTTON)  # 点击确认创建
        result = self.is_displayed(self.CREATE_SUB_CHAPTER_SUCCESS_ALERT)  # 检查是否出现创建子章节成功提示
        log.info(f"在章节中新增子章节结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def add_learning_unit_by_chapter(self, chapter_name):
        """给指定章节批量添加学习单元：点击该章节的添加学习单元、全选、确定，返回是否出现添加成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.get_add_learning_unit_button_locator_by_chapter(chapter_name))  # 点击该章节的添加学习单元
        self.click(self.ADD_LEARNING_UNIT_ALL_SELECT_CHECKBOX)  # 全选学习单元
        self.click(self.CONFIRM_SELECT_LEARNING_UNIT_BUTTON)  # 点击确定
        result = self.is_displayed(self.LEARNING_UNIT_ADD_SUCCESS_ALERT)  # 检查是否出现添加成功提示
        log.info(f"章节「{chapter_name}」添加学习单元结果：{result}")
        self.is_disappear(self.LEARNING_UNIT_ADD_SUCCESS_ALERT, timeout=7)  # 等待成功提示消失
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def copy_new_version_from_default(self, new_version_name):
        """从默认版本复制出新版本：版本管理 → 从其他版本复制 → 选默认版本 → 输入新版本名称 → 确定，返回是否出现复制版本成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.VERSION_MANAGEMENT_BUTTON)  # 点击版本管理
        self.click(self.COPY_FROM_OTHER_VERSION_BUTTON)  # 点击从其他版本复制
        self.click(self.VERSION_SELECT_DROPDOWN)  # 点击版本选择下拉框
        self.click(self.DEFAULT_VERSION_DROPDOWN_OPTION)  # 选择默认版本
        self.input_text(self.NEW_VERSION_NAME_INPUT, new_version_name)  # 输入新版本名称
        self.click(self.CONFIRM_COPY_BUTTON)  # 点击确定复制
        result = self.is_displayed(self.COPY_VERSION_SUCCESS_ALERT)  # 检查是否出现复制版本成功提示
        log.info(f"从默认版本复制新版本结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def relate_first_knowledge_by_chapter(self, chapter_title):
        """根据章节名称关联第一个知识点：点击该章节的知识图谱 → 勾选第一个知识点 → 确定，返回是否出现成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.get_knowledge_graph_button_locator_by_chapter(chapter_title))  # 点击该章节的知识图谱（增加知识点）
        self.click(self.FIRST_KNOWLEDGE_CHECKBOX)  # 勾选第一个知识点
        self.click(self.CONFIRM_SELECT_KNOWLEDGE_BUTTON)  # 点击确定
        result = self.is_displayed(self.SUCCESS_ADD_KNOWLEDGE_ALERT)  # 检查是否出现成功添加知识点提示
        log.info(f"章节 [{chapter_title}] 关联第一个知识点结果: {result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def new_video_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=True):
        """新建视频学习单元：填写表单、选择视频文件、创建，返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self._fill_learning_unit_form("视频", learning_unit_title, learning_unit_content, count_grade=count_grade)
        self.click(self.SELECT_VIDEO_FILE_BUTTON)  # 点击选择视频文件
        self.click(self.SELECT_FIRST_VIDEO_FILE_BUTTON)  # 选择第一个视频文件
        self.click(self.CONFIRM_SELECT_VIDEO_FILE_BUTTON)  # 确认选择
        self.click(self.NEW_LEARNING_UNIT_CREATE_BUTTON)  # 点击创建
        result = self.is_displayed(self.NEW_LEARNING_UNIT_CREATE_SUCCESS_ALERT)  # 检查是否出现创建成功提示
        log.info(f"新建视频学习单元结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def new_material_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=True):
        """新建资料学习单元：填写表单、选择资料文件、创建，返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self._fill_learning_unit_form("资料", learning_unit_title, learning_unit_content, count_grade=count_grade)
        self.click(self.SELECT_MATERIAL_FILE_BUTTON)  # 点击选择资料文件
        self.click(self.SELECT_FIRST_MATERIAL_FILE_BUTTON)  # 选择第一个资料文件
        self.click(self.CONFIRM_SELECT_MATERIAL_FILE_BUTTON)  # 确认选择
        self.click(self.NEW_LEARNING_UNIT_CREATE_BUTTON)  # 点击创建
        result = self.is_displayed(self.NEW_LEARNING_UNIT_CREATE_SUCCESS_ALERT)  # 检查是否出现创建成功提示
        log.info(f"新建资料学习单元结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def new_ppt_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=True):
        """新建课件学习单元：填写表单、选择课件文件、创建，返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self._fill_learning_unit_form("课件", learning_unit_title, learning_unit_content, count_grade=count_grade)
        self.click(self.SELECT_PPT_FILE_BUTTON)  # 点击选择课件文件
        self.click(self.SELECT_FIRST_PPT_FILE_BUTTON)  # 选择第一个课件文件
        self.click(self.CONFIRM_SELECT_PPT_FILE_BUTTON)  # 确认选择
        self.click(self.NEW_LEARNING_UNIT_CREATE_BUTTON)  # 点击创建
        result = self.is_displayed(self.NEW_LEARNING_UNIT_CREATE_SUCCESS_ALERT)  # 检查是否出现创建成功提示
        log.info(f"新建课件学习单元结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def new_discussion_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=True, anonymous_comment=False):
        """新建讨论学习单元：填写表单、可选匿名评论、创建，返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self._fill_learning_unit_form("讨论", learning_unit_title, learning_unit_content, count_grade=count_grade)
        if anonymous_comment:
            self.click(self.ANONYMOUS_COMMENT_SWITCH)  # 开启是否匿名评论
        self.click(self.NEW_LEARNING_UNIT_CREATE_BUTTON)  # 点击创建
        result = self.is_displayed(self.NEW_LEARNING_UNIT_CREATE_SUCCESS_ALERT)  # 检查是否出现创建成功提示
        log.info(f"新建讨论学习单元结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def new_homework_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=True):
        """新建作业学习单元：填写表单、选择作业、创建，返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self._fill_learning_unit_form("作业", learning_unit_title, learning_unit_content, count_grade=count_grade)
        self.click(self.SELECT_HOMEWORK_FILE_BUTTON)  # 点击选择作业
        self.click(self.SELECT_FIRST_HOMEWORK_BUTTON)  # 选择第一个作业
        self.click(self.CONFIRM_SELECT_HOMEWORK_BUTTON)  # 确认选择
        self.click(self.NEW_LEARNING_UNIT_CREATE_BUTTON)  # 点击创建
        result = self.is_displayed(self.NEW_LEARNING_UNIT_CREATE_SUCCESS_ALERT)  # 检查是否出现创建成功提示
        log.info(f"新建作业学习单元结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def new_exam_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=True):
        """新建考试学习单元：填写表单、选择试卷、创建，返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self._fill_learning_unit_form("考试", learning_unit_title, learning_unit_content, count_grade=count_grade)
        self.click(self.SELECT_EXAM_FILE_BUTTON)  # 点击选择试卷
        self.click(self.SELECT_FIRST_EXAM_BUTTON)  # 选择第一份试卷
        self.click(self.CONFIRM_SELECT_EXAM_BUTTON)  # 确认选择
        self.click(self.NEW_LEARNING_UNIT_CREATE_BUTTON)  # 点击创建
        result = self.is_displayed(self.NEW_LEARNING_UNIT_CREATE_SUCCESS_ALERT)  # 检查是否出现创建成功提示
        log.info(f"新建考试学习单元结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def new_link_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=True):
        """新建链接学习单元：填写表单、选择链接、创建，返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self._fill_learning_unit_form("链接", learning_unit_title, learning_unit_content, count_grade=count_grade)
        self.click(self.SELECT_LINK_FILE_BUTTON)  # 点击选择链接
        self.click(self.SELECT_FIRST_LINK_FILE_BUTTON)  # 选择第一个链接
        self.click(self.CONFIRM_SELECT_LINK_FILE_BUTTON)  # 确认选择
        self.click(self.NEW_LEARNING_UNIT_CREATE_BUTTON)  # 点击创建
        result = self.is_displayed(self.NEW_LEARNING_UNIT_CREATE_SUCCESS_ALERT)  # 检查是否出现创建成功提示
        log.info(f"新建链接学习单元结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def new_audio_learning_unit(self, learning_unit_title, learning_unit_content, count_grade=True):
        """新建音频学习单元：填写表单、选择音频文件、创建，返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self._fill_learning_unit_form("音频", learning_unit_title, learning_unit_content, count_grade=count_grade)
        self.click(self.SELECT_AUDIO_FILE_BUTTON)  # 点击选择音频文件
        self.click(self.SELECT_FIRST_AUDIO_FILE_BUTTON)  # 选择第一个音频文件
        self.click(self.CONFIRM_SELECT_AUDIO_FILE_BUTTON)  # 确认选择
        self.click(self.NEW_LEARNING_UNIT_CREATE_BUTTON)  # 点击创建
        result = self.is_displayed(self.NEW_LEARNING_UNIT_CREATE_SUCCESS_ALERT)  # 检查是否出现创建成功提示
        log.info(f"新建音频学习单元结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result

    def new_classroom_learning_unit(self, learning_unit_title, learning_unit_content):
        """新建课堂学习单元：填写表单、创建，返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self._fill_learning_unit_form("课堂", learning_unit_title, learning_unit_content, count_grade=False, allow_comment=True)
        self.click(self.NEW_LEARNING_UNIT_CREATE_BUTTON)  # 点击创建
        result = self.is_displayed(self.NEW_LEARNING_UNIT_CREATE_SUCCESS_ALERT)  # 检查是否出现创建成功提示
        log.info(f"新建课堂学习单元结果：{result}")
        self.switch_out_iframe()  # 切出课程工作空间 iframe
        self.switch_out_iframe()  # 切出课程工作台 iframe
        return result
