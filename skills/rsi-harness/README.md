# RSI 项目工作台

Skill 版本 **0.2.0**；适配本地 RSI runtime **1.0.2-local.1**。

让 Agent 在开发前找到项目规则，执行实际检查，保留绑定当前内容的证据，并在后续任务中复用经过检查的流程。适用于新项目配置、已有项目逐步接入，以及已接入项目的日常工作；不改变项目技术栈。

## 调用

```text
使用 $rsi-harness，为当前项目配置 RSI 工作台。
保留已有规则、脚本、CI 和 hook，先预览具体 Diff，再按已授权范围应用并验证。
```

```text
使用 $rsi-harness，按当前项目的规则继续修复任务。
先确认完成标准，再实际检查，分别报告已完成、待验证和失败项。
```

Codex CLI/IDE 可用 `/skills` 选择技能或输入 `$rsi-harness`。桌面选择器名称为“RSI项目工作台”。技能文件安装不等于项目接入；调用时才处理明确指定的项目，不批量改造其他项目。

## 安装和前置条件

完整技能目录可安装到 Codex 当前用户的 `~/.agents/skills/rsi-harness`；不需要修改全局 AGENTS.md 或 config.toml。同名目录存在时先比较，不覆盖本地工作。其他宿主路径以其文档为准。

**公开仓库不含 RSI runtime。** 原始资料没有提供明确的公开分发许可，因此本包只发布新写的工作流与导入器。使用者需要自行持有有权本地使用的固定版本修订 ZIP；指纹见 runtime-source.json。首次按 [运行时准备](references/runtime-setup.md) 离线导入一次，之后工具保存在技能自己的 assets/runtime 中，不再依赖原 ZIP 路径。只读适配和原创控制工具可直接使用；原门禁、运行证据与经验复用仍须先导入 runtime。

导入器只使用 Python 标准库，不联网，不运行归档内程序。dry-run 不写文件；已有不同内容或不完整 runtime 拒绝覆盖。runtime 更新需要单独审查来源与指纹，不自动升级。

## 资源入口

- [运行时准备](references/runtime-setup.md)：版本、离线导入和工具定位。
- [项目接入](references/onboarding.md)：新项目、冲突处理和旧 harness 迁移。
- [工作闭环](references/workflow.md)：change/verifier、运行证据与 procedure 复用。
- [适配与恢复](references/control.md)：只读发现、能力声明和长任务检查点。
- [受控比较](references/comparison.md)：冻结判据，比较一个候选，保留无效与不确定结论。
- [来源与验证](PROVENANCE.md)、[许可](LICENSE.md)、[贡献角色](AUTHORS.md)。

导入后，完整执行契约位于本地 assets/runtime/scaffold/SAFETY.md 和 RUNS.md。

## 0.2 的变化

新增两个可选标准库脚本：workspace.py 负责发现、profile 和只读恢复；compare.py 负责单候选实验。没有新增服务、依赖包、全局配置、自动循环或 hook 注册。原 runtime 与导入器固定不变。

当前实现用“受控经验改进工作台”描述更准确；RSI 是项目沿用的名称，不声称已实现学术意义的递归自我改进。

## 验证与限制

公开导入器使用合成 ZIP 做哈希、路径、已有内容保留与已校验字节绑定测试；仓库 CI 不下载或分发 RSI runtime。底层 runtime 的 85 项安全/运行回归只能由持有归档的维护者在本地导入后运行，不能把公开 CI 通过写成底层已复测。

自动证据仅 V1；结构检查不替代真实业务、部署或效果验证。validated 只表示任务标签不同的后续流程执行通过，不能证明独立会话或模型学习。runtime 没有可信签名、文件/网络或完整后代进程沙箱。原工具、业务与来源材料的许可均不由本包重新授予。
