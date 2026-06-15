"""测试套件 - 测试 Selenium 自动化和邮件处理"""

import pytest
import logging
from unittest.mock import Mock, patch, MagicMock

from core.selenium_handler import SeleniumHandler
from core.email_handler import EmailHandler
from core.advanced_agent import AdvancedRegistrationAgent

logger = logging.getLogger(__name__)


class TestSeleniumHandler:
    """Selenium 处理器测试"""

    def test_init_driver(self):
        """测试驱动程序初始化"""
        handler = SeleniumHandler(headless=True)
        # 注意：这需要安装 Chrome/Firefox，在 CI 环境中可能需要特殊配置
        assert handler.headless is True
        assert handler.timeout == 10

    def test_is_valid_url(self):
        """测试 URL 验证"""
        handler = SeleniumHandler()
        
        # 这是一个辅助函数的测试
        valid_urls = [
            'https://example.com',
            'http://github.com/signup',
            'https://www.google.com'
        ]
        
        invalid_urls = [
            'not a url',
            'htp://invalid',
            'ftp://unsupported.com'
        ]
        
        for url in valid_urls:
            try:
                from urllib.parse import urlparse
                result = urlparse(url)
                assert result.scheme in ['http', 'https']
            except Exception as e:
                pytest.fail(f"Failed to parse valid URL: {url}")


class TestEmailHandler:
    """邮件处理器测试"""

    def test_get_imap_server_gmail(self):
        """测试 Gmail IMAP 服务器获取"""
        handler = EmailHandler.__new__(EmailHandler)
        server = handler._EmailHandler__get_imap_server('test@gmail.com')
        assert server == 'imap.gmail.com'

    def test_get_imap_server_outlook(self):
        """测试 Outlook IMAP 服务器获取"""
        handler = EmailHandler.__new__(EmailHandler)
        # 先初始化必要属性
        handler.email_address = 'test@outlook.com'
        handler.password = 'dummy'
        handler.connection = None
        
        server = handler._get_imap_server('test@outlook.com')
        assert server == 'imap-mail.outlook.com'

    def test_decode_header(self):
        """测试邮件头解码"""
        handler = EmailHandler.__new__(EmailHandler)
        
        # 简单文本
        result = handler._decode_header('Simple Subject')
        assert result == 'Simple Subject'

    @patch('imaplib.IMAP4_SSL')
    def test_connection_failure(self, mock_imap):
        """测试连接失败处理"""
        mock_imap.side_effect = Exception("Connection failed")
        
        with patch('core.email_handler.logger') as mock_logger:
            handler = EmailHandler.__new__(EmailHandler)
            handler.email_address = 'test@gmail.com'
            handler.password = 'wrong_password'
            handler.imap_server = 'imap.gmail.com'
            handler.connection = None
            
            # 直接调用 connect 方法（避免 __init__ 中的自动连接）
            with patch('imaplib.IMAP4_SSL', side_effect=Exception("Connection failed")):
                result = handler.connect()
                assert result is False


class TestAdvancedAgent:
    """高级 Agent 测试"""

    def test_initialization(self):
        """测试 Agent 初始化"""
        agent = AdvancedRegistrationAgent(headless=True, use_email_verification=False)
        assert agent.headless is True
        assert agent.use_email_verification is False
        assert agent.selenium_handler is None

    def test_extract_domain(self):
        """测试域名提取"""
        agent = AdvancedRegistrationAgent()
        
        test_cases = [
            ('https://www.github.com/signup', 'github.com'),
            ('https://github.com', 'github.com'),
            ('http://example.com/register', 'example.com'),
        ]
        
        for url, expected_domain in test_cases:
            domain = agent._extract_domain(url)
            assert domain == expected_domain, f"Expected {expected_domain}, got {domain}"

    def test_get_account_mapping(self):
        """测试账号映射获取"""
        agent = AdvancedRegistrationAgent()
        
        # 应该返回列表
        mapping = agent.get_account_mapping()
        assert isinstance(mapping, list)


class TestIntegration:
    """集成测试"""

    def test_password_generation(self):
        """测试密码生成"""
        from core.password_manager import PasswordManager
        
        pm = PasswordManager()
        password = pm.generate_password(length=12, include_symbols=True)
        
        assert len(password) == 12
        assert any(c.isupper() for c in password)
        assert any(c.islower() for c in password)
        assert any(c.isdigit() for c in password)
        assert any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

    def test_password_strength_check(self):
        """测试密码强度检查"""
        from core.password_manager import PasswordManager
        
        pm = PasswordManager()
        
        # 弱密码
        weak = pm.check_password_strength('weak')
        assert 'Weak' in weak['strength'] or 'Very Weak' in weak['strength']
        
        # 强密码
        strong = pm.check_password_strength('StrongP@ss123')
        assert 'Strong' in strong['strength']

    def test_credential_config(self):
        """测试凭证配置"""
        from config.credentials_config import CredentialsConfig
        
        config = CredentialsConfig()
        
        # 测试添加邮箱
        config.add_email('test@gmail.com', priority=0)
        assert 'test@gmail.com' in config.get_emails()
        
        # 测试添加手机号
        config.add_phone('+86 138 0000 0000', priority=0)
        assert '+86 138 0000 0000' in config.get_phones()


if __name__ == '__main__':
    # 运行测试
    pytest.main([__file__, '-v'])
