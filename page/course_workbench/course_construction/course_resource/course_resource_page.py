# encoding: utf-8
# @File  : course_resource_page.py
# @Author: 孔敬淳
# @Date  : 2025/01/20
# @Desc  : 课程资源页面基类，封装课程资源相关的公共页面操作方法
from time import sleep
from selenium.webdriver.common.by import By

from logs.log import log
from page.course_workbench.course_workbench_page import CourseWorkbenchPage


class CourseResourcePage(CourseWorkbenchPage):
    """课程资源页面基类

    继承CourseWorkbenchPage类（CourseWorkbenchPage已继承BasePage），
    提供课程资源模块下所有页面的公共操作方法
    符合Selenium官方Page Object Model设计模式

    使用说明：
        课程资源模块下的各个具体页面应该继承此类，而不是直接继承BasePage
        这样可以复用公共的iframe切换、菜单导航等方法
    """

    def __init__(self, driver):
        """初始化课程资源页面

        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)

    # ==================== 元素定位器（静态定位器）====================
    # 课程资源通用iframe（子类可以重写此定位器）
    COURSE_RESOURCE_IFRAME = (By.XPATH, "//iframe[@id='course-workspace-iframe']")
    # 上传文件按钮
    UPLOAD_FILE_BUTTON = (By.XPATH, "(//button[contains(.,'上传文件')])[1]")
    # 文件输入框（隐藏的input[type="file"]元素，点击上传按钮后出现）
    FILE_INPUT = (By.XPATH, "//input[@type='file']")
    # 上传成功提示框（通用，子类可以重写）
    UPLOAD_SUCCESS_MESSAGE = (By.XPATH, "//p[contains(.,'上传成功')] | //p[contains(.,'保存成功')]")

    # ==================== 动态定位器方法（需要参数的定位器）====================

    # ==================== 公共页面操作方法 ====================

    def click_upload_file_button(self):
        """点击上传文件按钮

        Returns:
            bool: True表示点击成功，False表示失败
        """
        log.info(f"点击上传文件按钮，定位器为：{self.UPLOAD_FILE_BUTTON[1]}")
        return self.click(self.UPLOAD_FILE_BUTTON)

    def upload_file(self, file_path, timeout=30):
        """上传文件（完整流程）

        点击上传文件按钮后，定位文件输入框并上传文件

        Args:
            file_path: 文件路径（绝对路径）
            timeout: 超时时间(秒)，默认30秒

        Returns:
            bool: True表示上传成功，False表示失败
        """
        log.info(f"开始上传文件：{file_path}")

        # 点击上传文件按钮
        # self.click_upload_file_button()

        # 等待文件输入框出现（点击上传按钮后，通常会显示隐藏的input[type="file"]）
        try:
            # 等待文件输入框出现
            file_input_element = self.find_element(self.FILE_INPUT, timeout=timeout)
            log.info(f"找到文件输入框，定位器为：{self.FILE_INPUT[1]}")

            # 使用BasePage的upload_file方法上传文件（通过super()调用父类方法）
            super().upload_file(self.FILE_INPUT, file_path)
            log.info(f"文件路径已发送到文件输入框：{file_path}")

            # 等待上传完成（等待上传成功提示框出现）
            result = self.is_displayed(self.UPLOAD_SUCCESS_MESSAGE, timeout=timeout)
            if result:
                log.info(f"文件上传成功：{file_path}")
            else:
                log.warning(f"文件上传可能失败，未检测到成功提示：{file_path}")

            return result

        except Exception as e:
            log.error(f"文件上传失败：{file_path}，错误信息：{str(e)}")
            return False

    def upload_file_with_iframe(self, file_path, timeout=30):
        """在iframe中上传文件（完整流程）

        先切换到课程资源iframe，然后执行上传文件操作

        Args:
            file_path: 文件路径（绝对路径）
            timeout: 超时时间(秒)，默认30秒

        Returns:
            bool: True表示上传成功，False表示失败
        """
        log.info(f"在iframe中上传文件：{file_path}")

        # 切换到课程工作台iframe
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)
        # 切换到课程资源iframe
        self.switch_to_iframe(self.COURSE_RESOURCE_IFRAME)

        try:
            # 执行上传文件操作
            result = self.upload_file(file_path, timeout=timeout)
            sleep(1)
            return result
        finally:
            # 切出课程资源iframe
            self.switch_out_iframe()
            # 切出课程工作台iframe
            self.switch_out_iframe()
