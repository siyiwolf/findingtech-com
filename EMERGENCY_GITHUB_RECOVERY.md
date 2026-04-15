# 🚨 GitHub 连接中断紧急恢复指南

**时间**: 2026-04-16 06:09 (Asia/Shanghai)

**问题**: 无法推送至 `origin main` (HTTPS port 443 timeout)

**诊断**:
- ping: ✅ github.com (20.205.243.166) 可达
- nslookup: ✅ 解析正常
- curl to https://github.com: ✅ TLS握手成功，但数据传输阶段 hanging
- git fetch/push: ❌ 连接超时 (2+ minutes)
- SSH: ❌ 认证失败 (no registered public key)

**可能原因**:
1. 防火墙/代理限制大文件或长连接
2. 网络抖动/路由问题
3. GitHub API 端点间歇性不可达

---

## 📦 已准备的备份

1. **完整 Git Bundle** (26MB)
   ```
   /tmp/findingtech-com-2026-04-16.bundle
   ```
   包含所有分支和tags。可在有网络环境直接使用：

   ```bash
   git clone /tmp/findingtech-com-2026-04-16.bundle findingtech-com --origin local
   cd findingtech-com
   git remote add origin https://github.com/siyiwolf/findingtech-com.git
   git push -u origin main
   ```

2. **Reports ZIP** (6MB)
   - 已上传至 GitHub Release: https://github.com/siyiwolf/findingtech-com/releases/tag/v2026-04-16-upload
   - 文件: `reports_5785KB.zip`
   - 包含所有14个方向的 HTML + PDF

---

## 🛠️ 恢复选项（按优先级）

### 选项 A: 手动推送 Git Bundle (推荐)
在能访问 GitHub 的机器上执行:

```bash
# 1. 复制 bundle 到该机器
scp /tmp/findingtech-com-2026-04-16.bundle user@somewhere:/tmp/

# 2. 克隆并推送
git clone /tmp/findingtech-com-2026-04-16.bundle ftc
cd ftc
git remote set-url origin https://github.com/siyiwolf/findingtech-com.git
# 使用 personal access token 认证
git push -u origin main
```

### 选项 B: 使用 GitHub REST API (已尝试)
- 已创建 Release (v2026-04-16-upload) 并上传 ZIP
- 但 API 写入 `docs/` 时遇到 422 冲突 (文件已存在? 或sha校验问题)
- 可在修复网络后重试 `scripts/upload_via_api_v2.py`

### 选项 C: 临时降级方案 - 提供直链访问
在 GitHub 恢复前，可通过 Release 页面下载 ZIP 查看报告。

---

## 🔧 网络修复尝试 (不成功)

- 调整 `http.postBuffer` 到 500MB
- 设置 `http.lowSpeedLimit` 和 `http.lowSpeedTime`
- 直接 TLS 连接测试: `openssl s_client -connect github.com:443` 正常
- 排除 SSH 认证问题

---

## 📝 后续建议

1. **配置 SSH 密钥**以便在 HTTPS 阻塞时 fallback
   ```bash
   cat ~/.ssh/id_ed25519.pub  # 添加到 GitHub account
   git remote set-url origin git@github.com:siyiwolf/findingtech-com.git
   ```
2. **启用增量推送** (避免一次性大推送)
3. **监控网络质量** (packet loss, latency)

---

**Status**: 项目本地交付 14/20 directions 已完成，仅缺线上发布。内容安全存储在 `/tmp/findingtech-com-2026-04-16.bundle` 和 GitHub Release v2026-04-16-upload。

**紧急联系人**: CEO Agent
