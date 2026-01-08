# MemProcFS Helper Scripts

This directory contains a collection of Python scripts that provide convenient interfaces for common MemProcFS analysis tasks. These scripts are designed to simplify memory forensics workflows and automate repetitive analysis operations.

## Available Scripts

### 1. dump_process_memory.py

**Purpose**: Extracts the complete virtual memory of a process to a binary file for offline analysis.

**Usage**:
```bash
python dump_process_memory.py <process_name_or_pid> <output_file> -device <memory_source>
```

**Parameters**:
- `<process_name_or_pid>`: The name (e.g., `lsass.exe`) or PID (e.g., `456`) of the target process
- `<output_file>`: Path where the memory dump will be saved (e.g., `process_dump.bin`)
- `-device <memory_source>`: MemProcFS device specification (e.g., `-device memory.dmp` or `-device pmem`)

**Example**:
```bash
python dump_process_memory.py explorer.exe explorer_memory.bin -device C:/dumps/system.dmp
```

**Output**: A binary file containing the process's entire virtual memory space, suitable for analysis with tools like Ghidra, IDA Pro, or other binary analysis frameworks.

### 2. list_process_handles.py

**Purpose**: Enumerates all open handles for a specified process, including files, registry keys, events, and other kernel objects.

**Usage**:
```bash
python list_process_handles.py <process_name_or_pid> -device <memory_source>
```

**Parameters**:
- `<process_name_or_pid>`: The name or PID of the target process
- `-device <memory_source>`: MemProcFS device specification

**Example**:
```bash
python list_process_handles.py svchost.exe -device pmem
```

**Output**: A formatted list of handles with their types and names, useful for identifying:
- Open files and their paths
- Registry keys being accessed
- Network sockets and connections
- Synchronization objects (events, mutexes, semaphores)

### 3. yara_scan_process.py

**Purpose**: Performs YARA pattern matching on a process's memory to detect malware signatures, suspicious code patterns, or known IOCs (Indicators of Compromise).

**Usage**:
```bash
python yara_scan_process.py <process_name_or_pid> <yara_rule_file> -device <memory_source>
```

**Parameters**:
- `<process_name_or_pid>`: The name or PID of the target process
- `<yara_rule_file>`: Path to a YARA rule file (`.yar` or `.yara`)
- `-device <memory_source>`: MemProcFS device specification

**Example**:
```bash
python yara_scan_process.py lsass.exe malware_signatures.yara -device memory.dmp
```

**Output**: Matching YARA rules with their offsets and matched data, displayed in both UTF-8 (if readable) and hexadecimal formats.

## Common Workflows

### Workflow 1: Suspicious Process Analysis

```bash
# 1. List all processes to identify suspicious ones
memprocfs -device memory.dmp

# 2. Dump the process memory
python dump_process_memory.py suspicious.exe suspicious_dump.bin -device memory.dmp

# 3. List its handles to see what resources it's accessing
python list_process_handles.py suspicious.exe -device memory.dmp

# 4. Scan with YARA rules
python yara_scan_process.py suspicious.exe malware.yara -device memory.dmp
```

### Workflow 2: Malware Detection

```bash
# Scan multiple processes for known malware signatures
for process in svchost.exe explorer.exe notepad.exe; do
    python yara_scan_process.py "$process" known_malware.yara -device memory.dmp
done
```

### Workflow 3: File Handle Analysis

```bash
# Find which process has a specific file open
python list_process_handles.py explorer.exe -device memory.dmp | grep "C:\\Users"
```

## Requirements

- Python 3.7 or higher
- MemProcFS installed and accessible
- memprocfs Python package: `pip install memprocfs`
- YARA rules (for `yara_scan_process.py`)

## Error Handling

All scripts include error handling for common issues:

- **Process not found**: The script will report if the specified process doesn't exist
- **Invalid memory source**: If the device specification is incorrect, MemProcFS will report an error
- **File access errors**: The script will notify if it cannot read or write files
- **YARA rule errors**: Syntax errors in YARA rules will be reported

## Tips and Best Practices

1. **Use descriptive output filenames**: Include the process name and timestamp in dump filenames for easy identification
2. **Test YARA rules first**: Validate YARA rules before running large-scale scans
3. **Monitor resource usage**: Large memory dumps can consume significant disk space; ensure adequate storage
4. **Combine scripts**: Chain scripts together for comprehensive analysis workflows
5. **Document findings**: Save script output to log files for forensic reports

## Extending the Scripts

These scripts serve as templates for custom analysis. You can extend them by:

- Adding additional process information collection
- Integrating with external analysis tools
- Exporting results to structured formats (JSON, CSV)
- Implementing parallel processing for multiple processes
- Adding email or webhook notifications for findings

## Troubleshooting

### Script fails with "Process not found"
- Verify the process name or PID is correct
- Check that the memory source contains the process (it may have terminated)
- Use the MemProcFS command-line tool to list available processes

### YARA scan returns no matches
- Verify the YARA rule file is valid
- Check that the rule syntax is correct
- Ensure the process memory is being read correctly
- Try a simpler rule to test the scanning mechanism

### Memory dump is very large
- This is normal for large processes with significant virtual memory allocations
- Consider using compression or splitting the dump into smaller chunks
- Ensure sufficient disk space before running the dump

## References

- [MemProcFS Python API Documentation](https://github.com/ufrisk/MemProcFS/wiki/API_Python)
- [YARA Documentation](https://yara.readthedocs.io/)
- [MemProcFS Official Repository](https://github.com/ufrisk/MemProcFS)
