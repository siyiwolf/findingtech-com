# SwarmOS 多机器人编队协同系统架构

> 快速部署、AI调度、极致灵活的中大规模集群解决方案

---

## 🎯 设计目标

- **快速部署**：标准场景 2 周上线（传统方案 3-6 个月）
- **弹性扩展**：线性支持 10 → 1000 台机器人
- **智能调度**：AI 动态优化路径，吞吐提升 25%，拥堵减少 40%
- **高可用**：99.9% 可用性，单点故障不影响运行
- **国产自主**：不依赖 ROS 商业版，核心算法自研

---

## 🏗️ 系统架构（三层）

```
┌─────────────────────────────────────────────────────────────┐
│                  Management & Operation Layer               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Web UI    │  │  Mobile App │  │   API Gateway│        │
│  │ (Vue3 + TS) │  │ (Flutter)   │  │ (Kong)       │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│                  SwarmOS Cloud (SaaS)                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  SwarmScheduler (AI Engine)                         │   │
│  │  - Multi-agent RL (PPO)                             │   │
│  │  - Real-time optimization                           │   │
│  │  - Deadlock detection & resolution                  │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  State Manager                                       │   │
│  │  - Robot registry                                    │   │
│  │  - Task queue (Redis)                                │   │
│  │  - Map management                                    │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Data Pipeline                                       │   │
│  │  - Kafka (实时流)                                     │   │
│  │  - TimescaleDB (时序)                                │   │
│  │  - Elasticsearch (日志)                              │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                  Edge Layer (SwarmEdge)                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  SwarmAgent (边缘代理)                               │   │
│  │  - 本地调度（断网模式）                               │   │
│  │  - 协议转换 (AMR ↔ SwarmCloud)                      │   │
│  │  - 实时性保障（< 50ms）                              │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                  Robot Layer                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  AMR Vendor A│  │  AMR Vendor B│  │  Custom Bot │        │
│  │  (自有协议)   │  │  (REST API) │  │  (ROS 2)    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│  └─────────────────────────────────────────────────────┘    │
│  通过 SwarmBridge 适配器统一接入                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 核心模块设计

### 1. SwarmScheduler (AI 调度引擎)

**输入**：
- 机器人状态（位置、电量、负载、健康度）
- 任务队列（待搬运货物、目标位置、优先级）
- 地图信息（障碍物、通道、工作站）

**输出**：
- 每个机器人的下一个目标点（Waypoint）
- 路径规划（实时重规划）
- 任务分配（谁去取货、谁去送货）

**算法**：
- **基础层**：基于规则的负载均衡（快速启动）
- **增强层**：深度强化学习（PPO 算法），训练于仿真环境
- **评估指标**：吞吐量、平均等待时间、死亡率（任务失败）

**训练**：
- 仿真环境：Gazebo + custom warehouse scenarios
- 状态空间：机器人位置、任务队列长度、拥堵指数
- 奖励函数：+1 完成任务，-0.1 碰撞，-0.5 死锁

### 2. SwarmAgent (边缘代理)

**部署位置**：每个仓库现场的一台工控机

**功能**：
- 与 SwarmCloud 保持长连接（WebSocket）
- 云端指令 → 机器人原生协议转换
- 断网自治：基于本地规则维持基本运行
- 实时监控：机器人状态采集、告警触发

**性能要求**：
- 指令延迟 < 50ms（网络正常）
- 离线缓冲：可存储 1 小时任务数据
- 恢复机制：网络恢复后自动同步状态

### 3. SwarmBridge (设备桥接)

**目标**：适配不同厂商 AMR，统一接口

**实现**：
- 为每个 AMR 品牌实现 Bridge Driver
- Driver 实现统一接口：`navigate(waypoint)`, `pickup(item)`, `dropoff(location)`
- 配置驱动：YAML 文件定义协议映射（Modbus TCP, HTTP, MQTT, ROS2）

**支持列表**：
- 斯坦德（AutoSeagl） - OTA API
- 极智嘉（Geek+） - HTTP REST
- 快仓（Quicktron） - 私有 TCP
- 海康机器人 - 定制 SDK

---

## 📡 通信设计

### 机器人 ↔ SwarmAgent
- **协议**：原始厂商协议（HTTP, MQTT, ROS2, Modbus）
- **频率**：状态上报 1 Hz，事件实时

### SwarmAgent ↔ SwarmCloud
- **协议**：gRPC over TLS
- **消息**：
  - 机器人状态（Protobuf）
  - 任务指令（bidirectional streaming）
  - 心跳（30s）
- **容错**：自动重连，断线缓存

### SwarmCloud ↔ Web UI
- **协议**：GraphQL（灵活查询） + WebSocket（实时推送）
- **数据**：实时位置地图、任务进度、告警

---

## 🗃️ 数据模型

### Robot（机器人）
```yaml
id: "robot-001"
type: "amr"
vendor: "quicktron"
status: "idle" | "busy" | "charging" | "offline"
battery: 85.3  # %
position: {x: 1.2, y: 3.4, theta: 0.0}
load: {item_id: "sku-123", quantity: 2} | null
health: {motors: "ok", sensors: "warning", battery: "ok"}
last_seen: "2025-04-12T10:30:00Z"
```

### Task（任务）
```yaml
id: "task-456"
type: "pick_deliver"
source: "station-A"
target: "station-B"
priority: 1  # 1-5
assigned_to: ["robot-001"]  # 可能多个机器人协作
status: "pending" | "assigned" | "running" | "completed" | "failed"
created_at: "2025-04-12T10:25:00Z"
expected_completion: "2025-04-12T10:35:00Z"
```

### Mission（任务组）
```yaml
id: "mission-789"
tasks: ["task-456", "task-457", "task-458"]
assigned_robots: ["robot-001", "robot-002", "robot-003"]
overall_status: "in_progress"
start_time: "2025-04-12T10:20:00Z"
```

---

## 🔐 安全设计

- **设备认证**：基于证书（mTLS），每个 SwarmAgent 唯一
- **API鉴权**：OAuth 2.0 + JWT，RBAC 角色控制
- **数据加密**：传输层 TLS 1.3，存储加密（AES-256）
- **审计日志**：所有关键操作记录，不可删除
- **网络隔离**：SwarmEdge 部署在 DMZ，限制外网访问

---

## 🧪 测试方案

| 测试项 | 方法 | 工具 |
|--------|------|------|
| 单元测试 | 各模块功能验证 | pytest, jest |
| 集成测试 | 端到端流程 | 仿真环境（自定义） |
| 性能测试 | 100, 500, 1000 台规模 | Kubernetes 压力测试 |
| 故障注入 | 网络断开、机器人离线 | Chaos Engineering |
| 安全测试 | 渗透测试、漏洞扫描 | OWASP ZAP |

**仿真环境**：
- 仓库地图编辑器（Web）
- 机器人行为模拟（Python 脚本）
- 可视化回放（Vue + Canvas）

---

## 🚀 部署架构

### 小规模（< 50 台）
- SwarmCloud SaaS（云端托管）
- SwarmEdge 软件运行在客户现场 PC

### 中规模（50-500 台）
- SwarmCloud 私有部署（客户私有云）
- SwarmEdge 2 节点集群（高可用）
- 数据库独立部署

### 大规模（500+ 台）
- 多区域 SwarmEdge 部署（每个仓库独立）
- 中心 SwarmCloud 做全局调度（可选）
- 混合云架构（敏感数据本地，分析上云）

---

## 📈 监控与运维

- **监控**：Prometheus + Grafana（指标、日志、链路追踪）
- **告警**：机器人离线、任务堆积、SLA 不达标 → 企业微信/钉钉
- **日志**：ELK 集中收集，7 天保留
- **备份**：每日数据库快照，异地备份

---

## 📚 文档链接

- [API 规范](../api-specs/swarmos-api.yaml)
- [技术栈选型](../tech-stack/backend.md)
- [部署指南](../deployment/ci-cd.md)

---

**维护**：SwarmOS 研发团队  
**最后更新**：2025-04-12  
**版本**：v0.1（架构设计草案）
