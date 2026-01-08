# MemProcFS Agent Skill - 安装和设置指南

## 快速开始

本指南将帮助您为 Claude Code 安装和配置 MemProcFS Agent Skill。

## 前置条件

在安装 Skill 之前，请确保您拥有：

1. **Claude Code** 已安装并运行
2. **MemProcFS** 已安装在您的系统上
3. **Python 3.7+**（用于 Python API 支持）
4. **pip** 包管理器（用于安装 memprocfs Python 包）

## 第 1 步：安装 MemProcFS

### Windows

1. 从 [GitHub](https://github.com/ufrisk/MemProcFS/releases) 下载最新的 MemProcFS 版本
2. 安装 Dokany 文件系统库（虚拟文件系统挂载所需）
3. 将 MemProcFS 提取到您选择的位置（例如 `C:\Tools\MemProcFS`）
4. 将 MemProcFS 添加到系统 PATH

### Linux

```bash
# 安装依赖项
sudo apt-get update
sudo apt-get install libusb-1.0-0-dev fuse libfuse-dev

# 下载并提取 MemProcFS
wget https://github.com/ufrisk/MemProcFS/releases/download/v5.12/MemProcFS-5.12-linux.tar.gz
tar -xzf MemProcFS-5.12-linux.tar.gz
sudo mv MemProcFS /opt/
sudo ln -s /opt/MemProcFS/memprocfs /usr/local/bin/
```

### macOS

```bash
# 安装 macFuse（文件系统挂载所需）
brew install macfuse

# 下载并提取 MemProcFS
wget https://github.com/ufrisk/MemProcFS/releases/download/v5.12/MemProcFS-5.12-macos.tar.gz
tar -xzf MemProcFS-5.12-macos.tar.gz
sudo mv MemProcFS /opt/
sudo ln -s /opt/MemProcFS/memprocfs /usr/local/bin/
```

## 第 2 步：安装 Python 包（可选）

如果您计划使用 Python API 进行自动化分析：

```bash
pip install memprocfs
```

验证安装：

```bash
python -c "import memprocfs; print(memprocfs.__version__)"
```

## 第 3 步：加载内存镜像

使用 memprocfs.exe 将内存转储文件挂载为虚拟文件系统，以便进行取证分析。

### 基本用法

```bash
# 基本命令格式
memprocfs.exe -device <内存镜像路径> -forensic 1

# 示例：加载 Windows 10 x64 内存转储
memprocfs.exe -device c:\temp\win10x64-dump.raw -forensic 1
```

### 常用命令参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `-device` | 内存镜像文件路径 | `-device c:\temp\dump.raw` |
| `-forensic 1` | 启用取证模式 | `-forensic 1` |
| `-mount` | 指定挂载盘符（默认 M:） | `-mount N:` |
| `-v` | 显示详细输出 | `-v` |
| `-pagefile` | 指定页面文件路径 | `-pagefile c:\temp\pagefile.sys` |

### 加载完成后的操作

内存镜像加载成功后，MemProcFS 会将内存内容映射为虚拟文件系统。您可以通过访问挂载的盘符（默认 M:）进行取证分析：

```
M:\                           # 虚拟文件系统根目录
├── proc\                     # 进程信息
│   ├── <PID>\               # 各进程详细信息
│   │   ├── handles.txt      # 进程句柄
│   │   ├── modules.txt      # 加载的模块
│   │   └── memory.txt       # 内存映射
├── sys\                      # 系统信息
│   ├── sysinfo.txt          # 系统基本信息
│   ├── net\                  # 网络连接
│   └── users\               # 用户信息
├── forensic\                 # 取证分析模块
│   ├── findevil\            # 恶意行为检测
│   ├── timeline\            # 事件时间线
│   ├── yara\                # YARA 扫描
│   └── ntfs\                # NTFS 文件系统分析
└── registry\                 # 注册表配置单元
```

### 快速取证示例

```bash
# 查看系统信息
type M:\sys\sysinfo.txt

# 列出所有进程
dir M:\proc

# 查看网络连接
type M:\sys\net\netstat.txt

# 检查恶意行为
dir M:\forensic\findevil
```

## 第 4 步：安装 Skill

1. **定位 Skill 目录**

   找到您的 Claude Code Skill 目录：
   
   - **Windows**: `C:\Users\<YourUsername>\.claude\skills\`
   - **Linux/macOS**: `~/.claude/skills/`

2. **复制 Skill**

   将整个 `memprocfs-analysis` 目录复制到 Skill 目录：

   ```bash
   # Linux/macOS
   cp -r memprocfs-analysis ~/.claude/skills/

   # Windows (PowerShell)
   Copy-Item -Recurse memprocfs-analysis $env:USERPROFILE\.claude\skills\
   ```

3. **验证安装**

   检查目录结构是否正确：

   ```
   ~/.claude/skills/memprocfs-analysis/
   ├── SKILL.md
   ├── README.md
   ├── python-api-guide.md
   ├── forensic-workflows.md
   ├── filesystem-reference.md
   ├── examples.md
   ├── troubleshooting.md
   └── scripts/
   ```

## 第 5 步：重启 Claude Code

退出并重新启动 Claude Code 以加载新的 Skill。该 Skill 现在应该可以使用了。

## 验证

要验证 Skill 是否正确加载：

1. 打开 Claude Code
2. 询问："有哪些可用的 Skill？"
3. 在列表中查找 `memprocfs-assistant`

## 故障排除

### Skill 未加载

- 确保目录结构正确
- 检查所有 `.md` 文件是否存在
- 重启 Claude Code
- 检查 Claude Code 日志中的错误

### 找不到 MemProcFS

- 验证 MemProcFS 已安装并在您的 PATH 中
- 在 Windows 上，确保已安装 Dokany
- 在 Linux/macOS 上，确保已安装 FUSE/macFuse

### Python API 问题

- 验证 Python 3.7+ 已安装
- 运行 `pip install --upgrade memprocfs`
- 检查 memprocfs 包是否可从您的 Python 环境访问

## 后续步骤

1. 阅读 [README.md](README.md) 了解 Skill 的概述
2. 查看 [python-api-guide.md](python-api-guide.md) 了解 API 文档
3. 检查 [forensic-workflows.md](forensic-workflows.md) 了解常见工作流
4. 浏览 [examples.md](examples.md) 了解代码示例
