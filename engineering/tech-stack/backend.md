# 后端技术栈

---

## 🎯 技术选型原则

- **高并发**：支持千级机器人连接，万级 App 并发
- **可扩展**：微服务架构，按需水平扩展
- **容错性**：故障隔离，自动恢复
- **易运维**：容器化，监控完善
- **国产化**：优先国产中间件、数据库

---

## 📦 微服务架构

### 服务清单

| 服务名 | 职责 | 语言/框架 | 端口 | 依赖 |
|--------|------|-----------|------|------|
| `api-gateway` | API 统一入口、限流、鉴权 | Kong / APISIX | 80/443 | - |
| `auth-service` | 认证与授权（OAuth2/JWT） | Go + Gin | 8080 | PostgreSQL |
| `device-service` | 设备管理（注册、状态、OTA） | Go + Gin | 8081 | PostgreSQL, Redis |
| `scheduler-service` | AI 任务调度核心 | Python + FastAPI | 8082 | Redis, Kafka |
| `telemetry-service` | 时序数据采集与存储 | Go + InfluxDB | 8083 | TimescaleDB |
| `websocket-service` | 实时推送 | Node.js + Socket.IO | 3000 | Redis |
| `analytics-service` | 数据分析、报表 | Python + Pandas | 8084 | PostgreSQL, ClickHouse |
| `billing-service` | 订阅与计费 | Java / Go | 8085 | PostgreSQL |
| `notification-service` | 消息推送（邮件、短信、钉钉） | Go | 8086 | Redis, SMTP |
| `file-service` | 文件上传下载（OTA、图片） | Go | 8087 | MinIO |

---

## 🗃️ 数据库设计

### 主数据库（PostgreSQL 15）
- **用途**：设备元数据、用户、订单、配置
- **架构**：主从复制（1 主 2 从），读写分离
- **备份**：每日全量 + WAL 增量，保留 7 天
- **云服务**：阿里云 RDS / AWS RDS

### 时序数据库（TimescaleDB）
- **用途**：机器人位置轨迹、传感器数据
- **保留策略**：原始数据 30 天，降采样 1 年
- **压缩**：启用 TimescaleDB 压缩

### 缓存（Redis 7）
- **用途**：会话、实时状态、任务队列
- **架构**：哨兵模式（3 节点）
- **持久化**：AOF + RDB

### 对象存储（MinIO）
- **用途**：OTA 固件包、日志文件、用户上传
- **架构**：分布式（4 节点），纠删码
- **S3 兼容**：便于迁移至云存储

---

## 🔌 API 设计规范

### 通用原则
- **RESTful**：资源导向，使用 HTTP 动词
- **版本控制**：URL 路径 `/api/v1/` 或 Header `Accept: application/vnd.api.v1+json`
- **响应格式**：JSON，错误码 `{"code": 2000, "message": "OK", "data": {...}}`
- **认证**：JWT Token，`Authorization: Bearer <token>`
- **限流**：令牌桶算法，Redis 计数

### 示例：设备管理

```http
GET    /api/v1/devices                # 列表（分页）
POST   /api/v1/devices                # 注册新设备
GET    /api/v1/devices/:id            # 详情
PUT    /api/v1/devices/:id            # 更新配置
DELETE /api/v1/devices/:id            # 注销
GET    /api/v1/devices/:id/telemetry  # 查询遥测
POST   /api/v1/devices/:id/commands   # 发送指令
```

### WebSocket 实时流

```javascript
// 连接
const ws = new WebSocket('wss://api.findingtech.com/ws?token=xxx')

// 订阅机器人状态
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'device.telemetry',
  filters: {device_ids: ['robot-001']}
}))

// 接收消息
ws.onmessage = (event) => {
  const msg = JSON.parse(event.data)
  console.log(msg.data) // {robot_id, position, battery, ...}
}
```

---

## 📡 消息队列（Kafka）

### Topic 设计

| Topic | 分区 | 保留时间 | 用途 |
|-------|------|----------|------|
| `device.telemetry` | 6 | 7 天 | 机器人上报的传感器数据 |
| `device.command` | 6 | 1 天 | 云端下发的控制指令 |
| `task.assignment` | 3 | 1 天 | 任务分配事件 |
| `scheduler.events` | 3 | 1 天 | 调度引擎内部事件 |
| `audit.log` | 1 | 30 天 | 所有操作审计日志 |

### 消费者组
- `telemetry-processor`：消费设备遥测，写入 TimescaleDB
- `scheduler-engine`：消费任务事件，运行调度算法
- `alert-engine`：消费 telemetry，检测异常，触发告警

---

## 🔐 安全设计

### 认证与授权
- **OAuth 2.0**：用户登录，授权码模式
- **JWT**：访问令牌，有效期 2h，刷新令牌 30 天
- **RBAC**：角色（Admin, Operator, Viewer）
- **设备证书**：每个设备 X.509 证书，mTLS

### 数据加密
- 传输层：TLS 1.3，禁用弱密码套件
- 存储：敏感字段（手机号、位置）应用层加密（AES-256-GCM）
- 密钥管理：HashiCorp Vault / 阿里云 KMS

### 审计
- 所有 API 调用记录（谁、何时、做什么）
- 关键操作二次确认（删除设备、下发急停）
- 日志不可篡改（写入后只读）

---

## 🧪 测试策略

| 测试类型 | 工具 | 覆盖范围 |
|----------|------|----------|
| 单元测试 | pytest, jUnit, go test | 核心函数 |
| 集成测试 | Postman + Newman, Supertest | API 接口 |
| 端到端测试 | Cypress, Playwright | 用户流程 |
| 压力测试 | k6, JMeter | 1000 并发 |
| 安全测试 | OWASP ZAP, sqlmap | 漏洞扫描 |

---

## 🚀 部署架构

### 小规模（< 50 机器人）
- 单体部署（所有服务一个 Docker Compose）
- 数据库：PostgreSQL + Redis 单机
- 成本低，维护简单

### 中规模（50-500 机器人）
- 微服务拆分
- K8s 部署（EKS/ACK）
- 数据库：主从 + 读写分离
- Redis：哨兵模式

### 大规模（500+ 机器人）
- K8s 集群多节点
- 数据库：分库分表（Sharding）
- 消息队列：Kafka 集群（3+ 节点）
- CDN：静态资源、OTA 分发

---

## 📊 监控告警

### 监控栈
- **Prometheus**：指标采集（服务、主机、数据库）
- **Grafana**：可视化仪表盘
- **Alertmanager**：告警路由（企业微信、钉钉、短信）
- **ELK**：日志集中（Filebeat → Logstash → ES → Kibana）

### 关键指标

| 指标 | 阈值 | 告警 |
|------|------|------|
| API 成功率 | < 99.9% | P1 |
| 机器人在线率 | < 95% | P2 |
| 调度延迟 | > 500ms | P2 |
| 数据库连接池使用率 | > 80% | P3 |
| 磁盘使用率 | > 85% | P2 |

---

## 💰 成本预估（月，cloud）

| 服务 | 小规模 | 中规模 | 大规模 |
|------|--------|--------|--------|
| EKS / ACK 集群 | ¥5k | ¥20k | ¥100k |
| RDS PostgreSQL | ¥2k | ¥8k | ¥30k |
| Redis（云服务） | ¥1k | ¥3k | ¥10k |
| CDN / 带宽 | ¥1k | ¥5k | ¥20k |
| 对象存储 | ¥0.5k | ¥2k | ¥8k |
| 监控日志 | ¥0.5k | ¥2k | ¥5k |
| **合计** | **¥10k** | **¥40k** | **¥173k** |

---

**维护**：后端工程团队  
**最后更新**：2025-04-12  
**版本**：v0.1
