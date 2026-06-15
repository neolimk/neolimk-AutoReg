// ============= 全局变量 =============
const API_BASE = 'http://localhost:5000/api';
let websites = [];
let allAccounts = [];

// ============= 初始化 =============
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadDashboard();
    loadCredentials();
});

function setupEventListeners() {
    // 导航项点击事件
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const section = item.getAttribute('data-section');
            switchSection(section);
        });
    });

    // 搜索账号
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const keyword = e.target.value.trim();
            if (keyword) {
                searchAccounts(keyword);
            } else {
                loadAccounts();
            }
        });
    }

    // 网站URL输入框回车事件
    const websiteInput = document.getElementById('website-url');
    if (websiteInput) {
        websiteInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                addWebsite();
            }
        });
    }
}

// ============= 切换章节 =============
function switchSection(section) {
    // 隐藏所有章节
    document.querySelectorAll('.section').forEach(s => {
        s.classList.remove('active');
    });

    // 移除所有导航项的active类
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });

    // 显示目标章节
    const targetSection = document.getElementById(section);
    if (targetSection) {
        targetSection.classList.add('active');
    }

    // 标记导航项为active
    document.querySelector(`[data-section="${section}"]`).classList.add('active');

    // 更新页面标题
    const titles = {
        dashboard: '仪表盘',
        credentials: '凭证管理',
        register: '网站注册',
        accounts: '账号列表',
        settings: '设置'
    };
    document.getElementById('page-title').textContent = titles[section] || section;

    // 加载对应数据
    if (section === 'accounts') {
        loadAccounts();
    } else if (section === 'dashboard') {
        loadDashboard();
    }
}

// ============= 仪表盘 =============
async function loadDashboard() {
    try {
        // 加载凭证统计
        const credResponse = await fetch(`${API_BASE}/credentials/list`);
        const credData = await credResponse.json();

        if (credData.success) {
            document.getElementById('total-emails').textContent = credData.data.emails.length;
            document.getElementById('total-phones').textContent = credData.data.phones.length;
        }

        // 加载账号统计
        const accResponse = await fetch(`${API_BASE}/accounts/list`);
        const accData = await accResponse.json();

        if (accData.success) {
            document.getElementById('total-accounts').textContent = accData.total;
            document.getElementById('last-update').textContent = new Date().toLocaleTimeString('zh-CN');

            // 显示最近的账号
            const recentList = document.getElementById('recent-list');
            if (accData.data.length > 0) {
                const recentAccounts = accData.data.slice(0, 5);
                recentList.innerHTML = recentAccounts.map(acc => `
                    <div class="account-item">
                        <div class="account-info">
                            <div class="account-name">${acc.website}</div>
                            <div class="account-email">${acc.email}</div>
                        </div>
                        <span class="account-badge badge-success">${acc.status}</span>
                    </div>
                `).join('');
            } else {
                recentList.innerHTML = '<div class="empty-state"><i class="fas fa-inbox"></i><p>暂无数据</p></div>';
            }
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showToast('加载仪表盘失败', 'error');
    }
}

// ============= 凭证管理 =============
async function loadCredentials() {
    try {
        const response = await fetch(`${API_BASE}/credentials/list`);
        const data = await response.json();

        if (data.success) {
            displayEmails(data.data.emails);
            displayPhones(data.data.phones);
        }
    } catch (error) {
        console.error('Error loading credentials:', error);
        showToast('加载凭证失败', 'error');
    }
}

function displayEmails(emails) {
    const container = document.getElementById('email-list');
    if (emails.length === 0) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-envelope"></i><p>暂无邮箱</p></div>';
        return;
    }

    container.innerHTML = emails.map(email => `
        <div class="credential-item">
            <div class="credential-item-value">
                <div class="credential-item-main">${email}</div>
                <div class="credential-item-note">主邮箱</div>
            </div>
            <div class="credential-actions">
                <button class="btn-delete" onclick="removeCredential('email', '${email}')" title="删除">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

function displayPhones(phones) {
    const container = document.getElementById('phone-list');
    if (phones.length === 0) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-phone"></i><p>暂无手机号</p></div>';
        return;
    }

    container.innerHTML = phones.map(phone => `
        <div class="credential-item">
            <div class="credential-item-value">
                <div class="credential-item-main">${phone}</div>
                <div class="credential-item-note">主手机</div>
            </div>
            <div class="credential-actions">
                <button class="btn-delete" onclick="removeCredential('phone', '${phone}')" title="删除">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

function showAddEmailModal() {
    document.getElementById('add-email-modal').classList.add('active');
}

function showAddPhoneModal() {
    document.getElementById('add-phone-modal').classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

async function submitAddEmail() {
    const email = document.getElementById('email-input').value.trim();
    const notes = document.getElementById('email-notes').value.trim();

    if (!email) {
        showToast('请输入邮箱地址', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/credentials/add-email`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, notes })
        });

        const data = await response.json();

        if (data.success) {
            showToast(data.message, 'success');
            closeModal('add-email-modal');
            document.getElementById('email-input').value = '';
            document.getElementById('email-notes').value = '';
            displayEmails(data.data.emails);
        } else {
            showToast(data.error, 'error');
        }
    } catch (error) {
        console.error('Error adding email:', error);
        showToast('添加邮箱失败', 'error');
    }
}

async function submitAddPhone() {
    const phone = document.getElementById('phone-input').value.trim();
    const notes = document.getElementById('phone-notes').value.trim();

    if (!phone) {
        showToast('请输入手机号', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/credentials/add-phone`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phone, notes })
        });

        const data = await response.json();

        if (data.success) {
            showToast(data.message, 'success');
            closeModal('add-phone-modal');
            document.getElementById('phone-input').value = '';
            document.getElementById('phone-notes').value = '';
            displayPhones(data.data.phones);
        } else {
            showToast(data.error, 'error');
        }
    } catch (error) {
        console.error('Error adding phone:', error);
        showToast('添加手机号失败', 'error');
    }
}

async function removeCredential(type, value) {
    if (!confirm(`确定要删除此${type === 'email' ? '邮箱' : '手机号'}吗？`)) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/credentials/remove/${type}/${encodeURIComponent(value)}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            showToast(data.message, 'success');
            displayEmails(data.data.emails);
            displayPhones(data.data.phones);
        } else {
            showToast(data.error, 'error');
        }
    } catch (error) {
        console.error('Error removing credential:', error);
        showToast('删除失败', 'error');
    }
}

// ============= 网站注册 =============
function addWebsite() {
    const input = document.getElementById('website-url');
    const url = input.value.trim();

    if (!url) {
        showToast('请输入网站URL', 'warning');
        return;
    }

    if (!isValidUrl(url)) {
        showToast('URL格式不正确', 'warning');
        return;
    }

    if (websites.includes(url)) {
        showToast('此网站已添加', 'warning');
        return;
    }

    websites.push(url);
    input.value = '';
    updateWebsiteList();
    previewWebsite(url);
}

function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

function updateWebsiteList() {
    const container = document.getElementById('website-items');
    if (websites.length === 0) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-globe"></i><p>未添加任何网站</p></div>';
        document.getElementById('start-register').style.display = 'none';
        return;
    }

    container.innerHTML = websites.map((url, index) => `
        <div class="item">
            <span class="item-text" title="${url}">${url}</span>
            <button class="btn-remove" onclick="removeWebsite(${index})">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `).join('');

    document.getElementById('start-register').style.display = 'block';
}

function removeWebsite(index) {
    websites.splice(index, 1);
    updateWebsiteList();
}

async function previewWebsite(url) {
    try {
        const response = await fetch(`${API_BASE}/register/preview`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ website_url: url })
        });

        const data = await response.json();
        const previewContainer = document.getElementById('preview-content');

        if (data.success) {
            const preview = data.data;
            previewContainer.innerHTML = `
                <div>
                    <h5>${preview.website_name || preview.website_url}</h5>
                    <div style="margin-top: 15px;">
                        <p><strong>必填字段：</strong></p>
                        <ul style="margin-left: 15px; margin-bottom: 15px;">
                            ${preview.required_fields.map(f => `<li>${f}</li>`).join('')}
                        </ul>

                        ${preview.optional_fields.length > 0 ? `
                            <p><strong>可选字段：</strong></p>
                            <ul style="margin-left: 15px; margin-bottom: 15px;">
                                ${preview.optional_fields.map(f => `<li>${f}</li>`).join('')}
                            </ul>
                        ` : ''}

                        <p><strong>特殊要求：</strong></p>
                        <ul style="margin-left: 15px; margin-bottom: 15px;">
                            <li>验证码: ${preview.captcha_required ? '✓ 需要' : '✗ 不需要'}</li>
                            <li>邮箱验证: ${preview.email_verification ? '✓ 需要' : '✗ 不需要'}</li>
                        </ul>

                        <p><strong>预生成密码：</strong></p>
                        <div style="background: #f3f4f6; padding: 10px; border-radius: 4px; margin-top: 8px; font-family: monospace; word-break: break-all;">
                            ${preview.password_preview}
                        </div>

                        <p style="margin-top: 10px; font-size: 12px; color: #999;">
                            <i class="fas fa-info-circle"></i> 将使用配置的邮箱/手机号自动填充相应字段
                        </p>
                    </div>
                </div>
            `;
        } else {
            previewContainer.innerHTML = `<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>${data.error}</p></div>`;
        }
    } catch (error) {
        console.error('Error previewing website:', error);
        document.getElementById('preview-content').innerHTML = '<div class="empty-state"><i class="fas fa-error"></i><p>预览失败</p></div>';
    }
}

async function startRegistration() {
    if (websites.length === 0) {
        showToast('请至少添加一个网站', 'warning');
        return;
    }

    if (!confirm(`确定要开始注册这 ${websites.length} 个网站吗？`)) {
        return;
    }

    try {
        const btn = document.getElementById('start-register');
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 注册中...';

        const response = await fetch(`${API_BASE}/register/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ websites })
        });

        const data = await response.json();

        if (data.success) {
            showToast(data.message, 'success');
            websites = [];
            updateWebsiteList();
            loadAccounts();
            setTimeout(() => {
                switchSection('accounts');
            }, 1000);
        } else {
            showToast(data.error, 'error');
        }
    } catch (error) {
        console.error('Error starting registration:', error);
        showToast('注册失败', 'error');
    } finally {
        const btn = document.getElementById('start-register');
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-rocket"></i> 开始注册';
    }
}

// ============= 账号列表 =============
async function loadAccounts() {
    try {
        const response = await fetch(`${API_BASE}/accounts/list`);
        const data = await response.json();

        if (data.success) {
            allAccounts = data.data;
            displayAccounts(data.data);
        }
    } catch (error) {
        console.error('Error loading accounts:', error);
        showToast('加载账号失败', 'error');
    }
}

async function searchAccounts(keyword) {
    try {
        const response = await fetch(`${API_BASE}/accounts/search?q=${encodeURIComponent(keyword)}`);
        const data = await response.json();

        if (data.success) {
            displayAccounts(data.data);
        }
    } catch (error) {
        console.error('Error searching accounts:', error);
    }
}

function displayAccounts(accounts) {
    const tbody = document.getElementById('accounts-tbody');

    if (accounts.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">暂无账号</td></tr>';
        return;
    }

    tbody.innerHTML = accounts.map(acc => `
        <tr>
            <td><strong>${acc.website}</strong></td>
            <td>${acc.email}</td>
            <td>${acc.phone || '-'}</td>
            <td>
                <span class="password-cell">●●●●●●●●</span>
                <button class="btn-copy" onclick="viewPassword('${acc.website}')" title="查看">
                    <i class="fas fa-eye"></i>
                </button>
            </td>
            <td>
                <span class="status-badge ${acc.status === 'success' ? 'status-success' : 'status-failed'}">
                    ${acc.status === 'success' ? '成功' : '失败'}
                </span>
            </td>
            <td>${formatDate(acc.registration_time)}</td>
            <td>
                <button class="btn-copy" onclick="copyToClipboard('${acc.email}')" title="复制邮箱">
                    <i class="fas fa-copy"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

async function viewPassword(website) {
    try {
        const response = await fetch(`${API_BASE}/accounts/get/${encodeURIComponent(website)}`);
        const data = await response.json();

        if (data.success) {
            const acc = data.data;
            alert(`网站: ${acc.website}\n邮箱: ${acc.email}\n密码: ${acc.password}`);
        }
    } catch (error) {
        console.error('Error viewing password:', error);
        showToast('查看密码失败', 'error');
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('已复制到剪贴板', 'success');
    }).catch(err => {
        console.error('Copy failed:', err);
    });
}

async function exportAccounts(format) {
    try {
        window.location.href = `${API_BASE}/export/${format}`;
        showToast(`正在下载 ${format.toUpperCase()} 文件...`, 'success');
    } catch (error) {
        console.error('Error exporting accounts:', error);
        showToast('导出失败', 'error');
    }
}

// ============= 工具函数 =============
function formatDate(dateString) {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleString('zh-CN');
}

async function testPasswordGenerator() {
    try {
        const length = parseInt(document.getElementById('password-length').value);
        const includeSymbols = document.getElementById('include-symbols').checked;

        const response = await fetch(`${API_BASE}/tools/generate-password`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ length, include_symbols: includeSymbols })
        });

        const data = await response.json();

        if (data.success) {
            const pwd = data.data;
            alert(`生成的密码: ${pwd.password}\n强度: ${pwd.strength.strength}\n建议: ${pwd.strength.feedback.join(', ') || '无'}`);
        }
    } catch (error) {
        console.error('Error generating password:', error);
        showToast('生成密码失败', 'error');
    }
}

function clearAllData() {
    if (confirm('确定要删除所有数据吗？此操作不可撤销！')) {
        showToast('功能开发中...', 'warning');
    }
}

function backupData() {
    exportAccounts('json');
}

// ============= Toast 通知 =============
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// 关闭模态框点击背景
window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});
