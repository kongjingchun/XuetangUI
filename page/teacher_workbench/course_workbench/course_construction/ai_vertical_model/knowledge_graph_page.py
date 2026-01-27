# encoding: utf-8
# @File  : knowledge_graph_page.py
# @Author:
# @Date  :
# @Desc  : 知识图谱页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from page.teacher_workbench.course_workbench.course_workbench_page import CourseWorkbenchPage
from logs.log import log


class KnowledgeGraphPage(CourseWorkbenchPage, BasePage):
    """知识图谱页面类。

    对外只暴露“服务方法”（如新建主图谱、按图谱名称进入编辑、添加节点、按节点名称添加子级节点等），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 知识图谱列表（在课程工作空间 iframe 内）
    # 新建主图谱按钮
    CREATE_MAIN_GRAPH_BUTTON = (By.XPATH, "//button[./span[contains(.,'新建主图谱')]]")

    # ======================新建图谱弹窗======================
    # 图谱名称输入框
    CREATE_MAIN_GRAPH_NAME_INPUT = (By.XPATH, "//input[@placeholder='请输入图谱名称']")
    # 图谱描述输入框
    CREATE_MAIN_GRAPH_DESCRIPTION_INPUT = (By.XPATH, "//textarea[@placeholder='请输入图谱描述']")
    # 版本号输入框
    CREATE_MAIN_GRAPH_VERSION_INPUT = (By.XPATH, "//input[@placeholder='请输入版本号（可选）']")
    # 第1级标题输入框
    FIRST_LEVEL_TITLE_INPUT = (By.XPATH, "//input[@placeholder='第1级标题']")
    # 新建弹窗确定按钮
    CREATE_GRAPH_CONFIRM_BUTTON = (By.XPATH, "//button[./span[text()='确定']]")
    # 新建图谱成功 toast 文案
    CREATE_MAIN_GRAPH_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='新建图谱成功']")

    # ======================编辑数据======================
    # 添加数据按钮
    ADD_DATA_BUTTON = (By.XPATH, "//span[contains(.,'添加数据')]/parent::button")
    # 节点标题输入框
    NODE_TITLE_INPUT = (By.XPATH, "//input[@placeholder='请输入节点标题']")
    # 节点描述输入框
    NODE_DESCRIPTION_INPUT = (By.XPATH, "//textarea[@placeholder='请输入节点描述（可选）']")
    # 添加节点弹窗确定按钮
    ADD_NODE_CONFIRM_BUTTON = (By.XPATH, "//span[contains(.,'确定')]/parent::button")
    # 创建成功 toast 文案
    ADD_NODE_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='创建成功']")

    # ==================== 动态定位器 getter ====================

    def get_edit_data_button_locator(self, graph_name):
        """图谱名称 → 该图谱卡片上「编辑数据」按钮定位器。"""
        return (By.XPATH, f"//div[@class='hero-content' and .//h2[text()='{graph_name}']]//span[text()='编辑数据']/parent::button")

    def get_node_locator(self, node_name):
        """节点名称 → 节点项定位器。"""
        return (By.XPATH, f"//div[contains(@class,'node-item') and contains(.,'{node_name}')]")

    def get_sub_node_button_locator(self, node_name):
        """节点名称 → 该节点「子级」按钮定位器。"""
        return (By.XPATH, f"//div[contains(@class,'node-item') and contains(.,'{node_name}')]//span[contains(.,'子级')]/parent::button")

    # ==================== 服务方法（页面对外能力） ====================

    def click_edit_data_button_by_name(self, graph_name):
        """在知识图谱工作空间内，按图谱名称点击「编辑数据」进入编辑页，返回是否点击成功。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        locator = self.get_edit_data_button_locator(graph_name)  # 获取编辑数据按钮定位器
        log.info(f"根据图谱名称点击编辑数据按钮，定位器为：{locator[1]}")
        result = self.click(locator)  # 点击编辑数据按钮
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def create_main_graph(self, name, description=None, version=None, title=None):
        """新建主图谱（填写名称、可选描述/版本号/第1级标题后确定），返回是否出现新建图谱成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.CREATE_MAIN_GRAPH_BUTTON)  # 点击新建主图谱
        self.input_text(self.CREATE_MAIN_GRAPH_NAME_INPUT, name)  # 输入图谱名称
        if description:
            self.input_text(self.CREATE_MAIN_GRAPH_DESCRIPTION_INPUT, description)  # 输入图谱描述
        if version:
            self.input_text(self.CREATE_MAIN_GRAPH_VERSION_INPUT, version)  # 输入版本号
        if title:
            self.input_text(self.FIRST_LEVEL_TITLE_INPUT, title)  # 输入第1级标题
        self.click(self.CREATE_GRAPH_CONFIRM_BUTTON)  # 点击确定
        result = self.is_displayed(self.CREATE_MAIN_GRAPH_SUCCESS_MESSAGE)  # 检查是否出现新建成功提示
        log.info(f"新建主图谱结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def add_node(self, graph_name, title, description):
        """在编辑数据上下文中添加节点（点击添加数据、填写标题与描述、确定），返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.click(self.ADD_DATA_BUTTON)  # 点击添加数据
        self.input_text(self.NODE_TITLE_INPUT, title)  # 输入节点标题
        self.input_text(self.NODE_DESCRIPTION_INPUT, description)  # 输入节点描述
        self.click(self.ADD_NODE_CONFIRM_BUTTON)  # 点击确定
        result = self.is_displayed(self.ADD_NODE_SUCCESS_MESSAGE)  # 检查是否出现创建成功提示
        log.info(f"添加节点结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def add_sub_node_by_name(self, node_name, title, description):
        """在指定节点下添加子级节点（悬停该节点、点子级、填标题与描述、确定），返回是否出现创建成功提示。"""
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        self.hover(self.get_node_locator(node_name))  # 悬停到该节点
        self.click(self.get_sub_node_button_locator(node_name))  # 点击子级按钮
        self.input_text(self.NODE_TITLE_INPUT, title)  # 输入子级节点标题
        self.input_text(self.NODE_DESCRIPTION_INPUT, description)  # 输入子级节点描述
        self.click(self.ADD_NODE_CONFIRM_BUTTON)  # 点击确定
        result = self.is_displayed(self.ADD_NODE_SUCCESS_MESSAGE)  # 检查是否出现创建成功提示
        log.info(f"添加子级节点结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result
