# 从任务到证据，再到复用

运行前阅读本地 runtime 的 scaffold/RUNS.md；这里仅提供调用路线，不重新定义其 schema。

## 声明和执行

先明确用户要求和完成等级，写必要 problem/change；change 引用 active verifier。verifier frontmatter 的 command、inputs、checks 是单行 JSON 字符串数组，例如：

```yaml
command: ["{python}", "tools/verify.py"]
inputs: ["src/module.py"]
checks: ["tools/verify.py"]
failure_exit: 1
```

inputs 至少一项；检查程序及间接文件依赖要列全。路径使用项目内规范相对路径，拒绝链接、越界和运行记录等自反馈输入。工具不会自动发现漏列依赖。

```text
python -X utf8 <项目工具路径> run --change <ID> --task <TASK> --dry-run
python -X utf8 <项目工具路径> run --change <ID> --task <TASK>
python -X utf8 <项目工具路径> check
```

receipt 及有限 stdout/stderr 位于 .harness/ledger/evidence/runs/；基础 evidence 最后发布并指向 receipt。绑定涵盖所列输入、检查、验收器、规则、rubric、change 契约及实际工具指纹。前后指纹不同为 infra_error；普通检查失败为 fail。timeout/启动/输出错误不能当成已验证缺陷。

自动证据固定 V1。V2 交付生效、V3 真实结果、V4 人工校准需补充现实证据，不能由本机命令通过自动推断。reviewer 文本与文件哈希不核验人员身份或批准。

## 最小经验闭环

从完整 verifier fail 提炼 active procedure，保留 source_run、verifier 及与其一致的 command/inputs/checks。修复后：

```text
python -X utf8 <项目工具路径> reuse <PROCEDURE> --change <ID> --task <TASK> --dry-run
python -X utf8 <项目工具路径> reuse <PROCEDURE> --change <ID> --task <TASK>
python -X utf8 <项目工具路径> reuse <PROCEDURE> --status --json
```

recorded 表示有失败来源与流程；reused 表示实际执行过；validated 需要后续不同 task 标签下的可比较 pass，且当前绑定有效；曾满足条件后绑定/流程过期为 stale。不同 task 是调用方标签，不证明独立会话、因果学习或跨项目泛化。经验没有被后续实际使用，就只报告已记录。

receipt 没有签名；shell=False 不是文件、网络或后代进程沙箱。日志可能包含命令输出的敏感内容，按项目既有规则处理。无后台调度、自动批准、自动降低门槛或模型训练。
