---
name: agent-design-system-builder
description: 帮你把已确认的截图、Figma 设计或现有界面规范，稳定落实为不易跑偏的产品 UI。它会判断设计状态，建立设计契约、设计令牌与视觉 QA 流程，指导 Agent 复用组件、逐屏实现并兼顾响应式与无障碍要求。
version: 0.1.2
---

# Agent 设计系统构建器

## 核心原则

将已批准的设计决策视为**契约**，而不是灵感。把设计探索与实现分开。一旦设计获得批准，实现只能因明确的响应式、无障碍或平台约束而调整；不得悄悄改变产品风格。

## 首先对任务分类

编辑 UI 前，必须且只能选择一种模式：

1. **LOCKED** — 已有获批的截图、图片、Figma frame、原型或明确的视觉规范。保持它不变。
2. **EXISTING** — 代码库已有 token、组件或模式。扩展前先审计并记录现状。
3. **EXPLORE** — 尚无获批方向。提出 2–3 个连贯方向，获得批准后再锁定其中一个。

如果无法确定，优先选择 EXISTING，不要发明一套新的设计语言。

## 必需的项目产物

在进行大范围 UI 实现前，创建或更新：

- `DESIGN.md` — 产品级视觉与交互契约。
- token 的单一事实来源 — 优先沿用现有 token 文件；全新项目可使用兼容 DTCG 的 token 文件。
- `VISUAL_QA.md` — 获批参考、目标视口和验收检查项。
- 项目 Agent 规则（`AGENTS.md`、`CLAUDE.md` 或同类文件），并确保从规则文件可一步链接到 `DESIGN.md`。

使用 `assets/DESIGN-template.md`、`assets/tokens-dtcg-template.json`、`assets/VISUAL-QA-template.md`，以及 `assets/` 中的 Agent 规则片段。

## 强制工作流

1. **先审计证据。** 阅读现有 UI、token 文件、组件库、截图或 Figma 设计以及 Agent 规则。绝不能把推测出来的规则描述成既有事实。
2. **提取契约。** 记录视觉主张、布局与网格、间距、字体、颜色角色、圆角、层级与阴影、动效、图像语言、响应式行为、组件状态、信息密度和无障碍约束。
3. **将决策 token 化。** 优先使用 primitive → semantic → component 的 token 层级。已有适合的 token 时，不得新增硬编码的颜色、间距或字体数值。
4. **先复用，再创建。** 添加新基础组件前，先搜索已有组件和 variant。
5. **一次实现一个界面。** 保持层级、几何关系、密度、字体、素材取景、状态和交互模型。
6. **渲染并对照。** 使用可用的浏览器、渲染或截图工具，在目标视口下与获批参考进行比较；优先修复最大的视觉差异。
7. **执行对抗式 QA。** 检查响应式行为、键盘操作与焦点、对比度、交互状态、加载/空白/错误状态、溢出，以及与相邻界面的一致性。
8. **更新契约。** 如果获批变更确实改变了设计系统，应同步更新 token、组件和 `DESIGN.md`；不要让一次性 CSS 成为隐蔽的视觉偏移。

## LOCKED 模式的硬性规则

- 除非用户明确要求，否则不得重新设计、“改进”、简化、现代化，或替换成另一种审美风格。
- 不得因为另一种实现更容易，就改变文案层级、区块顺序、主要比例、关键颜色、字体特征、圆角或视觉密度。
- 响应式适配必须保留同一套视觉语法，不能变成一套新设计。
- 如果参考存在歧义，应列出歧义，并选择最小且合理的偏差。
- 当渲染能力可用时，不得仅凭代码检查就宣称完成。

## 接下来阅读

- 系统综合：`references/01-source-systems.md`
- 设计契约：`references/02-design-contract.md`
- Token：`references/03-token-architecture.md`
- 组件：`references/04-component-contract.md`
- 图片/Figma → 代码保真：`references/05-visual-fidelity-workflow.md`
- 无障碍与响应式：`references/06-accessibility-responsive.md`
- 审查清单：`references/07-review-checklist.md`
