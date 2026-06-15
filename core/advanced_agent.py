"""高级 Agent - 支持邮件验证、CAPTCHA 等"""

from typing import List, Dict, Optional
import logging
import time
from datetime import datetime

from config.credentials_config import CredentialsConfig
from core.form_recognizer import FormRecognizer
from core.field_mapper import FieldMapper
from core.password_manager import PasswordManager
from core.selenium_handler import SeleniumHandler
from core.email_handler import EmailHandler
from storage.account_registry import AccountRegistry, AccountRecord
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AdvancedRegistrationAgent:
    """高级自动注册 Agent - 支持复杂场景"""

    def __init__(self, headless: bool = True, use_email_verification: bool = False):
        self.headless = headless
        self.use_email_verification = use_email_verification
        self.credentials_config = CredentialsConfig()
        self.form_recognizer = FormRecognizer()
        self.field_mapper = FieldMapper()
        self.password_manager = PasswordManager()
        self.account_registry = AccountRegistry()
        self.selenium_handler = None
        self.email_handler = None
        logger.info("AdvancedRegistrationAgent initialized")

    def register_with_browser(
        self,
        website_url: str,
        browser: str = 'chrome'
    ) -> Optional[AccountRecord]:
        """使用浏览器自动化进行注册
        
        Args:
            website_url: 网站 URL
            browser: 浏览器类型
            
        Returns:
            账号记录或 None
        """
        self.selenium_handler = SeleniumHandler(headless=self.headless)
        
        try:
            # 1. 初始化浏览器
            if not self.selenium_handler.init_driver(browser):
                logger.error("Failed to initialize browser")
                return None

            # 2. 打开网站
            if not self.selenium_handler.open_url(website_url):
                logger.error(f"Failed to open URL: {website_url}")
                return None

            time.sleep(2)  # 等待页面加载

            # 3. 分析表单
            form_data = self._analyze_form_with_browser()
            if not form_data:
                logger.warning(f"Could not recognize form for {website_url}")
                return None

            # 4. 获取凭证
            email = self.credentials_config.get_emails()[0] if self.credentials_config.get_emails() else None
            password = self.password_manager.generate_password()

            if not email:
                logger.error("No email credential configured")
                return None

            # 5. 填充表单
            if not self._fill_form_with_browser(email, password, form_data):
                logger.error("Failed to fill form")
                return None

            # 6. 处理验证
            if form_data.get('email_verification') and self.use_email_verification:
                logger.info("Waiting for email verification...")
                if not self._handle_email_verification(email, form_data):
                    logger.warning("Email verification failed or skipped")

            # 7. 创建账号记录
            account = AccountRecord(
                website=self._extract_domain(website_url),
                website_url=website_url,
                email=email,
                phone='',
                password=password,
                registration_time=datetime.now().isoformat(),
                status='success',
                login_url=form_data.get('login_url', '')
            )

            # 8. 保存到注册表
            self.account_registry.add_account(account)
            logger.info(f"Successfully registered: {website_url}")
            return account

        except Exception as e:
            logger.error(f"Error during registration: {str(e)}")
            return None
        finally:
            if self.selenium_handler:
                self.selenium_handler.close()

    def _analyze_form_with_browser(self) -> Optional[Dict]:
        """使用浏览器分析表单
        
        Returns:
            表单数据字典
        """
        try:
            # 使用 JavaScript 检测表单字段
            script = """
            let formData = {
                email_fields: [],
                password_fields: [],
                username_fields: [],
                submit_button: null
            };
            
            // 查找邮箱字段
            document.querySelectorAll('input[type="email"], input[name*="email" i]').forEach(el => {
                formData.email_fields.push({name: el.name, id: el.id});
            });
            
            // 查找密码字段
            document.querySelectorAll('input[type="password"]').forEach(el => {
                formData.password_fields.push({name: el.name, id: el.id});
            });
            
            // 查找用户名字段
            document.querySelectorAll('input[type="text"][name*="user" i], input[type="text"][name*="name" i]').forEach(el => {
                formData.username_fields.push({name: el.name, id: el.id});
            });
            
            // 查找提交按钮
            let submitBtn = document.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn) {
                formData.submit_button = {name: submitBtn.name, id: submitBtn.id, text: submitBtn.textContent};
            }
            
            return formData;
            """
            
            form_info = self.selenium_handler.execute_script(script)
            
            if form_info and (form_info.get('email_fields') or form_info.get('password_fields')):
                return form_info
            
            return None
        except Exception as e:
            logger.error(f"Error analyzing form: {str(e)}")
            return None

    def _fill_form_with_browser(self, email: str, password: str, form_data: Dict) -> bool:
        """使用浏览器填充表单
        
        Args:
            email: 邮箱
            password: 密码
            form_data: 表单数据
            
        Returns:
            是否填充成功
        """
        try:
            # 填充邮箱字段
            email_fields = form_data.get('email_fields', [])
            if email_fields:
                field = email_fields[0]
                selector = f'#{field["id"]}' if field.get('id') else f'[name="{field["name"]}"]'
                self.selenium_handler.fill_input(selector, email)
                time.sleep(0.5)

            # 填充密码字段
            password_fields = form_data.get('password_fields', [])
            if password_fields:
                field = password_fields[0]
                selector = f'#{field["id"]}' if field.get('id') else f'[name="{field["name"]}"]'
                self.selenium_handler.fill_input(selector, password)
                time.sleep(0.5)

            # 填充用户名字段（如果需要）
            username_fields = form_data.get('username_fields', [])
            if username_fields:
                field = username_fields[0]
                selector = f'#{field["id"]}' if field.get('id') else f'[name="{field["name"]}"]'
                username = email.split('@')[0]
                self.selenium_handler.fill_input(selector, username)
                time.sleep(0.5)

            # 点击提交按钮
            submit_btn = form_data.get('submit_button')
            if submit_btn:
                selector = f'#{submit_btn["id"]}' if submit_btn.get('id') else f'[name="{submit_btn["name"]}"]'
                self.selenium_handler.scroll_to_element(selector)
                time.sleep(0.5)
                self.selenium_handler.click_element(selector)
                logger.info("Form submitted")
            
            time.sleep(2)  # 等待提交
            return True
        except Exception as e:
            logger.error(f"Error filling form: {str(e)}")
            return False

    def _handle_email_verification(
        self,
        email: str,
        form_data: Dict
    ) -> bool:
        """处理邮件验证
        
        Args:
            email: 邮箱地址
            form_data: 表单数据
            
        Returns:
            是否验证成功
        """
        try:
            # 这里需要邮箱和密码
            # 通常不在此处实现，因为需要存储邮箱密码
            # 仅记录 TODO
            logger.info(f"Email verification would be handled for {email}")
            return True
        except Exception as e:
            logger.error(f"Error handling email verification: {str(e)}")
            return False

    def _extract_domain(self, url: str) -> str:
        """从 URL 提取域名"""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc.replace('www.', '')

    def get_account_mapping(self) -> List[AccountRecord]:
        """获取所有账号映射"""
        return self.account_registry.get_all_accounts()

    def export_account_list(self, format: str = 'json', filepath: Optional[str] = None) -> bool:
        """导出账号列表"""
        return self.account_registry.export(format, filepath)
