# 在线网站取证系统

## 项目简介

在线网站取证系统是一个基于Flask的Web应用程序，专门用于网站数据的自动化采集、固定和取证分析。该系统提供了智能化的网页爬取功能，支持批量URL处理，并能将采集到的数据转换为结构化表格格式，为数字取证工作提供有力支持。

## 主要功能

### 🔍 智能固定
- **智能URL生成**：通过分析两个示例URL的模式，自动生成大量相似URL
- **异步并发爬取**：支持多进程+多线程的高效网页采集
- **自定义请求头**：支持配置User-Agent、Cookie等HTTP头信息
- **SSL兼容**：自动处理HTTPS和HTTP协议切换

### 📁 导入固定
- **批量URL处理**：支持从文本文件导入URL列表进行批量爬取
- **灵活配置**：可调整并发线程数和进程数以优化性能
- **错误处理**：完善的异常处理机制，确保爬取过程稳定

### 📊 转换表格
- **多格式支持**：自动识别HTML表格和JSON数据
- **智能转换**：使用4种不同算法将网页数据转换为CSV表格
- **数据处理**：支持pandas、demjson3等多种数据处理库

### 📦 文件管理
- **自动打包**：将爬取结果自动打包为ZIP文件
- **哈希校验**：为每个文件包生成MD5/SHA256哈希值
- **完整性保证**：确保取证数据的完整性和可验证性

## 技术架构

### 后端技术栈
- **Flask**：Web框架
- **aiohttp**：异步HTTP客户端
- **asyncio**：异步编程支持
- **multiprocessing**：多进程并发处理
- **pandas**：数据分析和处理
- **numpy**：数值计算支持

### 前端技术栈
- **HTML5 + CSS3**：响应式用户界面
- **JavaScript**：表单验证和交互逻辑
- **SVG图标**：矢量图标系统

## 安装配置

### 环境要求
- Python 3.7+
- Windows/Linux/macOS

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd 在线网站取证系统
```

2. **创建虚拟环境**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

### 依赖包说明
```
Flask>=2.0.0          # Web框架
aiohttp>=3.8.0        # 异步HTTP客户端
aiohttp-retry>=2.8.0  # HTTP重试机制
aiofiles>=0.8.0       # 异步文件操作
pandas>=1.3.0         # 数据分析
numpy>=1.21.0         # 数值计算
demjson3>=2.2.4       # JSON解析，demjson安装不上可以使用demjson3
jsoncsv>=1.2.0        # JSON转CSV
html5lib>=1.1         # HTML解析
```

## 使用说明

### 启动应用
```bash
python app.py
```
应用将在 `http://localhost:5000` 启动

### 功能使用

#### 1. 智能固定
1. 访问 `/intelligent_fix` 页面
2. 输入第一页和第二页的URL示例
3. 设置要爬取的总页数
4. 配置请求头信息（可选）
5. 调整线程数和进程数
6. 点击"开始固定"执行爬取

**示例**：
- 第一页URL: `https://example.com/list?page=1`
- 第二页URL: `https://example.com/list?page=2`
- 页数: `100`

#### 2. 导入固定
1. 准备包含URL列表的文本文件（每行一个URL）
2. 访问 `/import_fix` 页面
3. 上传URL文件
4. 配置请求头和并发参数
5. 开始批量爬取

#### 3. 转换表格
1. 完成网页爬取后，访问 `/conversion_table` 页面
2. 选择要处理的网站文件夹
3. 选择操作类型：
   - **处理数据**：将HTML/JSON转换为CSV表格
   - **下载文件**：直接下载原始爬取结果

## 项目结构

```
在线网站取证系统/
├── app.py                    # Flask主应用
├── async_web_scraper.py      # 异步网页爬虫模块
├── url_generator.py          # URL模式识别和生成
├── header_converter.py       # HTTP头格式转换
├── hash.py                   # 文件哈希计算
├── all_func_process_table.py # 数据表格处理
├── requirements.txt          # 依赖包列表
├── templates/                # HTML模板
│   ├── index.html           # 主页
│   ├── intelligent_fix.html # 智能固定页面
│   ├── import_fix.html      # 导入固定页面
│   ├── conversion_table.html# 转换表格页面
│   └── operation_manual.html# 操作手册
├── static/                   # 静态资源
│   ├── css/                 # 样式文件
│   ├── img/                 # 图标文件
│   └── video/               # 视频文件
├── process/                  # 数据处理模块
│   ├── pandas_html_to_table.py
│   ├── smart_mode_json_to_table.py
│   ├── pandas_json_to_table.py
│   └── jsontool_json_to_table.py
├── html_files/              # 爬取结果存储
├── zip_files/               # 压缩文件存储
├── hash_files/              # 哈希文件存储
├── final_files/             # 最终打包文件
└── uploads/                 # 上传文件临时存储
```

## 核心算法

### URL模式识别
系统通过分析两个示例URL的数字模式，自动识别页码规律：
1. 提取URL中的所有数字
2. 计算数字间的差值模式
3. 应用模式生成后续URL

### 异步并发爬取
- **多进程架构**：将URL列表分割到多个进程
- **异步IO**：每个进程内使用异步HTTP请求
- **信号量控制**：限制并发连接数避免服务器压力
- **重试机制**：网络失败时自动重试

### 数据格式转换
系统提供4种数据转换策略：
1. **pandas HTML解析**：适用于标准HTML表格
2. **智能JSON解析**：自动识别JSON数据结构
3. **pandas JSON处理**：结构化JSON数据转换
4. **通用JSON工具**：兼容各种JSON格式

## 注意事项

### 使用建议
1. **合理设置并发数**：避免对目标服务器造成过大压力
2. **遵守robots.txt**：尊重网站的爬虫协议
3. **设置请求间隔**：避免被反爬虫机制拦截
4. **备份重要数据**：定期备份爬取结果

### 法律合规
- 仅用于合法的数据采集和取证工作
- 遵守相关法律法规和网站使用条款
- 不得用于恶意攻击或非法数据获取

### 性能优化
- 根据网络环境调整超时时间
- 合理配置进程数和线程数
- 监控内存使用情况
- 定期清理临时文件

## 故障排除

### 常见问题

**Q: 爬取失败，提示连接超时**
A: 检查网络连接，适当增加超时时间，或降低并发数

**Q: 生成的ZIP文件为空**
A: 确认爬取过程成功完成，检查html_files目录是否有内容

**Q: 表格转换失败**
A: 检查网页内容格式，尝试不同的转换算法

**Q: 内存使用过高**
A: 减少并发进程数，分批处理大量URL

## 更新日志

### v1.0.0
- 初始版本发布
- 支持智能固定和导入固定功能
- 实现多种数据转换算法
- 添加文件哈希校验功能

## 贡献指南

欢迎提交Issue和Pull Request来改进项目：
1. Fork项目仓库
2. 创建功能分支
3. 提交代码更改
4. 发起Pull Request

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至项目维护者

---

**免责声明**：本工具仅供学习和合法的数据采集使用，使用者需自行承担使用风险和法律责任。
