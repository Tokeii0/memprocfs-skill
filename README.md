
# MemProcFS Agent Skill

[English](README_EN.md)

## 概述

**MemProcFS Agent Skill** 是一个为 Claude Code 设计的代理技能，旨在增强 Claude 在内存分析和数字取证领域的能力。该技能将 Claude 与强大的 MemProcFS 工具相结合，使用户能够进行深入的内存转储分析、实时内存调查和取证工作流程。

## 什么是 MemProcFS？

**MemProcFS** 是一个开源工具，它提供了一种将物理内存作为虚拟文件系统中的文件来查看的便捷方法。它支持多种内存获取方法，包括内存转储文件、实时内存（通过 WinPMEM 或 DumpIt）、虚拟机内存和远程内存获取（通过 LeechAgent）。

### 主要特性

-   **虚拟文件系统接口**: 通过标准文件操作访问内存内容和工件。
-   **多平台支持**: 支持 Windows、Linux、macOS 和 ARM64 架构。
-   **丰富的 API**: 提供 C/C++、C#、Java、Rust 和 Python 接口。
-   **取证模块**: 包括 YARA 扫描、文件恢复、事件日志解析等功能。
-   **插件架构**: 支持 C、Rust 和 Python 插件的自定义扩展。

## Skill 文件结构

```
memprocfs-analysis/
├── SKILL.md                      # Skill 元数据和主要指令
├── forensic-workflows.md         # 常见取证工作流指南
├── python-api-guide.md          # Python API 详细使用指南
├── filesystem-reference.md      # 虚拟文件系统结构参考
├── examples.md                  # 实际代码示例和用例
├── troubleshooting.md           # 常见问题和解决方案
└── scripts/                     # 可选的辅助脚本目录
```

## 安装和使用

### 1. 安装 Skill

将 `memprocfs-analysis` 目录复制到 Claude Code 的 Skill 目录中：

**在 Windows 上:**
```
C:\Users\<YourUsername>\.claude\skills\memprocfs-analysis\
```

**在 Linux/macOS 上:**
```
~/.claude/skills/memprocfs-analysis/
```

### 2. 安装 MemProcFS

根据您的操作系统，从 [MemProcFS GitHub 发布页面](https://github.com/ufrisk/MemProcFS/releases) 下载最新版本。

**Windows:**
- 下载并安装 Dokany 文件系统库（用于挂载虚拟文件系统）
- 下载 MemProcFS 二进制文件

**Linux:**
```bash
sudo apt-get install libusb-1.0 fuse
# 从发布页面下载 MemProcFS
```

**macOS:**
- 下载并安装 macFuse
- 从发布页面下载 MemProcFS

### 3. 安装 Python 包（可选）

如果您计划使用 Python API 进行自动化分析：

```bash
pip install memprocfs
```

### 4. 加载内存镜像

使用 memprocfs.exe 加载内存转储文件，将其挂载为虚拟文件系统：

**基本命令格式：**
```bash
memprocfs.exe -device <内存镜像路径> -forensic 1
```

**示例：**
```bash
# 加载 Windows 10 x64 内存转储
memprocfs.exe -device c:\temp\win10x64-dump.raw -forensic 1

# 加载内存转储并指定挂载点
memprocfs.exe -device c:\temp\win10x64-dump.raw -forensic 1 -mount M:
```

**参数说明：**
- `-device`: 指定内存镜像文件的路径（支持 .raw, .dmp, .mem 等格式）
- `-forensic 1`: 启用取证模式，生成取证相关的分析数据
- `-mount`: （可选）指定虚拟文件系统的挂载盘符，默认为 M:

**加载完成后：**

内存镜像加载成功后，您可以通过访问挂载的虚拟文件系统进行取证分析：

```
M:\                           # 虚拟文件系统根目录
├── proc\                     # 进程信息目录
├── sys\                      # 系统信息目录
│   ├── sysinfo.txt          # 系统基本信息
│   └── net\                  # 网络连接信息
├── forensic\                 # 取证分析模块
│   ├── findevil\            # 恶意行为检测
│   ├── timeline\            # 事件时间线
│   └── yara\                # YARA 扫描结果
└── registry\                 # 注册表信息
```

您可以像访问普通文件一样读取这些目录和文件，进行内存取证分析。

### 5. 重启 Claude Code

退出并重新启动 Claude Code 以加载新的 Skill。

## 使用示例

### 初始化 Skill

在 Claude Code 中，您可以通过以下方式启动 Skill：

> "分析位于 `/path/to/memory.dmp` 的内存转储文件"

> "对这个内存镜像进行取证调查"

> "使用 MemProcFS 识别这个内存转储中的恶意软件"

### Skill 将指导您完成

1.  **初始分类**: 识别关键系统信息、运行进程和网络连接。
2.  **引导分析**: 根据您的目标建议相关的 MemProcFS 模块和命令。
3.  **取证工作流**: 对于常见的取证任务，遵循结构化的工作流程。
4.  **Python 脚本生成**: 生成自动化分析脚本。

## 文档导航

| 文档 | 用途 |
|------|------|
| [forensic-workflows.md](forensic-workflows.md) | 常见取证任务的结构化工作流程 |
| [python-api-guide.md](python-api-guide.md) | MemProcFS Python API 的完整指南 |
| [filesystem-reference.md](filesystem-reference.md) | 虚拟文件系统结构和模块参考 |
| [examples.md](examples.md) | 实际代码示例和使用场景 |
| [troubleshooting.md](troubleshooting.md) | 常见问题和解决方案 |

## 常见工作流程

### 工作流程 1: 快速系统分类

1.  检查系统信息 (`sys/sysinfo`)
2.  列出所有运行进程 (`proc`)
3.  分析网络连接 (`sys/net`)
4.  识别登录用户 (`sys/users`)

### 工作流程 2: 恶意软件检测

1.  运行 FindEvil 扫描 (`forensic/findevil`)
2.  执行 YARA 扫描 (`forensic/yara`)
3.  分析可疑进程的内存
4.  转储可疑进程的可执行文件进行静态分析

### 工作流程 3: 文件和数据恢复

1.  分析 NTFS 元数据 (`forensic/ntfs`)
2.  检查 Prefetch 文件 (`forensic/prefetch`)
3.  生成系统活动时间线 (`forensic/timeline`)
4.  恢复网络浏览工件 (`forensic/web`)

## 故障排除

如果 Skill 未触发或遇到错误，请参考 [troubleshooting.md](troubleshooting.md) 获取详细的解决方案。

## 许可证

MemProcFS 在 GNU Affero General Public License v3.0 下发布。此 Skill 为 MemProcFS 的补充文档。

## 参考资源

-   [MemProcFS GitHub 项目](https://github.com/ufrisk/MemProcFS)
-   [MemProcFS 官方 Wiki](https://github.com/ufrisk/MemProcFS/wiki)
-   [LeechCore 项目](https://github.com/ufrisk/LeechCore)
-   [PCILeech 项目](https://github.com/ufrisk/pcileech)

## 支持和反馈

如有问题或建议，请访问 [MemProcFS GitHub Issues](https://github.com/ufrisk/MemProcFS/issues) 或加入 [PCILeech/MemProcFS Discord 社区](https://discord.gg/pcileech)。
