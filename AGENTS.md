# Agent 工作规则

本文件适用于整个仓库。先阅读 README.md、CONTRIBUTING.md、registry.json，以及目标 Skill 的 SKILL.md 和 PROVENANCE.md。

## 变更范围

- 用户任务和明确授权决定范围。本仓库约定不额外授予发布、消息发送、删除或跨仓库写入权限。
- 沿用 `skills/<name>/`；不要修改无关 Skill、个人配置或部署资源。
- 不将任务中的临时困难、某个工具的可用性或一次示例细节写成所有任务的永久强制流程。
- 新 Skill 必须有实际场景，并能说明与现有 Skill 的区别。优先复用现有设计治理，而不是再造冲突入口。

## 编写与同步

- SKILL.md 使用有针对性的 name/description；详细资料按需放 references，模板和示例放 assets。
- 新 Skill 版本写在 YAML `metadata.version`；现有顶层 version 继续兼容，编辑时不要无理由迁移所有旧 Skill。
- 同步 SKILL 版本、registry.json、根 README 目录行及子包 README / PROVENANCE 的版本记录。
- 不把账号、工作区路径、密钥、私有部署标识、未公开会话记录放入示例。保留必要的公开来源与许可边界。
- 第三方参考素材必须在来源说明逐项标注，并明确是否排除在包许可证之外；不因用户提供了图片就声称原创或 MIT 授权。

## 验证与交付

- 运行 `python scripts/validate-skills.py` 和 `python -m unittest discover -s tests`。
- 改动可运行示例时执行相关语法/行为检查；本仓库当前 JavaScript 示例用 `node --check skills/soft-surface-ui/assets/example/app.js`。
- 若改动视觉/交互且有可用渲染环境，运行示例检查实际行为。不能渲染时明确限制，不能把静态检查写成视觉通过。
- 修改校验器时添加有意义的正反例；不要通过放宽规则掩盖当前变更错误。
- 查看完整 diff，保持必要文件之外无临时产物。不要强推、重写已有发布标签或覆盖用户的并行修改。
- 用户已授权加入合集时可执行范围明确的新增或修复；遵守实际分支保护。较大架构变化用可审查分支/PR；不把每次文档修改变成额外的口头审批流程。
- 提交完成后验证远端文件/提交及可用 CI 结果，报告实际状态。不创建标签或 Release，除非用户要求发布版本。
