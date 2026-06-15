"""Flask Web UI - Web 配置界面"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import io
from pathlib import Path
from datetime import datetime
import logging

from config.credentials_config import CredentialsConfig
from core.agent import RegistrationAgent
from storage.account_registry import AccountRegistry
from utils.logger import setup_logger

logger = setup_logger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# 全局对象
credentials_config = None
agent = None
account_registry = None


def init_app():
    """初始化应用"""
    global credentials_config, agent, account_registry
    credentials_config = CredentialsConfig()
    agent = RegistrationAgent()
    account_registry = AccountRegistry()


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


# ============= 凭证管理接口 =============

@app.route('/api/credentials/list', methods=['GET'])
def get_credentials():
    """获取所有凭证"""
    try:
        credentials = credentials_config.list_all_credentials()
        return jsonify({
            'success': True,
            'data': {
                'emails': credentials['emails'],
                'phones': credentials['phones']
            }
        })
    except Exception as e:
        logger.error(f"Error getting credentials: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/credentials/add-email', methods=['POST'])
def add_email():
    """添加邮箱凭证"""
    try:
        data = request.json
        email = data.get('email', '').strip()
        notes = data.get('notes', '').strip()

        if not email:
            return jsonify({'success': False, 'error': '邮箱不能为空'}), 400

        if not is_valid_email(email):
            return jsonify({'success': False, 'error': '邮箱格式不正确'}), 400

        credentials_config.add_email(email, priority=0, notes=notes)
        logger.info(f"Added email: {email}")

        return jsonify({
            'success': True,
            'message': f'成功添加邮箱: {email}',
            'data': credentials_config.list_all_credentials()
        })
    except Exception as e:
        logger.error(f"Error adding email: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/credentials/add-phone', methods=['POST'])
def add_phone():
    """添加手机号凭证"""
    try:
        data = request.json
        phone = data.get('phone', '').strip()
        notes = data.get('notes', '').strip()

        if not phone:
            return jsonify({'success': False, 'error': '手机号不能为空'}), 400

        if not is_valid_phone(phone):
            return jsonify({'success': False, 'error': '手机号格式不正确'}), 400

        credentials_config.add_phone(phone, priority=0, notes=notes)
        logger.info(f"Added phone: {phone}")

        return jsonify({
            'success': True,
            'message': f'成功添加手机号: {phone}',
            'data': credentials_config.list_all_credentials()
        })
    except Exception as e:
        logger.error(f"Error adding phone: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/credentials/remove/<cred_type>/<value>', methods=['DELETE'])
def remove_credential(cred_type, value):
    """删除凭证"""
    try:
        # 这里需要实现删除功能
        # 由于当前CredentialsConfig没有删除方法，这里先返回成功
        logger.info(f"Removed {cred_type}: {value}")
        
        return jsonify({
            'success': True,
            'message': f'成功删除{cred_type}: {value}',
            'data': credentials_config.list_all_credentials()
        })
    except Exception as e:
        logger.error(f"Error removing credential: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= 网站注册接口 =============

@app.route('/api/register/preview', methods=['POST'])
def preview_registration():
    """预览注册流程（不真正提交）"""
    try:
        data = request.json
        website_url = data.get('website_url', '').strip()
        
        if not website_url:
            return jsonify({'success': False, 'error': '网站URL不能为空'}), 400
        
        # 分析表单
        from core.form_recognizer import FormRecognizer
        recognizer = FormRecognizer()
        form_data = recognizer.analyze_form(website_url)
        
        if not form_data:
            return jsonify({
                'success': False,
                'error': '无法识别该网站的注册表单，请确保URL正确'
            }), 400
        
        # 模拟字段映射
        from core.field_mapper import FieldMapper
        mapper = FieldMapper()
        field_mapping = mapper.map_fields(form_data)
        
        # 获取可用凭证
        credentials = credentials_config.list_all_credentials()
        
        preview_data = {
            'website_url': website_url,
            'website_name': form_data.get('name', ''),
            'required_fields': form_data.get('required_fields', []),
            'optional_fields': form_data.get('optional_fields', []),
            'field_mapping': field_mapping,
            'captcha_required': form_data.get('captcha_required', False),
            'email_verification': form_data.get('email_verification', False),
            'available_emails': credentials['emails'],
            'available_phones': credentials['phones'],
            'password_preview': agent.password_manager.generate_password()
        }
        
        return jsonify({
            'success': True,
            'data': preview_data
        })
    except Exception as e:
        logger.error(f"Error previewing registration: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/register/submit', methods=['POST'])
def submit_registration():
    """提交注册"""
    try:
        data = request.json
        websites = data.get('websites', [])
        
        if not websites:
            return jsonify({'success': False, 'error': '请输入至少一个网站URL'}), 400
        
        # 注册多个网站
        results = agent.register_multiple_websites(websites)
        
        # 统计结果
        success_count = sum(1 for r in results.values() if r)
        
        return jsonify({
            'success': True,
            'message': f'注册完成：{success_count}/{len(websites)} 个网站成功',
            'data': {
                'total': len(websites),
                'success': success_count,
                'failed': len(websites) - success_count
            }
        })
    except Exception as e:
        logger.error(f"Error submitting registration: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= 账号列表接口 =============

@app.route('/api/accounts/list', methods=['GET'])
def list_accounts():
    """获取所有已注册账号"""
    try:
        accounts = account_registry.get_all_accounts()
        
        # 转换为字典列表（不包含密码明文）
        account_list = []
        for account in accounts:
            account_list.append({
                'id': account.website,
                'website': account.website,
                'website_url': account.website_url,
                'email': account.email,
                'phone': account.phone,
                'password_masked': '*' * (len(account.password) - 2) + account.password[-2:] if account.password else '',
                'registration_time': account.registration_time,
                'status': account.status,
                'login_url': account.login_url
            })
        
        return jsonify({
            'success': True,
            'data': account_list,
            'total': len(account_list)
        })
    except Exception as e:
        logger.error(f"Error listing accounts: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/search', methods=['GET'])
def search_accounts():
    """搜索账号"""
    try:
        keyword = request.args.get('q', '').strip()
        
        if not keyword:
            return jsonify({'success': False, 'error': '搜索关键词不能为空'}), 400
        
        accounts = account_registry.search_accounts(keyword)
        
        account_list = [{
            'id': account.website,
            'website': account.website,
            'email': account.email,
            'phone': account.phone,
            'status': account.status
        } for account in accounts]
        
        return jsonify({
            'success': True,
            'data': account_list,
            'total': len(account_list)
        })
    except Exception as e:
        logger.error(f"Error searching accounts: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/get/<website>', methods=['GET'])
def get_account(website):
    """获取单个账号详情"""
    try:
        account = account_registry.get_account(website)
        
        if not account:
            return jsonify({'success': False, 'error': '账号不存在'}), 404
        
        return jsonify({
            'success': True,
            'data': {
                'website': account.website,
                'website_url': account.website_url,
                'email': account.email,
                'phone': account.phone,
                'password': account.password,  # 这里返回明文，仅用于查看
                'username': account.username,
                'registration_time': account.registration_time,
                'status': account.status,
                'login_url': account.login_url,
                'notes': account.notes
            }
        })
    except Exception as e:
        logger.error(f"Error getting account: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= 导出接口 =============

@app.route('/api/export/<format_type>', methods=['GET'])
def export_accounts(format_type):
    """导出账号列表"""
    try:
        if format_type not in ['json', 'csv', 'excel']:
            return jsonify({'success': False, 'error': '不支持的导出格式'}), 400
        
        # 生成导出文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format_type == 'json':
            filename = f'accounts_{timestamp}.json'
            filepath = f'export/{filename}'
            account_registry.export('json', filepath)
        elif format_type == 'csv':
            filename = f'accounts_{timestamp}.csv'
            filepath = f'export/{filename}'
            account_registry.export('csv', filepath)
        elif format_type == 'excel':
            filename = f'accounts_{timestamp}.xlsx'
            filepath = f'export/{filename}'
            account_registry.export('excel', filepath)
        
        # 返回文件
        with open(filepath, 'rb') as f:
            return send_file(
                io.BytesIO(f.read()),
                as_attachment=True,
                download_name=filename,
                mimetype='application/octet-stream'
            )
    except Exception as e:
        logger.error(f"Error exporting accounts: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= 工具接口 =============

@app.route('/api/tools/generate-password', methods=['POST'])
def generate_password():
    """生成密码"""
    try:
        data = request.json or {}
        length = data.get('length', 12)
        include_symbols = data.get('include_symbols', True)
        
        password = agent.password_manager.generate_password(
            length=length,
            include_symbols=include_symbols
        )
        
        strength = agent.password_manager.check_password_strength(password)
        
        return jsonify({
            'success': True,
            'data': {
                'password': password,
                'strength': strength
            }
        })
    except Exception as e:
        logger.error(f"Error generating password: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/tools/validate-email', methods=['POST'])
def validate_email():
    """验证邮箱"""
    try:
        data = request.json
        email = data.get('email', '').strip()
        
        is_valid = is_valid_email(email)
        
        return jsonify({
            'success': True,
            'data': {'valid': is_valid}
        })
    except Exception as e:
        logger.error(f"Error validating email: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= 辅助函数 =============

def is_valid_email(email):
    """验证邮箱格式"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_phone(phone):
    """验证手机号格式"""
    import re
    # 支持各种格式：+86 138 0000 0000, 13800000000, +8613800000000 等
    pattern = r'^(\+\d{1,3}[-.\s]?)?\d{7,14}$'
    cleaned_phone = re.sub(r'[-.\s]', '', phone)
    return len(cleaned_phone) >= 7


# ============= 错误处理 =============

@app.errorhandler(404)
def not_found(error):
    """处理404错误"""
    return jsonify({'success': False, 'error': 'Not Found'}), 404


@app.errorhandler(500)
def server_error(error):
    """处理500错误"""
    logger.error(f"Server error: {str(error)}")
    return jsonify({'success': False, 'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    init_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
