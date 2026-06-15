"""邮件处理模块 - 自动接收和验证邮件"""

from typing import List, Optional, Dict
import imaplib
import email
from email.header import decode_header
import logging
import re
import time
from datetime import datetime, timedelta

from utils.logger import setup_logger

logger = setup_logger(__name__)


class EmailHandler:
    """邮件处理器 - 用于接收验证码和确认链接"""

    def __init__(self, email_address: str, password: str, imap_server: str = None):
        """
        初始化邮件处理器
        
        Args:
            email_address: 邮箱地址
            password: 邮箱密码或应用密码
            imap_server: IMAP 服务器地址
        """
        self.email_address = email_address
        self.password = password
        self.imap_server = imap_server or self._get_imap_server(email_address)
        self.connection = None
        self.connect()

    def _get_imap_server(self, email_address: str) -> str:
        """根据邮箱获取 IMAP 服务器
        
        Args:
            email_address: 邮箱地址
            
        Returns:
            IMAP 服务器地址
        """
        domain_map = {
            'gmail.com': 'imap.gmail.com',
            'outlook.com': 'imap-mail.outlook.com',
            'hotmail.com': 'imap-mail.outlook.com',
            '163.com': 'imap.163.com',
            'qq.com': 'imap.qq.com',
            'sina.com': 'imap.sina.com',
            'foxmail.com': 'imap.qq.com',
        }
        domain = email_address.split('@')[1].lower()
        return domain_map.get(domain, f'imap.{domain}')

    def connect(self) -> bool:
        """连接到 IMAP 服务器
        
        Returns:
            是否连接成功
        """
        try:
            self.connection = imaplib.IMAP4_SSL(self.imap_server)
            self.connection.login(self.email_address, self.password)
            logger.info(f"Connected to IMAP server: {self.imap_server}")
            return True
        except Exception as e:
            logger.error(f"Error connecting to IMAP: {str(e)}")
            return False

    def disconnect(self) -> None:
        """断开连接"""
        try:
            if self.connection:
                self.connection.close()
                self.connection.logout()
                logger.info("Disconnected from IMAP server")
        except Exception as e:
            logger.error(f"Error disconnecting: {str(e)}")

    def get_verification_code(
        self,
        sender_keywords: List[str] = None,
        subject_keywords: List[str] = None,
        timeout: int = 300,
        code_pattern: str = r'\d{4,6}'
    ) -> Optional[str]:
        """获取验证码
        
        Args:
            sender_keywords: 发件人关键词列表
            subject_keywords: 主题关键词列表
            timeout: 超时时间（秒）
            code_pattern: 验证码正则表达式
            
        Returns:
            验证码或 None
        """
        try:
            start_time = time.time()
            while time.time() - start_time < timeout:
                # 选择收件箱
                self.connection.select('INBOX')
                
                # 搜索邮件
                status, messages = self.connection.search(None, 'ALL')
                if status != 'OK':
                    logger.warning("Failed to search emails")
                    time.sleep(5)
                    continue

                # 获取最新邮件
                message_ids = messages[0].split()
                if not message_ids:
                    logger.info("No emails found, waiting...")
                    time.sleep(5)
                    continue

                # 检查最新的几封邮件
                for msg_id in reversed(message_ids[-5:]):
                    try:
                        status, msg_data = self.connection.fetch(msg_id, '(RFC822)')
                        if status != 'OK':
                            continue

                        msg = email.message_from_bytes(msg_data[0][1])
                        
                        # 检查发件人
                        sender = msg.get('From', '').lower()
                        if sender_keywords:
                            if not any(keyword.lower() in sender for keyword in sender_keywords):
                                continue
                        
                        # 检查主题
                        subject = self._decode_header(msg.get('Subject', ''))
                        if subject_keywords:
                            if not any(keyword.lower() in subject.lower() for keyword in subject_keywords):
                                continue
                        
                        # 获取邮件正文
                        body = self._get_email_body(msg)
                        
                        # 查找验证码
                        match = re.search(code_pattern, body)
                        if match:
                            code = match.group()
                            logger.info(f"Found verification code: {code}")
                            return code
                    except Exception as e:
                        logger.error(f"Error processing email: {str(e)}")
                        continue

                logger.info("No verification code found, waiting...")
                time.sleep(5)

            logger.warning(f"Timeout waiting for verification code after {timeout}s")
            return None
        except Exception as e:
            logger.error(f"Error getting verification code: {str(e)}")
            return None

    def get_confirmation_link(
        self,
        sender_keywords: List[str] = None,
        subject_keywords: List[str] = None,
        link_pattern: str = r'https?://[^\s]+',
        timeout: int = 300
    ) -> Optional[str]:
        """获取确认链接
        
        Args:
            sender_keywords: 发件人关键词
            subject_keywords: 主题关键词
            link_pattern: 链接正则表达式
            timeout: 超时时间
            
        Returns:
            确认链接或 None
        """
        try:
            start_time = time.time()
            while time.time() - start_time < timeout:
                self.connection.select('INBOX')
                status, messages = self.connection.search(None, 'ALL')
                
                if status != 'OK':
                    time.sleep(5)
                    continue

                message_ids = messages[0].split()
                if not message_ids:
                    time.sleep(5)
                    continue

                for msg_id in reversed(message_ids[-5:]):
                    try:
                        status, msg_data = self.connection.fetch(msg_id, '(RFC822)')
                        if status != 'OK':
                            continue

                        msg = email.message_from_bytes(msg_data[0][1])
                        
                        # 检查发件人和主题
                        sender = msg.get('From', '').lower()
                        subject = self._decode_header(msg.get('Subject', ''))
                        
                        if sender_keywords:
                            if not any(kw.lower() in sender for kw in sender_keywords):
                                continue
                        
                        if subject_keywords:
                            if not any(kw.lower() in subject.lower() for kw in subject_keywords):
                                continue
                        
                        body = self._get_email_body(msg)
                        match = re.search(link_pattern, body)
                        
                        if match:
                            link = match.group()
                            logger.info(f"Found confirmation link")
                            return link
                    except Exception as e:
                        logger.error(f"Error processing email: {str(e)}")
                        continue

                logger.info("No confirmation link found, waiting...")
                time.sleep(5)

            logger.warning(f"Timeout waiting for confirmation link after {timeout}s")
            return None
        except Exception as e:
            logger.error(f"Error getting confirmation link: {str(e)}")
            return None

    def _decode_header(self, header_text: str) -> str:
        """解码邮件头
        
        Args:
            header_text: 邮件头文本
            
        Returns:
            解码后的文本
        """
        try:
            decoded_parts = decode_header(header_text)
            result = ""
            for part, encoding in decoded_parts:
                if isinstance(part, bytes):
                    result += part.decode(encoding or 'utf-8', errors='ignore')
                else:
                    result += str(part)
            return result
        except Exception as e:
            logger.error(f"Error decoding header: {str(e)}")
            return header_text

    def _get_email_body(self, msg: email.message.Message) -> str:
        """提取邮件正文
        
        Args:
            msg: 邮件对象
            
        Returns:
            邮件正文
        """
        body = ""
        try:
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        payload = part.get_payload(decode=True)
                        if payload:
                            body += payload.decode('utf-8', errors='ignore')
                    elif part.get_content_type() == 'text/html':
                        payload = part.get_payload(decode=True)
                        if payload:
                            body += payload.decode('utf-8', errors='ignore')
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body += payload.decode('utf-8', errors='ignore')
        except Exception as e:
            logger.error(f"Error extracting body: {str(e)}")
        
        return body

    def __del__(self):
        """析构函数"""
        self.disconnect()
