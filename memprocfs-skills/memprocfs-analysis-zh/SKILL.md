---
name: memprocfs-assistant-zh
description: 使用 MemProcFS 辅助进行内存分析和取证。当需要分析内存转储、调查系统活动或执行取证检查时使用。
---

# MemProcFS 助手

此 Skill 增强了我使用 **MemProcFS** 进行内存分析和取证的能力。当您请求帮助分析内存转储、进行实时内存分析或法医调查时，我将使用此 Skill 来指导我的行动。

## 核心能力

1.  **初步分类**: 我将首先对内存镜像进行初步分类，以识别关键系统信息、运行中的进程和网络连接。
2.  **引导式分析**: 我将根据您的目标，建议相关的 MemProcFS 模块和命令，引导您完成分析过程。
3.  **取证工作流**: 对于常见的取证任务，我将遵循结构化的工作流程以确保进行彻底的调查。详细步骤请参阅 [forensic-workflows.md](forensic-workflows.md)。
4.  **Python API 集成**: 我可以利用 MemProcFS API 生成 Python 脚本以进行自动化分析。完整指南请参阅 [python-api-guide.md](python-api-guide.md)。

## 附加资源

-   关于 MemProcFS 虚拟文件系统的完整参考，请参阅 [filesystem-reference.md](filesystem-reference.md)。
-   关于实际示例和用例，请参阅 [examples.md](examples.md)。
-   如果遇到任何问题，请查阅 [troubleshooting.md](troubleshooting.md) 指南。

## 开始使用

要开始使用，请向我提供您的内存转储文件路径或指定实时内存获取方法（例如 `pmem`、`fpga`）。例如：

> “分析位于 `/mnt/dumps/suspicious.dmp` 的内存转储”

> “使用 pmem 在此机器上开始实时分析。”
