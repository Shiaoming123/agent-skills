# Soft Surface UI

纯白轻量卡片与连续表面变形的可复用 Skill。将已经确认的参考转成明确的视觉参数、分层动效和可操作实现，而不是让 Agent 自由猜测风格。

- 版本：`0.1.0`
- 入口：[SKILL.md](SKILL.md)
- 许可：原创代码与文档为 MIT；示例裁图除外，见 [来源说明](PROVENANCE.md)

## 调用

```text
使用 $soft-surface-ui，保留当前产品的信息架构，应用纯白轻盈卡片风格。
先记录视觉约束，再实现卡片高度、底色和内容分层过渡，并检查快速切换与窄屏表现。
```

也可以明确说“运行这个 Skill 自带的例子”，或提供截图要求严格复刻。

## 包含内容

| 资源 | 用途 |
| --- | --- |
| [视觉系统](references/visual-system.md) | 色彩、间距、字体、圆角、阴影、组件解剖 |
| [动效配方](references/motion-system.md) | 分层时序、测量、打断、焦点与性能 |
| [项目接入](references/integration.md) | 现有治理、Figma、框架与真实业务适配 |
| [验收检查](references/verification.md) | 静态保真、快速切换、无障碍、验证范围 |
| [案例复盘](references/case-study.md) | 本次参考、实施选择和近似边界 |
| [运行指南](references/example-guide.md) | 本次完整示例及控制方式 |
| [样式变量](assets/primitives/tokens.css) | 独立可用的 CSS token 起点 |
| [示例入口](assets/example/index.html) | 无构建依赖的静态 HTML/CSS/JS 示例 |

## 运行示例

在本 Skill 目录执行：

```bash
python -m http.server 8080 --bind 127.0.0.1 --directory assets/example
```

访问 `http://127.0.0.1:8080`。也可直接打开示例 HTML。画廊还原七个组件，Morph 模式支持八状态切换、自动播放、慢速与同步网格。

这是独立实现的研究示例，跑步/草地使用图片动效近似；并非原作者源码或全部视频功能。详细边界见 [运行指南](references/example-guide.md)。
