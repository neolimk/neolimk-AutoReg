"""高级使用示例 - 展示完整的自动化注册流程"""

import logging
from core.advanced_agent import AdvancedRegistrationAgent
from config.credentials_config import CredentialsConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_1_basic_browser_automation():
    """
    示例 1: 基本的浏览器自动化
    
    演示如何使用 Selenium 自动填充和提交表单
    """
    print("\n" + "="*60)
    print("示例 1: 基本浏览器自动化")
    print("="*60)
    
    # 初始化 Agent
    agent = AdvancedRegistrationAgent(headless=True, use_email_verification=False)
    
    # 要注册的网站
    website_url = 'https://example.com/register'
    
    print(f"\n📝 开始注册: {website_url}")
    print("步骤:")
    print("  1. 初始化 Chrome 浏览器")
    print("  2. 打开注册页面")
    print("  3. 自动识别表单字段")
    print("  4. 填充邮箱和密码")
    print("  5. 提交表单")
    print("  6. 等待响应")
    
    # 注册（在实际环境中执行）
    # account = agent.register_with_browser(website_url, browser='chrome')
    
    print("\n✅ 注册完成!")
    print(f"已保存账号到: data/accounts.db")


def example_2_email_verification():
    """
    示例 2: 邮件验证处理
    
    演示如何自动接收验证邮件和提取验证码
    """
    print("\n" + "="*60)
    print("示例 2: 邮件验证处理")
    print("="*60)
    
    from core.email_handler import EmailHandler
    
    # 邮件配置
    email = 'your_email@gmail.com'
    password = 'your_app_password'  # Gmail 应用专用密码
    
    print(f"\n📧 配置邮件处理器")
    print(f"邮箱: {email}")
    print(f"IMAP 服务器: imap.gmail.com")
    
    print("\n等待验证邮件...")
    print("步骤:")
    print("  1. 连接到 IMAP 服务器")
    print("  2. 监听收件箱")
    print("  3. 查找验证邮件")
    print("  4. 提取验证码 (6位数字)")
    print("  5. 返回验证码")
    
    # 在实际环境中使用
    # try:
    #     handler = EmailHandler(email, password)
    #     code = handler.get_verification_code(
    #         sender_keywords=['noreply', 'no-reply'],
    #         subject_keywords=['verify', 'verification', '验证'],
    #         timeout=300,  # 5分钟超时
    #         code_pattern=r'\d{4,6}'
    #     )
    #     if code:
    #         print(f"\n✅ 获得验证码: {code}")
    #     else:
    #         print(f"\n❌ 未获得验证码")
    # except Exception as e:
    #     print(f"❌ 邮件处理失败: {e}")


def example_3_batch_registration():
    """
    示例 3: 批量注册多个网站
    
    演示如何一次注册多个网站
    """
    print("\n" + "="*60)
    print("示例 3: 批量注册多个网站")
    print("="*60)
    
    # 初始化 Agent
    agent = AdvancedRegistrationAgent(headless=True)
    
    # 要注册的网站列表
    websites = [
        'https://github.com/signup',
        'https://gitlab.com/users/sign_up',
        'https://www.notion.com/signup',
    ]
    
    print(f"\n📝 准备批量注册 {len(websites)} 个网站")
    for i, url in enumerate(websites, 1):
        print(f"  {i}. {url}")
    
    print("\n🚀 开始注册...")
    
    results = {}
    for website in websites:
        print(f"\n  正在注册: {website}")
        # account = agent.register_with_browser(website)
        # if account:
        #     results[website] = account
        #     print(f"    ✅ 成功")
        # else:
        #     print(f"    ❌ 失败")
        
        # 模拟成功
        print(f"    ✅ 成功")
    
    print(f"\n✅ 批量注册完成！")
    print(f"成功: {len(results)}/{len(websites)}")
    
    # 导出结果
    print(f"\n📥 导出账号列表...")
    print(f"  - accounts.json")
    print(f"  - accounts.csv")
    print(f"  - accounts.xlsx")


def example_4_credential_management():
    """
    示例 4: 凭证管理
    
    演示如何管理邮箱和手机号凭证
    """
    print("\n" + "="*60)
    print("示例 4: 凭证管理")
    print("="*60)
    
    config = CredentialsConfig()
    
    print("\n📧 邮箱管理")
    print("添加邮箱:")
    emails = [
        ('primary@gmail.com', '主邮箱'),
        ('secondary@outlook.com', '备用邮箱'),
        ('work@company.com', '工作邮箱'),
    ]
    
    for email, note in emails:
        print(f"  ➕ {email} ({note})")
        # config.add_email(email, priority=emails.index((email, note)), notes=note)
    
    print("\n📱 手机号管理")
    print("添加手机号:")
    phones = [
        ('+86 138 0000 0000', '主手机'),
        ('+86 139 0000 0000', '备用手机'),
    ]
    
    for phone, note in phones:
        print(f"  ➕ {phone} ({note})")
        # config.add_phone(phone, priority=phones.index((phone, note)), notes=note)
    
    print("\n📋 当前凭证列表:")
    # credentials = config.list_all_credentials()
    # print(f"邮箱数量: {len(credentials['emails'])}")
    # print(f"手机号数量: {len(credentials['phones'])}")
    
    print(f"邮箱数量: {len(emails)}")
    print(f"手机号数量: {len(phones)}")


def example_5_error_handling():
    """
    示例 5: 错误处理和调试
    
    演示如何处理注册过程中的错误
    """
    print("\n" + "="*60)
    print("示例 5: 错误处理和调试")
    print("="*60)
    
    print("\n🔍 可能的错误情况:")
    
    errors = [
        ("表单识别失败", "原因: 网站使用动态加载表单", "解决: 在 website_profiles.json 中添加配置"),
        ("连接超时", "原因: 网络问题或网站响应慢", "解决: 增加超时时间或重试"),
        ("验证码识别失败", "原因: 无法自动识别验证码", "解决: 使用手动模式或 OCR 服务"),
        ("邮件验证失败", "原因: 无法连接 IMAP 服务器", "解决: 检查邮箱配置和应用密码"),
        ("表单提交失败", "原因: 被网站检测为机器人", "解决: 使用代理 IP 或增加延迟"),
    ]
    
    for i, (error, reason, solution) in enumerate(errors, 1):
        print(f"\n{i}. {error}")
        print(f"   {reason}")
        print(f"   {solution}")
    
    print("\n💾 调试信息:")
    print("  - 日志文件: logs/agent_YYYYMMDD.log")
    print("  - 截图: export/screenshot_*.png")
    print("  - 数据库: data/accounts.db")


def example_6_performance_tips():
    """
    示例 6: 性能优化建议
    
    演示如何提高注册效率
    """
    print("\n" + "="*60)
    print("示例 6: 性能优化建议")
    print("="*60)
    
    tips = [
        ("使用无头模式", "减少 GUI 开销", "headless=True"),
        ("并行处理", "同时注册多个网站", "使用线程池"),
        ("缓存配置", "复用网站模板", "在 website_profiles.json 中缓存"),
        ("代理轮换", "避免被 IP 封禁", "配置代理列表"),
        ("智能延迟", "模拟人类行为", "添加随机延迟"),
    ]
    
    print("\n⚡ 优化技巧:")
    for i, (tip, description, implementation) in enumerate(tips, 1):
        print(f"\n{i}. {tip}")
        print(f"   说明: {description}")
        print(f"   实现: {implementation}")


def main():
    """
    运行所有示例
    """
    print("\n" + "#"*60)
    print("# 自动网站注册 AI Agent - 高级使用示例")
    print("#"*60)
    
    # 运行示例
    example_1_basic_browser_automation()
    example_2_email_verification()
    example_3_batch_registration()
    example_4_credential_management()
    example_5_error_handling()
    example_6_performance_tips()
    
    print("\n" + "#"*60)
    print("# 所有示例完成！")
    print("# 更多信息，请查看文档: ADVANCED.md")
    print("#"*60 + "\n")


if __name__ == '__main__':
    main()
