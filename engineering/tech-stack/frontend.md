# 前端技术栈

---

## 🎯 设计原则

- **跨平台**：支持 Web、iOS、Android
- **实时性**：WebSocket 推送，秒级更新
- **易用性**：简洁 UI，降低学习成本
- **响应式**：适配桌面、平板、手机
- **离线能力**：App 支持离线查看设备状态

---

## 📱 三端产品

| 产品 | 框架 | 目标用户 | 核心功能 |
|------|------|----------|----------|
| **CampBot App** | Flutter | 露营用户 | 一键启动、任务监控、手动遥控 |
| **SwarmOS UI** | Vue3 + TypeScript | 仓库管理员 | 实时地图、任务编排、报表分析 |
| **Finding Pro App** | Flutter | 户外探险者 | 卫星消息、位置共享、SOS 告警 |

---

## 🛠️ 技术选型

### Web 端（SwarmOS UI）

| 层级 | 技术 | 理由 |
|------|------|------|
| 框架 | Vue 3 + Composition API | 生态丰富，开发效率高 |
| 语言 | TypeScript | 类型安全，减少运行时错误 |
| UI 组件库 | Element Plus / AntDesign Vue | 企业级，组件齐全 |
| 状态管理 | Pinia | Vuex 下一代，轻量易用 |
| 路由 | Vue Router 4 | 官方，SPA 路由 |
| HTTP 客户端 | Axios | 拦截器、取消请求 |
| 实时通信 | Socket.IO Client | WebSocket 封装，自动重连 |
| 地图 | Deck.gl + Mapbox GL | 大规模点渲染（1000+ 机器人） |
| 图表 | ECharts / Apache Superset（嵌入） | 数据可视化 |
| 构建工具 | Vite | 快速 HMR，生产优化 |
| 测试 | Vitest + Cypress | 单元 + E2E |

### 移动端（Flutter）

| 组件 | 选型 | 说明 |
|------|------|------|
| 框架 | Flutter 3.x | 跨平台，原生性能 |
| 语言 | Dart | 类型安全，AOT 编译 |
| 状态管理 | Riverpod | Provider 升级版，更安全 |
| 路由 | go_router | 声明式，支持 Deep Linking |
| 网络 | Dio | 功能强大（拦截器、缓存） |
| 本地存储 | Hive / SQLite | 轻量，NoSQL / 关系 |
| 地图 | flutter_map（Leaflet） | 轻量，离线支持 |
| 蓝牙 | flutter_blue_plus | 设备直连 |
| 推送 | firebase_messaging | 跨平台推送（Android/iOS） |
| 图表 | fl_chart | Flutter 原生图表 |

### 混合方案（可选）

- **React Native**：如果团队更熟悉 React 生态
- **Capacitor**：Web 应用打包为原生壳，快速上线

---

## 🗺️ Web 端架构（SwarmOS UI）

```
src/
├── api/                    # API 客户端（Axios 封装）
│   ├── device.ts
│   ├── task.ts
│   └── auth.ts
├── stores/                 # Pinia 状态管理
│   ├── device.store.ts
│   ├── user.store.ts
│   └── ui.store.ts
├── components/             # 通用组件
│   ├── RobotCard.vue
│   ├── TaskList.vue
│   ├── MapView.vue
│   └── DashboardChart.vue
├── views/                  # 页面级组件
│   ├── Dashboard.vue      # 仪表盘
│   ├── RobotManagement.vue # 设备管理
│   ├── TaskOrchestration.vue # 任务编排
│   ├── RealTimeMap.vue    # 实时地图
│   ├── Analytics.vue      # 数据分析
│   └── Settings.vue       # 系统设置
├── router/                 # 路由配置
│   └── index.ts
├── composables/            # 组合式函数
│   ├── useWebSocket.ts
│   ├── usePermission.ts
│   └── useTheme.ts
├── utils/                 # 工具函数
│   ├── format.ts
│   └── validation.ts
├── assets/                # 静态资源
│   ├── images/
│   └── styles/
└── main.ts                # 入口
```

---

## 🎨 UI/UX 设计

### 设计系统
- **色彩**：Finding 品牌蓝 `#0057B8` 为主色，辅以天蓝 `#4A90E2`
- **字体**：Inter（英文）、Noto Sans SC（中文）
- **间距**：8px 基准单位，4/8/16/24/32 倍数
- **圆角**：4px（小）、8px（中）、16px（大）
- **阴影**：柔和阴影，层级区分

### 关键页面设计

#### 1. 仪表盘
- 核心指标卡片（设备总数、在线率、任务完成率）
- 实时地图（机器人位置、路径）
- 告警列表（最新 5 条）
- 吞吐量趋势图（24h）

#### 2. 设备管理
- 设备列表（表格，支持搜索、筛选）
- 设备详情（状态、遥测图表、控制按钮）
- 批量操作（重启、OTA 升级）

#### 3. 任务编排
- 任务创建（选择机器人、设置目标）
- 任务队列（拖拽调整优先级）
- 实时看板（任务进度、耗时）

#### 4. 数据分析
- 报表生成（日报、周报、月报）
- 自定义查询（时间范围、设备筛选）
- 导出 CSV/Excel

---

## 🔄 实时数据流

### WebSocket 连接
```javascript
// 连接管理
const socket = io('https://api.findingtech.com', {
  auth: { token: jwt }
})

// 订阅机器人状态
socket.emit('subscribe', {
  channel: 'device.telemetry',
  filter: {device_type: 'amr'}
})

// 接收消息
socket.on('telemetry', (data) => {
  // data: {device_id, position, battery, timestamp}
  updateRobotState(data.device_id, data)
})
```

### 地图实时更新
- 使用 Deck.gl `ScatterplotLayer` 渲染机器人位置
- 每秒更新（WebSocket 推送）
- 轨迹线：`PathLayer` 显示最近 100 个点
- 颜色编码：正常（蓝）、警告（黄）、离线（灰）

---

## 🔐 安全

- **XSS 防护**：Vue 自动转义，DOMPurify 处理富文本
- **CSRF 防护**：SameSite Cookie + CSRF Token
- **CSP**：Content Security Policy，限制外部资源
- **敏感数据**：不存储在 localStorage，使用内存

---

## 🧪 测试策略

| 测试类型 | 工具 | 覆盖率 |
|----------|------|--------|
| 单元测试 | Vitest | > 80% |
| 组件测试 | Vue Test Utils | 关键组件 |
| E2E 测试 | Cypress | 核心流程 |
| 视觉回归 | Percy / Chromatic | UI 一致性 |
| 性能测试 | Lighthouse | SEO / 性能评分 > 90 |

---

## 🚀 构建与部署

### 开发环境
```bash
# 克隆项目
git clone https://github.com/siyiwolf/findingtech-ui.git
cd findingtech-ui

# 安装依赖
pnpm install  # 推荐 pnpm

# 启动开发服务器
pnpm dev  # http://localhost:3000
```

### 生产构建
```bash
# 构建
pnpm build

# 输出到 dist/ 目录，直接部署到 Nginx / CDN
```

### CI/CD
- **GitHub Actions**：代码检查、测试、构建
- **分阶段部署**：Dev → Staging → Production
- **回滚**：保留最近 5 个版本，一键切换

---

## 📱 移动端（Flutter）

### 项目结构
```
lib/
├── main.dart
├── config/          # 配置（API 地址）
├── data/            # 数据层（Repository + API）
├── models/          # 数据模型
├── stores/          # Riverpod Provider
├── pages/           # 页面
│   ├── home_page.dart
│   ├── device_list_page.dart
│   ├── map_page.dart
│   └── settings_page.dart
├── widgets/         # 通用组件
└── utils/           # 工具
```

### 核心功能
- **蓝牙连接**：直接连接 Finding Pro / SwarmBot
- **卫星消息**：发送/接收北斗短报文
- **位置共享**：查看团队成员位置
- **SOS**：一键发送紧急告警（卫星 + App 推送）

---

## 📊 性能目标

| 指标 | 目标 |
|------|------|
| 首屏加载时间 | < 2s（4G 网络） |
| 地图渲染 | 1000 机器人 < 100ms |
| API 平均响应 | < 200ms |
| WebSocket 延迟 | < 100ms |
| App 安装包大小 | < 50MB（Flutter） |

---

## 💰 人力估算（前端）

| 角色 | 人数 | 职责 |
|------|------|------|
| Web 前端工程师 | 2 | SwarmOS UI 开发 |
| 移动端工程师 | 2 | Flutter App 开发（CampBot + Finding Pro） |
| UI/UX 设计师 | 1 | 界面设计、交互原型 |
| 前端架构师 | 1 | 技术选型、基建、性能优化 |

**总计**：6 人

---

**维护**：前端工程团队  
**最后更新**：2025-04-12  
**版本**：v0.1
