# MemProcFS Agent Skill - Installation and Setup Guide

## Quick Start

This guide will help you install and configure the MemProcFS Agent Skill for Claude Code.

## Prerequisites

Before installing the Skill, ensure you have:

1. **Claude Code** installed and running
2. **MemProcFS** installed on your system
3. **Python 3.7+** (for Python API support)
4. **pip** package manager (for installing the memprocfs Python package)

## Step 1: Install MemProcFS

### Windows

1. Download the latest MemProcFS release from [GitHub](https://github.com/ufrisk/MemProcFS/releases)
2. Install Dokany file system library (required for virtual file system mounting)
3. Extract MemProcFS to a location of your choice (e.g., \C:\Tools\MemProcFS\)
4. Add MemProcFS to your system PATH

### Linux

`ash
# Install dependencies
sudo apt-get update
sudo apt-get install libusb-1.0-0-dev fuse libfuse-dev

# Download and extract MemProcFS
wget https://github.com/ufrisk/MemProcFS/releases/download/v5.12/MemProcFS-5.12-linux.tar.gz
tar -xzf MemProcFS-5.12-linux.tar.gz
sudo mv MemProcFS /opt/
sudo ln -s /opt/MemProcFS/memprocfs /usr/local/bin/
`

### macOS

`ash
# Install macFuse (required for file system mounting)
brew install macfuse

# Download and extract MemProcFS
wget https://github.com/ufrisk/MemProcFS/releases/download/v5.12/MemProcFS-5.12-macos.tar.gz
tar -xzf MemProcFS-5.12-macos.tar.gz
sudo mv MemProcFS /opt/
sudo ln -s /opt/MemProcFS/memprocfs /usr/local/bin/
`

## Step 2: Install Python Package (Optional)

If you plan to use the Python API for automated analysis:

`ash
pip install memprocfs
`

Verify the installation:

`ash
python -c "import memprocfs; print(memprocfs.__version__)"
`

## Step 3: Load Memory Image

Use \memprocfs.exe\ to mount the memory dump file as a virtual file system for forensic analysis.

### Basic Usage

`ash
# Basic command format
memprocfs.exe -device <memory_image_path> -forensic 1

# Example: Load a Windows 10 x64 memory dump
memprocfs.exe -device c:\temp\win10x64-dump.raw -forensic 1
`

### Common Command Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| \-device\ | Path to the memory image file | \-device c:\temp\dump.raw\ |
| \-forensic 1\ | Enable forensic mode | \-forensic 1\ |
| \-mount\ | Specify mount drive letter (Default: M:) | \-mount N:\ |
| \-v\ | Show verbose output | \-v\ |
| \-pagefile\ | Specify page file path | \-pagefile c:\temp\pagefile.sys\ |

### Post-Loading Actions

Once the memory image is successfully loaded, MemProcFS maps the memory content as a virtual file system. You can perform forensic analysis by accessing the mounted drive (Default: M:):

`
M:\                           # Virtual file system root directory
├── proc\                     # Process information
│   ├── <PID>\               # Detailed information for each process
│   │   ├── handles.txt      # Process handles
│   │   ├── modules.txt      # Loaded modules
│   │   └── memory.txt       # Memory map
├── sys\                      # System information
│   ├── sysinfo.txt          # Basic system information
│   ├── net\                  # Network connections
│   └── users\               # User information
├── forensic\                 # Forensic analysis modules
│   ├── findevil\            # Malware detection
│   ├── timeline\            # Event timeline
│   ├── yara\                # YARA scanning
│   └── ntfs\                # NTFS file system analysis
└── registry\                 # Registry hives
`

### Quick Forensic Examples

`ash
# View system information
type M:\sys\sysinfo.txt

# List all processes
dir M:\proc

# View network connections
type M:\sys\net\netstat.txt

# Check for malicious activity
dir M:\forensic\findevil
`

## Step 4: Install the Skill

1. **Locate the Skill Directory**

   Find your Claude Code Skill directory:
   
   - **Windows**: \C:\Users\<YourUsername>\.claude\skills\\\
   - **Linux/macOS**: \~/.claude/skills/\

2. **Copy the Skill**

   Copy the entire \memprocfs-analysis\ directory to the Skill directory:

   `ash
   # Linux/macOS
   cp -r memprocfs-analysis ~/.claude/skills/

   # Windows (PowerShell)
   Copy-Item -Recurse memprocfs-analysis \C:\Users\woyouyuyuzheng\.claude\skills\
   `

3. **Verify Installation**

   Check that the directory structure is correct:

   `
   ~/.claude/skills/memprocfs-analysis/
   ├── SKILL.md
   ├── README.md
   ├── python-api-guide.md
   ├── forensic-workflows.md
   ├── filesystem-reference.md
   ├── examples.md
   ├── troubleshooting.md
   └── scripts/
   `

## Step 5: Restart Claude Code

Exit and restart Claude Code to load the new Skill. The Skill should now be available for use.

## Verification

To verify the Skill is loaded correctly:

1. Open Claude Code
2. Ask: "What Skills are available?"
3. Look for \memprocfs-assistant\ in the list

## Troubleshooting

### Skill Not Loading

- Ensure the directory structure is correct
- Check that all \.md\ files are present
- Restart Claude Code
- Check Claude Code logs for errors

### MemProcFS Not Found

- Verify MemProcFS is installed and in your PATH
- On Windows, ensure Dokany is installed
- On Linux/macOS, ensure FUSE/macFuse is installed

### Python API Issues

- Verify Python 3.7+ is installed
- Run \pip install --upgrade memprocfs\
- Check that the memprocfs package is accessible from your Python environment

## Next Steps

1. Read the [README.md](README.md) for an overview of the Skill
2. Review [python-api-guide.md](python-api-guide.md) for API documentation
3. Check [forensic-workflows.md](forensic-workflows.md) for common workflows
4. Explore [examples.md](examples.md) for code samples
