# 运行时准备

技能版本 0.1.0 使用 RSI runtime 1.0.2-local.1。公开仓库仅包含原创接入流程和离线导入器，未提供 runtime 下载地址或公开分发授权。使用者须自行持有有权本地使用的归档；没有归档时报告缺少前置条件，不能伪装为已配置。

本机安装后的布局：

```text
rsi-harness/
  SKILL.md
  scripts/import_runtime.py
  runtime-source.json
  assets/runtime/              # 本地导入，已从 Git 排除
    IMPORT.json
    scaffold/
      rsi
      templates/
      SAFETY.md
      RUNS.md
      tests/
      examples/demo/
```

先选定一个已安装且可运行的 Python 3.9+（当前实际验证为 Windows Python 3.13）。命令中的 <SKILL_ROOT> 是当前 SKILL.md 父目录，<ARCHIVE> 是使用者指定的归档文件；不是固定开发机路径：

```text
python -X utf8 <SKILL_ROOT>/scripts/import_runtime.py --archive <ARCHIVE> --dry-run
python -X utf8 <SKILL_ROOT>/scripts/import_runtime.py --archive <ARCHIVE>
python -X utf8 <SKILL_ROOT>/assets/runtime/scaffold/rsi --version
```

执行前核对 runtime-source.json 的归档与 CLI SHA256。导入器只在本地读取归档、验证固定指纹并导入 scaffold，不下载、不运行包内程序，也不修改项目。dry-run 零写入；同内容重复导入保留，已有不同或不完整目录拒绝覆盖。不提供 force 或自动更新；新版本需审查来源、指纹及 Diff 后另行升级。导入阶段要求单写入者，不承诺与其他程序并发改文件时的事务隔离。

首次导入成功后，后续会话直接使用技能自身 assets/runtime 内的工具，不再依赖原归档路径。GitHub 下载安装技能不会自动拥有 runtime；换电脑需重新导入。

固定同一 Python 运行 run 和 check。hook/CI 若后来经授权接入，用进程级 RSI_PYTHON 指向同一绝对解释器路径；不用改全局环境变量。本版拒绝项目内部的 executable（包括项目 .venv）；不能冒用另一项目的可变虚拟环境。
