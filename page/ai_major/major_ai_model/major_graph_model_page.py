# encoding: utf-8
# @File  : major_graph_model_page.py
# @Author:
# @Date  :
# @Desc  : 专业图谱模型页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class MajorGraphModelPage(BasePage):
    """专业图谱模型页面类。

    对外只暴露“服务方法”（如按菜单名进入子页、创建专业图谱概览、关联图谱等），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 专业AI模型主内容区域 iframe（与 major_ai_model 同源）
    MAJOR_AI_MODEL_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2110']")

    # ======================专业图谱概览======================
    # 创建专业图谱按钮
    CREATE_MAJOR_GRAPH_BUTTON = (By.XPATH, "//button[./span[contains(.,'创建专业图谱')]]")
    # 创建图谱名称输入框
    CREATE_MAJOR_GRAPH_INPUT = (By.XPATH, "//input[@placeholder='请输入图谱名称']")
    # 创建图谱弹窗中的创建按钮
    CREATE_MAJOR_GRAPH_CONFIRM_BUTTON = (By.XPATH, "//div[@aria-label='创建专业图谱']//button[./span[contains(.,'创建')]]")
    # 添加节点弹窗中的节点标题输入框
    NODE_TITLE_INPUT = (By.XPATH, "//div[@aria-label='添加节点']//input[contains(@placeholder,'节点标题')]")
    # 添加节点弹窗中的添加按钮
    ADD_NODE_BUTTON = (By.XPATH, "//div[@aria-label='添加节点']//button[contains(.,'添加')]")
    # 关联弹窗中的确定按钮
    ASSOCIATE_CONFIRM_BUTTON = (By.XPATH, "//button[contains(.,'确定')]")

    # ======================专业课程群图谱======================
    # 编辑图谱按钮
    EDIT_GRAPH_BUTTON = (By.XPATH, "//span[contains(.,'编辑图谱')]/parent::button")
    # 关联图谱成功 toast 文案
    ASSOCIATE_GRAPH_SUCCESS_MESSAGE = (By.XPATH, "//p[text()='关联图谱成功']")
    # 关联图谱按钮
    ASSOCIATE_GRAPH_BUTTON = (By.XPATH, "//span[contains(.,'关联图谱')]/parent::button")
    # 确定关联按钮
    CONFIRM_ASSOCIATE_GRAPH_BUTTON = (By.XPATH, "//span[contains(.,'确定关联')]/parent::button")

    # ==================== 动态定位器 getter ====================

    def get_menu_locator(self, menu_name):
        """菜单名称（如专业图谱概览、专业课程群图谱）→ 左侧菜单项定位器。"""
        return (By.XPATH, f"//span[text()='{menu_name}']/parent::li")

    def get_add_major_node_button_locator(self, node_type):
        """节点类型（能力/知识/素质/问题）→ 该类型节点「添加」按钮定位器。"""
        mapping = {
            '能力': "//h4[text()='专业能力节点']/following-sibling::div/button",
            '知识': "//h4[text()='专业知识节点']/following-sibling::div/button",
            '素质': "//h4[text()='专业素质节点']/following-sibling::div/button",
            '问题': "//h4[text()='专业问题节点']/following-sibling::div/button",
        }
        xpath = mapping.get(node_type, "//h4[text()='专业能力节点']/following-sibling::div/button")
        return (By.XPATH, xpath)

    def get_node_locator(self, node_name):
        """节点名称 → 图谱上的节点定位器。"""
        return (By.XPATH, f"//div[text()='{node_name}']")

    def get_associate_node_button_locator(self, node_name):
        """节点名称 → 该节点所在行的「关联」按钮定位器。"""
        return (By.XPATH, f"//div[contains(@class,'node-list') and contains(.,'{node_name}')]//button[2]")

    def get_associate_node_category_locator(self, category_name):
        """关联分类名称（能力/知识/素质/问题）→ 关联弹窗中该分类按钮定位器。"""
        mapping = {
            '能力': "//span[text()='专业能力节点']//parent::button",
            '知识': "//span[text()='专业知识节点']//parent::button",
            '素质': "//span[text()='专业素质节点']//parent::button",
            '问题': "//span[text()='专业问题节点']//parent::button",
        }
        for k, v in mapping.items():
            if k in category_name:
                return (By.XPATH, v)
        return (By.XPATH, "//span[text()='专业能力节点']//parent::button")

    def get_checkbox_locator(self, node_name):
        """节点名称 → 关联弹窗中该节点对应复选框定位器。"""
        return (By.XPATH, f"//label[contains(.,'{node_name}')]/span[1]")

    def get_graph_checkbox_locator(self, graph_name):
        """图谱名称 → 关联图谱弹窗中该图谱行复选框定位器。"""
        return (By.XPATH, f"//tr[contains(.,'{graph_name}')]//span[@class='el-checkbox__inner']")

    # ==================== 服务方法（页面对外能力） ====================

    def click_menu_by_name(self, menu_name):
        """按菜单名称点击左侧菜单项进入对应子页，返回是否点击成功。"""
        self.switch_to_iframe(self.MAJOR_AI_MODEL_IFRAME)  # 切入专业AI模型 iframe
        locator = self.get_menu_locator(menu_name)  # 获取菜单项定位器
        log.info(f"点击菜单：{menu_name}，定位器为：{locator[1]}")
        result = self.click(locator)  # 点击菜单项
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def create_major_graph_overview(self):
        """创建专业图谱概览：新建图谱，依次添加能力/知识/素质/问题四类节点，并建立能力→知识、素质→问题关联。返回最后一步点击是否成功。"""
        self.switch_to_iframe(self.MAJOR_AI_MODEL_IFRAME)  # 切入专业AI模型 iframe

        self.click(self.CREATE_MAJOR_GRAPH_BUTTON)  # 点击创建专业图谱
        self.input_text(self.CREATE_MAJOR_GRAPH_INPUT, "测试图谱")  # 输入图谱名称
        self.click(self.CREATE_MAJOR_GRAPH_CONFIRM_BUTTON)  # 点击创建确认

        for node_type, title in [("能力", "测试能力节点"), ("知识", "测试知识节点"), ("素质", "测试素质节点"), ("问题", "测试问题节点")]:
            self.click(self.get_add_major_node_button_locator(node_type))  # 点击该类型添加节点
            self.input_text(self.NODE_TITLE_INPUT, title)  # 输入节点标题
            self.click(self.ADD_NODE_BUTTON)  # 点击添加节点

        self.hover(self.get_node_locator("测试能力节点"))  # 悬停到能力节点
        self.click(self.get_associate_node_button_locator("测试能力节点"))  # 点击关联按钮
        self.click(self.get_associate_node_category_locator("知识"))  # 选择知识分类
        self.click(self.get_checkbox_locator("测试知识节点"))  # 勾选知识节点
        self.click(self.ASSOCIATE_CONFIRM_BUTTON)  # 点击确定

        self.hover(self.get_node_locator("测试素质节点"))  # 悬停到素质节点
        self.click(self.get_associate_node_button_locator("测试素质节点"))  # 点击关联按钮
        self.click(self.get_associate_node_category_locator("问题"))  # 选择问题分类
        self.click(self.get_checkbox_locator("测试问题节点"))  # 勾选问题节点
        result = self.click(self.ASSOCIATE_CONFIRM_BUTTON)  # 点击确定

        log.info(f"创建专业图谱概览结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def associate_graph(self, graph_name):
        """在专业课程群图谱下关联指定名称的图谱，返回是否出现「关联图谱成功」提示。"""
        self.switch_to_iframe(self.MAJOR_AI_MODEL_IFRAME)  # 切入专业AI模型 iframe
        self.click(self.EDIT_GRAPH_BUTTON)  # 点击编辑图谱
        self.click(self.ASSOCIATE_GRAPH_BUTTON)  # 点击关联图谱
        self.click(self.get_graph_checkbox_locator(graph_name))  # 勾选指定图谱
        self.click(self.CONFIRM_ASSOCIATE_GRAPH_BUTTON)  # 点击确定关联
        result = self.is_displayed(self.ASSOCIATE_GRAPH_SUCCESS_MESSAGE)  # 检查是否出现关联成功提示
        log.info(f"关联图谱结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result
