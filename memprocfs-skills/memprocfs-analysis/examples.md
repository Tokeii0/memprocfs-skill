# MemProcFS Use Cases and Examples

This document provides practical examples of how to use MemProcFS for various memory analysis tasks.

## Example 1: Listing Processes with High Network Activity

**Goal**: Identify processes that have a large number of active network connections.

```python
import memprocfs

vmm = memprocfs.Vmm(['-device', 'path/to/your/dump.raw'])

# A simple threshold for "high" network activity
CONNECTION_THRESHOLD = 20

for process in vmm.process_all():
    try:
        net_connections = process.net()
        if net_connections and len(net_connections) > CONNECTION_THRESHOLD:
            print(f"Process {process.name} (PID: {process.pid}) has {len(net_connections)} network connections.")
            for conn in net_connections:
                print(f"  {conn.ip_local}:{conn.port_local} -> {conn.ip_remote}:{conn.port_remote} ({conn.state})")
    except Exception as e:
        # Some processes might not have network connections or may be inaccessible
        pass
```

## Example 2: Finding Evidence of Code Injection

**Goal**: Use the `findevil` module to scan for signs of code injection in a process.

This can be done directly through the file system by reading the output of the `findevil` module for a specific process.

1.  Navigate to the process directory: `cd /proc/<pid>/`
2.  Read the `findevil` results: `cat findevil`

**Programmatic Approach (Python):**

```python
import memprocfs

vmm = memprocfs.Vmm(['-device', 'path/to/your/dump.raw'])

# Using the forensic module
findevil_results = vmm.fs.readfile('/forensic/findevil/summary.txt')
print(findevil_results.decode())

# To check a specific process
process = vmm.process('explorer.exe')
if process:
    try:
        process_findevil = process.fs.readfile('findevil')
        print(f"FindEvil results for {process.name}:\n{process_findevil.decode()}")
    except memprocfs.errors.VmmError as e:
        print(f"Could not get FindEvil results for {process.name}: {e}")
```

## Example 3: Dumping All Modules from a Process

**Goal**: Extract all loaded DLLs and the main executable from a suspicious process for further analysis.

This can be done by copying the files from the `/proc/<pid>/bin/` directory.

**Programmatic Approach (Python):**

```python
import memprocfs
import os

def dump_modules(vmm, process_name, output_dir):
    process = vmm.process(process_name)
    if not process:
        print(f"Process '{process_name}' not found.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for module in process.module_all():
        try:
            module_data = module.fs.read()
            output_path = os.path.join(output_dir, f"{module.name}")
            with open(output_path, 'wb') as f:
                f.write(module_data)
            print(f"Dumped {module.name} to {output_path}")
        except Exception as e:
            print(f"Failed to dump {module.name}: {e}")

# Example usage:
# dump_modules(vmm, 'svchost.exe', '/tmp/svchost_modules/')
```
