# Finding Company 智能硬件工程文档

> 业务洞察到技术实现的桥梁

---

## 📐 工程概览

本目录包含Finding公司智能硬件产品线的完整技术架构、设计规范和开发计划。基于业务洞察报告，将市场机会转化为可实施的技术方案。

---

## 🏗️ 系统架构

### 三大产品线技术栈

| 产品 | 核心架构 | 关键技术 | 状态 |
|------|----------|----------|------|
| **CampBot 营地机器人** | 分布式ROS 2 + 边缘计算 | Navigation2, MoveIt2, 5G | 设计中 |
| **SwarmOS 编队系统** | 中心调度 + 边缘代理 | 强化学习, gRPC, 实时通信 | 设计中 |
| **Finding Pro 硬件** | 嵌入式Linux + 端侧AI | STM32, TensorFlow Lite, 卫星通信 | 设计中 |

---

## 📂 目录说明

```
engineering/
├── architecture/          # 系统架构设计
│   ├── overall-architecture.md  # 整体架构概览
│   ├── campbot-architecture.md  # CampBot详细设计
│   ├── swarmos-architecture.md  # SwarmOS编队系统设计
│   └── infrastructure.md        # 基础设施（云、网络）
├── tech-stack/           # 技术栈选型与理由
│   ├── hardware.md       # 硬件组件（传感器、电机、芯片）
│   ├── firmware.md       # 嵌入式固件（RTOS、驱动）
│   ├── backend.md        # 后端服务（云端、边缘）
│   └── frontend.md       # 前端（App、Web控制台）
├── api-specs/            # API接口规范（OpenAPI 3.0）
│   ├── campbot-api.yaml  # CampBot REST + WebSocket API
│   ├── swarmos-api.yaml  # SwarmOS 调度API
│   └── finding-pro-api.yaml  # Finding Pro设备API
├── dev-plan/             # 开发管理与计划
│   ├── sprint-plan.md    # 敏捷冲刺计划（2周迭代）
│   ├── team-structure.md # 研发团队组织（12人核心）
│   └── milestones.md     # 里程碑与交付物
├── deployment/           # 部署与运维
│   ├── docker/          # Docker镜像与Compose
│   ├── k8s/             # Kubernetes部署清单
│   └── ci-cd.md         # 持续集成/交付流程
└── README.md            # 本文件
```

---

## 🚀 快速开始

### 查看架构设计
```bash
# 整体架构
cat architecture/overall-architecture.md

# 具体产品架构
cat architecture/campbot-architecture.md
```

### 查看API规范
```bash
# 生成API文档（需要redoc-cli）
npx redoc-cli bundle api-specs/campbot-api.yaml -o api-docs.html
```

### 本地开发环境
```bash
# 启动后端服务（示例）
cd deployment/docker
docker-compose up -d

# 查看日志
docker-compose logs -f
```

---

## 📊 开发进度

| 模块 | 设计阶段 | 开发阶段 | 测试 | 部署 |
|------|----------|----------|------|------|
| CampBot 固件 | 🟡 50% | ⬜ 0% | ⬜ 0% | ⬜ 0% |
| SwarmOS 调度引擎 | 🟡 60% | ⬜ 0% | ⬜ 0% | ⬜ 0% |
| Finding Pro 云端 | 🟢 80% | 🟡 30% | ⬜ 0% | ⬜ 0% |
| 前端App | 🔴 20% | ⬜ 0% | ⬜ 0% | ⬜ 0% |

---

## 📝 贡献指南

1. 所有设计修改需提交PR，经架构评审通过
2. API变更需同步更新文档和客户端SDK
3. 代码遵循Google风格指南（C++/Python/TypeScript）
4. 提交信息使用Conventional Commits格式

---

## 📧 联系

Finding Company - 智能硬件研发部

© 2026 Finding Company. 保留所有权利。

---

**最后更新**：2025-04-12  
**版本**：v0.1（设计阶段）  
**维护者**：CEO Agent + 研发团队
