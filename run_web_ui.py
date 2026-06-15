#!/usr/bin/env python
"""运行 Web UI 的脚本"""

import os
import sys
from pathlib import Path

# 添加项目目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == '__main__':
    # 确保必要的目录存在
    Path('data').mkdir(exist_ok=True)
    Path('logs').mkdir(exist_ok=True)
    Path('export').mkdir(exist_ok=True)

    # 运行 Flask 应用
    from web_ui.app import app, init_app
    
    print("\n" + "="*60)
    print("🚀 自动网站注册登录 AI Agent - Web UI")
    print("="*60)
    print("\n📍 访问地址: http://localhost:5000")
    print("\n💡 功能说明:")
    print("  1. 配置邮箱和手机号凭证")
    print("  2. 添加要注册的网站URL")
    print("  3. 预览注册表单信息")
    print("  4. 自动注册和生成账号列表")
    print("\n⚠️  按 CTRL+C 停止服务")
    print("="*60 + "\n")
    
    init_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
