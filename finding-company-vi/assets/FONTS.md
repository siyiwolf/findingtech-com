# 字体规范 | Typography Guidelines

## 一、中英文字体搭配

### 首选方案（已购买/已授权）

| 用途 | 英文字体 | 中文字体 | 字体文件 |
|------|----------|----------|----------|
| 标题 | Inter Bold | 思源黑体 Bold | `Inter-Bold.ttf` + `SourceHanSansSC-Bold.otf` |
| 正文 | Inter Regular | 思源黑体 Regular | `Inter-Regular.ttf` + `SourceHanSansSC-Regular.otf` |
| 代码 | JetBrains Mono | N/A | `JetBrainsMono-Regular.ttf` |

### 免费替代方案（系统字体）

| 用途 | 英文字体 | 中文字体 | 说明 |
|------|----------|----------|------|
| 标题 | Inter (Google Fonts) | 苹方 (macOS) / 思源黑体 (Windows/Linux) | 优先使用，通过CSS引入 |
| 正文 | Inter (Google Fonts) | 苹方 / Noto Sans SC (Android) | 注意Linux下可能需要手动安装 |
| 代码 | JetBrains Mono | 等宽字体 | 开发环境专用 |

## 二、字体加载建议

### Web/Documents

```html
<!-- Google Fonts 引入 -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">

<!-- 中文字体降级方案 -->
<style>
  body {
    font-family: 'Inter', 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  }
</style>
```

### PDF/Print

- **PPT导出PDF**: 确保系统中已安装对应字体，导出时勾选"嵌入字体"
- **Word转PDF**: Office 2016+ 支持嵌入字体，勾选"将字体嵌入文件"（仅用于查看，不可编辑）

## 三、字号规范

| 场景 | 英文大小 | 中文大小 | 行距 | 用途 |
|------|----------|----------|------|------|
| 封面标题 | 64-72pt | 36-42pt | 1.2 | PPT封面、大标题 |
| 一级标题 | 28-32pt | 22-26pt | 1.4 | PPT章节、文档H1 |
| 二级标题 | 22-24pt | 18-20pt | 1.5 | PPT小节、文档H2 |
| 三级标题 | 18pt | 16pt | 1.5 | 文档H3 |
| 正文 | 14-16pt | 12-14pt | 1.6-1.8 | 文档正文 |
| 说明文字 | 12pt | 10-11pt | 1.6 | 图表注释、页脚 |

## 四、字重使用

| 字重 | 英文 | 中文 | 使用场景 |
|------|------|------|----------|
| Light | 300 | N/A | 极少使用 |
| Regular | 400 | Regular | 正文、引用 |
| Medium | 500 | Medium | 次要标题 |
| SemiBold | 600 | SemiBold | 副标题、卡片标题 |
| **Bold** | **700** | **Bold** | **主标题、强调** |
| ExtraBold | 800 | 800 | 大标题、数据展示 |

## 五、许可说明

- **Inter**: SIL Open Font License (OFL) ✅ 免费商用
- **JetBrains Mono**: SIL Open Font License (OFL) ✅ 免费商用
- **思源黑体 (Source Han Sans)**: SIL Open Font License (OFL) ✅ 免费商用
- **Noto Sans SC**: Apache License 2.0 ✅ 免费商用
- **苹方 (PingFang SC)**: Apple Propritary ⚠️ 仅限Apple生态

## 六、文件名规范

```
fonts/
├── Inter-Bold.ttf
├── Inter-SemiBold.ttf
├── Inter-Regular.ttf
├── SourceHanSansSC-Bold.otf
├── SourceHanSansSC-Regular.otf
├── JetBrainsMono-Bold.ttf
└── JetBrainsMono-Regular.ttf
```

## 七、注意事项

1. **Fallback顺序**: 英文字体在前，中文字体在后
2. **避免系统差异**: Linux用户可能无苹方，建议提供思源黑体作为fallback
3. **PDF嵌入**: 发送给外部的PDF务必确保字体已嵌入
4. **Web应用**: 使用WebFont加载，避免系统差异导致渲染不一致

## 八、下载链接

- Inter: https://fonts.google.com/inter
- JetBrains Mono: https://www.jetbrains.com/lp/mono/
- 思源黑体: https://github.com/adobe-fonts/source-han-sans
- Noto Sans SC: https://fonts.google.com/noto/specimen/Noto+Sans+SC

---

**维护人**: Finding Company Design Team
**最后更新**: 2026-04-11
