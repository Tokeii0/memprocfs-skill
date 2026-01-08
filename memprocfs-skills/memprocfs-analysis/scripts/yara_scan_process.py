'''
This script performs a YARA scan on a specified process.

Usage: python yara_scan_process.py <process_name_or_pid> <yara_rule_file> [vmm_args...]
'''

import memprocfs
import sys

def yara_scan_process(proc_identifier, rule_file, vmm_args):
    '''
    Performs a YARA scan on a process's memory.

    :param proc_identifier: The name or PID of the process to scan.
    :param rule_file: Path to the YARA rule file.
    :param vmm_args: A list of arguments to initialize MemProcFS.
    '''
    try:
        # Read YARA rules
        with open(rule_file, 'r') as f:
            yara_rules = f.read()

        # Initialize VMM
        vmm = memprocfs.Vmm(vmm_args)
        print(f"MemProcFS initialized with args: {vmm_args}")

        # Find the process
        try:
            pid = int(proc_identifier)
            process = vmm.process(pid)
        except ValueError:
            process = vmm.process(proc_identifier)

        if not process:
            print(f"Error: Process '{proc_identifier}' not found.")
            return

        print(f"Scanning process: {process.name} (PID: {process.pid}) with rules from {rule_file}")

        # Perform YARA scan
        matches = process.search.yara(yara_rules)

        if not matches:
            print("No YARA matches found.")
            return

        print("\n--- YARA Matches Found ---")
        for match in matches:
            print(f"Rule: {match['rule']}, Offset: {match['offset']:#x}")
            # Print the matched data in a readable format
            try:
                print(f"  Matched String: {match['data'].decode('utf-8', errors='ignore')}")
            except:
                print(f"  Matched Data (hex): {match['data'].hex()}")

    except FileNotFoundError:
        print(f"Error: YARA rule file not found at {rule_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python yara_scan_process.py <process_name_or_pid> <yara_rule_file> [vmm_args...]")
        print("Example: python yara_scan_process.py lsass.exe suspicious.yara -device memory.dmp")
        sys.exit(1)

    process_id = sys.argv[1]
    yara_file = sys.argv[2]
    vmm_arguments = sys.argv[3:]

    if not vmm_arguments:
        print("Error: VMM arguments are required (e.g., '-device <path_to_dump>').")
        sys.exit(1)

    yara_scan_process(process_id, yara_file, vmm_arguments)
