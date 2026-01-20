# encoding: utf-8
# @File  : MajorGraphModelPage.py
# @Author: 孔敬淳
# @Date  : 2025/12/31
# @Desc  : 专业图谱模型页面对象类，封装专业图谱模型相关的页面操作方法
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class MajorGraphModelPage(BasePage):
    """专业图谱模型页面类

    继承BasePage类，提供专业图谱模型页面元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化专业图谱模型页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # 专业AI模型iframe
    MAJOR_AI_MODEL_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2110']")

    # ==================== 专业图谱概览元素定位器 ==============================================================

    # 创建专业图谱按钮
    CREATE_MAJOR_GRAPH_BUTTON = (By.XPATH, "//button[./span[contains(.,'创建专业图谱')]]")
    # 创建图谱名称输入框
    CREATE_MAJOR_GRAPH_INPUT = (By.XPATH, "//input[@placeholder='请输入图谱名称']")
    # 创建图谱创建按钮
    CREATE_MAJOR_GRAPH_CONFIRM_BUTTON = (By.XPATH, "//div[@aria-label='创建专业图谱']//button[./span[contains(.,'创建')]]")
    # 节点标题输入框
    NODE_TITLE_INPUT = (By.XPATH, "//div[@aria-label='添加节点']//input[contains(@placeholder,'节点标题')]")
    # 添加节点按钮
    ADD_NODE_BUTTON = (By.XPATH, "//div[@aria-label='添加节点']//button[contains(.,'添加')]")
    # 关联确定按钮
    ASSOCIATE_CONFIRM_BUTTON = (By.XPATH, "//button[contains(.,'确定')]")

    # ==================== 专业图谱概览动态定位器方法（需要参数的定位器）==============================================================

    def get_menu_locator(self, menu_name):
        """获取根据菜单名称定位菜单的定位器

        Args:
            menu_name: 菜单名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//span[text()='{menu_name}']/parent::li")

    def get_add_major_node_button_locator(self, node_type):
        """获取专业节点添加按钮的定位器

        Args:
            node_type: 节点类型，可选值：'能力'、'知识'、'素质'、'问题'

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        if '能力' in node_type:
            return (By.XPATH, "//h4[text()='专业能力节点']/following-sibling::div/button")
        elif '知识' in node_type:
            return (By.XPATH, "//h4[text()='专业知识节点']/following-sibling::div/button")
        elif '素质' in node_type:
            return (By.XPATH, "//h4[text()='专业素质节点']/following-sibling::div/button")
        elif '问题' in node_type:
            return (By.XPATH, "//h4[text()='专业问题节点']/following-sibling::div/button")
        else:
            return (By.XPATH, "//h4[text()='专业能力节点']/following-sibling::div/button")

    def get_node_locator(self, node_name):
        """获取根据节点名称定位节点的定位器

        Args:
            node_name: 节点名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//div[text()='{node_name}']")

    def get_associate_node_button_locator(self, node_name):
        """获取根据节点名称定位关联按钮的定位器

        Args:
            node_name: 节点名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//div[contains(@class,'node-list') and contains(.,'{node_name}')]//button[2]")

    def get_associate_node_category_locator(self, node_name):
        """获取根据节点名称定位关联分类的定位器

        Args:
            node_name: 节点名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        if '能力' in node_name:
            return (By.XPATH, "//span[text()='专业能力节点']//parent::button")
        elif '知识' in node_name:
            return (By.XPATH, "//span[text()='专业知识节点']//parent::button")
        elif '素质' in node_name:
            return (By.XPATH, "//span[text()='专业素质节点']//parent::button")
        elif '问题' in node_name:
            return (By.XPATH, "//span[text()='专业问题节点']//parent::button")
        else:
            return (By.XPATH, "//span[text()='专业能力节点']//parent::button")

    def get_checkbox_locator(self, node_name):
        """获取根据节点名称定位复选框的定位器

        Args:
            node_name: 节点名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//label[contains(.,'{node_name}')]/span[1]")

    # ==================== 专业图谱概览页面操作方法 ==============================================================  ==============================================================

    def click_menu_by_name(self, menu_name):
        """根据菜单名称点击菜单

        Args:
            menu_name: 菜单名称

        Returns:
            点击操作结果
        """
        # 切换到专业AI模型iframe
        self.switch_to_iframe(self.MAJOR_AI_MODEL_IFRAME)
        # 根据菜单名称点击菜单
        locator = self.get_menu_locator(menu_name)
        log.info(f"点击菜单：{menu_name}，定位器为：{locator[1]}")
        result = self.click(locator)
        # 切出专业AI模型iframe
        self.switch_out_iframe()
        return result

    # ==================== 专业图谱概览操作方法 ==============================================================

    def click_create_major_graph_button(self):
        """点击创建专业图谱按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击创建专业图谱按钮，定位器为：{self.CREATE_MAJOR_GRAPH_BUTTON[1]}")
        return self.click(self.CREATE_MAJOR_GRAPH_BUTTON)

    def input_create_major_graph_input(self, graph_name):
        """输入创建图谱名称

        Args:
            graph_name: 图谱名称

        Returns:
            输入操作结果
        """
        log.info(f"输入创建图谱名称：{graph_name}，定位器为：{self.CREATE_MAJOR_GRAPH_INPUT[1]}")
        return self.input_text(self.CREATE_MAJOR_GRAPH_INPUT, graph_name)

    def click_create_major_graph_confirm_button(self):
        """点击创建图谱确认按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击创建图谱确认按钮，定位器为：{self.CREATE_MAJOR_GRAPH_CONFIRM_BUTTON[1]}")
        return self.click(self.CREATE_MAJOR_GRAPH_CONFIRM_BUTTON)

    def click_add_major_node_button(self, node_type):
        """点击专业节点添加按钮（通用方法）

        Args:
            node_type: 节点类型，可选值：'能力'、'知识'、'素质'、'问题'

        Returns:
            点击操作结果
        """
        locator = self.get_add_major_node_button_locator(node_type)
        log.info(f"点击专业{node_type}节点添加按钮，定位器为：{locator[1]}")
        return self.click(locator)

    def input_node_title_input(self, node_title):
        """输入节点标题

        Args:
            node_title: 节点标题

        Returns:
            输入操作结果
        """
        log.info(f"输入节点标题：{node_title}，定位器为：{self.NODE_TITLE_INPUT[1]}")
        return self.input_text(self.NODE_TITLE_INPUT, node_title)

    def click_add_node_button(self):
        """点击添加节点按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击添加节点按钮，定位器为：{self.ADD_NODE_BUTTON[1]}")
        return self.click(self.ADD_NODE_BUTTON)

    def hover_node_by_name(self, node_name):
        """鼠标悬停到节点名称

        Args:
            node_name: 节点名称

        Returns:
            悬停操作结果
        """
        locator = self.get_node_locator(node_name)
        log.info(f"鼠标悬停到节点名称'{node_name}'，定位器为：{locator[1]}")
        return self.hover(locator)

    def click_associate_node_button_by_name(self, node_name):
        """根据节点名称点击关联按钮

        Args:
            node_name: 节点名称

        Returns:
            点击操作结果
        """
        locator = self.get_associate_node_button_locator(node_name)
        log.info(f"根据节点名称'{node_name}'点击关联按钮，定位器为：{locator[1]}")
        return self.click(locator)

    def click_associate_node_category_by_name(self, node_name):
        """根据节点名称点击关联分类

        Args:
            node_name: 节点名称

        Returns:
            点击操作结果
        """
        locator = self.get_associate_node_category_locator(node_name)
        log.info(f"根据节点名称'{node_name}'点击关联分类，定位器为：{locator[1]}")
        return self.click(locator)

    def click_checkbox_by_name(self, node_name):
        """根据节点名称点击复选框

        Args:
            node_name: 节点名称

        Returns:
            点击操作结果
        """
        locator = self.get_checkbox_locator(node_name)
        log.info(f"根据节点名称'{node_name}'点击复选框，定位器为：{locator[1]}")
        return self.click(locator)

    def click_associate_confirm_button(self):
        """点击关联确定按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击关联确定按钮，定位器为：{self.ASSOCIATE_CONFIRM_BUTTON[1]}")
        return self.click(self.ASSOCIATE_CONFIRM_BUTTON)

    def create_major_graph_overview(self):
        """创建专业图谱概览流程

        Returns:
            bool: True表示创建成功，False表示创建失败
        """
        # 切换到专业AI模型iframe
        self.switch_to_iframe(self.MAJOR_AI_MODEL_IFRAME)
        # 点击创建专业图谱按钮
        self.click_create_major_graph_button()
        # 输入图谱名称
        self.input_create_major_graph_input("测试图谱")
        # 点击创建确认按钮
        self.click_create_major_graph_confirm_button()
        # 点击专业能力节点添加按钮
        self.click_add_major_node_button("能力")
        # 输入节点标题
        self.input_node_title_input("测试能力节点")
        # 点击添加节点按钮
        self.click_add_node_button()
        # 点击专业知识节点添加按钮
        self.click_add_major_node_button("知识")
        # 输入节点标题
        self.input_node_title_input("测试知识节点")
        # 点击添加节点按钮
        self.click_add_node_button()
        # 点击专业素质节点添加按钮
        self.click_add_major_node_button("素质")
        # 输入节点标题
        self.input_node_title_input("测试素质节点")
        # 点击添加节点按钮
        self.click_add_node_button()
        # 点击专业问题节点添加按钮
        self.click_add_major_node_button("问题")
        # 输入节点标题
        self.input_node_title_input("测试问题节点")
        # 点击添加节点按钮
        self.click_add_node_button()
        # 鼠标悬停到测试能力节点
        self.hover_node_by_name("测试能力节点")
        # 点击测试能力节点关联按钮
        self.click_associate_node_button_by_name("测试能力节点")
        # 点击测试能力节点关联分类
        self.click_associate_node_category_by_name("知识")
        # 点击测试知识节点复选框
        self.click_checkbox_by_name("测试知识节点")
        # 点击测试知识节点关联确定按钮
        self.click_associate_confirm_button()
        # 鼠标悬停到测试素质节点
        self.hover_node_by_name("测试素质节点")
        # 点击测试素质节点关联按钮
        self.click_associate_node_button_by_name("测试素质节点")
        # 点击测试素质节点关联分类
        self.click_associate_node_category_by_name("问题")
        # 点击测试问题节点复选框
        self.click_checkbox_by_name("测试问题节点")
        # 点击测试问题节点关联确定按钮
        result = self.click_associate_confirm_button()
        # 切出专业AI模型iframe
        self.switch_out_iframe()
        log.info(f"创建专业图谱概览结果：{result}")
        return result

    # ==================== 专业课程群图谱元素定位 ==============================================================
    # 专业AI模型iframe
    MAJOR_AI_MODEL_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2110']")
    # 编辑图谱按钮
    EDIT_GRAPH_BUTTON = (By.XPATH, "//span[contains(.,'编辑图谱')]/parent::button")
    # 关联图谱成功提示框
    ASSOCIATE_GRAPH_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='关联图谱成功']")

    # ==================== 专业课程群图谱页面操作方法 ==============================================================
    def click_edit_graph_button(self):
        """点击编辑图谱按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击编辑图谱按钮，定位器为：{self.EDIT_GRAPH_BUTTON[1]}")
        return self.click(self.EDIT_GRAPH_BUTTON)
    # ==================== 群图谱管理元素定位 ==============================================================
    # 关联图谱按钮
    ASSOCIATE_GRAPH_BUTTON = (By.XPATH, "//span[contains(.,'关联图谱')]/parent::button")
    # 确定关联按钮
    CONFIRM_ASSOCIATE_GRAPH_BUTTON = (By.XPATH, "//span[contains(.,'确定关联')]/parent::button")

    def get_graph_checkbox_locator_by_name(self, graph_name):
        """根据图谱名称返回复选框的定位器

        Args:
            graph_name: 图谱名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, f"//tr[contains(.,'{graph_name}')]//span[@class='el-checkbox__inner']")

    # ==================== 群图谱管理操作方法 ==============================================================

    def click_associate_graph_button(self):
        """点击关联图谱按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击关联图谱按钮，定位器为：{self.ASSOCIATE_GRAPH_BUTTON[1]}")
        return self.click(self.ASSOCIATE_GRAPH_BUTTON)

    def click_graph_checkbox_by_name(self, graph_name):
        """根据图谱名称点击复选框

        Args:
            graph_name: 图谱名称

        Returns:
            点击操作结果
        """
        locator = self.get_graph_checkbox_locator_by_name(graph_name)
        log.info(f"根据图谱名称'{graph_name}'点击复选框，定位器为：{locator[1]}")
        return self.click(locator)

    def click_confirm_associate_graph_button(self):
        """点击确定关联按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击确定关联按钮，定位器为：{self.CONFIRM_ASSOCIATE_GRAPH_BUTTON[1]}")
        return self.click(self.CONFIRM_ASSOCIATE_GRAPH_BUTTON)

    def assert_associate_graph_success(self):
        """断言关联图谱成功

        Returns:
            断言操作结果
        """
        log.info(f"断言关联图谱成功，定位器为：{self.ASSOCIATE_GRAPH_SUCCESS_MESSAGE[1]}")
        return self.is_displayed(self.ASSOCIATE_GRAPH_SUCCESS_MESSAGE)

    def associate_graph(self, graph_name):
        """关联图谱

        Args:
            graph_name: 图谱名称

        Returns:
            关联操作结果
        """
        # 切换到专业AI模型iframe
        self.switch_to_iframe(self.MAJOR_AI_MODEL_IFRAME)
        # 点击编辑图谱按钮
        self.click_edit_graph_button()
        # 点击关联图谱按钮
        self.click_associate_graph_button()
        # 根据图谱名称点击复选框
        self.click_graph_checkbox_by_name(graph_name)
        # 点击确定关联按钮
        self.click_confirm_associate_graph_button()
        # 断言关联图谱成功
        result = self.assert_associate_graph_success()
        # 切出专业AI模型iframe
        self.switch_out_iframe()
        log.info(f"关联图谱结果：{result}")
        return result
