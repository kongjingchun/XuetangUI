# encoding: utf-8
# @File  : training_program_revision_page.py
# @Author:
# @Date  :
# @Desc  : 培养方案修订页面对象类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class TrainingProgramRevisionPage(BasePage):
    """培养方案修订页面类。

    对外只暴露“服务方法”（如更新专业信息、培养目标、毕业要求、目标支撑、课程体系、课程支撑等），
    不暴露每个按钮/输入框的 click/input 封装。定位器与 getter 集中维护，服务内部直接使用。
    涵盖 5 个子页：专业信息、培养目标、毕业要求、课程体系、课程支撑。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 培养方案修订所在 iframe（与培养方案管理同源）
    TRAINING_PROGRAM_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2102']")
    # 保存按钮
    SAVE_BUTTON = (By.XPATH, "//button[contains(.,'保存')]")
    # 取消按钮
    CANCEL_BUTTON = (By.XPATH, "//button[contains(.,'取消')]")
    # 完成编辑按钮
    COMPLETE_EDIT_BUTTON = (By.XPATH, "//button[contains(.,'完成编辑')]")

    # ======================专业信息======================
    # 专业描述输入框
    MAJOR_DESCRIPTION_INPUT = (By.XPATH, "//textarea[contains(@placeholder,'专业概述')]")

    # ======================培养目标======================
    # 培养目标概述文本域
    TRAINING_OBJECTIVE_OVERVIEW_TEXTAREA = (By.XPATH, "//textarea[contains(@placeholder,'培养目标概述') or contains(@placeholder,'请输入培养目标概述')]")
    # 添加目标按钮
    ADD_TRAINING_OBJECTIVE_BUTTON = (By.XPATH, "//button[contains(.,'添加目标')]")
    # 培养目标描述文本域
    TRAINING_OBJECTIVE_DESCRIPTION_TEXTAREA = (By.XPATH, "//textarea[contains(@placeholder,'培养目标描述') or contains(@placeholder,'请输入培养目标描述')]")
    # 培养目标弹窗保存按钮
    TRAINING_OBJECTIVE_SAVE_BUTTON = (By.XPATH, "//div[./button[contains(.,'取消')]]/button[contains(.,'保存')]")

    # ======================毕业要求======================
    # 毕业要求概述文本域
    GRADUATION_REQUIREMENT_DESCRIPTION_TEXTAREA = (By.XPATH, "//textarea[contains(@placeholder,'毕业要求概述')]")
    # 添加指标点按钮
    ADD_INDICATOR_POINT_BUTTON = (By.XPATH, "//button[contains(.,'添加指标点')]")

    # ======================课程体系======================
    # 添加课程按钮
    ADD_COURSE_BUTTON = (By.XPATH, "//span[text()=' 添加课程 ']/parent::button")
    # 课程搜索输入框
    COURSE_SEARCH_INPUT = (By.XPATH, "//div[@aria-label='选择课程']//input[@placeholder='搜索课程名称或代码']")
    # 确认添加课程按钮
    CONFIRM_ADD_COURSE_BUTTON = (By.XPATH, "//div[@aria-label='选择课程']//button[contains(.,'确认添加')]")

    # ======================课程支撑======================
    # 课程支撑确定按钮
    COURSE_SUPPORT_CONFIRM_BUTTON = (By.XPATH, "//span[text()='确定']/parent::button")

    # ==================== 动态定位器 getter ====================

    def get_revision_tab_locator(self, tab_name):
        """标签页名称（如专业信息、培养目标、毕业要求、目标支撑、课程体系、课程支撑）→ 标签页定位器。"""
        return (By.XPATH, f"//span[text()='{tab_name}']/parent::div")

    def get_save_success_message_locator(self, content="保存成功"):
        """提示文案（默认“保存成功”）→ 保存成功提示定位器。"""
        return (By.XPATH, f"//p[contains(.,'{content}')]")

    def get_indicator_point_name_input_locator(self, indicator_index=1):
        """指标点序号（从 1 开始）→ 该指标点名称输入框定位器。"""
        return (By.XPATH, f"//div[@class = 'requirements-list']/div[{indicator_index}]//input[@placeholder='指标点名称']")

    def get_indicator_point_description_textarea_locator(self, indicator_index=1):
        """指标点序号（从 1 开始）→ 该指标点描述文本域定位器。"""
        return (By.XPATH, f"//div[@class = 'requirements-list']/div[{indicator_index}]//textarea[contains(@placeholder,'指标点')]")

    def get_expand_button_locator(self, indicator_index=1):
        """指标点序号（从 1 开始）→ 该指标点展开按钮定位器。"""
        return (By.XPATH, f"//div[@class = 'requirements-list']/div[{indicator_index}]//button[contains(.,'展开')]")

    def get_add_decomposed_indicator_point_button_locator(self, indicator_index=1):
        """指标点序号（从 1 开始）→ 该指标点「添加分解指标点」按钮定位器。"""
        return (By.XPATH, f"//div[@class = 'requirements-list']/div[{indicator_index}]//button[contains(.,'添加分解指标点')]")

    def get_decomposed_indicator_point_name_input_locator(self, indicator_index=1, decomposed_index=1):
        """指标点序号、分解指标点序号（从 1 开始）→ 分解指标点名称输入框定位器。"""
        return (By.XPATH, f"//div[@class = 'requirements-list']/div[{indicator_index}]//div[@class='sub-requirements-list']/div[{decomposed_index}]//input[@placeholder='分解指标点名称']")

    def get_decomposed_indicator_point_description_textarea_locator(self, indicator_index=1, decomposed_index=1):
        """指标点序号、分解指标点序号（从 1 开始）→ 分解指标点描述文本域定位器。"""
        return (By.XPATH, f"//div[@class = 'requirements-list']/div[{indicator_index}]//div[@class='sub-requirements-list']/div[{decomposed_index}]//textarea[contains(@placeholder,'分解指标点')]")

    def get_target_support_select_button_locator(self, index=1):
        """选择按钮序号（从 1 开始）→ 目标支撑选择按钮定位器。"""
        return (By.XPATH, f"(//span[text()='选择'])[{index}]")

    def get_target_support_level_option_locator(self, level="高支撑"):
        """支撑等级（高支撑/中支撑/低支撑/无支撑）→ 目标支撑等级选项定位器。"""
        return (By.XPATH, f"//div[@aria-hidden='false']//span[contains(.,'{level}')]")

    def get_course_checkbox_by_name_locator(self, course_name):
        """课程名称 → 选择课程弹窗中该课程复选框定位器。"""
        return (By.XPATH, f"//div[@aria-label='选择课程']//tr[contains(.,'{course_name}')]//span[@class='el-checkbox__inner']")

    def get_associate_course_button_locator(self, index=1):
        """按钮序号（从 1 开始）→ 关联课程按钮定位器。"""
        return (By.XPATH, f"(//button[contains(.,'关联课程')])[{index}]")

    def get_course_support_checkbox_by_name_locator(self, course_name):
        """课程名称 → 课程支撑弹窗中该课程复选框定位器。"""
        return (By.XPATH, f"//div[@aria-label='课程管理']//tr[contains(.,'{course_name}')]//span[@class='el-checkbox__inner']")

    def get_course_support_level_option_locator(self, index=1, level="H"):
        """选择按钮序号、支撑等级（H/M/L）→ 课程支撑等级选项定位器。"""
        return (By.XPATH, f"//div[@class='requirements-tree']/div[{index}]//span[contains(.,'{level}')]")

    # ==================== 服务方法（页面对外能力） ====================

    def update_major_info(self, description=None):
        """更新专业信息（填写专业描述并保存），返回是否出现保存成功提示。"""
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)  # 切入培养方案修订 iframe
        self.click(self.get_revision_tab_locator("专业信息"), timeout=10)  # 点击专业信息标签
        if description is not None:
            self.input_text(self.MAJOR_DESCRIPTION_INPUT, description)  # 输入专业描述
        self.click(self.SAVE_BUTTON, timeout=10)  # 点击保存
        result = self.is_displayed(self.get_save_success_message_locator())  # 检查是否出现保存成功提示
        log.info(f"更新专业信息结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def update_training_objective(self, overview=None, description=None):
        """更新培养目标（概述、添加目标并填写描述后保存），返回是否出现保存成功提示。"""
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)  # 切入培养方案修订 iframe
        self.click(self.get_revision_tab_locator("培养目标"), timeout=10)  # 点击培养目标标签
        if overview is not None:
            self.input_text(self.TRAINING_OBJECTIVE_OVERVIEW_TEXTAREA, overview)  # 输入培养目标概述
        self.click(self.SAVE_BUTTON, timeout=10)  # 点击保存
        self.click(self.ADD_TRAINING_OBJECTIVE_BUTTON, timeout=10)  # 点击添加目标
        if description is not None:
            self.input_text(self.TRAINING_OBJECTIVE_DESCRIPTION_TEXTAREA, description)  # 输入培养目标描述
        self.click(self.TRAINING_OBJECTIVE_SAVE_BUTTON, timeout=10)  # 点击目标弹窗保存
        self.click(self.SAVE_BUTTON, timeout=10)  # 点击保存
        result = self.is_displayed(self.get_save_success_message_locator())  # 检查是否出现保存成功提示
        log.info(f"更新培养目标结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def update_graduation_requirement(
        self,
        description=None,
        indicator_index=1,
        indicator_name=None,
        indicator_description=None,
        decomposed_indicator_index=1,
        decomposed_indicator_name=None,
        decomposed_indicator_description=None,
    ):
        """更新毕业要求（概述、指标点及分解指标点），返回是否出现保存成功提示。"""
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)  # 切入培养方案修订 iframe
        self.click(self.get_revision_tab_locator("毕业要求"), timeout=10)  # 点击毕业要求标签
        if description is not None:
            self.input_text(self.GRADUATION_REQUIREMENT_DESCRIPTION_TEXTAREA, description)  # 输入毕业要求概述
        self.click(self.ADD_INDICATOR_POINT_BUTTON, timeout=10)  # 点击添加指标点
        if indicator_name is not None:
            self.input_text(self.get_indicator_point_name_input_locator(indicator_index), indicator_name)  # 输入指标点名称
        if indicator_description is not None:
            self.input_text(self.get_indicator_point_description_textarea_locator(indicator_index), indicator_description)  # 输入指标点描述
        self.click(self.get_expand_button_locator(indicator_index), timeout=10)  # 展开该指标点
        self.click(self.get_add_decomposed_indicator_point_button_locator(indicator_index), timeout=10)  # 点击添加分解指标点
        if decomposed_indicator_name is not None:
            self.input_text(
                self.get_decomposed_indicator_point_name_input_locator(indicator_index, decomposed_indicator_index),
                decomposed_indicator_name,
            )  # 输入分解指标点名称
        if decomposed_indicator_description is not None:
            self.input_text(
                self.get_decomposed_indicator_point_description_textarea_locator(indicator_index, decomposed_indicator_index),
                decomposed_indicator_description,
            )  # 输入分解指标点描述
        self.click(self.SAVE_BUTTON, timeout=10)  # 点击保存
        result = self.is_displayed(self.get_save_success_message_locator())  # 检查是否出现保存成功提示
        log.info(f"更新毕业要求结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def update_target_support(self, index=1, level="高支撑"):
        """更新目标支撑（选择第 index 个选择按钮并设为指定等级），返回是否出现保存成功提示。"""
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)  # 切入培养方案修订 iframe
        self.click(self.get_revision_tab_locator("目标支撑"), timeout=10)  # 点击目标支撑标签
        self.click(self.get_target_support_select_button_locator(index), timeout=10)  # 点击第 index 个选择按钮
        self.click(self.get_target_support_level_option_locator(level), timeout=10)  # 选择支撑等级
        self.click(self.SAVE_BUTTON, timeout=10)  # 点击保存
        result = self.is_displayed(self.get_save_success_message_locator())  # 检查是否出现保存成功提示
        log.info(f"更新目标支撑结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def update_course_system(self, course_name):
        """更新课程体系（添加课程并确认），返回是否出现成功添加提示。"""
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)  # 切入培养方案修订 iframe
        self.click(self.get_revision_tab_locator("课程体系"), timeout=10)  # 点击课程体系标签
        self.click(self.ADD_COURSE_BUTTON, timeout=10)  # 点击添加课程
        self.input_text(self.COURSE_SEARCH_INPUT, course_name)  # 输入课程名称搜索
        self.click(self.get_course_checkbox_by_name_locator(course_name), timeout=10)  # 勾选该课程
        self.click(self.CONFIRM_ADD_COURSE_BUTTON, timeout=10)  # 点击确认添加
        result = self.is_displayed(self.get_save_success_message_locator("成功添加"))  # 检查是否出现成功添加提示
        log.info(f"更新课程体系结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result

    def update_course_support(self, index=1, course_name=None, level="H"):
        """更新课程支撑（第 1 个关联课程入口选课并确定，再设置第 index 个支撑等级为 level，完成编辑），返回是否出现编辑完成提示。"""
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)  # 切入培养方案修订 iframe
        self.click(self.get_revision_tab_locator("课程支撑"), timeout=10)  # 点击课程支撑标签
        self.click(self.get_associate_course_button_locator(1), timeout=10)  # 点击第一个关联课程入口
        self.click(self.get_course_support_checkbox_by_name_locator(course_name), timeout=10)  # 勾选该课程
        self.click(self.COURSE_SUPPORT_CONFIRM_BUTTON, timeout=10)  # 点击确定
        self.click(self.get_course_support_level_option_locator(index=index, level=level), timeout=10)  # 选择支撑等级
        self.click(self.COMPLETE_EDIT_BUTTON, timeout=10)  # 点击完成编辑
        result = self.is_displayed(self.get_save_success_message_locator("编辑完成"))  # 检查是否出现编辑完成提示
        log.info(f"更新课程支撑结果：{result}")
        self.switch_out_iframe()  # 切回默认上下文
        return result
