
'"""
This script lists all open handles for a specified process.

Usage: python list_process_handles.py <process_name_or_pid> [vmm_args...]
"""'

import memprocfs
import sys

def list_process_handles(proc_identifier, vmm_args):
    """
    Lists all open handles for a given process.

    :param proc_identifier: The name or PID of the process.
    :param vmm_args: A list of arguments to initialize MemProcFS.
    """
    try:
        vmm = memprocfs.Vmm(vmm_args)
        print(f"MemProcFS initialized with args: {vmm_args}")

        try:
            pid = int(proc_identifier)
            process = vmm.process(pid)
        except ValueError:
            process = vmm.process(proc_identifier)

        if not process:
            print(f"Error: Process '{proc_identifier}' not found.")
            return

        print(f"--- Handles for {process.name} (PID: {process.pid}) ---")

        handles = process.handle_all()
        if not handles:
            print("No open handles found.")
            return

        for handle in handles:
            print(f"- Handle: {handle.handle_value:#x}, Type: {handle.type}, Name: {handle.name}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python list_process_handles.py <process_name_or_pid> [vmm_args...]")
        print("Example: python list_process_handles.py explorer.exe -device memory.dmp")
        sys.exit(1)

    process_id = sys.argv[1]
    vmm_arguments = sys.argv[2:]

    if not vmm_arguments:
        print("Error: VMM arguments are required (e.g., '-device <path_to_dump>').")
        sys.exit(1)

    list_process_handles(process_id, vmm_arguments)
