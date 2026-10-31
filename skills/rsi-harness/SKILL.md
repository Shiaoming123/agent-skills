---
name: rsi-harness
description: 为当前或指定代码项目配置 RSI 工作台，建立项目规则、验收器、运行证据和经验复用流程。用于用户要求接入、初始化、检查或继续使用 RSI harness；普通问答不触发项目迁移。
metadata:
  version: "0.2.0"
---

# RSI 项目工作台

把用户目标落实为项目规则、可执行检查、当前版本的证据和可复用流程。保持小任务轻量，沿用项目已有技术栈、测试和发布方式。

## 入口与范围

以本文件所在目录为 SKILL_ROOT。原创的可选控制工具是 scripts/workspace.py 和 scripts/compare.py；它们只需 Python 3.10+ 标准库。原项目门禁与证据工具入口为 SKILL_ROOT/assets/runtime/scaffold/rsi。公开技能不包含第三方 RSI runtime；本机首次导入见 [运行时准备](references/runtime-setup.md)。工具缺失时先核对本地归档，不下载替代实现，也不把“安装技能”当作“项目已接入”。

调用“为当前项目配置 RSI”授权接入该项目；先确认实际项目根目录及其指令、工作树、入口、检查、CI、hook 和忽略规则。没有指向具体项目时不得批量扫描接入。仅阅读本技能不授予迁移权限。项目外操作、凭证、费用、发布及破坏性变更继续按当次授权处理。

## 接入或继续工作

1. **识别状态。** 可先用 `python <SKILL_ROOT>/scripts/workspace.py inspect <根>` 只读发现入口；代码、文档、数据与混合项目沿用已有结构，未知事实不猜测。已有 .harness 时读取其配置和任务所需规则；init 的 preserve 不代表升级或验收通过。未接入时按 [项目接入](references/onboarding.md) 生成候选，先 dry-run 并展示实际写入/冲突 Diff；在用户已授权的对应范围内继续应用，范围或语义有歧义时只问影响决定的问题。
2. **配置项目事实。** 从现有来源确认目标、边界和真实检查命令，填必要入口。缺失内容明确待确认，不编造业务规则或把演示数据变成项目事实。保留现有脚本、文档、CI 和 hook，不使用 --force；不自动安装 hook/CI、不改全局配置。
3. **先声明验收。** 为实际任务明确 change 等级及 active verifier 的 command/inputs/checks。先读 runtime 的 SAFETY.md；执行取证或复用前读 RUNS.md。沿用已审查的检查命令，先 run --dry-run 再执行。列全被测文件与检查程序依赖，固定同一 Python 解释器。
4. **取证与复用。** run 自动证据仅 V1；done 要当前绑定有效且达到原要求的 pass。V2–V4 的补充材料字段不证明身份或批准。仅从完整 fail 提炼 procedure，reuse 必须实际执行其 recipe；状态查询见 [工作闭环](references/workflow.md)。
5. **核验接入。** 使用实际安装位置的工具运行 check / doctor 和项目必要检查。存在有效待提交树且需要提交门禁时检查 --staged。题库不足警告、尚待确认目标、未配置业务验收、未安装提交拦截均明确报告；结构全绿不能替代业务完成。

## 可选的长任务与机制迭代

需要跨会话恢复时，按 [适配与恢复](references/control.md) 预览 profile，声明实际宿主能力，追加任务检查点。resume 只读并返回 ready/blocked，不执行下一步；未知外部操作先核对，不能自动重放。能力声明始终 verified:false，owner/revision 不是锁。小任务不强制创建这些状态文件。

改进规则、工具或流程时，先固定具体可观测判据，再按 [受控比较](references/comparison.md) 在隔离副本比较一个候选与当前版本。默认只预览，显式执行才启动可信评分器；无效实验不得解释为改进。无自动晋级、全局安装或真实项目迁移，不将机制验收写成模型学习或严格 RSI。

## 交付

简要说明接入了哪个项目、实际新增/保留/冲突文件、执行的检查、证据位置和未完成项。部署、真实效果、跨会话发现或模型学习没有实测就不宣称完成。

CLI 的 --confirm-write 仅表示写入意图，不替代用户批准。不得自行设置 RSI_SKIP、降低 change 等级、改判据或基线来过闸。runtime 无可信签名或操作系统沙箱；不把记录经验描述为模型训练。原始 runtime 的来源与许可不由本技能重新授予，见 [来源](PROVENANCE.md)。
