# encoding: utf-8
# @File  : UserManagePage.py
# @Author: 孔敬淳
# @Date  : 2025/12/25/14:33
# @Desc  : 用户管理页面对象类，封装用户管理相关的页面操作方法
from time import sleep
from selenium.webdriver.common.by import By

from base.BasePage import BasePage
from logs.log import log


class UserManagePage(BasePage):
    """用户管理页面类

    继承BasePage类，提供用户管理页面的元素操作方法
    符合Selenium官方Page Object Model设计模式
    """

    def __init__(self, driver):
        """初始化用户管理页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
    # 用户管理iframe
    USER_MANAGE_IFRAME = (By.XPATH, "//iframe[@id='app-iframe-2006']")
    # 新增用户按钮
    ADD_USER_BUTTON = (By.XPATH, "//div[@class='el-dropdown toolbar-button']")
    # 提交用户按钮
    SUBMIT_USER_BUTTON = (By.XPATH, "//div[@class = 'dialog-footer']/button[contains(.,'创建用户')]")
    # 创建成功提示框
    CREATE_SUCCESS_ALERT = (By.XPATH, "//p[contains(text(),'创建成功')]")
    # 用户绑定输入框
    USER_BIND_INPUT = (By.XPATH, "//input[@placeholder='请输入平台用户ID']")
    # 确认绑定按钮
    USER_BIND_CONFIRM_BUTTON = (By.XPATH, "//span[contains(.,'确认绑定')]/parent::button")
    # 绑定成功提示框
    BIND_SUCCESS_ALERT = (By.XPATH, "//p[contains(text(),'绑定用户成功')]")
    # 工号筛选输入框
    SEARCH_CODE_INPUT = (By.XPATH, "//input[contains(@placeholder,'请输入工号/学号')]")
    # 删除用户按钮
    DELETE_USER_BUTTON = (By.XPATH, "//button[contains(.,'删除用户')]")
    # 删除确认按钮
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//div[contains(@aria-label,'确认删除') or contains(@aria-label,'删除')]//button[contains(.,'删除')]")
    # 删除成功提示框
    DELETE_SUCCESS_ALERT = (By.XPATH, "//p[contains(text(),'删除成功')]")
    # 新建用户关闭所属学院下拉框
    NEW_USER_DEPT_DROPDOWN_CLOSE = (By.XPATH, "//label[text()='所属学院']//following-sibling::div//div[@class='el-select__suffix']")

    # ==================== 动态定位器方法（需要参数的定位器）====================

    def get_add_user_role_select_locator(self, role_name):
        """获取创建用户角色选择的定位器

        Args:
            role_name: 角色名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//li[contains(.,'" + role_name + "')]")

    def get_create_user_input_locator(self, input_name):
        """获取创建用户输入框的定位器

        Args:
            input_name: 输入框名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[contains(@aria-label,'创建')]//input[contains(@placeholder,'" + input_name + "')]")

    def get_search_input_locator(self, input_name):
        """获取搜索输入框的定位器

        Args:
            input_name: 搜索方式名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//input[contains(@placeholder,'" + input_name + "')]")

    def get_user_bind_button_locator(self, user_code):
        """获取用户绑定按钮的定位器

        Args:
            user_code: 用户工号

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//tr[contains(.,'" + user_code + "')]//button[contains(.,'绑定')]")

    def get_edit_button_by_code_locator(self, code):
        """获取根据工号定位编辑按钮的定位器

        Args:
            code: 工号/学号

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//tr[.//td[contains(.,'" + code + "')]]//button[contains(.,'编辑')]")

    # 新建用户根据角色返回学院下拉框
    def get_new_user_dept_dropdown_locator(self, role_name):
        """获取新建用户学院下拉框的定位器

        Args:
            role_name: 角色名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "//div[contains(@aria-label,'" + role_name + "')]//span[text()='请选择学院']")

    # 新建用户根据院系返回学院下拉框选项
    def get_new_user_dept_dropdown_option_locator(self, dept_name):
        """获取新建用户学院下拉框选项的定位器

        Args:
            dept_name: 学院名称

        Returns:
            tuple: 定位器元组 (By.XPATH, xpath)
        """
        return (By.XPATH, "(//li/span[text()='" + dept_name + "'])[2]")

    # ==================== 页面操作方法 ====================

    def move_add_user_button(self):
        """鼠标悬停到创建按钮

        Returns:
            悬停操作结果
        """
        log.info(f"鼠标悬停到手动创建按钮，定位器为：{self.ADD_USER_BUTTON[1]}")
        return self.hover(self.ADD_USER_BUTTON)

    def click_add_user_role_select(self, role_name):
        """点击选择创建的用户角色身份

        Args:
            role_name: 角色名称（如：创建教务管理员、创建教师、创建学生）

        Returns:
            点击操作结果
        """
        locator = self.get_add_user_role_select_locator(role_name)
        log.info(f"创建的角色身份为：{role_name}，定位器为：{locator[1]}")
        return self.click(locator)

    def input_user_value(self, input_name, value):
        """输入用户信息

        Args:
            input_name: 输入框名称
            value: 输入值

        Returns:
            输入操作结果
        """
        locator = self.get_create_user_input_locator(input_name)
        log.info(f"输入用户信息：{input_name}为：{value}，定位器为：{locator[1]}")
        return self.input_text(locator, value)

    def click_new_user_dept_dropdown(self, role_name):
        """点击新建用户学院下拉框

        Args:
            role_name: 角色名称

        Returns:
            点击操作结果
        """
        locator = self.get_new_user_dept_dropdown_locator(role_name)
        log.info(f"点击新建用户学院下拉框，定位器为：{locator[1]}")
        return self.click(locator)

    def click_new_user_dept_dropdown_option(self, dept_name):
        """点击新建用户学院下拉框选项

        Args:
            dept_name: 学院名称

        Returns:
            点击操作结果
        """
        locator = self.get_new_user_dept_dropdown_option_locator(dept_name)
        log.info(f"点击新建用户学院下拉框选项，定位器为：{locator[1]}")
        return self.click(locator)

    def click_new_user_dept_dropdown_close(self):
        """点击新建用户学院下拉框关闭

        Returns:
            点击操作结果
        """
        log.info(f"点击新建用户学院下拉框关闭，定位器为：{self.NEW_USER_DEPT_DROPDOWN_CLOSE[1]}")
        return self.click(self.NEW_USER_DEPT_DROPDOWN_CLOSE)

    def click_submit_user_button(self):
        """点击提交信息按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击提交信息按钮，定位器为：{self.SUBMIT_USER_BUTTON[1]}")
        return self.click(self.SUBMIT_USER_BUTTON)

    def is_create_success_alert_display(self):
        """判断创建成功的提示框是否出现

        Returns:
            bool: True表示创建成功，False表示失败
        """
        log.info(f"判断创建成功的提示框是否出现，定位器为：{self.CREATE_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.CREATE_SUCCESS_ALERT)

    def input_search_input(self, input_name, value):
        """向搜索输入框输入内容

        Args:
            input_name: 要填写的搜索方式
            value: 填入的值

        Returns:
            输入操作结果
        """
        locator = self.get_search_input_locator(input_name)
        log.info(f"通过{input_name}搜索{value}，定位器为：{locator[1]}")
        return self.input_text(locator, value)

    def click_user_bind_button(self, user_name):
        """点击用户绑定按钮

        Args:
            user_name: 用户名

        Returns:
            点击操作结果
        """
        locator = self.get_user_bind_button_locator(user_name)
        log.info(f"点击用户绑定按钮：{user_name}，定位器为：{locator[1]}")
        return self.click(locator)

    def input_user_bind_input(self, user_id):
        """输入用户绑定ID

        Args:
            user_id: 用户ID

        Returns:
            输入操作结果
        """
        log.info(f"输入用户绑定ID：{user_id}，定位器为：{self.USER_BIND_INPUT[1]}")
        return self.input_text(self.USER_BIND_INPUT, user_id)

    def click_user_bind_confirm_button(self):
        """点击确认绑定

        Returns:
            点击操作结果
        """
        log.info(f"点击确认绑定，定位器为：{self.USER_BIND_CONFIRM_BUTTON[1]}")
        return self.click(self.USER_BIND_CONFIRM_BUTTON)

    def is_user_bind_success_alert_display(self):
        """判断绑定成功的提示框是否出现

        Returns:
            bool: True表示绑定成功，False表示失败
        """
        log.info(f"判断绑定成功的提示框是否出现，定位器为：{self.BIND_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.BIND_SUCCESS_ALERT)

    def create_user(self, role_name, user_info):
        """创建用户

        Args:
            role_name: 创建的角色名称（如：创建教务管理员、创建教师、创建学生）
            user_info: 用户信息字典，key为字段名称，value为字段值
                      例如：{"姓名": "张三", "工号": "001", "手机": "13800138000", "邮箱": "test@example.com"}

        Returns:
            bool: True表示创建成功，False表示失败
        """
        self.switch_to_iframe(self.USER_MANAGE_IFRAME)
        self.move_add_user_button()
        self.click_add_user_role_select(role_name)

        # 根据user_info字典动态输入用户信息
        for input_name, value in user_info.items():
            if input_name == '学院':
                self.click_new_user_dept_dropdown(role_name)
                self.click_new_user_dept_dropdown_option(value)
                self.click_new_user_dept_dropdown_close()
            else:
                self.input_user_value(input_name, str(value))
        self.click_submit_user_button()
        results = self.is_create_success_alert_display()
        self.switch_out_iframe()
        log.info("创建用户结果：" + str(results))
        return results

    def bind_user(self, user, user_id):
        """绑定用户

        Args:
            user: 用户名的一个信息：姓名、工号或手机号等
            user_id: 用户ID

        Returns:
            bool: True表示绑定成功，False表示失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.USER_MANAGE_IFRAME)
        # 输入工号进行搜索
        self.input_search_input("工号", user)
        sleep(1)
        # 点击用户绑定按钮
        self.click_user_bind_button(user)
        # 输入用户绑定ID
        self.input_user_bind_input(user_id)
        # 点击确认绑定按钮
        self.click_user_bind_confirm_button()
        # 判断绑定成功提示框是否出现
        result = self.is_user_bind_success_alert_display()
        # 切出iframe
        self.switch_out_iframe()
        log.info("绑定用户结果：" + str(result))
        return result

    def input_search_code(self, code):
        """输入工号进行搜索

        Args:
            code: 工号/学号

        Returns:
            输入操作结果
        """
        log.info(f"输入工号：{code}，定位器为：{self.SEARCH_CODE_INPUT[1]}")
        return self.input_text(self.SEARCH_CODE_INPUT, code)

    def click_edit_button_by_code(self, code):
        """根据工号点击编辑按钮

        Args:
            code: 工号/学号

        Returns:
            点击操作结果
        """
        locator = self.get_edit_button_by_code_locator(code)
        log.info(f"根据工号'{code}'点击编辑按钮，定位器为：{locator[1]}")
        sleep(1)  # 等待搜索结果加载
        return self.click(locator, timeout=15)

    def click_delete_user_button(self):
        """点击删除用户按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击删除用户按钮，定位器为：{self.DELETE_USER_BUTTON[1]}")
        return self.click(self.DELETE_USER_BUTTON, timeout=15)

    def click_delete_confirm_button(self):
        """点击删除确认按钮

        Returns:
            点击操作结果
        """
        log.info(f"点击删除确认按钮，定位器为：{self.DELETE_CONFIRM_BUTTON[1]}")
        return self.click(self.DELETE_CONFIRM_BUTTON, timeout=15)

    def is_delete_success_alert_display(self):
        """判断删除成功提示框是否出现（p标签）

        Returns:
            bool: True表示删除成功提示框出现，False表示未出现
        """
        log.info(f"判断删除成功提示框是否出现，定位器为：{self.DELETE_SUCCESS_ALERT[1]}")
        return self.is_displayed(self.DELETE_SUCCESS_ALERT)

    def delete_user_by_code(self, code):
        """根据工号删除用户

        Args:
            code: 工号

        Returns:
            bool: True表示删除成功，False表示删除失败
        """
        # 切换到iframe
        self.switch_to_iframe(self.USER_MANAGE_IFRAME)
        # 输入工号搜索
        self.input_search_input("工号", code)
        sleep(1)
        # 点击编辑按钮
        self.click_edit_button_by_code(code)
        # 点击删除用户按钮
        self.click_delete_user_button()
        # 点击删除确认按钮
        self.click_delete_confirm_button()
        # 断言删除成功提示框是否出现
        result = self.is_delete_success_alert_display()
        # 切出iframe
        self.switch_out_iframe()
        log.info(f"删除用户结果：{result}")
        return result
