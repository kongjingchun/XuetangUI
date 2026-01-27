# encoding: utf-8
# @File  : course_resource_page.py
# @Author:
# @Date  :
# @Desc  : 课程资源页面基类。按 Selenium 官方 Page Object 理念：对外暴露“页面提供的服务”，
#         不在每个定位器上封装 click/input，服务方法内部直接用 self.click(locator)/self.input_text(...)。
from time import sleep

from selenium.webdriver.common.by import By

from logs.log import log
from page.teacher_workbench.course_workbench.course_workbench_page import CourseWorkbenchPage


class CourseResourcePage(CourseWorkbenchPage):
    """课程资源页面基类。

    继承 CourseWorkbenchPage，提供课程资源模块下各页面的公共能力（如 iframe 切换、上传文件等）。
    对外只暴露“服务方法”，不暴露每个按钮/输入框的 click/input 封装。定位器集中维护，服务内部直接使用。
    """

    def __init__(self, driver):
        super().__init__(driver)

    # ======================元素定位器（静态）======================
    # 上传文件按钮
    UPLOAD_FILE_BUTTON = (By.XPATH, "(//button[contains(.,'上传文件')])[1]")
    # 文件输入框（隐藏的 input[type="file"] 元素，点击上传按钮后出现）
    FILE_INPUT = (By.XPATH, "//input[@type='file']")
    # 上传成功提示框（通用，子类可重写）
    UPLOAD_SUCCESS_MESSAGE = (By.XPATH, "//p[contains(.,'上传成功')] | //p[contains(.,'保存成功')]")

    # ==================== 动态定位器 getter ====================
    # （本基类无动态定位器）

    # ==================== 服务方法（页面对外能力） ====================

    def upload_file(self, file_path, timeout=30):
        """上传文件（点击上传按钮后定位文件输入框并发送文件路径）。

        供子类在 iframe 内已就绪时调用，或测试在已切到正确上下文时调用。

        Args:
            file_path: 文件路径（绝对路径）
            timeout: 超时时间（秒），默认 30 秒

        Returns:
            bool: True 表示发送成功，False 表示失败
        """
        log.info(f"开始上传文件：{file_path}")
        try:
            self.find_element(self.FILE_INPUT, timeout=timeout)  # 等待文件输入框出现
            log.info(f"找到文件输入框，定位器为：{self.FILE_INPUT[1]}")
            super().upload_file(self.FILE_INPUT, file_path)
            log.info(f"文件路径已发送到文件输入框：{file_path}")
            return True
        except Exception as e:
            log.warning(f"文件上传可能失败：{file_path}，错误信息：{str(e)}")
            return False

    def upload_file_with_iframe(self, file_path, timeout=30):
        """在课程资源 iframe 中上传文件（完整流程）。

        先切换到课程工作台 iframe、再切换到课程工作空间 iframe，执行上传后等待上传成功提示。

        Args:
            file_path: 文件路径（绝对路径）
            timeout: 超时时间（秒），默认 30 秒

        Returns:
            bool: True 表示检测到上传成功提示，False 表示未检测到
        """
        log.info(f"在 iframe 中上传文件：{file_path}")
        self.switch_to_iframe(self.COURSE_WORKBENCH_IFRAME)  # 切入课程工作台 iframe
        self.switch_to_iframe(self.COURSE_WORKSPACE_IFRAME)  # 切入课程工作空间 iframe
        try:
            self.upload_file(file_path, timeout=timeout)
            sleep(1)
            result = self.is_displayed(self.UPLOAD_SUCCESS_MESSAGE, timeout=timeout)
            if result:
                log.info(f"文件上传成功：{file_path}")
            else:
                log.warning(f"文件上传可能失败，未检测到成功提示：{file_path}")
            return result
        finally:
            self.switch_out_iframe()  # 切出课程工作空间 iframe
            self.switch_out_iframe()  # 切出课程工作台 iframe
