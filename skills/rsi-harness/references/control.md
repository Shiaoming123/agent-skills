# 项目适配、能力与长任务恢复（0.2）

这组工具为可选的原创控制层，只需 Python 3.10+ 标准库。不依赖模型 API，不安装服务、hook 或 CI。小任务沿用原流程；需要跨会话恢复或受控机制实验时才启用。

## 先识别，再适配

`python <SKILL_ROOT>/scripts/workspace.py inspect <项目根>` 只读查找常见入口、锁文件、规则和 CI 的路径，不读取业务文件正文、不要求 Git 或 .harness、不写缓存。CI 发现枚举工作流目录的项名称，按名称稳定选取前 20 项，选择时最多保留 20 个指针；不递归、不读文件正文。它不是完整架构识别器。

根据发现的入口读项目原说明，确认真实源文件、生成文件、受保护目录、验收命令和发布入口。代码项目沿用其模块边界；文档项目沿用索引和来源；数据项目沿用 schema 与数据校验；多语言或多包项目把现有根入口指向子项目。未知处保留 unknown，不搬迁目录、不统一技术栈、不运行发现到的脚本。

现有 hook 和 CI 先记录，再审查是否需要接线；工具不会自动注册宿主事件。遇到 PDF、表格、媒体或二进制文件，沿用项目已有读取/导出工具；先辨别原件、可编辑源、导出物和生成物，不把“能读文件”当作“可以重写文件”。不为每种后缀另建框架。

## 能力声明

profile/checkpoint/resume 用于已接入项目，要求 .harness/harness.json 的 schema=1、project_id 为 32 位小写十六进制。

`python <SKILL_ROOT>/scripts/workspace.py profile <项目根>` 默认预览；显式加 `--write` 才创建 .harness/state/control/profile.json。相同内容保留，不同内容拒绝覆盖。迁移已有 profile 需要单独审查；没有自动覆盖参数。

可加 `--declarations <JSON>`，例如：

`{ "capabilities": { "network_boundary": "unavailable", "pause_resume": "advisory" } }`

仅支持 event_hooks、path_isolation、network_boundary、process_termination、pause_resume、cost_metering、immutable_evaluator。状态为 supported/enforced/advisory/unavailable；这些都是调用方声明，始终带 verified:false。即使填写 enforced，也没有经过工具验证，不可据此认为宿主有沙箱、预算硬限制或不可变评分器。

## 记录和恢复

把以下 JSON 存在任务指定位置（不要存敏感信息）：

```json
{
  "goal": "修复导出重复行",
  "scope": "仅导出模块与对应测试",
  "phase": "active",
  "next_step": "阅读失败用例，再检查去重边界",
  "bindings": ["src/export.py", "tests/test_export.py"],
  "steps_used": 2,
  "max_steps": 8,
  "effects": []
}
```

```text
python <SKILL_ROOT>/scripts/workspace.py checkpoint <根> --task export-fix --input <JSON> --owner agent-A --expected-revision 0
python <SKILL_ROOT>/scripts/workspace.py resume <根> --task export-fix
```

第一次 expected-revision 为 0，追加下一版用现有 revision。每版以新文件独占创建，保留历史；owner 和 revision 用于发现冲突，不是身份认证、锁或事务。并发和崩溃后若有冲突/残缺文件，停止并审查，不能删除历史来继续。owner 不能自动转移。

每版绑定项目配置、profile、显式输入文件和 .harness/rules 下直接的 *.md。输入必须为现有、规范的相对路径，不能引用 state、ledger、派生索引或运行回执。补充声明实际依赖；工具不会自动发现全部依赖。它没有可信签名，也不能防同权限程序篡改或改后复原。

resume 只返回 JSON，不运行 next_step、不重放外部操作，也不启动循环。调用方必须看 state=ready/blocked，不能只看退出码：正常返回 blocked 的退出码也是 0。输入/规则/profile/配置变化、未知外部操作、步数用尽、任务已 done 都阻止继续。

例如发文请求超时，无法确认是否已发布，effects 写 `[{"id":"publish-article","status":"unknown","idempotent":false}]`。即使 idempotent:true 仍会阻断；先到外部系统核对，再按事实追加 confirmed 版本。不要盲目再发一次。步数由调用方如实记录，它不是自动计费或进程级预算。

ready 只表示声明绑定和记录允许继续；执行前仍须读取当前任务授权和项目规则。下一步由宿主在原授权内执行，完成一个有意义步骤后再追加检查点。规则变化后重新审查，不能仅重写检查点来绕过变更。
