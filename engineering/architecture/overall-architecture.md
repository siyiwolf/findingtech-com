# Finding智能硬件整体架构设计

> 统一技术平台，支持多产品线快速部署

---

## 🎯 设计原则

1. **模块化**：核心组件可复用，产品线按需组合
2. **异构兼容**：支持不同硬件平台（ARM Cortex-M, x86, GPU）
3. **端边云协同**：端侧实时响应 + 边缘智能 + 云端分析
4. **国产自主**：核心算法自研，减少外部依赖
5. **安全可靠**：多级冗余，故障自恢复

---

## 🏛️ 整体架构图（分层）

```
┌─────────────────────────────────────────────────────────────┐
│                        Application Layer                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ CampBot App │  │ SwarmOS UI  │  │ Finding Pro │        │
│  │ (Mobile)    │  │ (Web/Desktop)│  │ (Mobile)    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│                    Service Layer (Cloud)                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Device Mgmt │  │ Data Analytics│  │ AI Training │        │
│  │ (SaaS)      │  │ (BigQuery)   │  │ (PyTorch)   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ OTA Update  │  │ Billing      │  │ Notification│        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│                    Edge Layer                                │
│  ┌────────────────────────────────────────────────────┐     │
│  │           SwarmEdge Server (Kubernetes)           │     │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐         │     │
│  │  │Scheduler│  │Monitor  │  │Gateway  │         │     │
│  │  └─────────┘  └─────────┘  └─────────┘         │     │
│  └────────────────────────────────────────────────────┘     │
├─────────────────────────────────────────────────────────────┤
│                    Device Layer                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  CampBot    │  │ Finding Pro │  │  SwarmBot   │        │
│  │  Robot      │  │  Device     │  │  (AMR)      │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│  ┌─────────────┐  ┌─────────────┐                        │
│  │  Sensor     │  │  Actuator   │                        │
│  │  Network    │  │  Power      │                        │
│  └─────────────┘  └─────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 核心组件

### Application Layer
- **CampBot App**：iOS/Android，蓝牙/Wi-Fi直连机器人，场景配置
- **SwarmOS UI**：Web控制台，实时监控、任务编排、数字孪生
- **Finding Pro App**：移动端，卫星通信、位置共享、SOS

### Service Layer (Cloud)
- **Device Management**：设备注册、状态同步、OTA升级（SaaS，多租户）
- **Data Analytics**：大数据分析（用户行为、设备健康、业务指标）
- **AI Training**：模型训练（调度算法、异常检测、预测维护）
- **Billing**：订阅管理、套餐计费（卫星服务、SaaS）
- **Notification**：推送（预警、OTA、营销）

### Edge Layer
- **SwarmEdge Server**：边缘服务器（或云托管），运行SwarmOS核心调度引擎
  - Scheduler：多机协同调度（强化学习）
  - Monitor：实时监控、健康检查、告警
  - Gateway：协议转换（机器人 ↔ 云端）

### Device Layer
- **CampBot Robot**：6种 specialized 机器人（搭建、搬运、巡逻、能源、烹饪、环境）
- **Finding Pro**：手持卫星终端（嵌入式Linux + STM32 + 卫星模组）
- **SwarmBot**：AMR底盘 + 传感器 + SwarmAgent软件
- **Sensor Network**：温湿度、CO、烟雾、GPS、IMU、激光雷达
- **Actuator**：电机、机械臂、加热器、制冷片
- **Power**：锂电池组 + 太阳能管理 + 无线充电

---

## 🔄 数据流

### 典型场景：CampBot搭建帐篷

1. **用户操作**：App选择"搭建3人帐篷A"，点击开始
2. **App → Cloud**：HTTP请求，创建任务
3. **Cloud → SwarmEdge**：任务分配（根据机器人位置、电量）
4. **SwarmEdge → Robots**：通过MQTT/ROS2下发指令（任务队列）
5. **Robots执行**：
   - AssemblyBot：展开帐篷、打地钉
   - CarrierBot：搬运配件
   - ClimateBot：监测温湿度
6. **状态反馈**：机器人周期性发布状态（ROS2 topic → MQTT → Cloud）
7. **App更新**：WebSocket推送进度，用户看到实时状态
8. **任务完成**：所有机器人报告完成 → Cloud记录日志 → App通知用户

---

## 🔐 安全架构

| 层级 | 措施 |
|------|------|
| **设备** | 安全启动（Secure Boot）、TLS 1.3、硬件加密芯片 |
| **通信** | 双向TLS认证、证书轮换、防重放攻击 |
| **云端** | OAuth 2.0 + JWT、RBAC、API限流、WAF |
| **数据** | 端到端加密（卫星消息）、GDPR合规、数据匿名化 |

---

## 🛢️ 数据存储

| 数据类型 | 存储 | 用途 |
|----------|------|------|
| 设备元数据 | PostgreSQL | 设备注册、用户绑定 |
| 时序数据 | TimescaleDB | 传感器数据、位置轨迹 |
| 日志 | Elasticsearch | 操作日志、故障排查 |
| 对象存储 | MinIO / S3 | OTA包、图片、视频 |
| 缓存 | Redis | 会话、实时状态 |

---

## 📡 通信协议

| 场景 | 协议 | 说明 |
|------|------|------|
| 机器人 ↔ SwarmEdge | ROS 2 (DDS) + MQTT over TLS | 低延迟、可靠 |
| SwarmEdge ↔ Cloud | gRPC + HTTP/2 | 高性能RPC |
| App ↔ Cloud | HTTP/3 + WebSocket | 移动友好 |
| 卫星通信 | 北斗短报文 + 铱星 | 低带宽、高延迟 |

---

## 🧩 模块复用策略

| 模块 | 复用场景 | 实现方式 |
|------|----------|----------|
| **SwarmAgent** | 所有机器人 | 统一客户端，配置适配不同硬件 |
| **Device SDK** | App与Cloud通信 | 统一REST/WebSocket封装 |
| **OTA Service** | 所有设备 | 统一差分升级，支持断点续传 |
| **AI Inference** | 端侧AI | TensorFlow Lite模型，跨平台 |
| **Monitoring** | Cloud+Edge | Prometheus + Grafana统一监控 |

---

## 📈 可扩展性

- **水平扩展**：SwarmEdge无状态，Kubernetes自动扩缩容
- **产品线扩展**：新设备只需实现SwarmAgent接口
- **功能扩展**：微服务架构，新增服务不影响现有
- **地域扩展**：多区域SwarmEdge部署，就近接入

---

## 📚 参考文档

- [CampBot 架构详细设计](campbot-architecture.md)
- [SwarmOS 架构详细设计](swarmos-architecture.md)
- [基础设施设计](infrastructure.md)

---

**维护**：架构委员会  
**最后更新**：2025-04-12  
**版本**：v0.1
