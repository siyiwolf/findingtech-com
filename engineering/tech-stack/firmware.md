# 嵌入式固件技术栈

---

## 🎯 设计原则

- **实时性**：关键控制回路（电机、避障）周期 ≤ 10ms
- **可靠性**：看门狗、内存保护、故障自恢复
- **可维护性**：模块化、日志、远程调试
- **安全性**：安全启动、代码签名、防篡改

---

## 🔧 操作系统选型

| 产品 | 操作系统 | 理由 |
|------|----------|------|
| Finding Pro | FreeRTOS | 轻量、成熟、社区活跃 |
| CampBot 机器人 | ROS 2 (Humble) | 机器人生态复杂，需要中间件 |
| SwarmBot (AMR) | Ubuntu 20.04 + ROS 2 | 计算密集，需完整 Linux |
| SwarmEdge (边缘) | Ubuntu 22.04 | 服务器应用 |

---

## 📦 核心软件组件

### ROS 2 (Robot Operating System 2)

**版本**：Humble Hawksbill (Ubuntu 22.04 LTS)

**关键包**：
- **Navigation2**：自主导航（AMCL、DWB控制器、行为树）
- **MoveIt2**：机械臂运动规划（AssemblyBot、CookBot）
- **rviz2 / Foxglove**：可视化调试
- **ros2_control**：硬件抽象、控制器管理
- **slam_toolbox**：同步建图与定位

**定制开发**：
- `campbot_coordination`：多机协同调度
- `swarm_bridge`：厂商协议转换
- `teleop_ui`：手动遥控界面

### FreeRTOS (Finding Pro)

- **任务调度**：优先级抢占式
- **通信**：Queue、Semaphore、Event Group
- **外设驱动**：GPS、显示屏、按键、卫星模组
- **网络**：lwIP + mbedTLS（TLS 1.3）
- **更新**：A/B 分区、滚动升级

---

## 🧩 固件架构（CampBot 示例）

```
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Mission Mgr │  │ Behavior Tree│  │ Safety Watch│        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│                ROS 2 Middleware (RMW)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Publisher    │  │ Subscriber   │  │ Service/Client│       │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│                Hardware Abstraction Layer                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Motor Driver │  │ Sensor Driver│  │ GPIO Control│        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│                OS / BSP                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Linux Kernel (Ubuntu) / FreeRTOS                  │   │
│  │  Device Tree / HAL                                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧠 核心算法

### 1. 导航与避障（Nav2 Stack）

**组件**：
- **定位**：AMCL（自适应蒙特卡洛定位） + 激光雷达/视觉里程计
- **路径规划**：NavFn（全局）+ DWB（局部动态窗口）
- **代价地图**：占用栅格、层（障碍物、速度、 inflation）
- **行为树**：导航行为编排（Navigate → Recover → Spin）

**参数调优**：
- 最大速度 < 1.5 m/s（安全）
- 加速/减速度限制 < 0.5 m/s²
- 障碍物停止距离 < 0.3m

### 2. 机械臂运动规划（MoveIt2）

- **运动学**：KDL IK 快速逆解
- **路径规划**：RRT* Connect
- **轨迹生成**：时间最优参数化（TOT）
- **碰撞检测**：FCL 库

### 3. 多机协同调度（自研）

**算法**：拍卖算法（Auction-based）+ 预留占位（Reservation Table）
- 每个机器人投标任务（基于距离、电量）
- 中央协调器分配，确保无冲突
- 死锁检测与解除（等待图分析）

---

## 📡 通信协议栈

| 层级 | 协议 | 用途 |
|------|------|------|
| 应用层 | ROS 2 Topics/Actions/Services | 机器人内部通信 |
| 传输层 | DDS (RTPS over UDP) | ROS 2 默认传输 |
| 网络层 | IPv4/IPv6 | - |
| 边缘层 | MQTT 5.0 | SwarmEdge ↔ SwarmCloud |
| 云端 | gRPC | SwarmCloud 内部服务 |

---

## 🔐 安全机制

- **固件签名**：ED25519，启动时验证
- **安全启动**：U-Boot + TrustZone (if available)
- **加密存储**：敏感数据（证书、密钥）存入 TPM/SE05X
- **OTA 安全**：差分更新 + 签名校验 + 回滚保护

---

## 🧪 测试策略

| 测试类型 | 工具 | 覆盖率目标 |
|----------|------|------------|
| 单元测试 | gtest, rostest | > 80% |
| 集成测试 | Gazebo 仿真 + rqt_test | 全流程 |
| 性能测试 | `ros2 topic hz`, `perf` | 实时性达标 |
| 压力测试 | 长期运行（72h） | 内存泄漏 < 1MB/h |
| 硬件在环 | 实际机器人 + 仿真混合 | 场景覆盖 |

**仿真环境**：
- 使用 Gazebo Classic / Ignition
- 构建仓库/营地场景模型（SDF/URDF）
- 模拟传感器噪声、故障注入

---

## 🛠️ 开发环境

### 本地开发（Linux）
```bash
# 安装 ROS 2 Humble
sudo apt install ros-humble-desktop

# 创建工作空间
mkdir -p ~/campbot_ws/src
cd ~/campbot_ws
colcon build

# 运行仿真
ros2 launch campbot_sim campbot_world.launch.py
```

### 交叉编译（嵌入式）
- 使用 `ament_cmake` 工具链
- 目标平台：aarch64 (Jetson), armhf (STM32)
- 工具链文件：`toolchain-aarch64.cmake`

### IDE
- **VS Code** + ROS Extension（推荐）
- **CLion** + ROS 插件
- **Qt Creator**（Qt GUI）

---

## 📦 依赖管理

- **ROS 2 packages**：apt 安装系统级，colcon 构建工作空间
- **C++ 库**：Conan（第三方库如 OpenCV, PCL）
- **Python 库**：pip + virtualenv
- **固件**：PlatformIO（MCU 开发）

---

## 🔄 持续集成

GitHub Actions 配置（.github/workflows）：

```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install ROS 2
        run: sudo apt install ros-humble-desktop
      - name: Build
        run: |
          source /opt/ros/humble/setup.bash
          colcon build --packages-select campbot_core
      - name: Test
        run: |
          colcon test --packages-select campbot_core
          colcon test-result --verbose
```

---

## 📝 编码规范

- **C++**：Google C++ Style Guide，使用 clang-format
- **Python**：PEP 8 + black + flake8
- **ROS**：遵循 REP-144（代码组织）、REP-2000（消息定义）
- **Commit**：Conventional Commits (`feat:`, `fix:`, `docs:`)

---

## 🚀 部署流程

1. **代码提交** → GitHub PR
2. **CI 构建** → 自动运行单元测试
3. **镜像构建** → Docker 镜像推送到 registry
4. **同步仿真** → 部署到仿真环境进行集成测试
5. **OTA 发布** → 手动触发生产环境升级

---

**维护**：嵌入式软件团队  
**最后更新**：2025-04-12  
**版本**：v0.1
