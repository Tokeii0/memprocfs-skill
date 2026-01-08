
'""" 
此脚本列出指定进程的所有打开句柄。

用法: python list_process_handles.py <进程名或PID> [vmm_args...]
"""'

import memprocfs
import sys

def list_process_handles(proc_identifier, vmm_args):
    """
    列出给定进程的所有打开句柄。

    :param proc_identifier: 进程的名称或 PID。
    :param vmm_args: 用于初始化 MemProcFS 的参数列表。
    """
    try:
        vmm = memprocfs.Vmm(vmm_args)
        print(f"MemProcFS 已使用参数初始化: {vmm_args}")

        try:
            pid = int(proc_identifier)
            process = vmm.process(pid)
        except ValueError:
            process = vmm.process(proc_identifier)

        if not process:
            print(f"错误: 未找到进程 '{proc_identifier}'。")
            return

        print(f"--- {process.name} (PID: {process.pid}) 的句柄 ---")

        handles = process.handle_all()
        if not handles:
            print("未找到打开的句柄。")
            return

        for handle in handles:
            print(f"- 句柄: {handle.handle_value:#x}, 类型: {handle.type}, 名称: {handle.name}")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python list_process_handles.py <进程名或PID> [vmm_args...]")
        print("示例: python list_process_handles.py explorer.exe -device memory.dmp")
        sys.exit(1)

    process_id = sys.argv[1]
    vmm_arguments = sys.argv[2:]

    if not vmm_arguments:
        print("错误: 需要 VMM 参数 (例如, '-device <转储路径>')。")
        sys.exit(1)

    list_process_handles(process_id, vmm_arguments)
