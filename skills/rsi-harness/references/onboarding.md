# 新项目与已有项目接入

SKILL_ROOT 由当前技能路径决定，CLI 为其 assets/runtime/scaffold/rsi。先读同目录 SAFETY.md。明确目标项目根目录；运行命令时工作目录与目标不能混淆。

## 新项目

1. 读取可用说明、现有文件和用户目标，选用项目原有技术栈与验收命令。
2. 从完整 runtime 的 scaffold/rsi 调用 init <目标> --dry-run。展示 create/preserve/conflict 和候选 Diff；确认对应新增已在授权范围内再 init <目标>，不加 --force。已有任何不同内容冲突时，整次拒绝且零写入。
3. init 生成项目独立 project_id、.harness、入口、脚本、模板与 docs。填写有依据的项目目标和必要规则；不能把通用骨架中的空白或样例称为业务已配置。
4. 在项目根目录运行 check、doctor，再执行已确认的项目检查。当前 lite/standard 的题库不足只警告，strict 会阻断；不要为凑数生成无意义题目或擅自降低要求。

示意命令，路径需替换并按所用 shell 正确引用：

```text
python -X utf8 <CLI> init <目标> --dry-run
python -X utf8 <CLI> init <目标>
python -X utf8 <目标>/scripts/rsi check
python -X utf8 <目标>/scripts/rsi doctor
```

## 已有项目

接入授权不包含替换其原有规则、验收语义或发布入口。盘点 AGENTS/CLAUDE/RSI、未提交修改、脚本、CI、hooksPath、忽略规则和实际检查命令。不要提交、stash、reset 或清理用户的其他工作。

标准 init 有冲突时，在独立候选目录生成，再逐文件比较；不使用 force、备份后覆盖或未知 hook 自动串联。按当前授权只添加必要内容：

- 缺少 .harness 时可从候选增加它；工具若与原 scripts/rsi 冲突，放到 .harness/bin/rsi。
- 保留原入口正文，只追加简短真源和工具指针。原 docs/脚本/CI/hook 保持有效；运行协议可另加 .harness/RUNS.md。
- 使用搬迁后的工具路径实际跑 check/doctor。此布局不使用假定 scripts/rsi 的标准 hook/CI 安装器；未来接线需项目原入口显式调用并审查。
- 检查 baseline.json 是否被原 .gitignore 排除；不能未经范围确认改写原忽略策略。

已有 .harness 时，init 仅保留，不升级。缺 project_id 或 verifier 契约时在候选中补充迁移 Diff，沿用稳定项目身份并保留历史账本。旧手填 pass 不能支持新版 done；复验当前内容，未取到足够证据就保留 verifying，不能批量改状态或降等级。

接入结束区分：骨架已装、目标与规则已填、业务验收已配置、实际检查通过、提交拦截已接入。这些是不同结果；不以 check 全绿替代其他项。
