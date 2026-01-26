# 测试用例 Order 和 Story 列表（从小到大排序）

| Order | Story | 文件 |
|-------|-------|------|
| 100 | api注册cms账户 | test_001_user.py |
| 110 | 创建用户 | test_001_user.py |
| 115 | 初始化密码 | test_001_user.py |
| 116 | 绑定用户 | test_001_user.py |
| 117 | 分配角色 | test_001_user.py |
| 120 | 创建院系 | test_002_dept.py |
| 130 | 创建专业 | test_003_major.py |
| 140 | 创建行政班 | test_004_admin_class.py |
| 150 | 创建课程 | test_005_course.py |
| 160 | 创建培养方案 | test_006_training_program.py |
| 170 | 修订培养方案 | test_006_training_program.py |
| 180 | 专业门户管理 | test_007_major_portal.py |
| 190 | 专业图谱概览 | test_008_ai_model.py |
| 200 | 添加知识图谱 | test_009_ai_vertical_model.py |
| 210 | 专业课程群图谱 | test_008_ai_model.py |
| 215 | 创建教师 | test_001_user.py |
| 216 | 绑定教师 | test_001_user.py |
| 217 | 初始化教师密码 | test_001_user.py |
| 220 | 编辑课程大纲 | test_010_course_outline.py |
| 290 | 测试课程资源 | test_011_course_resource.py |
| 300 | 测试教学班管理 | test_012_teaching_class.py |
| 310 | 测试课程内容 | test_013_course_content.py |
| 610 | 删除培养方案 | test_999_delete_data.py |
| 620 | 删除课程 | test_999_delete_data.py |
| 630 | 删除行政班 | test_999_delete_data.py |
| 640 | 删除专业 | test_999_delete_data.py |
| 650 | 删除院系 | test_999_delete_data.py |
| 660 | 删除用户 | test_999_delete_data.py |
| 670 | 删除cms用户 | test_999_delete_data.py |

## 按 Order 分组的 Story 列表

### Order 100-119（用户管理基础）
- **100**: api注册cms账户
- **110**: 创建用户
- **115**: 初始化密码
- **116**: 绑定用户
- **117**: 分配角色

### Order 120-149（基础数据创建）
- **120**: 创建院系
- **130**: 创建专业
- **140**: 创建行政班
- **150**: 创建课程

### Order 150-219（培养方案和AI模型）
- **160**: 创建培养方案
- **170**: 修订培养方案
- **180**: 专业门户管理
- **190**: 专业图谱概览
- **200**: 添加知识图谱
- **210**: 专业课程群图谱
- **215**: 创建教师
- **216**: 绑定教师
- **217**: 初始化教师密码

### Order 220-319（课程相关）
- **220**: 编辑课程大纲
- **290**: 测试课程资源
- **300**: 测试教学班管理
- **310**: 测试课程内容

### Order 610-670（数据清理）
- **610**: 删除培养方案
- **620**: 删除课程
- **630**: 删除行政班
- **640**: 删除专业
- **650**: 删除院系
- **660**: 删除用户
- **670**: 删除cms用户
