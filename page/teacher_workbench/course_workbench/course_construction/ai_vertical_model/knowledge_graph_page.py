# encoding: utf-8
# @File  : KnowledgeGraphPage.py
# @Author: 孔敬淳
# @Date  : 2025/01/14
# @Desc  : 知识图谱页面对象类，封装知识图谱相关的页面操作方法

from selenium.webdriver.common.by import By

from base.base_page import BasePage
from page.teacher_workbench.course_workbench.course_workbench_page import CourseWorkbenchPage
from logs.log import log


class KnowledgeGraphPage(CourseWorkbenchPage, BasePage):
    """知识图谱页面类

    继承BasePage类，提供知识图谱页面元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化知识图谱页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 知识图谱页面定位器=============================================================
    # 新建主图谱button
    CREATE_MAIN_GRAPH_BUTTON = (By.XPATH, "//button[./span[contains(.,'新建主图谱')]]")

    def get_edit_data_button_locator_by_name(self, graph_name):
        """根据图谱名称返回编辑数据按钮的定位器

        Args:
            graph_name: 图谱名称
        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//div[@class='hero-content' and //h2[text()='{graph_name}']]//span[text()='编辑数据']/parent::button")

    # ==================== 知识图谱页面操作方法 ============================================================================================

    def click_create_main_graph_button(self):
        """点击新建主图谱按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击新建主图谱按钮，定位器为：{self.CREATE_MAIN_GRAPH_BUTTON[1]}")
        return self.click(self.CREATE_MAIN_GRAPH_BUTTON)

    def click_edit_data_button_by_name(self, graph_name):
        """根据图谱名称点击编辑数据按钮

        Args:
            graph_name: 图谱名称

        Returns:
            点击操作结果
        """
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 根据图谱名称点击编辑数据按钮
        locator = self.get_edit_data_button_locator_by_name(graph_name)
        log.info(f"根据图谱名称点击编辑数据按钮，定位器为：{locator[1]}")
        result = self.click(locator)
        # 切出知识图谱iframe
        self.switch_out_iframe()
        return result

    # ====================新建图谱页面定位器==============================================================

    # 新建主图谱名称输入框
    CREATE_MAIN_GRAPH_NAME_INPUT = (By.XPATH, "//input[@placeholder='请输入图谱名称']")
    # 新建主图谱描述输入框
    CREATE_MAIN_GRAPH_DESCRIPTION_INPUT = (By.XPATH, "//textarea[@placeholder='请输入图谱描述']")
    # 新建主图谱版本号输入框
    CREATE_MAIN_GRAPH_VERSION_INPUT = (By.XPATH, "//input[@placeholder='请输入版本号（可选）']")
    # 第1级标题输入框
    FIRST_LEVEL_TITLE_INPUT = (By.XPATH, "//input[@placeholder='第1级标题']")
    # 确定按钮
    CONFIRM_BUTTON = (By.XPATH, "//button[./span[text()='确定']]")
    # 新建图谱成功提示框
    CREATE_MAIN_GRAPH_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='新建图谱成功']")

    # =====================新建知识图谱界面操作方法============================================================================================

    def input_create_main_graph_name(self, name):
        """输入新建知识图谱名称

        Args:
            name: 新建知识图谱名称

        Returns:
            输入操作结果
        """
        log.info(f"输入新建知识图谱名称：{name}，定位器为：{self.CREATE_MAIN_GRAPH_NAME_INPUT[1]}")
        return self.input_text(self.CREATE_MAIN_GRAPH_NAME_INPUT, name)

    def input_create_main_graph_description(self, description):
        """输入新建知识图谱描述

        Args:
            description: 新建主图谱描述

        Returns:
            输入操作结果
        """
        log.info(f"输入新建主图谱描述：{description}，定位器为：{self.CREATE_MAIN_GRAPH_DESCRIPTION_INPUT[1]}")
        return self.input_text(self.CREATE_MAIN_GRAPH_DESCRIPTION_INPUT, description)

    def input_create_main_graph_version(self, version):
        """输入新建主图谱版本号

        Args:
            version: 新建主图谱版本号

        Returns:
            输入操作结果
        """
        log.info(f"输入新建主图谱版本号：{version}，定位器为：{self.CREATE_MAIN_GRAPH_VERSION_INPUT[1]}")
        return self.input_text(self.CREATE_MAIN_GRAPH_VERSION_INPUT, version)

    def input_first_level_title(self, title):
        """输入第1级标题

        Args:
            title: 第1级标题

        Returns:
            输入操作结果
        """
        log.info(f"输入第1级标题：{title}，定位器为：{self.FIRST_LEVEL_TITLE_INPUT[1]}")
        return self.input_text(self.FIRST_LEVEL_TITLE_INPUT, title)

    def click_create_main_graph_confirm_button(self):
        """点击新建主图谱确定按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击确定按钮，定位器为：{self.CONFIRM_BUTTON[1]}")
        return self.click(self.CONFIRM_BUTTON)

    # 断言新建图谱成功
    def assert_create_main_graph_success(self):
        """断言新建图谱成功

        Returns:
            断言操作结果
        """
        log.info(f"断言新建图谱成功，定位器为：{self.CREATE_MAIN_GRAPH_SUCCESS_MESSAGE[1]}")
        return self.is_displayed(self.CREATE_MAIN_GRAPH_SUCCESS_MESSAGE)

    def create_main_graph(self, name, description=None, version=None, title=None):
        """新建主图谱

        Args:
            name: 新建主图谱名称
            description: 新建主图谱描述
            version: 新建主图谱版本号
            title: 第1级标题
        """
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 点击新建主图谱按钮
        self.click_create_main_graph_button()
        # 输入新建主图谱名称
        self.input_create_main_graph_name(name)
        if description:
            # 输入新建主图谱描述
            self.input_create_main_graph_description(description)
        if version:
            # 输入新建主图谱版本号
            self.input_create_main_graph_version(version)
        if title:
            # 输入第1级标题
            self.input_first_level_title(title)
        # 点击确定按钮
        self.click_create_main_graph_confirm_button()
        # 断言新建图谱成功
        result = self.assert_create_main_graph_success()
        log.info(f"新建主图谱结果：{result}")
        # 切回顶层文档
        self.switch_out_iframe()
        return result

    # ====================编辑数据页面定位器==============================================================
    # 添加数据按钮
    ADD_DATA_BUTTON = (By.XPATH, "//span[contains(.,'添加数据')]/parent::button")
    # 节点标题输入框
    NODE_TITLE_INPUT = (By.XPATH, "//input[@placeholder='请输入节点标题']")
    # 节点描述输入框
    NODE_DESCRIPTION_INPUT = (By.XPATH, "//textarea[@placeholder='请输入节点描述（可选）']")
    # 确定按钮
    CONFIRM_BUTTON = (By.XPATH, "//span[contains(.,'确定')]/parent::button")
    # 添加节点成功提示框
    ADD_NODE_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='创建成功']")

    def get_node_locator_by_name(self, node_name):
        """根据节点名称返回节点定位器

        Args:
            node_name: 节点名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//div[contains(@class,'node-item') and contains(.,'{node_name}')]")

    def get_sub_node_button_locator_by_name(self, node_name):
        """根据节点名称返回子级按钮的定位器

        Args:
            node_name: 节点名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//div[contains(@class,'node-item') and contains(.,'{node_name}')]//span[contains(.,'子级')]/parent::button")

# =====================编辑数据页面操作方法============================================================================================

    def click_add_data_button(self):
        """点击添加数据按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击添加数据按钮，定位器为：{self.ADD_DATA_BUTTON[1]}")
        return self.click(self.ADD_DATA_BUTTON)

    def input_node_title(self, title):
        """输入节点标题

        Args:
            title: 节点标题

        Returns:
            输入操作结果
        """
        log.info(f"输入节点标题：{title}，定位器为：{self.NODE_TITLE_INPUT[1]}")
        return self.input_text(self.NODE_TITLE_INPUT, title)

    def input_node_description(self, description):
        """输入节点描述

        Args:
            description: 节点描述

        Returns:
            输入操作结果
        """
        log.info(f"输入节点描述：{description}，定位器为：{self.NODE_DESCRIPTION_INPUT[1]}")
        return self.input_text(self.NODE_DESCRIPTION_INPUT, description)

    def click_add_node_confirm_button(self):
        """点击添加节点确定按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击添加节点确定按钮，定位器为：{self.CONFIRM_BUTTON[1]}")
        return self.click(self.CONFIRM_BUTTON)

    def assert_add_node_success(self):
        """断言添加节点成功

        Returns:
            断言操作结果
        """
        log.info(f"断言添加节点成功，定位器为：{self.ADD_NODE_SUCCESS_MESSAGE[1]}")
        return self.is_displayed(self.ADD_NODE_SUCCESS_MESSAGE)

    def add_node(self, graph_name, title, description):
        """添加节点

        Args:
            graph_name: 图谱名称
            title: 节点标题
            description: 节点描述
        """
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 点击添加数据按钮
        self.click_add_data_button()
        # 输入节点标题
        self.input_node_title(title)
        # 输入节点描述
        self.input_node_description(description)
        # 点击确定按钮
        self.click_add_node_confirm_button()
        # 断言添加节点成功
        result = self.assert_add_node_success()
        log.info(f"添加节点结果：{result}")
        # 切回顶层文档
        self.switch_out_iframe()
        return result

    def hover_node_by_name(self, node_name):
        """鼠标悬停到节点名称

        Args:
            node_name: 节点名称

        Returns:
            悬停操作结果
        """
        locator = self.get_node_locator_by_name(node_name)
        log.info(f"鼠标悬停到节点名称'{node_name}'，定位器为：{locator[1]}")
        return self.hover(locator)

    def click_sub_node_button_by_name(self, node_name):
        """根据节点名称点击子级按钮

        Args:
            node_name: 节点名称

        Returns:
            点击操作结果
        """
        locator = self.get_sub_node_button_locator_by_name(node_name)
        log.info(f"根据节点名称'{node_name}'点击子级按钮，定位器为：{locator[1]}")
        return self.click(locator)
    # 根据节点名称添加子级节点

    def add_sub_node_by_name(self, node_name, title, description):
        """根据节点名称添加子级节点

        Args:
            node_name: 节点名称
            title: 子级节点标题
            description: 子级节点描述
        """
        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程工作空间iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)
        # 鼠标悬停到节点名称
        self.hover_node_by_name(node_name)
        # 点击子级按钮
        self.click_sub_node_button_by_name(node_name)
        # 输入子级节点标题
        self.input_node_title(title)
        # 输入子级节点描述
        self.input_node_description(description)
        # 点击确定按钮
        self.click_add_node_confirm_button()
        # 断言添加子级节点成功
        result = self.assert_add_node_success()
        log.info(f"添加子级节点结果：{result}")
        # 切回顶层文档
        self.switch_out_iframe()
        return result
