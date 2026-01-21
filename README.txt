一、项目结构说明
#项目根目录结构
XuetangUI/
├──.gitignore  # Git忽略文件配置
├──.python-version  # Python版本配置文件
├──.vscode/  # VS Code编辑器配置目录
│  ├──launch.json  # 调试启动配置
│  └──tasks.json  # 任务配置
│
├──base/  # 基础类目录（PageObject基类）
│  ├──__init__.py  # 基础类模块初始化文件
│  └──base_page.py  # 基础页面类（Page Object Model基类）
│
├──page/  # 页面对象目录（PageObject实现类）
│  ├──__init__.py  # 页面对象模块初始化文件
│  ├──ai_major/  # AI专业建设系统页面
│  │  ├──__init__.py  # AI专业建设系统模块初始化文件
│  │  ├──major_ai_model/  # AI模型相关页面
│  │  │  ├──__init__.py  # AI模型模块初始化文件
│  │  │  ├──major_ai_model_page.py  # AI模型页面
│  │  │  ├──major_graph_model_page.py  # 专业图谱模型页面
│  │  │  └──major_course_group_graph_page.py  # 专业课程组图谱页面
│  │  ├──major_manage_page.py  # 专业管理页面
│  │  ├──major_portal_manage_page.py  # 专业门户管理页面
│  │  ├──training_program_manage/  # 培养方案管理页面
│  │  │  ├──__init__.py  # 培养方案管理模块初始化文件
│  │  │  └──training_program_manage_page.py  # 培养方案管理页面
│  │  └──training_program_revision_page.py  # 培养方案修订页面
│  ├──cms/  # CMS系统页面
│  │  ├──__init__.py  # CMS系统模块初始化文件
│  │  └──cms_user_manage_page.py  # CMS用户管理页面
│  ├──dean_manage/  # 教务管理页面
│  │  ├──__init__.py  # 教务管理模块初始化文件
│  │  ├──user_manage_page.py  # 用户管理页面
│  │  ├──role_manage_page.py  # 角色管理页面
│  │  ├──course_manage_page.py  # 课程管理页面
│  │  └──admin_class_manage_page.py  # 行政班管理页面
│  ├──department_manage/  # 院系管理页面
│  │  ├──__init__.py  # 院系管理模块初始化文件
│  │  └──dept_list_manage_page.py  # 院系列表管理页面
│  ├──teacher_workbench/  # 教师工作台页面
│  │  ├──__init__.py  # 教师工作台页面对象模块初始化文件
│  │  └──my_teaching_courses_page.py  # 我教的课页面
│  ├──course_workbench/  # 课程工作台页面
│  │  ├──__init__.py  # 课程工作台页面对象模块初始化文件
│  │  ├──course_construction/  # 课程建设页面
│  │  │  ├──__init__.py  # 课程建设页面对象模块初始化文件
│  │  │  ├──ai_vertical_model/  # AI垂直模型页面
│  │  │  │  ├──__init__.py  # AI垂直模型模块初始化文件
│  │  │  │  └──knowledge_graph_page.py  # 知识图谱页面
│  │  │  ├──course_outline/  # 课程大纲页面
│  │  │  │  ├──__init__.py  # 课程大纲模块初始化文件
│  │  │  │  ├──course_info_page.py  # 课程信息页面
│  │  │  │  ├──course_objective_page.py  # 课程目标页面
│  │  │  │  ├──construction_history_page.py  # 建设历程页面
│  │  │  │  └──course_team_page.py  # 课程团队页面
│  │  │  └──course_resource/  # 课程资源页面
│  │  │     ├──__init__.py  # 课程资源模块初始化文件
│  │  │     ├──course_resource_page.py  # 课程资源页面
│  │  │     ├──link_page.py  # 链接页面
│  │  │     └──question_bank_page.py  # 题库页面
│  │  └──course_workbench_page.py  # 课程工作台页面
│  ├──login/  # 登录相关页面
│  │  ├──__init__.py  # 登录模块初始化文件
│  │  └──login_page.py  # 登录页面
│  ├──left_menu_page.py  # 左侧菜单页面
│  └──top_menu_page.py  # 顶部菜单页面
│
├──testcases/  # 测试用例目录
│  ├──__init__.py  # 测试用例模块初始化文件
│  ├──conftest.py  # pytest配置文件（fixture定义和钩子函数）
│  ├──conftest.py.bak  # pytest配置文件备份
│  ├──helpers/  # 测试辅助工具目录
│  │  ├──__init__.py  # 测试辅助工具模块初始化文件
│  │  └──test_context_helper.py  # 测试上下文辅助工具类（封装登录、切换身份、切换学校等公共操作）
│  ├──testgqkt/  # 测试用例集合
│  │  ├──__init__.py  # 测试用例集合模块初始化文件
│  │  ├──test_001_user.py  # 用户管理测试用例
│  │  ├──test_002_dept.py  # 院系管理测试用例
│  │  ├──test_003_major.py  # 专业管理测试用例
│  │  ├──test_004_admin_class.py  # 行政班管理测试用例
│  │  ├──test_005_course.py  # 课程管理测试用例
│  │  ├──test_006_training_program.py  # 培养方案管理测试用例
│  │  ├──test_007_major_portal.py  # 专业门户管理测试用例
│  │  ├──test_008_ai_model.py  # AI模型测试用例
│  │  ├──test_009_ai_vertical_model.py  # AI垂直模型测试用例
│  │  ├──test_010_course_outline.py  # 课程大纲测试用例
│  │  └──test_011_course_resource.py  # 课程资源测试用例
│  └──test_999_delete_data.py  # 数据清理测试用例
│
├──common/  # 公共工具目录
│  ├──__init__.py  # 公共工具模块初始化文件
│  ├──tools.py  # 通用工具函数
│  ├──yaml_config.py  # YAML配置文件读取
│  ├──mysql_operate.py  # MySQL数据库操作
│  ├──redis_operation.py  # Redis操作
│  ├──process_redis.py  # Redis进程处理（测试进度管理）
│  ├──process_file.py  # 文件进程处理（测试进度管理）
│  ├──ding_talk.py  # 钉钉通知
│  ├──ocr_identify.py  # OCR识别
│  ├──find_img.py  # 图片查找
│  └──report_add_img.py  # 报告图片添加
│
├──config/  # 配置文件目录
│  ├──__init__.py  # 配置文件模块初始化文件
│  ├──driver_config.py  # WebDriver驱动配置
│  └──environment.yaml  # 环境配置文件
│
├──driver_files/  # 浏览器驱动文件目录
│  ├──chromedriver  # Chrome浏览器驱动（macOS）
│  ├──chromedriver_linux  # Chrome浏览器驱动（Linux）
│  └──chromedriver.exe  # Chrome浏览器驱动（Windows）
│
├──file/  # 测试文件目录（用于文件上传测试）
│  ├──test.7z  # 7z压缩文件测试文件
│  ├──test.bmp  # BMP图片测试文件
│  ├──test.csv  # CSV表格测试文件
│  ├──test.doc  # DOC文档测试文件
│  ├──test.docx  # DOCX文档测试文件
│  ├──test.dps  # DPS演示文稿测试文件
│  ├──test.et  # ET电子表格测试文件
│  ├──test.gif  # GIF图片测试文件
│  ├──test.jpeg  # JPEG图片测试文件
│  ├──test.jpg  # JPG图片测试文件
│  ├──test.key  # Key演示文稿测试文件
│  ├──test.mp3  # MP3音频测试文件
│  ├──test.mp4  # MP4视频测试文件
│  ├──test.numbers  # Numbers电子表格测试文件
│  ├──test.pages  # Pages文档测试文件
│  ├──test.pdf  # PDF文档测试文件
│  ├──test.png  # PNG图片测试文件
│  ├──test.ppt  # PPT演示文稿测试文件
│  ├──test.pptx  # PPTX演示文稿测试文件
│  ├──test.rar  # RAR压缩文件测试文件
│  ├──test.rtf  # RTF文档测试文件
│  ├──test.tar  # TAR压缩文件测试文件
│  ├──test.tif  # TIF图片测试文件
│  ├──test.txt  # TXT文本测试文件
│  ├──test.wps  # WPS文档测试文件
│  ├──test.xls  # XLS电子表格测试文件
│  ├──test.xlsx  # XLSX电子表格测试文件
│  └──test.zip  # ZIP压缩文件测试文件
│
├──logs/  # 日志目录
│  ├──__init__.py  # 日志模块初始化文件
│  ├──all_logs/  # 所有日志文件目录
│  │  └──*.log  # 按时间戳命名的日志文件（格式：YYYYMMDDHHMM.log）
│  ├──log.py  # 日志配置
│  ├──failed_testcases.json  # 失败测试用例记录
│  └──test_process.json  # 测试过程记录
│
├──img/  # 图片资源目录
│  ├──search.png  # 搜索图片
│  ├──source.png  # 源图片
│  └──*.jpg  # 其他图片资源
│
├──assets/  # 资源文件目录
│  └──style.css  # 样式文件
│
├──UIreport/  # UI测试报告输出目录（Allure报告）
│  └──report/  # 生成的HTML报告目录
│
├──requirements.txt  # Python依赖包列表
├──pytest.ini  # pytest配置文件
├──pyproject.toml  # 项目配置文件
├──setup.cfg  # 安装配置文件
├──pyrightconfig.json  # Pyright类型检查配置文件
├──testcase_result.py  # 测试用例结果处理脚本
├──view_report_http.py  # 启动HTTP服务器查看Allure报告（Python脚本）
├──view_report.sh  # 启动HTTP服务器查看Allure报告（Shell脚本）
├──查看报告说明.md  # Allure报告查看说明文档
├──Dockerfile  # Docker镜像构建文件
├──LINUX_DEPLOY.md  # Linux部署说明文档
├──test.log  # pytest日志文件（由pytest.ini配置生成）
├──report.html  # pytest-html生成的HTML报告
└──README.txt  # 项目说明文档（本文件）

二、测试Linux准备工作
    依赖：
        Python      3.13.5
        pip         25.3
        git
    步骤：
        1. 安装Python依赖包
           pip install -r requirements.txt
        
        2. 配置环境变量
           编辑 config/environment.yaml 文件，配置测试环境信息
        
        3. 运行测试用例
           pytest testcases/ -v
        
        4. 生成Allure报告
           pytest testcases/ --alluredir=UIreport -v
           allure generate UIreport -o UIreport/report --clean
        
        5. 查看报告
           方法1：allure serve UIreport
           方法2：python3 view_report_http.py
           方法3：./view_report.sh
           详细说明请参考：查看报告说明.md

三、测试执行说明
    1. 运行所有测试用例
       pytest testcases/ -v
    
    2. 运行指定测试文件
       pytest testcases/testgqkt/test_001_user.py -v
    
    3. 运行指定测试用例
       pytest testcases/testgqkt/test_001_user.py::TestUser::test_001_create_user -v
    
    4. 并行执行测试（4个进程）
       pytest testcases/ -n 4
    
    5. 生成Allure报告
       pytest testcases/ --alluredir=UIreport -v
       allure generate UIreport -o UIreport/report --clean
    
    6. 查看测试日志
       日志文件保存在 logs/all_logs/ 目录下，按时间戳命名（格式：YYYYMMDDHHMM.log）
       测试执行结果汇总报告会在日志文件末尾自动生成

四、注意事项
    1. 在IDE中编辑测试用例文件时，不会创建日志文件，避免干扰开发
    2. 只有在真正执行测试时，才会创建日志文件和输出日志内容
    3. 测试报告需要使用HTTP服务器访问，不能直接打开HTML文件
    4. 详细报告查看说明请参考：查看报告说明.md
