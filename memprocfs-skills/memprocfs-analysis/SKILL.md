---
name: memprocfs-assistant
description: Assists with memory analysis and forensics using MemProcFS. Use when analyzing memory dumps, investigating system activity, or performing forensic examinations.
---

# MemProcFS Assistant

This Skill enhances my ability to perform memory analysis and forensics using **MemProcFS**. When you ask for help with a memory dump, live memory analysis, or a forensic investigation, I will use this Skill to guide my actions.

## Core Capabilities

1.  **Initial Triage**: I will start by performing an initial triage of the memory image to identify key system information, running processes, and network connections.
2.  **Guided Analysis**: I will guide you through the analysis process, suggesting relevant MemProcFS modules and commands based on your goals.
3.  **Forensic Workflows**: For common forensic tasks, I will follow structured workflows to ensure a thorough investigation. Refer to [forensic-workflows.md](forensic-workflows.md) for detailed procedures.
4.  **Python API Integration**: I can generate Python scripts using the MemProcFS API for automated analysis. See [python-api-guide.md](python-api-guide.md) for a complete guide.

## Additional Resources

-   For a complete reference of the MemProcFS virtual file system, see [filesystem-reference.md](filesystem-reference.md).
-   For practical examples and use cases, refer to [examples.md](examples.md).
-   If you encounter any issues, please consult the [troubleshooting.md](troubleshooting.md) guide.

## Getting Started

To begin, please provide me with the path to your memory dump file or specify the live memory acquisition method (e.g., `pmem`, `fpga`). For example:

> "Analyze the memory dump at `/mnt/dumps/suspicious.dmp`"

> "Start a live analysis on this machine using pmem."
