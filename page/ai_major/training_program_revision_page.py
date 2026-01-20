# encoding: utf-8
# @File  : TrainingProgramRevisionPage.py
# @Author: 孔敬淳
# @Date  : 2025/12/31
# @Desc  : 培养方案修订页面对象类，封装培养方案修订相关的页面操作方法

from time import sleep
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from logs.log import log


class TrainingProgramRevisionPage(BasePage):
    """培养方案修订页面类

    继承BasePage类，提供培养方案修订页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    包含5个子页面：专业信息、培养目标、毕业要求、课程体系、课程支撑
    """

    def __init__(self, driver):
        """初始化培养方案修订页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
    # 培养方案管理iframe
    TRAINING_PROGRAM_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2102']")
    # 保存按钮
    SAVE_BUTTON = (By.XPATH, "//button[contains(.,'保存')]")
    # 取消按钮
    CANCEL_BUTTON = (By.XPATH, "//button[contains(.,'取消')]")
    # 专业描述输入框
    MAJOR_DESCRIPTION_INPUT = (By.XPATH, "//textarea[contains(@placeholder,'专业概述')]")
    # 培养目标概述文本域
    TRAINING_OBJECTIVE_OVERVIEW_TEXTAREA = (By.XPATH, "//textarea[contains(@placeholder,'培养目标概述') or contains(@placeholder,'请输入培养目标概述')]")
    # 添加目标按钮
    ADD_TRAINING_OBJECTIVE_BUTTON = (By.XPATH, "//button[contains(.,'添加目标')]")
    # 培养目标描述文本域
    TRAINING_OBJECTIVE_DESCRIPTION_TEXTAREA = (By.XPATH, "//textarea[contains(@placeholder,'培养目标描述') or contains(@placeholder,'请输入培养目标描述')]")
    # 培养目标保存按钮
    TRAINING_OBJECTIVE_SAVE_BUTTON = (By.XPATH, "//div[./button[contains(.,'取消')]]/button[contains(.,'保存')]")
    # 毕业要求描述文本域
    GRADUATION_REQUIREMENT_DESCRIPTION_TEXTAREA = (By.XPATH, "//textarea[contains(@placeholder,'毕业要求概述')]")
    # 添加指标点按钮
    ADD_INDICATOR_POINT_BUTTON = (By.XPATH, "//button[contains(.,'添加指标点')]")
    # 添加课程按钮
    ADD_COURSE_BUTTON = (By.XPATH, "//span[text()=' 添加课程 ']/parent::button")
    # 课程搜索输入框
    COURSE_SEARCH_INPUT = (By.XPATH, "//div[@aria-label='选择课程']//input[@placeholder='搜索课程名称或代码']")
    # 确认添加课程按钮
    CONFIRM_ADD_COURSE_BUTTON = (By.XPATH, "//div[@aria-label='选择课程']//button[contains(.,'确认添加')]")
    # 课程支撑确认按钮
    COURSE_SUPPORT_CONFIRM_BUTTON = (By.XPATH, "//span[text()='确定']/parent::button")
    # 完成编辑按钮
    COMPLETE_EDIT_BUTTON = (By.XPATH, "//button[contains(.,'完成编辑')]")

    # ==================== 动态定位器方法（需要参数的定位器）====================

    def get_revision_tab_locator(self, tab_name):
        """获取修订页面标签页的定位器

        Args:
            tab_name: 标签页名称，如 '专业信息'、'培养目标'、'毕业要求'、'目标支撑'、'课程体系'、'课程支撑'

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//span[text()='" + tab_name + "']/parent::div")

    def get_save_success_alert_locator(self, content="保存成功"):
        """获取保存成功提示框的定位器

        Args:
            content: 提示框内容文本，默认为"保存成功"

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//p[contains(.,'" + content + "')]")

    def get_indicator_point_name_input_locator(self, indicator_index=1):
        """获取指标点名称输入框的定位器

        Args:
            indicator_index: 指标点序号，从1开始，默认为1（第1个指标点）

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@class = 'requirements-list']/div[" + str(indicator_index) + "]//input[@placeholder='指标点名称']")

    def get_indicator_point_description_textarea_locator(self, indicator_index=1):
        """获取指标点描述文本域的定位器

        Args:
            indicator_index: 指标点序号，从1开始，默认为1（第1个指标点）

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@class = 'requirements-list']/div[" + str(indicator_index) + "]//textarea[contains(@placeholder,'指标点')]")

    def get_expand_button_locator(self, indicator_index=1):
        """获取展开按钮的定位器

        Args:
            indicator_index: 指标点序号，从1开始，默认为1（第1个指标点）

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@class = 'requirements-list']/div[" + str(indicator_index) + "]//button[contains(.,'展开')]")

    def get_add_decomposed_indicator_point_button_locator(self, indicator_index=1):
        """获取添加分解指标点按钮的定位器

        Args:
            indicator_index: 指标点序号，从1开始，默认为1（第1个指标点）

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@class = 'requirements-list']/div[" + str(indicator_index) + "]//button[contains(.,'添加分解指标点')]")

    def get_decomposed_indicator_point_name_input_locator(self, indicator_index=1, decomposed_index=1):
        """获取分解指标点名称输入框的定位器

        Args:
            indicator_index: 指标点序号，从1开始，默认为1（第1个指标点）
            decomposed_index: 分解指标点序号，从1开始，默认为1（第1个分解指标点）

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@class = 'requirements-list']/div[" + str(indicator_index) + "]//div[@class='sub-requirements-list']/div[" + str(decomposed_index) + "]//input[@placeholder='分解指标点名称']")

    def get_decomposed_indicator_point_description_textarea_locator(self, indicator_index=1, decomposed_index=1):
        """获取分解指标点描述文本域的定位器

        Args:
            indicator_index: 指标点序号，从1开始，默认为1（第1个指标点）
            decomposed_index: 分解指标点序号，从1开始，默认为1（第1个分解指标点）

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@class = 'requirements-list']/div[" + str(indicator_index) + "]//div[@class='sub-requirements-list']/div[" + str(decomposed_index) + "]//textarea[contains(@placeholder,'分解指标点')]")

    def get_target_support_select_button_locator(self, index=1):
        """获取目标支撑选择按钮的定位器

        Args:
            index: 选择按钮序号，从1开始，默认为1（第1个选择按钮）

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "(//span[text()='选择'])[" + str(index) + "]")

    def get_target_support_level_option_locator(self, level="高支撑"):
        """获取目标支撑等级选项的定位器

        Args:
            level: 支撑等级，有高支撑、中支撑、低支撑无支撑4个选项

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@aria-hidden='false']//span[contains(.,'" + level + "')]")

    def get_add_course_button_locator(self):
        """获取添加课程按钮的定位器

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//span[text()=' 添加课程 ']/parent::button")

    def get_course_search_input_locator(self):
        """获取搜索课程名称或代码的搜索框的定位器

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@aria-label='选择课程']//input[@placeholder='搜索课程名称或代码']")

    def get_course_checkbox_by_name_locator(self, course_name):
        """获取根据课程名称定位复选框的定位器

        Args:
            course_name: 课程名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@aria-label='选择课程']//tr[contains(.,'" + course_name + "')]//span[@class='el-checkbox__inner']")

    def get_confirm_add_course_button_locator(self):
        """获取确认添加课程按钮的定位器

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@aria-label='选择课程']//button[contains(.,'确认添加')]")

    def get_associate_course_button_locator(self, index=1):
        """获取关联课程按钮的定位器

        Args:
            index: 按钮序号，从1开始，默认为1（第1个关联课程按钮）

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "(//button[contains(.,'关联课程')])[" + str(index) + "]")

    def get_course_support_checkbox_by_name_locator(self, course_name):
        """获取课程支撑页面根据课程名称定位复选框的定位器

        Args:
            course_name: 课程名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@aria-label='课程管理']//tr[contains(.,'" + course_name + "')]//span[@class='el-checkbox__inner']")

    def get_course_support_level_option_locator(self, index=1, level="H"):
        """获取课程支撑等级选项的定位器

        Args:
            index: 选择按钮序号，从1开始，默认为1（第1个选择按钮）
            level: 支撑等级，H表示高支撑，M表示中支撑，L表示低支撑

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[@class='requirements-tree']/div[" + str(index) + "]//span[contains(.,'" + level + "')]")

    # ==================== 页面操作方法 ====================

    def switch_out_training_program_manage_iframe(self):
        """从培养方案管理iframe切出

        Returns:
            切换操作结果
        """
        log.info("从培养方案管理iframe切出")
        return self.switch_out_iframe()

    def click_tab(self, tab_name):
        """点击标签页

        Args:
            tab_name: 标签页名称，如 '专业信息'、'培养目标'、'毕业要求'、'目标支撑'、'课程体系'、'课程支撑'

        Returns:
            点击操作结果
        """
        locator = self.get_revision_tab_locator(tab_name)
        log.info(f"点击标签页：{tab_name}，定位器为：{locator[1]}")
        return self.click(locator, timeout=10)

    def click_save_button(self):
        """点击保存按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击保存按钮，定位器为：{self.SAVE_BUTTON[1]}")
        return self.click(self.SAVE_BUTTON, timeout=10)

    def click_cancel_button(self):
        """点击取消按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击取消按钮，定位器为：{self.CANCEL_BUTTON[1]}")
        return self.click(self.CANCEL_BUTTON, timeout=10)

    def is_save_success_alert_display(self, content="保存成功"):
        """根据内容判断保存成功提示框是否出现

        Args:
            content: 提示框内容文本，默认为"保存成功"

        Returns:
            bool: True表示保存成功提示框出现，False表示未出现
        """
        locator = self.get_save_success_alert_locator(content)
        log.info(f"查看保存成功提示框是否出现，定位器为：{locator[1]}")
        return self.is_displayed(locator)

    # ==================== 专业信息页面操作方法 ====================
    def input_major_description(self, description):
        """输入专业描述

        Args:
            description: 专业描述内容

        Returns:
            输入操作结果
        """
        log.info(f"输入专业描述：{description}，定位器为：{self.MAJOR_DESCRIPTION_INPUT[1]}")
        return self.input_text(self.MAJOR_DESCRIPTION_INPUT, description)

    def update_major_info(self, description=None):
        """更新专业信息

        Args:
            description: 专业描述内容

        Returns:
            bool: True表示更新成功，False表示更新失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)

        # 点击专业信息标签页
        self.click_tab("专业信息")
        # 输入专业描述
        self.input_major_description(description)
        # 点击保存按钮
        self.click_save_button()
        # 断言保存成功提示框是否出现
        result = self.is_save_success_alert_display()

        # 切出iframe
        self.switch_out_training_program_manage_iframe()

        log.info(f"更新专业信息结果：{result}")
        return result

    # ==================== 培养目标页面操作方法 ====================
    def input_training_objective_overview(self, overview):
        """输入培养目标概述

        Args:
            overview: 培养目标概述内容

        Returns:
            输入操作结果
        """
        log.info(f"输入培养目标概述：{overview}，定位器为：{self.TRAINING_OBJECTIVE_OVERVIEW_TEXTAREA[1]}")
        return self.input_text(self.TRAINING_OBJECTIVE_OVERVIEW_TEXTAREA, overview)

    def click_add_training_objective_button(self):
        """点击添加目标按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击添加目标按钮，定位器为：{self.ADD_TRAINING_OBJECTIVE_BUTTON[1]}")
        return self.click(self.ADD_TRAINING_OBJECTIVE_BUTTON, timeout=10)

    def input_training_objective_description(self, description):
        """输入培养目标描述

        Args:
            description: 培养目标描述内容

        Returns:
            输入操作结果
        """
        log.info(f"输入培养目标描述：{description}，定位器为：{self.TRAINING_OBJECTIVE_DESCRIPTION_TEXTAREA[1]}")
        return self.input_text(self.TRAINING_OBJECTIVE_DESCRIPTION_TEXTAREA, description)

    def click_training_objective_save_button(self):
        """点击培养目标保存按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击培养目标保存按钮，定位器为：{self.TRAINING_OBJECTIVE_SAVE_BUTTON[1]}")
        return self.click(self.TRAINING_OBJECTIVE_SAVE_BUTTON, timeout=10)

    def update_training_objective(self, overview=None, description=None):
        """更新培养目标

        Args:
            overview: 培养目标概述内容
            description: 培养目标描述内容

        Returns:
            bool: True表示更新成功，False表示更新失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)

        # 点击培养目标标签页
        self.click_tab("培养目标")
        # 输入培养目标概述
        self.input_training_objective_overview(overview)
        # 点击保存按钮
        self.click_save_button()
        # 点击添加目标按钮
        self.click_add_training_objective_button()
        # 输入培养目标描述
        self.input_training_objective_description(description)
        # 点击保存培养目标按钮
        self.click_training_objective_save_button()
        # 点击保存按钮
        self.click_save_button()
        # 断言保存成功提示框是否出现
        result = self.is_save_success_alert_display()

        # 切出iframe
        self.switch_out_training_program_manage_iframe()

        log.info(f"更新培养目标结果：{result}")
        return result

    # ==================== 毕业要求页面操作方法 ====================
    def input_graduation_requirement_description(self, description):
        """输入毕业要求概述

        Args:
            description: 毕业要求概述内容

        Returns:
            输入操作结果
        """
        log.info(f"输入毕业要求概述：{description}，定位器为：{self.GRADUATION_REQUIREMENT_DESCRIPTION_TEXTAREA[1]}")
        return self.input_text(self.GRADUATION_REQUIREMENT_DESCRIPTION_TEXTAREA, description)

    def click_add_indicator_point_button(self):
        """点击添加指标点按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击添加指标点按钮，定位器为：{self.ADD_INDICATOR_POINT_BUTTON[1]}")
        return self.click(self.ADD_INDICATOR_POINT_BUTTON, timeout=10)

    def input_indicator_point_name(self, name, indicator_index=1):
        """输入指标点名称

        Args:
            name: 指标点名称
            indicator_index: 指标点序号，从1开始，默认为1（第1个指标点）

        Returns:
            输入操作结果
        """
        locator = self.get_indicator_point_name_input_locator(indicator_index)
        log.info(f"输入指标点名称（索引：{indicator_index}）：{name}，定位器为：{locator[1]}")
        return self.input_text(locator, name)

    def input_indicator_point_description(self, description, indicator_index=1):
        """输入指标点描述

        Args:
            description: 指标点描述内容
            indicator_index: 指标点序号，从1开始，默认为1（第1个指标点）

        Returns:
            输入操作结果
        """
        locator = self.get_indicator_point_description_textarea_locator(indicator_index)
        log.info(f"输入指标点描述（索引：{indicator_index}）：{description}，定位器为：{locator[1]}")
        return self.input_text(locator, description)

    def click_expand_button(self, indicator_index=1):
        """点击展开按钮

        Args:
            indicator_index: 指标点序号，从1开始，默认为1（第1个指标点）

        Returns:
            点击操作结果
        """
        locator = self.get_expand_button_locator(indicator_index)
        log.info(f"点击展开按钮（指标点索引：{indicator_index}），定位器为：{locator[1]}")
        return self.click(locator, timeout=10)

    def click_add_decomposed_indicator_point_button(self, indicator_index=1):
        """点击添加分解指标点按钮

        Args:
            indicator_index: 指标点序号，从1开始，默认为1（第1个指标点）

        Returns:
            点击操作结果
        """
        locator = self.get_add_decomposed_indicator_point_button_locator(indicator_index)
        log.info(f"点击添加分解指标点按钮（指标点索引：{indicator_index}），定位器为：{locator[1]}")
        return self.click(locator, timeout=10)

    def input_decomposed_indicator_point_name(self, name, indicator_index=1, decomposed_index=1):
        """输入分解指标点名称

        Args:
            name: 分解指标点名称
            indicator_index: 指标点序号，从1开始，默认为1（第1个指标点）
            decomposed_index: 分解指标点序号，从1开始，默认为1（第1个分解指标点）

        Returns:
            输入操作结果
        """
        locator = self.get_decomposed_indicator_point_name_input_locator(indicator_index, decomposed_index)
        log.info(f"输入分解指标点名称（指标点索引：{indicator_index}，分解指标点索引：{decomposed_index}）：{name}，定位器为：{locator[1]}")
        return self.input_text(locator, name)

    def input_decomposed_indicator_point_description(self, description, indicator_index=1, decomposed_index=1):
        """输入分解指标点描述

        Args:
            description: 分解指标点描述内容
            indicator_index: 指标点序号，从1开始，默认为1（第1个指标点）
            decomposed_index: 分解指标点序号，从1开始，默认为1（第1个分解指标点）

        Returns:
            输入操作结果
        """
        locator = self.get_decomposed_indicator_point_description_textarea_locator(indicator_index, decomposed_index)
        log.info(f"输入分解指标点描述（指标点索引：{indicator_index}，分解指标点索引：{decomposed_index}）：{description}，定位器为：{locator[1]}")
        return self.input_text(locator, description)

    def update_graduation_requirement(self, description=None, indicator_index=1, indicator_name=None, indicator_description=None, decomposed_indicator_index=1, decomposed_indicator_name=None, decomposed_indicator_description=None):
        """更新毕业要求

        Args:
            description: 毕业要求概述内容
            indicator_index: 指标点序号，从1开始，默认为1（第1个指标点）
            indicator_name: 指标点名称
            indicator_description: 指标点描述内容
            decomposed_indicator_index: 分解指标点序号，从1开始，默认为1（第1个分解指标点）
            decomposed_indicator_name: 分解指标点名称
            decomposed_indicator_description: 分解指标点描述内容

        Returns:
            bool: True表示更新成功，False表示更新失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)

        # 点击毕业要求标签页
        self.click_tab("毕业要求")
        # 输入毕业要求概述
        self.input_graduation_requirement_description(description)
        # 点击添加指标点按钮
        self.click_add_indicator_point_button()
        # 输入指标点名称
        self.input_indicator_point_name(indicator_name, indicator_index)
        # 输入指标点描述
        self.input_indicator_point_description(indicator_description, indicator_index)
        # 点击展开按钮
        self.click_expand_button(indicator_index)
        # 点击添加分解指标点按钮
        self.click_add_decomposed_indicator_point_button(indicator_index)
        # 输入分解指标点名称
        self.input_decomposed_indicator_point_name(decomposed_indicator_name, indicator_index, decomposed_indicator_index)
        # 输入分解指标点描述
        self.input_decomposed_indicator_point_description(decomposed_indicator_description, indicator_index, decomposed_indicator_index)
        # 点击保存按钮
        self.click_save_button()
        # 断言保存成功提示框是否出现
        result = self.is_save_success_alert_display()

        # 切出iframe
        self.switch_out_training_program_manage_iframe()

        log.info(f"更新毕业要求结果：{result}")
        return result

    # ==================== 目标支撑页面操作方法 ====================
    def click_target_support_select_button(self, index=1):
        """点击目标支撑选择按钮

        Args:
            index: 选择按钮序号，从1开始，默认为1（第1个选择按钮）

        Returns:
            点击操作结果
        """
        locator = self.get_target_support_select_button_locator(index)
        log.info(f"点击目标支撑选择按钮（索引：{index}），定位器为：{locator[1]}")
        return self.click(locator, timeout=10)

    def click_target_support_level_option(self, level="高支撑"):
        """点击目标支撑等级选项

        Args:
            level: 支撑等级，有高支撑、中支撑、低支撑、无支撑4个选项

        Returns:
            点击操作结果
        """
        locator = self.get_target_support_level_option_locator(level)
        log.info(f"点击目标支撑等级选项：{level}，定位器为：{locator[1]}")
        return self.click(locator, timeout=10)

    def update_target_support(self, index=1, level="高支撑"):
        """更新目标支撑

        Args:
            index: 选择按钮序号，从1开始，默认为1（第1个选择按钮）
            level: 支撑等级，有高支撑、中支撑、低支撑、无支撑4个选项

        Returns:
            bool: True表示更新成功，False表示更新失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)

        # 点击目标支撑标签页
        self.click_tab("目标支撑")
        # 点击目标支撑选择按钮
        self.click_target_support_select_button(index)
        # 点击目标支撑等级选项
        self.click_target_support_level_option(level)
        # 点击保存按钮
        self.click_save_button()
        # 断言保存成功提示框是否出现
        result = self.is_save_success_alert_display()

        # 切出iframe
        self.switch_out_training_program_manage_iframe()

        log.info(f"更新目标支撑结果：{result}")
        return result
    # ==================== 课程体系页面操作方法 ====================

    def click_add_course_button(self):
        """点击添加课程按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击添加课程按钮，定位器为：{self.ADD_COURSE_BUTTON[1]}")
        return self.click(self.ADD_COURSE_BUTTON, timeout=10)

    def input_course_search(self, search_keyword):
        """输入课程搜索关键词（课程名称或代码）

        Args:
            search_keyword: 搜索关键词（课程名称或代码）

        Returns:
            输入操作结果
        """
        log.info(f"输入课程搜索关键词：{search_keyword}，定位器为：{self.COURSE_SEARCH_INPUT[1]}")
        return self.input_text(self.COURSE_SEARCH_INPUT, search_keyword)

    def click_course_checkbox_by_name(self, course_name):
        """根据课程名称点击复选框

        Args:
            course_name: 课程名称

        Returns:
            点击操作结果
        """
        locator = self.get_course_checkbox_by_name_locator(course_name)
        log.info(f"根据课程名称点击复选框，课程名称：{course_name}，定位器为：{locator[1]}")
        return self.click(locator, timeout=10)

    def click_confirm_add_course_button(self):
        """点击确认添加课程按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击确认添加课程按钮，定位器为：{self.CONFIRM_ADD_COURSE_BUTTON[1]}")
        return self.click(self.CONFIRM_ADD_COURSE_BUTTON, timeout=10)

    def update_course_system(self, course_name=None):
        """更新课程体系

        Args:
            course_name: 课程名称

        Returns:
            bool: True表示更新成功，False表示更新失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)

        # 点击课程体系标签页
        self.click_tab("课程体系")
        # 点击添加课程按钮
        self.click_add_course_button()
        # 输入课程搜索关键词
        self.input_course_search(course_name)
        sleep(1)
        # 点击课程复选框
        self.click_course_checkbox_by_name(course_name)
        # 点击确认添加课程按钮
        self.click_confirm_add_course_button()
        # 断言保存成功提示框是否出现
        result = self.is_save_success_alert_display("成功添加")

        # 切出iframe
        self.switch_out_training_program_manage_iframe()

        log.info(f"更新课程体系结果：{result}")
        return result

    # ==================== 课程支撑页面操作方法 ====================

    def click_associate_course_button(self, index=1):
        """点击关联课程按钮

        Args:
            index: 按钮序号，从1开始，默认为1（第1个关联课程按钮）

        Returns:
            点击操作结果
        """
        locator = self.get_associate_course_button_locator(index)
        log.info(f"点击关联课程按钮（索引：{index}），定位器为：{locator[1]}")
        return self.click(locator, timeout=10)

    def click_course_support_checkbox_by_name(self, course_name):
        """课程支撑页面根据课程名称点击复选框

        Args:
            course_name: 课程名称

        Returns:
            点击操作结果
        """
        locator = self.get_course_support_checkbox_by_name_locator(course_name)
        log.info(f"课程支撑页面根据课程名称点击复选框，课程名称：{course_name}，定位器为：{locator[1]}")
        return self.click(locator, timeout=10)

    def click_course_support_confirm_button(self):
        """点击课程支撑页面关联课程确定按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击课程支撑页面关联课程确定按钮，定位器为：{self.COURSE_SUPPORT_CONFIRM_BUTTON[1]}")
        return self.click(self.COURSE_SUPPORT_CONFIRM_BUTTON, timeout=10)

    def click_course_support_level_option(self, index=1, level="H"):
        """点击课程支撑等级选项

        Args:
            index: 选择按钮序号，从1开始，默认为1（第1个选择按钮）
            level: 支撑等级，H表示高支撑，M表示中支撑，L表示低支撑

        Returns:
            点击操作结果
        """
        locator = self.get_course_support_level_option_locator(index, level)
        log.info(f"点击课程支撑等级选项（索引：{index}，支撑等级：{level}），定位器为：{locator[1]}")
        return self.click(locator, timeout=10)

    def click_complete_edit_button(self):
        """点击完成编辑按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击完成编辑按钮，定位器为：{self.COMPLETE_EDIT_BUTTON[1]}")
        return self.click(self.COMPLETE_EDIT_BUTTON, timeout=10)

    def update_course_support(self, index=1, course_name=None, level="H"):
        """更新课程支撑

        Args:
            index: 关联课程按钮序号，从1开始，默认为1（第1个关联课程按钮）
            course_name: 课程名称
            level: 支撑等级，H表示高支撑，M表示中支撑，L表示低支撑

        Returns:
            bool: True表示更新成功，False表示更新失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.TRAINING_PROGRAM_MANAGE_IFRAME)
        # 点击课程支撑标签页
        self.click_tab("课程支撑")
        # 点击关联课程按钮（不传index，每次都选第一个关联课程按钮，因为点击完成编辑后，对应的关联课程按钮会消失）
        self.click_associate_course_button()
        # 点击课程支撑复选框
        self.click_course_support_checkbox_by_name(course_name)
        # 点击课程支撑页面关联课程确定按钮
        self.click_course_support_confirm_button()
        # 点击课程支撑等级选项
        self.click_course_support_level_option(index=index, level=level)
        # 点击完成编辑按钮
        self.click_complete_edit_button()
        # 断言保存成功提示框是否出现
        result = self.is_save_success_alert_display("编辑完成")

        # 切出iframe
        self.switch_out_training_program_manage_iframe()

        log.info(f"更新课程支撑结果：{result}")
        return result
