# MemProcFS Python API: 综合指南

本指南全面概述了 MemProcFS Python API，重点介绍其在内存取证中的实际应用。

## 1. 初始化与核心对象

`Vmm` 对象是所有 API 功能的入口点。它的初始化方式与可执行文件类似，通过命令行参数进行。

```python
import memprocfs

# --- 初始化示例 ---

# 从内存转储文件初始化
vmm = memprocfs.Vmm(['-device', 'path/to/memory.dmp'])

# 使用 WinPMEM 从实时内存初始化
# vmm = memprocfs.Vmm(['-device', 'pmem'])

# 从 PCILeech FPGA 设备初始化
# vmm = memprocfs.Vmm(['-device', 'fpga'])
```

## 2. `Vmm` 基础对象

`vmm` 对象提供了对所有主要组件的访问。

| 属性 | 描述 |
|---|---|
| `vmm.process` | 按名称或 PID 访问进程。 |
| `vmm.process_all` | 遍历所有正在运行的进程。 |
| `vmm.reg_key` | 访问注册表项。 |
| `vmm.fs` | 与虚拟文件系统交互。 |
| `vmm.memory` | 访问原始物理内存。 |
| `vmm.info` | 有关内存镜像的常规信息。 |
| `vmm.hex` | 一个以十六进制/ASCII 格式打印数据的实用工具。 |

## 3. 进程分析 (`VmmProcess`)

进程对象是内存分析的核心。它们提供了有关进程状态的丰富信息。

```python
# 获取一个进程对象
proc = vmm.process('lsass.exe')

if proc:
    print(f"--- 进程: {proc.name} (PID: {proc.pid}) ---")
    print(f"路径: {proc.path}")
    print(f"命令行: {proc.command_line}")
    print(f"父进程 PID: {proc.pid_parent}")

    # --- 每个进程的文件系统 ---
    # 像访问文件系统一样访问文件、句柄、模块等。
    
    # 列出加载的模块
    print("\n[模块]")
    for module in proc.module_all():
        print(f"- {module.name}: {hex(module.base)} - {hex(module.size)}")

    # 列出打开的句柄
    print("\n[句柄]")
    for handle in proc.handle_all():
        print(f"- 类型: {handle.type}, 名称: {handle.name}")

    # 从进程虚拟内存中读取
    peb_data = proc.memory.read(proc.peb_address, 0x100)
    print("\n[PEB 十六进制转储]")
    print(vmm.hex(peb_data))
```

## 4. 注册表分析 (`VmmRegKey`, `VmmRegValue`)

该 API 提供了对内存中注册表配置单元的直接访问。

```python
# --- 示例: 读取自动运行项 ---

run_key_path = 'HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'

try:
    run_key = vmm.reg_key(run_key_path)
    print(f"\n--- 从 {run_key_path} 读取的自动运行项 ---")
    for value in run_key.values():
        print(f"- {value.name}: {value.vstr()}")
except memprocfs.errors.VmmError:
    print(f"找不到注册表项: {run_key_path}")
```

## 5. 取证分析 (YARA & FindEvil)

以编程方式利用内置的取证功能。

### YARA 扫描

您可以在物理内存或单个进程上执行 YARA 扫描。

```python
# --- 示例: 对进程进行 YARA 扫描 ---

yara_rules = """
rule suspicious_string {
    strings:
        $s1 = "mimikatz" nocase
    condition:
        $s1
}
"""

proc_to_scan = vmm.process('lsass.exe')
if proc_to_scan:
    matches = proc_to_scan.search.yara(yara_rules)
    if matches:
        print("\n--- 发现 YARA 匹配项 ---")
        for match in matches:
            print(f"规则: {match['rule']}, 偏移量: {hex(match['offset'])}, 匹配项: {match['data']}")
```

### FindEvil

`findevil` 模块用于检测常见的恶意软件模式，可以通过虚拟文件系统访问。

```python
# 读取所有发现的摘要
findevil_summary = vmm.fs.readfile('/forensic/findevil/summary.txt')
print("\n--- FindEvil 摘要 ---")
print(findevil_summary.decode())
```

## 6. Jupyter Notebook 集成

MemProcFS 非常适合在 Jupyter Notebooks 中进行交互式分析。逐步探索内存、可视化数据和记录发现的能力使其成为研究人员和分析师的强大工具。

**在 Notebook 单元格中设置:**
```python
import memprocfs
import pandas as pd

# 初始化 VMM
vmm = memprocfs.Vmm(['-device', 'path/to/memory.dmp'])

# 示例: 获取所有进程并显示在 DataFrame 中
procs = [{'pid': p.pid, 'name': p.name, 'path': p.path} for p in vmm.process_all()]
df = pd.DataFrame(procs)
display(df)
```

## 7. 访问虚拟文件系统 (VFS)

MemProcFS 的很大一部分功能来自其虚拟文件系统。您可以使用 `vmm.fs` 对象访问文档中提到的任何路径（例如 `/forensic/ntfs`、`/sys/net` 或每个进程的 `/proc/<pid>/handles`）。

```python
# --- 示例: 读取时间线文件 ---

try:
    # 时间线可能很大，因此最好分块读取或直接保存。
    timeline_data = vmm.fs.readfile("/forensic/timeline/timeline.csv")
    with open("timeline.csv", "wb") as f:
        f.write(timeline_data)
    print("\n时间线已保存到 timeline.csv")
except memprocfs.errors.VmmError as e:
    print(f"\n读取时间线失败: {e}")

# --- 示例: 列出从进程中恢复的文件 ---

# 查找一个可能包含有趣打开文件的进程，例如编辑器或浏览器
proc_to_inspect = vmm.process("notepad.exe")

if proc_to_inspect:
    print(f"\n--- 从 {proc_to_inspect.name} 中可恢复的文件 ---")
    try:
        # 路径对应于每个进程的文件系统
        vfs_path = f"/proc/{proc_to_inspect.pid}/files/handles/"
        open_files = vmm.fs.listdir(vfs_path)
        for f in open_files:
            print(f"- {f.name} (大小: {f.size})")
            # 然后您可以使用 vmm.fs.readfile(vfs_path + f.name) 读取文件
    except memprocfs.errors.VmmError as e:
        print(f"无法列出进程的文件: {e}")
```

这种方法允许您以编程方式访问 MemProcFS 在其文件系统中公开的任何工件，包括您列出的那些，例如 `eventlog`、`prefetch`、`ntfs`、`bitlocker` 信息以及每个进程的数据，如 `memmap`、`minidump` 和 `threads`。
