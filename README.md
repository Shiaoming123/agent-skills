# Agent Skills

[![Validate Skills](https://github.com/Shiaoming123/agent-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Shiaoming123/agent-skills/actions/workflows/validate.yml)

将实际项目中验证过的方法，整理为 Agent 可以按需加载、复用和持续改进的工作技能。

由 **Shiaoming123** 维护的原创 Skill 合集，当前涵盖设计治理、界面风格与动效、内容发布前审查。每个 Skill 独立组织、独立版本管理，并记录来源、许可和适用边界。

## Skill 目录

| Skill | 版本 | 适合解决什么问题 | 许可 |
| --- | --- | --- | --- |
| [agent-design-system-builder](skills/agent-design-system-builder/) | `0.1.2` | 从已确认的参考建立 Design Contract、设计令牌、组件规则和视觉验收流程，减少 Agent 实现时的设计漂移。 | MIT |
| [social-content-preflight](skills/social-content-preflight/) | `0.1.2` | 依据明确的平台规则与账号约束，审查待发布内容，输出风险、修改建议与发布前检查结果。 | MIT |
| [soft-surface-ui](skills/soft-surface-ui/) | `0.1.0` | 复用纯白留白、轻边框、柔和阴影的卡片风格，实现外壳连续变形与内容分层过渡；附完整交互示例。 | MIT（代码与文档）；参考图片除外 |

机器可读目录见 [`registry.json`](registry.json)。第三方 Skill 的镜像或搬运不属于本仓库的收录范围。

## 快速开始

### 1. 获取仓库

```bash
git clone https://github.com/Shiaoming123/agent-skills.git
cd agent-skills
```

### 2. 安装所需 Skill

以 Codex、macOS / Linux 默认目录为例，将完整的 Skill 文件夹复制到 `~/.codex/skills/`：

```bash
mkdir -p ~/.codex/skills
cp -R skills/soft-surface-ui ~/.codex/skills/
```

如果设置了 `CODEX_HOME`，使用其 `skills/` 子目录。同名目录已存在时，先比较本地修改与版本再更新。其他支持 Skill 的 Agent，请按该工具的说明选择技能目录，保留 `SKILL.md`、references 和 assets 的相对结构。

不需要安装全部 Skill，也无需把整个仓库复制进技能目录。此操作只安装技能文件，不会执行示例、配置外部服务或发布项目。

### 3. 在任务中调用

```text
使用 $soft-surface-ui，为当前界面应用纯白轻盈卡片风格。
保留现有功能与布局，记录视觉参数，实现自然的内容切换，并验证窄屏和快速连点。
```

```text
使用 $agent-design-system-builder，将这份已确认的设计整理成开发契约，
建立可复用的 tokens、组件规则和视觉验收清单。
```

每个 Skill 的适用场景、操作路径和资源入口都在各自的 `SKILL.md` 中。宿主是否支持自动发现、何时刷新 Skill 列表，以该工具的实际行为为准。

## 交互示例：Soft Surface UI

本次组件复刻已随 Skill 一起提供，包含画廊、八种研究态、自动播放、慢速与同步网格观察器；另有便签编辑、消息筛选和活动图表选中。

```bash
python -m http.server 8080 --bind 127.0.0.1 \
  --directory skills/soft-surface-ui/assets/example
```

在浏览器打开 `http://127.0.0.1:8080`。无需构建或下载依赖；也可直接打开示例 HTML。

- [示例运行与交互说明](skills/soft-surface-ui/references/example-guide.md)
- [视觉参数与组件解剖](skills/soft-surface-ui/references/visual-system.md)
- [分层动效实现配方](skills/soft-surface-ui/references/motion-system.md)

示例来自对外部视觉参考的独立实现。图片是参考截图裁片，跑步与草地动效使用近似处理；它们的权利与验证范围见 [来源说明](skills/soft-surface-ui/PROVENANCE.md)。

## 仓库结构

```text
agent-skills/
├── README.md                    # 使用入口与 Skill 目录
├── registry.json                # 名称、路径、版本、许可与状态
├── AGENTS.md                    # Agent 在仓库中的工作约定
├── CONTRIBUTING.md              # 收录、维护、版本与发布规则
├── scripts/validate-skills.py    # 仓库结构与元数据校验
├── tests/                       # 校验器行为测试
└── skills/
    └── <skill-name>/
        ├── SKILL.md             # 技能入口
        ├── README.md            # 面向使用者的说明
        ├── LICENSE.md           # 许可与例外范围
        ├── PROVENANCE.md        # 来源与已执行验证
        ├── AUTHORS.md           # 作者与贡献角色
        ├── agents/             # 可选：宿主 UI 元数据
        ├── references/         # 可选：按需阅读的详细方法
        └── assets/             # 可选：模板、示例与素材
```

## 质量与维护

修改后，在仓库根目录运行：

```bash
python scripts/validate-skills.py
python -m unittest discover -s tests
node --check skills/soft-surface-ui/assets/example/app.js
```

CI 执行相同检查。结构与语法检查不等于浏览器视觉验收、业务正确性或内容合规保证；Skill 应说明实际做过的验证与尚未确认的部分。

- **独立版本**：每个 Skill 单独维护版本；发布标签使用 `<skill-name>-v<version>`。
- **逐层加载**：入口保持简洁，详细方法放 references，可运行材料放 assets。
- **证据可追溯**：原创内容、参考资料和第三方素材分开说明，不扩张许可范围。
- **改动可审查**：保持变更聚焦；更新 Skill 时同步版本、索引、说明与必要验证。

完整约定见 [维护与贡献指南](CONTRIBUTING.md)，Agent 执行要求见 [AGENTS.md](AGENTS.md)。

## 反馈与贡献

通过 [Issues](https://github.com/Shiaoming123/agent-skills/issues) 提交使用反馈，附 Skill 名称、版本、任务输入、预期与实际结果，以及可公开的最小示例。请移除密钥、账号信息和私人业务数据。

贡献前阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。优先提交基于真实任务的小范围改进；新增 Skill 应说明它与现有技能的区别，以及为何值得独立维护。

## 许可

各 Skill 的 `LICENSE.md` 和 `PROVENANCE.md` 共同说明许可与来源。根目录 [MIT License](LICENSE.md) 不替代子包的许可例外，也不授予第三方图片、品牌或参考作品的使用权。
