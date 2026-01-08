# Forensic Workflows with MemProcFS

This document outlines structured workflows for common forensic tasks using MemProcFS. These workflows are designed to be comprehensive and repeatable.

## Workflow 1: Initial System Triage

**Goal**: Quickly gather essential information about the system state at the time of memory acquisition.

1.  **System Information**: Check the `sys/sysinfo` directory to identify the operating system version, architecture, and other basic details.
2.  **Process Listing**: List all running processes by examining the contents of the `proc` directory. Pay attention to suspicious or unexpected process names.
3.  **Network Connections**: Analyze active network connections by inspecting the `sys/net` directory. Look for unusual remote addresses or ports.
4.  **User Activity**: Identify logged-in users and their activity by exploring the `sys/users` directory.

## Workflow 2: Malware Detection and Analysis

**Goal**: Identify and analyze potential malware on the system.

1.  **Run FindEvil**: Use the `forensic/findevil` module to automatically scan for common signs of malware, such as code injection, hooked functions, and hidden processes.
2.  **YARA Scanning**: Perform a YARA scan across all process memory using the `forensic/yara` module with a comprehensive ruleset.
    ```bash
    # Example command within the MemProcFS file system
    cat /forensic/yara/all_processes > yara_results.txt
    ```
3.  **Analyze Suspicious Processes**: For any process flagged as suspicious, perform a deeper analysis:
    -   Examine its memory map (`proc/<pid>/memmap`).
    -   Dump its executable and modules for static analysis (`proc/<pid>/bin`).
    -   Inspect its network connections and open handles.

## Workflow 3: File and Data Recovery

**Goal**: Recover files, data, and artifacts from memory.

1.  **NTFS Analysis**: Explore the `forensic/ntfs` module to analyze the NTFS file system metadata and potentially recover deleted files.
2.  **Prefetch Files**: Examine the `forensic/prefetch` directory to identify recently executed applications.
3.  **Timeline Generation**: Create a timeline of system activity using the `forensic/timeline` module. This can help correlate events and establish a sequence of actions.
4.  **Web Artifacts**: Use the `forensic/web` module to recover browsing history, cache, and other web-related artifacts.
