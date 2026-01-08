# MemProcFS 辅助脚本

此目录包含一系列 Python 脚本，为常见的 MemProcFS 分析任务提供便捷的接口。这些脚本旨在简化内存取证工作流程并自动化重复的分析操作。

## 可用脚本

### 1. dump_process_memory.py

**用途**: 将进程的完整虚拟内存提取到二进制文件以供离线分析。

**用法**:
```bash
python dump_process_memory.py <进程名或PID> <输出文件> -device <内存源>
```

**参数**:
- `<进程名或PID>`: 目标进程的名称 (例如 `lsass.exe`) 或 PID (例如 `456`)
- `<输出文件>`: 内存转储将被保存的路径 (例如 `process_dump.bin`)
- `-device <内存源>`: MemProcFS 设备规范 (例如 `-device memory.dmp` 或 `-device pmem`)

**示例**:
```bash
python dump_process_memory.py explorer.exe explorer_memory.bin -device C:/dumps/system.dmp
```

**输出**: 包含进程整个虚拟内存空间的二进制文件，适合用 Ghidra、IDA Pro 或其他二进制分析框架进行分析。

### 2. list_process_handles.py

**用途**: 枚举指定进程的所有打开句柄，包括文件、注册表项、事件和其他内核对象。

**用法**:
```bash
python list_process_handles.py <进程名或PID> -device <内存源>
```

**参数**:
- `<进程名或PID>`: 目标进程的名称或 PID
- `-device <内存源>`: MemProcFS 设备规范

**示例**:
```bash
python list_process_handles.py svchost.exe -device pmem
```

**输出**: 格式化的句柄列表，包含其类型和名称，用于识别：
- 打开的文件及其路径
- 正在访问的注册表项
- 网络套接字和连接
- 同步对象 (事件、互斥体、信号量)

### 3. yara_scan_process.py

**用途**: 对进程内存执行 YARA 模式匹配，以检测恶意软件签名、可疑代码模式或已知的 IOC (妥协指标)。

**用法**:
```bash
python yara_scan_process.py <进程名或PID> <yara_rule_file> -device <内存源>
```

**参数**:
- `<进程名或PID>`: 目标进程的名称或 PID
- `<yara_rule_file>`: YARA 规则文件的路径 (`.yar` 或 `.yara`)
- `-device <内存源>`: MemProcFS 设备规范

**示例**:
```bash
python yara_scan_process.py lsass.exe malware_signatures.yara -device memory.dmp
```

**输出**: 匹配的 YARA 规则及其偏移量和匹配数据，以 UTF-8 (如果可读) 和十六进制格式显示。

## 常见工作流程

### 工作流程 1: 可疑进程分析

```bash
# 1. 列出所有进程以识别可疑的
memprocfs -device memory.dmp

# 2. 转储进程内存
python dump_process_memory.py suspicious.exe suspicious_dump.bin -device memory.dmp

# 3. 列出其句柄以查看它访问的资源
python list_process_handles.py suspicious.exe -device memory.dmp

# 4. 使用 YARA 规则扫描
python yara_scan_process.py suspicious.exe malware.yara -device memory.dmp
```

### 工作流程 2: 恶意软件检测

```bash
# 扫描多个进程以查找已知的恶意软件签名
for process in svchost.exe explorer.exe notepad.exe; do
    python yara_scan_process.py "$process" known_malware.yara -device memory.dmp
done
```

### 工作流程 3: 文件句柄分析

```bash
# 查找哪个进程打开了特定文件
python list_process_handles.py explorer.exe -device memory.dmp | grep "C:\\Users"
```

## 要求

- Python 3.7 或更高版本
- 已安装并可访问 MemProcFS
- memprocfs Python 包: `pip install memprocfs`
- YARA 规则 (用于 `yara_scan_process.py`)

## 错误处理

所有脚本都包含常见问题的错误处理：

- **未找到进程**: 如果指定的进程不存在，脚本将报告
- **无效的内存源**: 如果设备规范不正确，MemProcFS 将报告错误
- **文件访问错误**: 如果脚本无法读取或写入文件，将通知
- **YARA 规则错误**: YARA 规则中的语法错误将被报告

## 提示和最佳实践

1. **使用描述性的输出文件名**: 在转储文件名中包含进程名称和时间戳，便于识别
2. **首先测试 YARA 规则**: 在运行大规模扫描之前验证 YARA 规则
3. **监控资源使用**: 大型内存转储可能消耗大量磁盘空间；确保有足够的存储空间
4. **组合脚本**: 将脚本链接在一起以进行全面分析
5. **记录发现**: 将脚本输出保存到日志文件以供取证报告使用

## 扩展脚本

这些脚本可作为自定义分析的模板。您可以通过以下方式扩展它们：

- 添加额外的进程信息收集
- 与外部分析工具集成
- 将结果导出为结构化格式 (JSON、CSV)
- 实现多个进程的并行处理
- 为发现添加电子邮件或 webhook 通知

## 故障排除

### 脚本失败，显示"未找到进程"
- 验证进程名称或 PID 是否正确
- 检查内存源是否包含该进程 (它可能已终止)
- 使用 MemProcFS 命令行工具列出可用进程

### YARA 扫描未返回任何匹配项
- 验证 YARA 规则文件是否有效
- 检查规则语法是否正确
- 确保正确读取进程内存
- 尝试使用更简单的规则来测试扫描机制

### 内存转储非常大
- 这对于具有大量虚拟内存分配的大型进程是正常的
- 考虑使用压缩或将转储分割成较小的块
- 运行转储之前确保有足够的磁盘空间

## 参考资源

- [MemProcFS Python API 文档](https://github.com/ufrisk/MemProcFS/wiki/API_Python)
- [YARA 文档](https://yara.readthedocs.io/)
- [MemProcFS 官方仓库](https://github.com/ufrisk/MemProcFS)
