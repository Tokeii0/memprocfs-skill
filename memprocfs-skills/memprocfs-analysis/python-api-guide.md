# MemProcFS Python API: A Comprehensive Guide

This guide provides a comprehensive overview of the MemProcFS Python API, focusing on practical applications for memory forensics.

## 1. Initialization and Core Object

The `Vmm` object is the entry point to all API functionality. It's initialized with command-line arguments, similar to the executable.

```python
import memprocfs

# --- Initialization Examples ---

# From a memory dump file
vmm = memprocfs.Vmm(['-device', 'path/to/memory.dmp'])

# From live memory using WinPMEM
# vmm = memprocfs.Vmm(['-device', 'pmem'])

# From a PCILeech FPGA device
# vmm = memprocfs.Vmm(['-device', 'fpga'])
```

## 2. The `Vmm` Base Object

The `vmm` object provides access to all major components.

| Property | Description |
|---|---|
| `vmm.process` | Access processes by name or PID. |
| `vmm.process_all` | Iterate over all running processes. |
| `vmm.reg_key` | Access registry keys. |
| `vmm.fs` | Interact with the virtual file system. |
| `vmm.memory` | Access raw physical memory. |
| `vmm.info` | General information about the memory image. |
| `vmm.hex` | A utility to print data in a hex/ASCII format. |

## 3. Process Analysis (`VmmProcess`)

Process objects are central to memory analysis. They provide a wealth of information about a process's state.

```python
# Get a process object
proc = vmm.process('lsass.exe')

if proc:
    print(f"--- Process: {proc.name} (PID: {proc.pid}) ---")
    print(f"Path: {proc.path}")
    print(f"Command Line: {proc.command_line}")
    print(f"Parent PID: {proc.pid_parent}")

    # --- Per-Process File System ---
    # Access files, handles, modules, etc., as if they were in a file system.
    
    # List loaded modules
    print("\n[Modules]")
    for module in proc.module_all():
        print(f"- {module.name}: {hex(module.base)} - {hex(module.size)}")

    # List open handles
    print("\n[Handles]")
    for handle in proc.handle_all():
        print(f"- Type: {handle.type}, Name: {handle.name}")

    # Read from process virtual memory
    peb_data = proc.memory.read(proc.peb_address, 0x100)
    print("\n[PEB Hex Dump]")
    print(vmm.hex(peb_data))
```

## 4. Registry Analysis (`VmmRegKey`, `VmmRegValue`)

The API provides direct access to the registry hives in memory.

```python
# --- Example: Reading AutoRun Keys ---

run_key_path = 'HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'

try:
    run_key = vmm.reg_key(run_key_path)
    print(f"\n--- AutoRun Keys from {run_key_path} ---")
    for value in run_key.values():
        print(f"- {value.name}: {value.vstr()}")
except memprocfs.errors.VmmError:
    print(f"Could not find registry key: {run_key_path}")
```

## 5. Forensic Analysis (YARA & FindEvil)

Leverage built-in forensic capabilities programmatically.

### YARA Scanning

You can perform YARA scans on physical memory or individual processes.

```python
# --- Example: YARA scan on a process ---

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
        print("\n--- YARA Matches Found ---")
        for match in matches:
            print(f"Rule: {match['rule']}, Offset: {hex(match['offset'])}, Matched: {match['data']}")
```

### FindEvil

The `findevil` module, which detects common malware patterns, can be accessed via the virtual file system.

```python
# Read the summary of all findings
findevil_summary = vmm.fs.readfile('/forensic/findevil/summary.txt')
print("\n--- FindEvil Summary ---")
print(findevil_summary.decode())
```

## 6. Jupyter Notebook Integration

MemProcFS is ideal for interactive analysis in Jupyter Notebooks. The ability to incrementally explore memory, visualize data, and document findings makes it a powerful tool for researchers and analysts.

**Setup in a Notebook Cell:**
```python
import memprocfs
import pandas as pd

# Initialize VMM
vmm = memprocfs.Vmm(['-device', 'path/to/memory.dmp'])

# Example: Get all processes and display in a DataFrame
procs = [{'pid': p.pid, 'name': p.name, 'path': p.path} for p in vmm.process_all()]
df = pd.DataFrame(procs)
display(df)
```

```
## 7. Accessing the Virtual File System (VFS)

A significant portion of MemProcFS's power comes from its virtual file system. You can access any path mentioned in the documentation (such as `/forensic/ntfs`, `/sys/net`, or per-process `/proc/<pid>/handles`) using the `vmm.fs` object.

```python
# --- Example: Reading the timeline file ---

try:
    # The timeline can be large, so it's best to read it in chunks or save it directly.
    timeline_data = vmm.fs.readfile("/forensic/timeline/timeline.csv")
    with open("timeline.csv", "wb") as f:
        f.write(timeline_data)
    print("\nTimeline saved to timeline.csv")
except memprocfs.errors.VmmError as e:
    print(f"\nFailed to read timeline: {e}")

# --- Example: Listing files recovered from a process ---

# Find a process that might have interesting open files, like an editor or browser
proc_to_inspect = vmm.process("notepad.exe")

if proc_to_inspect:
    print(f"\n--- Recoverable files from {proc_to_inspect.name} ---")
    try:
        # Path corresponds to the per-process file system
        vfs_path = f"/proc/{proc_to_inspect.pid}/files/handles/"
        open_files = vmm.fs.listdir(vfs_path)
        for f in open_files:
            print(f"- {f.name} (Size: {f.size})")
            # You could then read the file with vmm.fs.readfile(vfs_path + f.name)
    except memprocfs.errors.VmmError as e:
        print(f"Could not list files for process: {e}")
```

This approach allows you to programmatically access any artifact that MemProcFS exposes in its file system, including those you listed, such as `eventlog`, `prefetch`, `ntfs`, `bitlocker` info, and per-process data like `memmap`, `minidump`, and `threads`.
