"""Selenium 浏览器自动化处理模块 - 真实浏览器自动化"""

from typing import Dict, List, Optional, Tuple
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

from utils.logger import setup_logger

logger = setup_logger(__name__)


class SeleniumHandler:
    """Selenium 浏览器自动化处理器"""

    def __init__(self, headless: bool = True, timeout: int = 10):
        """
        初始化 Selenium 处理器
        
        Args:
            headless: 是否使用无头模式
            timeout: 等待超时时间（秒）
        """
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.wait = None

    def init_driver(self, browser: str = 'chrome') -> bool:
        """初始化 WebDriver
        
        Args:
            browser: 浏览器类型 (chrome, firefox)
            
        Returns:
            初始化是否成功
        """
        try:
            if browser.lower() == 'chrome':
                options = webdriver.ChromeOptions()
                if self.headless:
                    options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option('excludeSwitches', ['enable-automation'])
                options.add_experimental_option('useAutomationExtension', False)
                
                from webdriver_manager.chrome import ChromeDriverManager
                self.driver = webdriver.Chrome(
                    service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
                    options=options
                )
            elif browser.lower() == 'firefox':
                options = webdriver.FirefoxOptions()
                if self.headless:
                    options.add_argument('--headless')
                
                from webdriver_manager.firefox import GeckoDriverManager
                self.driver = webdriver.Firefox(
                    service=webdriver.firefox.service.Service(GeckoDriverManager().install()),
                    options=options
                )
            else:
                logger.error(f"Unsupported browser: {browser}")
                return False

            self.wait = WebDriverWait(self.driver, self.timeout)
            logger.info(f"WebDriver initialized successfully with {browser}")
            return True
        except Exception as e:
            logger.error(f"Error initializing WebDriver: {str(e)}")
            return False

    def open_url(self, url: str) -> bool:
        """打开 URL
        
        Args:
            url: 要打开的 URL
            
        Returns:
            是否成功打开
        """
        try:
            if not self.driver:
                return False
            self.driver.get(url)
            logger.info(f"Opened URL: {url}")
            return True
        except Exception as e:
            logger.error(f"Error opening URL: {str(e)}")
            return False

    def find_element(self, selector: str, by: By = By.CSS_SELECTOR, wait: bool = True):
        """查找元素
        
        Args:
            selector: CSS 选择器或 XPath
            by: 查找方式
            wait: 是否等待元素出现
            
        Returns:
            元素对象或 None
        """
        try:
            if wait:
                element = self.wait.until(EC.presence_of_element_located((by, selector)))
            else:
                element = self.driver.find_element(by, selector)
            return element
        except TimeoutException:
            logger.warning(f"Timeout waiting for element: {selector}")
            return None
        except NoSuchElementException:
            logger.warning(f"Element not found: {selector}")
            return None

    def find_elements(self, selector: str, by: By = By.CSS_SELECTOR):
        """查找多个元素
        
        Args:
            selector: CSS 选择器或 XPath
            by: 查找方式
            
        Returns:
            元素列表
        """
        try:
            elements = self.driver.find_elements(by, selector)
            return elements
        except Exception as e:
            logger.error(f"Error finding elements: {str(e)}")
            return []

    def fill_input(self, selector: str, value: str, clear: bool = True) -> bool:
        """填充输入框
        
        Args:
            selector: CSS 选择器
            value: 要填充的值
            clear: 是否先清空
            
        Returns:
            是否成功填充
        """
        try:
            element = self.find_element(selector)
            if not element:
                return False
            
            if clear:
                element.clear()
            element.send_keys(value)
            logger.debug(f"Filled input: {selector}")
            return True
        except Exception as e:
            logger.error(f"Error filling input: {str(e)}")
            return False

    def click_element(self, selector: str) -> bool:
        """点击元素
        
        Args:
            selector: CSS 选择器
            
        Returns:
            是否成功点击
        """
        try:
            element = self.find_element(selector)
            if not element:
                return False
            
            # 使用 JavaScript 点击以避免某些问题
            self.driver.execute_script("arguments[0].click();", element)
            logger.debug(f"Clicked element: {selector}")
            return True
        except Exception as e:
            logger.error(f"Error clicking element: {str(e)}")
            return False

    def submit_form(self, form_selector: str = None) -> bool:
        """提交表单
        
        Args:
            form_selector: 表单选择器（可选）
            
        Returns:
            是否成功提交
        """
        try:
            if form_selector:
                form = self.find_element(form_selector)
                if form:
                    form.submit()
            else:
                # 查找任何提交按钮并点击
                submit_buttons = [
                    'button[type="submit"]',
                    'input[type="submit"]',
                    '[role="button"][aria-label*="submit" i]'
                ]
                for selector in submit_buttons:
                    if self.click_element(selector):
                        logger.info(f"Form submitted via: {selector}")
                        return True
            return False
        except Exception as e:
            logger.error(f"Error submitting form: {str(e)}")
            return False

    def wait_for_element(self, selector: str, timeout: int = None) -> bool:
        """等待元素出现
        
        Args:
            selector: CSS 选择器
            timeout: 超时时间
            
        Returns:
            元素是否出现
        """
        try:
            timeout = timeout or self.timeout
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return True
        except TimeoutException:
            logger.warning(f"Timeout waiting for element: {selector}")
            return False

    def get_text(self, selector: str) -> Optional[str]:
        """获取元素文本
        
        Args:
            selector: CSS 选择器
            
        Returns:
            元素文本或 None
        """
        try:
            element = self.find_element(selector, wait=False)
            return element.text if element else None
        except Exception as e:
            logger.error(f"Error getting text: {str(e)}")
            return None

    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """获取元素属性
        
        Args:
            selector: CSS 选择器
            attribute: 属性名
            
        Returns:
            属性值或 None
        """
        try:
            element = self.find_element(selector, wait=False)
            return element.get_attribute(attribute) if element else None
        except Exception as e:
            logger.error(f"Error getting attribute: {str(e)}")
            return None

    def execute_script(self, script: str, *args):
        """执行 JavaScript 脚本
        
        Args:
            script: JavaScript 代码
            *args: 参数
            
        Returns:
            脚本执行结果
        """
        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            logger.error(f"Error executing script: {str(e)}")
            return None

    def take_screenshot(self, filepath: str) -> bool:
        """截图
        
        Args:
            filepath: 截图保存路径
            
        Returns:
            是否成功截图
        """
        try:
            self.driver.save_screenshot(filepath)
            logger.info(f"Screenshot saved: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error taking screenshot: {str(e)}")
            return False

    def switch_to_iframe(self, selector: str) -> bool:
        """切换到 iframe
        
        Args:
            selector: iframe 选择器
            
        Returns:
            是否成功切换
        """
        try:
            iframe = self.find_element(selector)
            if iframe:
                self.driver.switch_to.frame(iframe)
                logger.debug(f"Switched to iframe: {selector}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error switching to iframe: {str(e)}")
            return False

    def switch_to_default_content(self) -> bool:
        """切换回默认内容"""
        try:
            self.driver.switch_to.default_content()
            return True
        except Exception as e:
            logger.error(f"Error switching to default content: {str(e)}")
            return False

    def scroll_to_element(self, selector: str) -> bool:
        """滚动到元素
        
        Args:
            selector: CSS 选择器
            
        Returns:
            是否成功滚动
        """
        try:
            element = self.find_element(selector)
            if element:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)  # 等待滚动完成
                return True
            return False
        except Exception as e:
            logger.error(f"Error scrolling to element: {str(e)}")
            return False

    def wait_and_close_popup(self, selector: str, max_wait: int = 5) -> bool:
        """等待并关闭弹出框
        
        Args:
            selector: 关闭按钮选择器
            max_wait: 最长等待时间
            
        Returns:
            是否成功关闭
        """
        try:
            for _ in range(max_wait):
                elements = self.find_elements(selector)
                if elements:
                    self.driver.execute_script("arguments[0].click();", elements[0])
                    logger.info(f"Popup closed: {selector}")
                    time.sleep(0.5)
                    return True
                time.sleep(1)
            return False
        except Exception as e:
            logger.error(f"Error closing popup: {str(e)}")
            return False

    def close(self) -> None:
        """关闭浏览器"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("WebDriver closed")
        except Exception as e:
            logger.error(f"Error closing WebDriver: {str(e)}")

    def __del__(self):
        """析构函数"""
        self.close()
