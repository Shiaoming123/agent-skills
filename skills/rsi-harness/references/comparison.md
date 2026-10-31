# 单候选受控比较（0.2）

比较器是可选的机制验收工具，不会自动修改、晋级或安装候选。先写清想改善的具体行为、共享任务、评分函数和预算，再执行。每次只有一个 baseline 和一个 candidate。

## 使用

将两份待比较文件放在不相交、互不嵌套的隔离目录，把可信 Python 评分器、共享输入和 policy 放在两者之外。评分器从环境变量 RSI_SUBJECT_ROOT 读取待测根目录；成功时 stdout 仅输出 JSON，如 `{"score":0.75}`。score 必须为 0..1 的有限数值。比较的是评分而非退出码；非零退出、超时、过量输出或无效 JSON 判为实验无效。

policy 示例（替换成实际绝对路径）：

```json
{
  "schema": 1,
  "isolated": true,
  "baseline": "/absolute/experiment/baseline",
  "candidate": "/absolute/experiment/candidate",
  "subject_files": ["scripts/workspace.py", "scripts/import_runtime.py"],
  "grader": "/absolute/experiment/grader.py",
  "inputs": ["/absolute/experiment/cases.json"],
  "trials": 2,
  "timeout_seconds": 20,
  "min_delta": 0.1,
  "deterministic": true
}
```

subject_files 必须列全实际待测代码/规则依赖，允许某版本缺少文件（指纹为 null）；不允许目录、Git 元数据、链接或路径别名。inputs 列全共享数据依赖。评分器不得修改待测文件或共享文件；需要临时项目时，在独立临时目录创建。

```text
python <SKILL_ROOT>/scripts/compare.py <policy.json>
python <SKILL_ROOT>/scripts/compare.py <policy.json> --execute --output <新的报告.json>
```

默认只验证和预览，不启动评分器、不写文件。显式 --execute 才运行；--output 必须在两个待测目录之外，且目标不存在，冲突在评分前拒绝。无效实验返回 2，其他结果返回 0；判断结论必须读取 decision。

冻结 policy、评分器、共享输入、显式待测文件以及本工具、导入辅助器和当前解释器的 SHA256。每次评分后复核指纹，变化则 invalid。同一解释器、评分器、输入和单次时间预算用于双方，轮次交替 AB/BA。每方每轮独立启动评分器，最多 5 轮、每次最多 30 秒；输出只读至每流 1 MiB，报告保留摘要、不保存原始业务输出。

每轮计算 candidate-baseline。所有差值至少达到 min_delta 才 candidate_preferred；全部相反则 baseline_preferred；全部为零 equivalent；其余 inconclusive。deterministic:false 的随机实验一律 inconclusive，保留观察值，不能据此晋级。此工具没有统计显著性检验。

## 边界

isolated:true 是调用方对副本的声明，不是操作系统沙箱。评分器被视为可信程序，仍能按当前用户权限访问文件、网络和启动后代；本工具只能终止直接评分进程。它不能限制真实模型费用、整个进程树或瞬时磁盘写入，输出限额在轮询中检测，临时文件可能短暂超限。需要这些能力时应另行选择经过验证的宿主隔离方式。

指纹检查能发现检查点间持续存在的修改，不能防同权限恶意程序修改后恢复。根目录之外的未声明依赖、环境变量、系统差异等仍由实验设计者负责。不要把候选自己生成的解释当作外部评判，不要在候选内放评分器，不得降低基线或改评分规则以凑出提升。

本次 0.1→0.2 的合成机制对照用于检查新增控制层是否按契约工作；不证明模型能力、自主研究能力、真实业务收益或严格学术意义的递归自我改进。晋级、全局安装和真实项目接入始终是独立的后续动作。
