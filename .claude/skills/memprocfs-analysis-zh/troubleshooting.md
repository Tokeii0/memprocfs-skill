# MemProcFS Skill 故障排除

本指南旨在帮助您解决在使用 MemProcFS 助手 Skill 时可能遇到的常见问题。

## 问题：Skill 未触发

如果您在提出相关问题时 Skill 未激活，请尝试以下方法：

1.  **更具体地提问**：使用 Skill 描述中的关键字。不要只说“看看这个内存转储”，而是尝试“分析位于...的内存转储”或“对此镜像展开取证调查”。
2.  **检查 Skill 可用性**：询问“有哪些可用的 Skill？”以确保 `memprocfs-assistant` Skill 已正确加载。
3.  **重启 Claude Code**：如果 Skill 是最近添加的，您可能需要重启应用程序才能加载它。

## 问题：MemProcFS 错误

如果您遇到 MemProcFS 本身报告的错误，请考虑以下常见原因：

1.  **无效的内存转储路径**：确保内存转储文件的路径正确，并且可以从 MemProcFS 运行的环境中访问。
2.  **驱动程序问题**：对于实时内存分析，请确保已正确安装并加载所需的驱动程序（例如 WinPMEM、Dokany）。
3.  **权限问题**：MemProcFS 可能需要管理员或 root 权限才能访问某些系统资源，尤其是在进行实时分析时。
4.  **内存镜像损坏**：内存转储文件可能已损坏或不完整。如果可能，请尝试重新获取镜像。

## 问题：Python API 脚本失败

如果 Skill 生成的 Python 脚本失败，请检查以下内容：

1.  **`memprocfs` 包**：确保 `memprocfs` Python 包已安装在正确的环境中 (`pip install memprocfs`)。
2.  **VMM 初始化**：验证传递给 `memprocfs.Vmm([...])` 的参数是否适合您的设置（例如，正确的设备类型和路径）。
3.  **对象存在性**：脚本可能正在尝试访问内存镜像中不存在的进程或文件。在使用对象之前，请添加检查以确保它们不为 `None`。

## 通用提示

-   **详细输出**：从命令行运行 MemProcFS 时，使用 `-v` (verbose) 或 `-vv` (very verbose) 标志以获取更详细的输出，这有助于诊断问题。
-   **查阅 Wiki**：官方的 [MemProcFS Wiki](https://github.com/ufrisk/MemProcFS/wiki) 是获取详细文档和高级用法的绝佳资源。
