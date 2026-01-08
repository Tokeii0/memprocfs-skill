'''
This script dumps the memory of a specified process to a file for offline analysis.

Usage: python dump_process_memory.py <process_name_or_pid> <output_file> [vmm_args...]
'''

import memprocfs
import sys

def dump_process_memory(proc_identifier, output_file, vmm_args):
    '''
    Dumps the virtual memory of a process to a file.

    :param proc_identifier: The name or PID of the process to dump.
    :param output_file: The path to save the memory dump.
    :param vmm_args: A list of arguments to initialize MemProcFS.
    '''
    try:
        # Initialize the VMM instance
        vmm = memprocfs.Vmm(vmm_args)
        print(f"MemProcFS initialized with args: {vmm_args}")

        # Identify the process
        try:
            pid = int(proc_identifier)
            process = vmm.process(pid)
        except ValueError:
            process = vmm.process(proc_identifier)

        if not process:
            print(f"Error: Process '{proc_identifier}' not found.")
            return

        print(f"Found process: {process.name} (PID: {process.pid})")

        # Read the entire process memory
        # This reads the virtual memory as a single contiguous block, similar to vmemd file.
        print("Reading process memory... This may take a while.")
        mem_data = process.memory.read(0, process.get_map_vmem().get('size', 0))

        if not mem_data:
            print("Error: Failed to read process memory.")
            return

        # Write the memory to the output file
        with open(output_file, 'wb') as f:
            f.write(mem_data)
        
        print(f"Successfully dumped {len(mem_data)} bytes of memory for {process.name} to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python dump_process_memory.py <process_name_or_pid> <output_file> [vmm_args...]")
        print("Example: python dump_process_memory.py lsass.exe lsass.dmp -device memory.dmp")
        sys.exit(1)

    process_id = sys.argv[1]
    out_file = sys.argv[2]
    vmm_arguments = sys.argv[3:]

    if not vmm_arguments:
        print("Error: VMM arguments are required (e.g., '-device <path_to_dump>').")
        sys.exit(1)

    dump_process_memory(process_id, out_file, vmm_arguments)
