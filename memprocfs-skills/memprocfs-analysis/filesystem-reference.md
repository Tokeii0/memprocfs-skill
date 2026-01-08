# MemProcFS Virtual File System Reference

This document provides a reference for the virtual file system structure exposed by MemProcFS.

## Root Directory (`/`)

-   **/conf/**: Configuration files and settings.
-   **/forensic/**: Modules for forensic analysis.
-   **/misc/**: Miscellaneous utilities and information.
-   **/proc/**: A directory for each running process, identified by its PID.
-   **/sys/**: System-wide information and modules.
-   **/vm/**: Information related to the virtual machine, if applicable.

## Forensic Modules (`/forensic/`)

-   **/csv/**: Output from various modules in CSV format.
-   **/files/**: Recovered files from memory.
-   **/findevil/**: Results from the FindEvil malware scanner.
-   **/json/**: Output from various modules in JSON format.
-   **/ntfs/**: NTFS file system analysis.
-   **/prefetch/**: Prefetch file analysis.
-   **/timeline/**: System activity timeline.
-   **/web/**: Web browsing artifacts.
-   **/yara/**: YARA scanning results.

## System Information (`/sys/`)

-   **/certificates/**: System certificate information.
-   **/drivers/**: Loaded kernel drivers.
-   **/memory/**: Physical memory map.
-   **/net/**: Network connections and statistics.
-   **/objects/**: Kernel objects.
-   **/pool/**: Kernel pool information.
-   **/proc/**: Summary of running processes.
-   **/services/**: System services.
-   **/syscall/**: System call information.
-   **/sysinfo/**: General system information.
-   **/tasks/**: Scheduled tasks.
-   **/users/**: User accounts and sessions.

## Process Information (`/proc/<pid>/`)

-   **/bin/**: The process executable and its loaded modules.
-   **/console/**: Console command history.
-   **/files/**: Open file handles.
-   **/handles/**: All open handles.
-   **/heaps/**: Process heap information.
-   **/memmap/**: The process's virtual memory map.
-   **/minidump/**: A minidump of the process.
-   **/modules/**: Loaded modules (DLLs).
-   **/threads/**: Process threads.
-   **/token/**: Security token information.
-   **/vmemd/**: The entire virtual memory of the process as a single file.
