## 🚀 快速开始指南

### 📋 目录
- [一键启动](#一键启动)
- [Web 界面使用](#web-界面使用)
- [功能演示](#功能演示)
- [常见问题](#常见问题)

---

## 一键启动

### 1️⃣ 环境准备

```bash
# 克隆项目
git clone https://github.com/neolimk/neolimk-moneyprintr.git
cd neolimk-moneyprintr

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖（确保已更新 requirements.txt）
pip install -r requirements.txt
```

### 2️⃣ 启动 Web 服务

```bash
python run_web_ui.py
```

你会看到类似的输出：

```
============================================================
🚀 自动网站注册登录 AI Agent - Web UI
============================================================

📝 访问地址: http://localhost:5000

💡 功能说明:
  1. 配置邮箱和手机号凭证
  2. 添加要注册的网站URL
  3. 预览注册表单信息
  4. 自动注册和生成账号列表

⚠️  按 CTRL+C 停止服务
============================================================
```

### 3️⃣ 打开浏览器

访问 **http://localhost:5000** 即可进入 Web 界面

---

## Web 界面使用

### 1. 🔑 **凭证管理** (第一步必做)

**位置**: 侧边栏 → 凭证管理

#### 添加邮箱

1. 点击 **"+ 添加邮箱"** 按钮
2. 输入邮箱地址（如 `your_email@gmail.com`）
3. 可选：添加备注（如 "我的Gmail账户"）
4. 点击 **"添加"**

<img src="docs/screenshots/add_email.png" width="400" alt="添加邮箱">

#### 添加手机号

1. 点击 **"+ 添加手机号"** 按钮
2. 输入手机号（支持格式）：
   - `13800000000`
   - `+86 138 0000 0000`
   - `+8613800000000`
3. 可选：添加备注
4. 点击 **"添加"**

<img src="docs/screenshots/add_phone.png" width="400" alt="添加手机号">

### 2. 📝 **网站注册** (第二步)

**位置**: 侧边栏 → 网站注册

#### 流程演示

**第一步：输入网站 URL**
```
输入框中粘贴网站注册页面URL，例如：
https://example.com/register
https://github.com/signup
```

**第二步：点击"+ 添加网站"**
- 网站会出现在左侧列表中
- 可以继续添加多个网站

**第三步：预览注册信息**
- 右侧会自动显示该网站的表单信息
- 包括必填字段、可选字段、特殊要求
- 显示将使用的邮箱/手机号
- 预览生成的密码

**第四步：点击"🚀 开始注册"**
- 系统将自动填充表单
- 自动生成密码
- 自动提交注册

### 3. 📊 **账号列表** (第三步：查看结果)

**位置**: 侧边栏 → 账号列表

#### 功能说明

| 功能 | 说明 |
|------|------|
| 🔍 **搜索框** | 按网站名或邮箱快速查找 |
| 👁️ **查看密码** | 点击眼睛图标查看完整密码 |
| 📋 **复制邮箱** | 一键复制邮箱地址 |
| 📥 **导出** | 支持 JSON、CSV、Excel 三种格式 |

#### 导出数据

点击相应的导出按钮：

```
┌─────────────────────────────────────┐
│ 📥 JSON  │ 📥 CSV  │ 📥 Excel        │
└─────────────────────────────────────┘
```

**导出格式示例（JSON）：**
```json
{
  "accounts": [
    {
      "website": "example.com",
      "email": "your_email@gmail.com",
      "phone": "+86138000000",
      "password": "SecurePass123!@#",
      "registration_time": "2024-06-15T10:30:00",
      "status": "success",
      "login_url": "https://example.com/login"
    }
  ],
  "summary": {
    "total": 1,
    "success": 1,
    "failed": 0
  }
}
```

### 4. 📈 **仪表盘** (实时统计)

**位置**: 侧边栏 → 仪表盘

显示以下统计信息：

- ✅ **已注册账号** - 总数
- 📧 **配置的邮箱** - 已添加的邮箱数量
- 📱 **配置的手机号** - 已添加的手机号数量
- 🕐 **最后更新时间** - 最近操作时间
- 📋 **最近注册的账号** - 列表展示

### 5. ⚙️ **设置** (可选配置)

**位置**: 侧边栏 → 设置

#### 密码生成设置

```
🔐 密码长度: [12] (8-32)
☑️ 包含特殊符号
[测试密码生成] 按钮 - 验证密码生成
```

#### 浏览器设置

```
☑️ 无头模式（后台运行）
☐ 使用代理IP
```

#### 数据管理

```
[清空所有数据]  - 谨慎操作，不可撤销
[备份数据]      - 导出所有数据备份
```

---

## 功能演示

### 完整注册流程示例

#### 场景：一天内注册 3 个网站账号

**第 1 步：配置凭证（只需配置一次）**

```
凭证管理
├─ 邮箱 1: primary@gmail.com
├─ 邮箱 2: secondary@outlook.com
└─ 手机号: +86 138 0000 0000
```

**第 2 步：批量添加网站**

```
网站注册
├─ https://www.example.com/register
├─ https://github.com/signup
└─ https://another-site.com/register
```

**第 3 步：预览和检查**

- 预览 example.com 的表单（需要邮箱、密码）
- 预览 github.com 的表单（需要邮箱、密码、username）
- 预览 another-site.com 的表单

**第 4 步：一键注册**

点击 "🚀 开始注册"，系统自动：
1. 识别每个网站的表单
2. 填充对应的邮箱和密码
3. 提交注册请求
4. 记录注册结果

**第 5 步：查看结果**

```
账号列表
┌──────────────┬──────────────────────┬──────────┬────────────────────┐
│ 网站         │ 邮箱                 │ 密码     │ 状态               │
├──────────────┼──────────────────────┼──────────┼────────────────────┤
│ example.com  │ primary@gmail.com    │ ••••••   │ ✓ 成功             │
│ github.com   │ primary@gmail.com    │ ••••••   │ ✓ 成功             │
│ another-site │ secondary@outlook.com│ ••••••   │ ✓ 成功             │
└──────────────┴──────────────────────┴──────────┴────────────────────┘
```

**第 6 步：导出数据**

点击 "📥 JSON" / "📥 CSV" / "📥 Excel" 下载账号列表

---

## 常见问题

### ❓ Q1: 启动时出现 "端口 5000 已被占用" 错误

**解决方案：**

```bash
# 方案 1: 杀死占用 5000 的进程
# macOS/Linux:
lsof -ti:5000 | xargs kill -9

# Windows (PowerShell 管理员运行):
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# 方案 2: 修改端口
# 编辑 run_web_ui.py，将端口改为其他数字
app.run(debug=True, host='0.0.0.0', port=5001)  # 改成 5001
```

### ❓ Q2: 提交表单时失败，说"无法识别表单"

**原因和解决：**

1. **网站 URL 不是注册页面**
   - 确保 URL 直接指向注册表单页面
   - 例如：`https://github.com/signup` 而不是 `https://github.com`

2. **网站使用了动态表单加载**
   - 某些网站通过 JavaScript 动态生成表单
   - 系统可能无法识别
   - 解决：在 `config/website_profiles.json` 中添加该网站的配置

3. **网站的表单字段名称非标准**
   - 在 `config/website_profiles.json` 中为该网站添加自定义配置

**查看完整配置示例：**
```json
{
  "example.com": {
    "name": "Example Website",
    "form_selectors": {
      "email_field": "[name='email']",
      "password_field": "[name='password']"
    }
  }
}
```

### ❓ Q3: 导出的 Excel 文件打不开

**解决方案：**

```bash
# 确保已安装 openpyxl
pip install openpyxl>=3.1.0

# 如果问题仍存在，导出为 CSV 或 JSON
```

### ❓ Q4: 密码生成过于复杂，某些网站不接受

**解决方案：**

在设置页面中：
1. 取消勾选 "包含特殊符号"
2. 减少密码长度
3. 点击 "测试密码生成" 验证

### ❓ Q5: 页面显示"暂无数据"，是否出错了？

**检查清单：**

1. ✅ 确认已添加邮箱/手机号凭证
2. ✅ 确认已添加网站 URL
3. ✅ 确认已点击 "开始注册"
4. ✅ 查看浏览器控制台是否有错误信息（F12）

### ❓ Q6: 如何修改已注册账号的信息？

**当前版本不支持直接编辑，可以：**

1. 导出数据（JSON/CSV）
2. 用文本编辑器修改
3. 手动重新导入（功能开发中）

### ❓ Q7: 数据存储在哪里？是否安全？

**数据存储位置：**

```
项目目录
├── data/
│   └── accounts.db  ← SQLite 数据库（本地存储）
└── logs/
    └── agent_*.log  ← 操作日志
```

**安全性说明：**
- ✅ 所有数据存储在本地，不上传到云端
- ✅ 密码使用 AES 加密存储
- ✅ 仅在内存中短期存放明文密码
- ✅ 导出的文件默认包含明文密码（谨慎保管）

---

## 🎯 进阶功能

### 为特定网站添加自定义配置

编辑 `config/website_profiles.json`：

```json
{
  "websites": {
    "mysite.com": {
      "name": "My Site",
      "registration_url": "https://mysite.com/register",
      "form_selectors": {
        "email_field": "[name='email']",
        "password_field": "[name='password']",
        "submit_button": "[type='submit']"
      },
      "required_fields": ["email", "password"],
      "optional_fields": ["phone"],
      "captcha_required": true,
      "email_verification": true
    }
  }
}
```

### 使用命令行接口（CLI）

```bash
# 添加邮箱凭证
python main.py config --email your@gmail.com

# 注册网站
python main.py register https://example.com/register https://github.com/signup

# 列出所有账号
python main.py list-accounts

# 导出账号
python main.py export --format json --output my_accounts.json
```

---

## 📞 技术支持

如果遇到问题：

1. 📖 查看 [项目 README](README.md)
2. 🔍 查看日志文件：`logs/agent_*.log`
3. 🐛 提交 Issue：https://github.com/neolimk/neolimk-moneyprintr/issues
4. 💬 查看浏览器控制台错误（F12 → Console）

---

## 📝 更新日志

### v1.0.0 (当前版本)

✅ **功能完成：**
- 凭证管理（邮箱、手机号）
- 网站表单识别
- 自动填充和提交
- 账号映射和导出
- 密码生成和管理
- Web UI 界面
- JSON/CSV/Excel 导出

🔄 **功能开发中：**
- 验证码识别
- 邮件验证自动化
- 代理 IP 支持
- 账号编辑和删除
- 数据导入功能

---

**祝你使用愉快！🎉**
