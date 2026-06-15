# 高级功能文档

## 📖 目录

- [Selenium 浏览器自动化](#selenium-浏览器自动化)
- [邮件验证自动化](#邮件验证自动化)
- [高级 Agent 功能](#高级-agent-功能)
- [常见问题](#常见问题)
- [性能优化](#性能优化)

---

## Selenium 浏览器自动化

### 🎯 概述

Selenium 模块提供了真实的浏览器自动化能力，可以处理复杂的动态网站。

### 📦 基本使用

```python
from core.selenium_handler import SeleniumHandler

# 初始化处理器
handler = SeleniumHandler(headless=True, timeout=10)

# 初始化浏览器驱动
handler.init_driver(browser='chrome')  # 或 'firefox'

# 打开网站
handler.open_url('https://example.com/register')

# 填充输入框
handler.fill_input('[name="email"]', 'user@example.com')
handler.fill_input('[name="password"]', 'SecurePassword123!')

# 点击按钮
handler.click_element('button[type="submit"]')

# 等待元素出现
handler.wait_for_element('.success-message', timeout=5)

# 获取文本内容
status = handler.get_text('.status')
print(f"注册状态: {status}")

# 截图
handler.take_screenshot('registration_complete.png')

# 关闭浏览器
handler.close()
```

### 🔧 高级操作

#### 处理 iframe

```python
# 切换到 iframe
handler.switch_to_iframe('iframe[name="payment"]')

# 在 iframe 中进行操作
handler.fill_input('[name="card"]', '4111111111111111')

# 切换回默认内容
handler.switch_to_default_content()
```

#### 滚动和弹窗

```python
# 滚动到元素
handler.scroll_to_element('[name="agree_checkbox"]')

# 关闭弹窗
handler.wait_and_close_popup('.close-button', max_wait=5)
```

#### 执行 JavaScript

```python
# 执行 JavaScript 代码
result = handler.execute_script("return document.title;")
print(f"页面标题: {result}")

# 获取页面信息
script = """
return {
    title: document.title,
    url: document.location.href,
    forms: document.querySelectorAll('form').length
};
"""
page_info = handler.execute_script(script)
```

### ⚙️ 配置选项

```python
# 无头模式（后台运行，更快）
handler = SeleniumHandler(headless=True)

# 显示模式（可视化调试）
handler = SeleniumHandler(headless=False)

# 自定义超时
handler = SeleniumHandler(timeout=20)
```

---

## 邮件验证自动化

### 🎯 概述

邮件处理模块支持自动接收验证邮件、提取验证码和确认链接。

### 📧 支持的邮箱服务

| 邮箱服务 | IMAP 服务器 | 备注 |
|---------|-----------|------|
| Gmail | imap.gmail.com | 需要应用密码 |
| Outlook | imap-mail.outlook.com | 标准密码 |
| 163 | imap.163.com | 标准密码 |
| QQ | imap.qq.com | 需要授权码 |
| 新浪 | imap.sina.com | 标准密码 |

### 基本使用

```python
from core.email_handler import EmailHandler

# Gmail 示例
email = 'your_email@gmail.com'
password = 'your_app_password'  # Gmail 应用专用密码

handler = EmailHandler(email, password)

# 获取验证码
code = handler.get_verification_code(
    sender_keywords=['noreply', 'no-reply'],  # 邮件来自关键词
    subject_keywords=['verify', 'verification', '验证'],  # 主题关键词
    timeout=300,  # 5 分钟超时
    code_pattern=r'\d{4,6}'  # 4-6 位数字
)

if code:
    print(f"验证码: {code}")
else:
    print("未获得验证码")
```

### 获取确认链接

```python
link = handler.get_confirmation_link(
    sender_keywords=['support', 'noreply'],
    subject_keywords=['confirm', 'verification'],
    link_pattern=r'https?://[^\s]+',
    timeout=300
)

if link:
    print(f"确认链接: {link}")
```

### Gmail 配置说明

**第 1 步：启用 2 步验证**
1. 访问 https://myaccount.google.com
2. 左侧菜单 → 安全
3. 启用 "两步验证"

**第 2 步：生成应用密码**
1. 在安全页面 → "应用密码"
2. 选择应用：Mail
3. 选择设备：Windows 电脑（或其他）
4. 生成密码
5. 复制生成的 16 位密码

**第 3 步：使用密码**
```python
handler = EmailHandler(
    'your_email@gmail.com',
    'xxxx xxxx xxxx xxxx'  # 16 位应用密码
)
```

---

## 高级 Agent 功能

### 🎯 完整注册流程

```python
from core.advanced_agent import AdvancedRegistrationAgent

# 初始化 Agent
agent = AdvancedRegistrationAgent(
    headless=True,  # 后台运行
    use_email_verification=True  # 启用邮件验证
)

# 使用浏览器注册
account = agent.register_with_browser(
    website_url='https://github.com/signup',
    browser='chrome'
)

if account:
    print(f"✅ 注册成功")
    print(f"网站: {account.website}")
    print(f"邮箱: {account.email}")
    print(f"密码: {account.password}")
else:
    print(f"❌ 注册失败")
```

### 📊 获取注册结果

```python
# 获取所有账号
accounts = agent.get_account_mapping()

for account in accounts:
    print(f"{account.website}: {account.email} - {account.status}")

# 导出账号列表
agent.export_account_list('json', 'accounts.json')
agent.export_account_list('csv', 'accounts.csv')
agent.export_account_list('excel', 'accounts.xlsx')
```

---

## 常见问题

### ❓ Q1: 如何处理验证码？

**当前支持的方式：**

1. **手动输入**
   ```python
   handler.take_screenshot('captcha.png')
   # 用户查看截图并输入验证码
   code = input("请输入验证码: ")
   handler.fill_input('[name="captcha"]', code)
   ```

2. **使用 OCR 服务** (需要集成)
   ```python
   # 未来功能：集成 Tesseract 或付费 API
   code = ocr_handler.recognize_captcha('captcha.png')
   ```

3. **验证码求解 API** (需要集成)
   ```python
   # 使用第三方服务如 2captcha.com
   code = captcha_solver.solve(captcha_image)
   ```

### ❓ Q2: Chrome 找不到或版本不匹配

**解决方案：**

```bash
# 安装 webdriver-manager（自动管理驱动）
pip install webdriver-manager

# 或手动指定 Chrome 路径
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
service = Service('/path/to/chromedriver')
driver = webdriver.Chrome(service=service, options=options)
```

### ❓ Q3: 如何在 Docker 中运行？

**Dockerfile 示例：**

```dockerfile
FROM python:3.11-slim

# 安装依赖
RUN apt-get update && apt-get install -y \
    chromium-browser \
    chromium-chromedriver \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "run_web_ui.py"]
```

### ❓ Q4: 如何避免被检测为机器人？

**最佳实践：**

```python
from core.selenium_handler import SeleniumHandler
import time
import random

handler = SeleniumHandler(headless=False)  # 显示浏览器
handler.init_driver('chrome')

# 添加随机延迟
time.sleep(random.uniform(1, 3))

# 使用标准的浏览器行为
handler.open_url('https://example.com')

# 模拟鼠标移动
actions = webdriver.common.action_chains.ActionChains(handler.driver)
actions.move_by_offset(100, 100).pause(random.uniform(0.5, 1)).perform()

# 随机滚动
handler.execute_script(f"window.scrollBy(0, {random.randint(100, 300)});")
```

---

## 性能优化

### 🚀 并行注册

```python
from concurrent.futures import ThreadPoolExecutor
import threading

def register_website(agent, url):
    return agent.register_with_browser(url)

# 使用线程池并行注册
websites = [
    'https://github.com/signup',
    'https://gitlab.com/users/sign_up',
    'https://www.notion.com/signup',
]

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(
        lambda url: register_website(agent, url),
        websites
    ))

print(f"完成 {len(results)} 个注册")
```

### 💾 缓存和重用

```python
# 缓存网站配置
import json

cache = {}

def get_form_config(domain):
    if domain in cache:
        return cache[domain]
    
    # 获取配置
    with open('config/website_profiles.json') as f:
        profiles = json.load(f)
    
    config = profiles['websites'].get(domain)
    cache[domain] = config
    return config
```

### 🔄 重试机制

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def register_with_retry(agent, url):
    return agent.register_with_browser(url)

# 自动重试最多 3 次
result = register_with_retry(agent, 'https://example.com/register')
```

---

## 🔗 相关资源

- [Selenium 文档](https://www.selenium.dev/documentation/)
- [WebDriver 等待策略](https://www.selenium.dev/documentation/webdriver/waits/)
- [IMAP 协议](https://tools.ietf.org/html/rfc3501)
- [BeautifulSoup 文档](https://www.crummy.com/software/BeautifulSoup/)

---

**最后更新**: 2024-06-15
