# MemProcFS Agent Skill

## Overview

**MemProcFS Agent Skill** is an agent skill designed for Claude Code to enhance its capabilities in memory analysis and digital forensics. This skill integrates Claude with the powerful MemProcFS tool, enabling users to perform deep memory dump analysis, live memory investigation, and forensic workflows.

## What is MemProcFS?

**MemProcFS** is an open-source tool that provides a convenient way to view physical memory as files in a virtual file system. It supports various memory acquisition methods, including memory dump files, live memory (via WinPMEM or DumpIt), virtual machine memory, and remote memory acquisition (via LeechAgent).

### Key Features

-   **Virtual File System Interface**: Access memory content and artifacts through standard file operations.
-   **Multi-Platform Support**: Supports Windows, Linux, macOS, and ARM64 architectures.
-   **Rich API**: Provides C/C++, C#, Java, Rust, and Python interfaces.
-   **Forensic Modules**: Includes features like YARA scanning, file recovery, event log parsing, and more.
-   **Plugin Architecture**: Supports custom extensions via C, Rust, and Python plugins.

## Skill File Structure

`
memprocfs-analysis/
├── SKILL.md                      # Skill metadata and main instructions
├── forensic-workflows.md         # Guides for common forensic workflows
├── python-api-guide.md           # Detailed guide for Python API usage
├── filesystem-reference.md       # Reference for virtual file system structure
├── examples.md                   # Practical code examples and use cases
├── troubleshooting.md            # Common issues and solutions
└── scripts/                      # Directory for optional helper scripts
`

## Installation and Usage

### 1. Install the Skill

Copy the \memprocfs-analysis\ directory to the Claude Code Skill directory:

**On Windows:**
`
C:\Users\<YourUsername>\.claude\skills\memprocfs-analysis\
`

**On Linux/macOS:**
`
~/.claude/skills/memprocfs-analysis/
`

### 2. Install MemProcFS

Download the latest version from the [MemProcFS GitHub Releases page](https://github.com/ufrisk/MemProcFS/releases) based on your operating system.

**Windows:**
- Download and install the Dokany file system library (for mounting the virtual file system).
- Download MemProcFS binaries.

**Linux:**
`ash
sudo apt-get install libusb-1.0 fuse
# Download MemProcFS from the releases page
`

**macOS:**
- Download and install macFuse.
- Download MemProcFS from the releases page.

### 3. Install Python Package (Optional)

If you plan to use the Python API for automated analysis:

`ash
pip install memprocfs
`

### 4. Load Memory Image

Use \memprocfs.exe\ to load the memory dump file and mount it as a virtual file system:

**Basic Command Format:**
`ash
memprocfs.exe -device <memory_image_path> -forensic 1
`

**Examples:**
`ash
# Load a Windows 10 x64 memory dump
memprocfs.exe -device c:\temp\win10x64-dump.raw -forensic 1

# Load memory dump and specify mount point
memprocfs.exe -device c:\temp\win10x64-dump.raw -forensic 1 -mount M:
`

**Parameter Explanation:**
- \-device\: Specifies the path to the memory image file (supports .raw, .dmp, .mem, etc.).
- \-forensic 1\: Enables forensic mode, generating forensic-related analysis data.
- \-mount\: (Optional) Specifies the drive letter for the virtual file system mount, default is \M:\.

**After Loading:**

Once the memory image is successfully loaded, you can access the mounted virtual file system for forensic analysis:

`
M:\                           # Virtual file system root
├── proc\                     # Process information directory
├── sys\                      # System information directory
│   ├── sysinfo.txt           # Basic system information
│   └── net\                  # Network connection information
├── forensic\                 # Forensic analysis modules
│   ├── findevil\             # Malware detection
│   ├── timeline\             # Event timeline
│   └── yara\                 # YARA scan results
└── registry\                 # Registry information
`

You can read these directories and files just like accessing normal files to perform memory forensic analysis.

### 5. Restart Claude Code

Exit and restart Claude Code to load the new Skill.

## Usage Examples

### Initializing the Skill

In Claude Code, you can start the Skill in the following ways:

> "Analyze the memory dump file located at \/path/to/memory.dmp\"

> "Conduct a forensic investigation on this memory image"

> "Use MemProcFS to identify malware in this memory dump"

### The Skill Will Guide You Through

1.  **Initial Triage**: Identify key system information, running processes, and network connections.
2.  **Guided Analysis**: Suggest relevant MemProcFS modules and commands based on your goals.
3.  **Forensic Workflows**: Follow structured workflows for common forensic tasks.
4.  **Python Script Generation**: Generate automated analysis scripts.

## Documentation Navigation

| Document | Purpose |
|----------|---------|
| [forensic-workflows.md](forensic-workflows.md) | Structured workflows for common forensic tasks |
| [python-api-guide.md](python-api-guide.md) | Complete guide for MemProcFS Python API |
| [filesystem-reference.md](filesystem-reference.md) | Reference for virtual file system structure and modules |
| [examples.md](examples.md) | Practical code examples and usage scenarios |
| [troubleshooting.md](troubleshooting.md) | Common issues and solutions |

## Common Workflows

### Workflow 1: Rapid System Triage

1.  Check system information (\sys/sysinfo\)
2.  List all running processes (\proc\)
3.  Analyze network connections (\sys/net\)
4.  Identify logged-in users (\sys/users\)

### Workflow 2: Malware Detection

1.  Run FindEvil scan (\orensic/findevil\)
2.  Execute YARA scan (\orensic/yara\)
3.  Analyze memory of suspicious processes
4.  Dump executable files of suspicious processes for static analysis

### Workflow 3: File and Data Recovery

1.  Analyze NTFS metadata (\orensic/ntfs\)
2.  Check Prefetch files (\orensic/prefetch\)
3.  Generate system activity timeline (\orensic/timeline\)
4.  Recover web browsing artifacts (\orensic/web\)

## Troubleshooting

If the Skill does not trigger or you encounter errors, please refer to [troubleshooting.md](troubleshooting.md) for detailed solutions.

## License

MemProcFS is released under the GNU Affero General Public License v3.0. This Skill is supplementary documentation for MemProcFS.

## Resources

-   [MemProcFS GitHub Project](https://github.com/ufrisk/MemProcFS)
-   [MemProcFS Official Wiki](https://github.com/ufrisk/MemProcFS/wiki)
-   [LeechCore Project](https://github.com/ufrisk/LeechCore)
-   [PCILeech Project](https://github.com/ufrisk/pcileech)

## Support and Feedback

For issues or suggestions, please visit [MemProcFS GitHub Issues](https://github.com/ufrisk/MemProcFS/issues) or join the [PCILeech/MemProcFS Discord Community](https://discord.gg/pcileech).
