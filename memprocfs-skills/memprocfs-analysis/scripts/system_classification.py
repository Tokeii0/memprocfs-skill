'''
This script performs an initial system classification by collecting key information
about the memory image, including system info, running processes, network connections,
and user accounts.

Usage: python system_classification.py -device <memory_source> [--output <report_file>]
'''

import memprocfs
import sys
import json
from datetime import datetime

def system_classification(vmm_args, output_file=None):
    '''
    Performs comprehensive system classification.

    :param vmm_args: A list of arguments to initialize MemProcFS.
    :param output_file: Optional path to save the classification report as JSON.
    '''
    try:
        vmm = memprocfs.Vmm(vmm_args)
        print(f"MemProcFS initialized with args: {vmm_args}")

        classification_report = {
            'timestamp': datetime.now().isoformat(),
            'system_info': {},
            'processes': [],
            'network_connections': [],
            'users': []
        }

        # 1. System Information
        print("\n[*] Collecting system information...")
        try:
            sysinfo_path = '/sys/sysinfo'
            sysinfo_data = vmm.vfs.readfile(sysinfo_path)
            classification_report['system_info'] = {
                'raw': sysinfo_data.decode('utf-8', errors='ignore')
            }
            print(f"    System info collected from {sysinfo_path}")
        except Exception as e:
            print(f"    Warning: Could not collect system info: {e}")

        # 2. Running Processes
        print("\n[*] Collecting running processes...")
        try:
            for process in vmm.process_all():
                process_info = {
                    'pid': process.pid,
                    'name': process.name,
                    'path': process.path,
                    'ppid': process.pid_parent
                }
                classification_report['processes'].append(process_info)
            print(f"    Found {len(classification_report['processes'])} running processes")
        except Exception as e:
            print(f"    Warning: Could not collect process list: {e}")

        # 3. Network Connections
        print("\n[*] Collecting network connections...")
        try:
            net_path = '/sys/net'
            net_data = vmm.vfs.readfile(net_path)
            classification_report['network_connections'] = {
                'raw': net_data.decode('utf-8', errors='ignore')[:1000]  # First 1000 chars
            }
            print(f"    Network info collected from {net_path}")
        except Exception as e:
            print(f"    Warning: Could not collect network info: {e}")

        # 4. User Accounts
        print("\n[*] Collecting user accounts...")
        try:
            users_path = '/sys/users'
            users_data = vmm.vfs.readfile(users_path)
            classification_report['users'] = {
                'raw': users_data.decode('utf-8', errors='ignore')[:1000]
            }
            print(f"    User info collected from {users_path}")
        except Exception as e:
            print(f"    Warning: Could not collect user info: {e}")

        # Print Summary
        print("\n" + "="*60)
        print("SYSTEM CLASSIFICATION SUMMARY")
        print("="*60)
        print(f"Timestamp: {classification_report['timestamp']}")
        print(f"Running Processes: {len(classification_report['processes'])}")
        print(f"Network Connections: {'Present' if classification_report['network_connections'] else 'Not available'}")
        print(f"User Accounts: {'Present' if classification_report['users'] else 'Not available'}")

        # Print top processes
        print("\nTop Processes (by PID):")
        for proc in sorted(classification_report['processes'], key=lambda x: x['pid'])[:10]:
            print(f"  - {proc['name']} (PID: {proc['pid']}, PPID: {proc['ppid']})")

        # Save report if requested
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(classification_report, f, indent=2)
            print(f"\nReport saved to: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python system_classification.py -device <memory_source> [--output <report_file>]")
        print("Example: python system_classification.py -device memory.dmp --output classification.json")
        sys.exit(1)

    vmm_arguments = []
    output_file = None

    # Parse arguments
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        else:
            vmm_arguments.append(sys.argv[i])
            i += 1

    if not vmm_arguments:
        print("Error: VMM arguments are required (e.g., '-device <path_to_dump>').")
        sys.exit(1)

    system_classification(vmm_arguments, output_file)
