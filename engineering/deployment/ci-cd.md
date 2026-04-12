# CI/CD 持续集成与交付规范

---

## 🎯 目标

- **自动化**：代码提交 → 构建 → 测试 → 部署全流程自动化
- **快速反馈**：开发人员 10 分钟内知道构建结果
- **质量门禁**：只有通过测试的代码才能进入 Staging/Production
- **可追溯**：每个发布对应 Git commit，支持回滚

---

## 🏗️ 架构

```
Developer → GitHub Push → GitHub Actions → Build & Test → Docker Image → 
  └─> Staging (自动部署) → 人工审批 → Production (K8s) → 监控告警
```

---

## 📦 组件

| 组件 | 工具 | 版本 | 用途 |
|------|------|------|------|
| 代码托管 | GitHub / GitLab | - | 版本控制 |
| CI/CD | GitHub Actions | - | 自动化流水线 |
| 容器 Registry | Docker Hub / GHCR | - | 镜像存储 |
| 编排 | Kubernetes (EKS/ACK/K3s) | 1.28+ | 容器编排 |
| 配置管理 | Helm | 3.x | K8s 部署包 |
| 镜像扫描 | Trivy | - | 安全漏洞扫描 |
| 通知 | 企业微信/钉钉 Webhook | - | 构建状态通知 |

---

## 🔄 流水线设计

### 1. 代码检查（静态分析）

```yaml
name: Lint
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install black flake8 mypy
      - name: Run black
        run: black --check .
      - name: Run flake8
        run: flake8 .
      - name: Run mypy
        run: mypy .
```

### 2. 单元测试 + 构建

```yaml
name: Test & Build
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v3
      - name: Set up Go
        uses: actions/setup-go@v4
        with:
          go-version: '1.22'
      - name: Run tests
        run: |
          go test -v ./... -coverprofile=coverage.out
          go tool cover -html=coverage.out -o coverage.html
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Docker meta
        id: meta
        uses: crazy-max/ghaction-docker-meta@v1
        with:
          images: findingtech/${{ github.event.repository.name }}
          tag-sha: true
      - name: Login to DockerHub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: ${{ github.ref == 'refs/heads/main' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=findingtech/${{ github.event.repository.name }}:buildcache
          cache-to: type=registry,ref=findingtech/${{ github.event.repository.name }}:buildcache,mode=max
```

### 3. 部署到 Staging（自动）

```yaml
name: Deploy to Staging
on:
  push:
    branches: [ develop ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to K8s
        env:
          KUBECONFIG: ${{ secrets.KUBECONFIG_STAGING }}
        run: |
          helm upgrade --install device-service ./helm/device-service \
            --namespace finding-staging \
            --set image.tag=${{ github.sha }} \
            --wait --timeout 5m
      - name: Smoke test
        run: |
          curl -f https://staging-api.findingtech.com/health
```

### 4. 部署到 Production（手动审批）

```yaml
name: Deploy to Production
on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Release version (e.g., v1.2.3)'
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to K8s
        env:
          KUBECONFIG: ${{ secrets.KUBECONFIG_PROD }}
        run: |
          helm upgrade --install device-service ./helm/device-service \
            --namespace finding-prod \
            --set image.tag=${{ github.event.inputs.version }} \
            --wait --timeout 10m
      - name: Post-deployment check
        run: |
          curl -f https://api.findingtech.com/health
          # 检查关键指标
          curl -s https://api.findingtech.com/metrics | grep up
```

---

## 🧪 测试策略集成

| 测试层级 | 触发时机 | 工具 |
|----------|----------|------|
| 单元测试 | 每次 push | pytest, go test, jest |
| 集成测试 | Merge 到 develop | Postman/Newman, Supertest |
| 端到端测试 | 每日凌晨 | Cypress / Playwright |
| 性能测试 | 每周 | k6, JMeter |
| 安全扫描 | 每次 build | Trivy, Snyk, OWASP ZAP |

**质量门禁**：
- 单元测试覆盖率 >= 80%
- 集成测试全部通过
- 没有 HIGH 级别安全漏洞
- 镜像扫描无 Critical 漏洞

---

## 📊 监控与告警

### 应用监控
- **指标**：Prometheus + Grafana
  - HTTP 成功率、延迟、QPS
  - 数据库连接数、慢查询
  - 机器人在线数、任务队列长度
- **告警规则**：
  ```yaml
  groups:
    - name: api_alerts
      rules:
        - alert: HighErrorRate
          expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
          for: 2m
          annotations:
            summary: "API 错误率过高"
    - alert: DeviceOffline
      expr: device_online{status="offline"} > 10
      for: 5m
  ```

### 日志
- 所有服务输出 JSON 日志到 stdout
- Filebeat 收集 → Elasticsearch
- Kibana 查询

---

## 🔐 安全合规

- **镜像扫描**：Trivy 扫描每个 Docker 镜像，发现 CVE 阻塞构建
- **依赖检查**：Dependabot / Renovate 自动更新依赖
- **密钥管理**：GitHub Secrets / HashiCorp Vault，不硬编码
- **合规性**：代码扫描（CodeQL），满足 ISO27001 要求

---

## 🔄 回滚策略

- **金丝雀发布**：先部署 5% 流量，观察 30 分钟，无问题全量
- **蓝绿部署**：新版本（蓝）与旧版本（绿）并存，切换流量
- **快速回滚**：一键回滚到上一版本（`helm rollback`）
- **数据库迁移**：Liquibase/Flyway，支持回滚 SQL

---

## 💰 成本优化

- **镜像层缓存**：利用 GitHub Actions 缓存，加速构建
- **按需启动作业**：`suppo
- **资源请求限制**：K8s 设置 requests/limits，避免资源争抢
- **自动伸缩**：HPA 根据 CPU/自定义指标自动扩缩容
- **Spot 实例**：Staging 环境使用 Spot 实例降低成本

---

## 📚 文档与培训

- **Runbook**：每个服务有部署、运维手册
- **Postmortem**：每次生产事故后分析，改进措施
- **Onboarding**：新工程师 1 天上手指南
- **定期演练**：每季度灾难恢复演练

---

**维护**：DevOps 团队  
**最后更新**：2025-04-12  
**版本**：v0.1
