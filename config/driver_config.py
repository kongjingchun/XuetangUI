# encoding: utf-8
# @File  : driver_config.py
# @Author: 孔敬淳
# @Date  : 2025/12/01/17:52
# @Desc  : Chrome 浏览器驱动配置类

import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from common.tools import get_project_path, sep
from common.yaml_config import GetConf


class DriverConfig:
    # ChromeDriver 镜像配置
    CHROMEDRIVER_URL = "https://mirrors.huaweicloud.com/chromedriver"
    CHROMEDRIVER_LATEST_URL = "https://mirrors.huaweicloud.com/chromedriver/LATEST_RELEASE"

    # 添加日志导入
    from logs.log import log

    # 本地ChromeDriver路径（优先使用）
    # 根据操作系统选择对应的driver文件
    @staticmethod
    def _get_chromedriver_filename():
        """根据操作系统返回对应的chromedriver文件名"""
        if sys.platform == "win32":
            return "chromedriver.exe"
        elif sys.platform.startswith("linux"):
            return "chromedriver_linux"
        elif sys.platform == "darwin":  # macOS
            return "chromedriver"  # macOS版本使用chromedriver
        else:
            # 其他系统默认使用chromedriver
            return "chromedriver"

    @staticmethod
    def get_local_chromedriver_path():
        """获取本地ChromeDriver路径（根据操作系统）"""
        filename = DriverConfig._get_chromedriver_filename()
        return os.path.join(get_project_path(), "driver_files", filename)

    @staticmethod
    def _configure_chrome_options() -> webdriver.ChromeOptions:
        """
        配置 Chrome 浏览器选项

        Returns:
            ChromeOptions: 配置好的 Chrome 选项对象
        """
        options = webdriver.ChromeOptions()

        # 去除"Chrome正受到自动测试软件控制"的提示
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # 安全与证书相关配置（解决 HTTPS 警告）
        security_args = [
            "--disable-features=HttpsFirstMode",
            "--ignore-certificate-errors",
            "--allow-insecure-localhost",
            "--ignore-ssl-errors=true",
            "--allow-running-insecure-content",
            "--disable-web-security",
            "--disable-site-isolation-trials",
            "--disable-3d-apis",
        ]

        # 系统兼容性配置
        compatibility_args = [
            "--disable-gpu",  # 禁用GPU加速，解决某些系统上的图形渲染问题
            "--no-sandbox",  # 禁用沙箱模式，适用于容器化环境或权限受限的系统
            "--disable-dev-shm-usage",  # 禁用devshm使用，解决内存不足问题
        ]
        
        # macOS 系统专用配置（解决 Chrome instance exited 问题）
        if sys.platform == "darwin":
            compatibility_args.extend([
                "--disable-software-rasterizer",  # 禁用软件光栅化
                "--disable-extensions",  # 禁用扩展
                "--disable-background-networking",  # 禁用后台网络
                "--disable-background-timer-throttling",  # 禁用后台定时器节流
                "--disable-renderer-backgrounding",  # 禁用渲染器后台化
                "--disable-backgrounding-occluded-windows",  # 禁用被遮挡窗口的后台化
                "--disable-breakpad",  # 禁用崩溃报告
                "--disable-component-update",  # 禁用组件更新
                "--disable-default-apps",  # 禁用默认应用
                "--disable-domain-reliability",  # 禁用域可靠性
                "--disable-features=TranslateUI",  # 禁用翻译UI
                "--disable-sync",  # 禁用同步
                "--metrics-recording-only",  # 仅记录指标
                "--no-first-run",  # 不运行首次运行向导
                "--safebrowsing-disable-auto-update",  # 禁用安全浏览自动更新
                "--password-store=basic",  # 使用基本密码存储
            ])

        # 读取配置，判断是否使用Headless模式
        try:
            deploy_config = GetConf().get_info("部署环境")
            use_headless = deploy_config.get("是否Headless模式", False) if deploy_config else False
        except Exception:
            # 如果读取配置失败，默认根据操作系统判断
            # Linux系统默认使用headless，Mac和Windows默认不使用
            use_headless = sys.platform.startswith("linux")
        
        # Headless模式相关配置（所有平台统一，参考 Chrome 官方与 Selenium 最佳实践）
        # 参考：https://developer.chrome.com/docs/chromium/new-headless
        # 要点：1) 使用 --headless（Chrome 112+ 已与 headful 共用代码）；2) 必须设置 --window-size（否则 Linux 等易出现点击/输入异常）
        headless_args = []
        if use_headless:
            headless_args = [
                "--headless",  # 统一使用 --headless（各平台一致，避免 Linux 上 --headless=new 的焦点/点击问题）
                "--window-size=1920,1080",  # Headless 下必须设置视口，否则元素“可见/可点击”判断易出错
                "--disable-software-rasterizer",
                "--disable-extensions",
                "--disable-background-networking",
                "--disable-background-timer-throttling",
                "--disable-renderer-backgrounding",
                "--disable-backgrounding-occluded-windows",
                "--disable-breakpad",
                "--disable-component-extensions-with-background-pages",
                "--disable-default-apps",
                "--disable-domain-reliability",
                "--disable-features=TranslateUI",
                "--disable-ipc-flooding-protection",
                "--disable-sync",
                "--metrics-recording-only",
                "--no-first-run",
                "--safebrowsing-disable-auto-update",
                "--enable-automation",
                "--password-store=basic",
                "--remote-debugging-port=0",
            ]
            DriverConfig.log.info(f"启用Headless模式（{sys.platform}），视口 1920x1080")
        else:
            DriverConfig.log.info(f"使用有界面模式（{sys.platform}）")
        
        # Linux系统专用配置（无论是否headless都需要）
        linux_specific_args = []
        if sys.platform.startswith("linux"):
            linux_specific_args = []

        # macOS 系统：设置 Chrome 二进制路径（如果存在）
        if sys.platform == "darwin":
            chrome_binary_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            if os.path.exists(chrome_binary_path):
                options.binary_location = chrome_binary_path
        
        # 应用所有配置参数
        for arg in security_args + compatibility_args + headless_args + linux_specific_args:
            options.add_argument(arg)

        # 设置用户数据目录（避免权限问题）
        # Linux系统或Headless模式下需要设置用户数据目录
        if sys.platform.startswith("linux") or use_headless:
            import tempfile
            import uuid
            # 为每个实例创建唯一的用户数据目录，避免冲突
            if use_headless:
                # Headless 模式下使用带时间戳的唯一目录
                unique_id = str(uuid.uuid4())[:8]
                user_data_dir = os.path.join(tempfile.gettempdir(), f"chrome_user_data_{unique_id}")
            else:
                user_data_dir = os.path.join(tempfile.gettempdir(), "chrome_user_data")
            os.makedirs(user_data_dir, exist_ok=True)
            options.add_argument(f"--user-data-dir={user_data_dir}")
            if use_headless:
                DriverConfig.log.info(f"Headless模式用户数据目录: {user_data_dir}")

        return options

    @staticmethod
    def _get_chromedriver_path() -> str:
        """
        获取ChromeDriver路径，根据配置文件决定是否只使用本地路径

        Returns:
            str: ChromeDriver可执行文件路径

        Raises:
            FileNotFoundError: 当本地和网络都无法获取chromedriver时抛出异常
        """
        # 读取配置文件，判断是否本地部署
        try:
            deploy_config = GetConf().get_info("部署环境")
            use_local_only = deploy_config.get("是否本地部署", False) if deploy_config else False
        except Exception:
            # 如果读取配置失败，默认使用本地优先策略
            use_local_only = False

        # 优先使用本地chromedriver
        local_path = DriverConfig.get_local_chromedriver_path()

        # 添加日志，方便调试
        from logs.log import log
        log.info(f"当前操作系统: {sys.platform}")
        log.info(f"期望的ChromeDriver路径: {local_path}")
        log.info(f"文件是否存在: {os.path.exists(local_path)}")

        # 检查是否存在旧的chromedriver文件（可能是macOS版本）
        old_chromedriver_path = os.path.join(get_project_path(), "driver_files", "chromedriver")
        if os.path.exists(old_chromedriver_path) and sys.platform.startswith("linux"):
            log.warning(f"检测到旧的chromedriver文件: {old_chromedriver_path}")
            log.warning(f"Linux系统应使用chromedriver_linux，请确保 {local_path} 文件存在")

        # 检查文件是否存在（Windows上不检查执行权限，因为Windows不使用Unix权限系统）
        if os.path.exists(local_path):
            # 在Windows上，必须使用.exe扩展名的文件
            if sys.platform == "win32":
                # Windows系统：确保文件有.exe扩展名
                if local_path.endswith('.exe'):
                    return local_path
                # 如果没有.exe扩展名，忽略该文件（可能是其他平台的版本）
            else:
                # 在非Windows系统上检查执行权限和文件格式
                if os.access(local_path, os.X_OK):
                    # 尝试验证文件是否真的可以执行（检查文件格式）
                    # 如果文件格式错误（比如macOS版本在Linux上），会抛出OSError
                    try:
                        import subprocess
                        # 尝试执行 --version 命令来验证文件是否可用
                        result = subprocess.run(
                            [local_path, "--version"],
                            capture_output=True,
                            timeout=5
                            # 注意：capture_output=True 已经会捕获stdout和stderr，不能再指定stderr参数
                        )
                        # 如果执行成功（返回码为0），说明文件可用
                        if result.returncode == 0:
                            return local_path
                    except (OSError, subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
                        # 文件格式错误或无法执行，跳过本地文件，使用webdriver-manager下载
                        log.warning(f"本地ChromeDriver文件格式错误或无法执行: {local_path}")
                        log.warning(f"错误信息: {str(e)}")
                        log.warning(f"将尝试使用webdriver-manager下载")
                        pass

        # 如果配置为本地部署（只使用本地driver），直接抛出异常
        if use_local_only:
            if os.path.exists(local_path):
                # 文件存在但无法使用（可能是格式错误）
                error_msg = (
                    f"本地ChromeDriver文件格式错误或无法执行！\n"
                    f"配置为本地部署（是否本地部署: true）\n"
                    f"本地路径: {local_path}\n"
                    f"可能原因：\n"
                    f"1. chromedriver文件与当前操作系统不匹配（如macOS版本在Linux上运行）\n"
                    f"2. chromedriver文件已损坏\n"
                    f"3. chromedriver文件架构不匹配（如x86_64版本在ARM系统上运行）\n"
                    f"解决方案：\n"
                    f"1. 删除错误的chromedriver文件: rm {local_path}\n"
                    f"2. 下载匹配当前操作系统的chromedriver文件到: {local_path}\n"
                    f"3. 确保chromedriver有执行权限: chmod +x {local_path}\n"
                    f"4. 确保chromedriver版本与Chrome浏览器版本匹配\n"
                    f"5. 如需允许网络下载，请在environment.yaml中设置 是否本地部署: false"
                )
            else:
                # 文件不存在
                error_msg = (
                    f"无法找到本地ChromeDriver！\n"
                    f"配置为本地部署（是否本地部署: true）\n"
                    f"本地路径不存在: {local_path}\n"
                    f"解决方案：\n"
                    f"1. 将匹配的chromedriver文件放置到: {local_path}\n"
                    f"2. 确保chromedriver有执行权限: chmod +x {local_path}\n"
                    f"3. 确保chromedriver版本与Chrome浏览器版本匹配\n"
                    f"4. 如需允许网络下载，请在environment.yaml中设置 是否本地部署: false"
                )
            raise FileNotFoundError(error_msg)

        # 如果本地不存在且允许网络下载，尝试使用webdriver-manager（需要网络）
        try:
            log.info(f"本地ChromeDriver不存在或不可用，尝试使用webdriver-manager下载...")
            
            # 配置webdriver-manager的缓存目录为本地driver_files目录
            # 这样下载的文件会直接保存到本地，避免重复下载
            driver_files_dir = os.path.join(get_project_path(), "driver_files")
            os.makedirs(driver_files_dir, exist_ok=True)
            
            driver_manager = ChromeDriverManager(
                url=DriverConfig.CHROMEDRIVER_URL,
                latest_release_url=DriverConfig.CHROMEDRIVER_LATEST_URL
                # 不设置cache_valid_range，永久保留下载的文件
            )
            downloaded_path = driver_manager.install()
            log.info(f"webdriver-manager下载的ChromeDriver路径: {downloaded_path}")

            # 验证下载的文件是否可用
            if os.path.exists(downloaded_path):
                try:
                    import subprocess
                    result = subprocess.run(
                        [downloaded_path, "--version"],
                        capture_output=True,
                        timeout=5
                        # 注意：capture_output=True 已经会捕获stdout和stderr，不能再指定stderr参数
                    )
                    if result.returncode == 0:
                        log.info(f"下载的ChromeDriver验证成功")
                        # 无论验证是否成功，都尝试将文件保存到本地driver_files目录
                        # 这样下次就可以直接使用本地文件，避免重复下载
                        try:
                            import shutil
                            # 确保driver_files目录存在
                            os.makedirs(os.path.dirname(local_path), exist_ok=True)
                            # 如果本地文件已存在，先删除
                            if os.path.exists(local_path):
                                os.remove(local_path)
                            # 复制下载的文件到本地目录
                            shutil.copy2(downloaded_path, local_path)
                            # 设置执行权限（非Windows系统）
                            if sys.platform != "win32":
                                os.chmod(local_path, 0o755)
                            log.info(f"已将下载的ChromeDriver保存到本地: {local_path}")
                            log.info(f"下次启动时将直接使用本地文件，避免重复下载")
                            return local_path
                        except Exception as copy_error:
                            log.warning(f"保存ChromeDriver到本地失败: {str(copy_error)}")
                            log.warning(f"将使用webdriver-manager下载的路径: {downloaded_path}")
                            return downloaded_path
                    else:
                        log.warning(f"下载的ChromeDriver验证失败，返回码: {result.returncode}")
                        # 即使验证失败，也尝试保存到本地，可能只是版本信息获取失败
                        try:
                            import shutil
                            if os.path.exists(local_path):
                                os.remove(local_path)
                            shutil.copy2(downloaded_path, local_path)
                            if sys.platform != "win32":
                                os.chmod(local_path, 0o755)
                            log.info(f"已将下载的ChromeDriver保存到本地: {local_path}")
                            return local_path
                        except Exception as copy_error:
                            log.error(f"保存ChromeDriver到本地失败: {str(copy_error)}")
                            return downloaded_path
                except (OSError, subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
                    log.warning(f"下载的ChromeDriver验证过程出错: {str(e)}")
                    # 即使验证出错，也尝试保存到本地
                    try:
                        import shutil
                        if os.path.exists(local_path):
                            os.remove(local_path)
                        shutil.copy2(downloaded_path, local_path)
                        if sys.platform != "win32":
                            os.chmod(local_path, 0o755)
                        log.info(f"已将下载的ChromeDriver保存到本地: {local_path}")
                        return local_path
                    except Exception as copy_error:
                        log.error(f"保存ChromeDriver到本地失败: {str(copy_error)}")
                        return downloaded_path

            return downloaded_path
        except Exception as e:
            # 无外网环境下的友好提示
            error_msg = (
                f"无法获取ChromeDriver！\n"
                f"本地路径不存在: {local_path}\n"
                f"网络下载失败（可能是无外网环境）: {str(e)}\n"
                f"解决方案：\n"
                f"1. 将匹配的chromedriver文件放置到: {local_path}\n"
                f"2. 确保chromedriver有执行权限: chmod +x {local_path}\n"
                f"3. 确保chromedriver版本与Chrome浏览器版本匹配"
            )
            raise FileNotFoundError(error_msg) from e

    @staticmethod
    def _create_chrome_service() -> ChromeService:
        """
        创建 ChromeDriver 服务实例

        Returns:
            ChromeService: ChromeDriver 服务对象
        """
        chromedriver_path = DriverConfig._get_chromedriver_path()
        return ChromeService(chromedriver_path)

    @staticmethod
    def driver_config() -> WebDriver:
        """
        初始化 Chrome 浏览器驱动，兼容 Selenium 4.36

        Returns:
            WebDriver: Chrome WebDriver 实例
        """
        from selenium.common.exceptions import SessionNotCreatedException

        options = DriverConfig._configure_chrome_options()
        service = DriverConfig._create_chrome_service()

        # 初始化 Chrome 浏览器实例
        try:
            driver = webdriver.Chrome(service=service, options=options)
        except SessionNotCreatedException as e:
            # 捕获版本不匹配错误，自动处理
            error_msg = str(e)
            if "version" in error_msg.lower() or "only supports" in error_msg.lower() or "supports Chrome version" in error_msg:
                DriverConfig.log.warning(f"检测到ChromeDriver版本不匹配: {error_msg}")
                DriverConfig.log.warning("将删除旧版本ChromeDriver，并使用webdriver-manager下载匹配版本")

                # 删除旧版本的chromedriver
                local_path = DriverConfig.get_local_chromedriver_path()
                if os.path.exists(local_path):
                    try:
                        os.remove(local_path)
                        DriverConfig.log.info(f"已删除旧版本ChromeDriver: {local_path}")
                    except Exception as remove_error:
                        DriverConfig.log.warning(f"删除旧版本ChromeDriver失败: {str(remove_error)}")

                # 使用webdriver-manager下载匹配的版本
                try:
                    # 配置webdriver-manager的缓存目录为本地driver_files目录
                    driver_files_dir = os.path.join(get_project_path(), "driver_files")
                    os.makedirs(driver_files_dir, exist_ok=True)
                    
                    driver_manager = ChromeDriverManager(
                        url=DriverConfig.CHROMEDRIVER_URL,
                        latest_release_url=DriverConfig.CHROMEDRIVER_LATEST_URL
                        # 不设置cache_valid_range，永久保留下载的文件
                    )
                    downloaded_path = driver_manager.install()
                    DriverConfig.log.info(f"webdriver-manager下载的ChromeDriver路径: {downloaded_path}")

                    # 将下载的文件保存到本地driver_files目录，避免下次重复下载
                    try:
                        import shutil
                        # 确保driver_files目录存在
                        os.makedirs(os.path.dirname(local_path), exist_ok=True)
                        if os.path.exists(local_path):
                            os.remove(local_path)
                        shutil.copy2(downloaded_path, local_path)
                        # 设置执行权限（非Windows系统）
                        if sys.platform != "win32":
                            os.chmod(local_path, 0o755)
                        DriverConfig.log.info(f"已将下载的ChromeDriver保存到本地: {local_path}")
                        DriverConfig.log.info(f"下次启动时将直接使用本地文件，避免重复下载")
                    except Exception as copy_error:
                        DriverConfig.log.warning(f"保存ChromeDriver到本地失败: {str(copy_error)}")
                        DriverConfig.log.warning(f"将使用webdriver-manager下载的路径: {downloaded_path}")

                    # 重新创建service并初始化driver
                    # 优先使用保存到本地的文件
                    final_path = local_path if os.path.exists(local_path) else downloaded_path
                    service = ChromeService(final_path)
                    driver = webdriver.Chrome(service=service, options=options)
                    DriverConfig.log.info("使用新下载的ChromeDriver成功启动浏览器")
                except Exception as download_error:
                    DriverConfig.log.error(f"使用webdriver-manager下载失败: {str(download_error)}")
                    raise SessionNotCreatedException(
                        f"ChromeDriver版本不匹配，且无法自动下载匹配版本。\n"
                        f"原始错误: {error_msg}\n"
                        f"下载错误: {str(download_error)}\n"
                        f"请手动下载匹配Chrome浏览器版本的ChromeDriver到: {local_path}"
                    ) from download_error
            else:
                # 其他SessionNotCreatedException，直接抛出
                raise

        # 浏览器窗口设置
        driver.maximize_window()  # 设置浏览器全屏
        driver.delete_all_cookies()  # 删除所有cookies

        return driver
