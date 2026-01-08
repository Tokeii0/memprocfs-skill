'''
此脚本将指定进程的内存转储到文件以供离线分析。

用法: python dump_process_memory.py <进程名或PID> <输出文件> [vmm_args...]
'''

import memprocfs
import sys

def dump_process_memory(proc_identifier, output_file, vmm_args):
    '''
    将进程的虚拟内存转储到文件。

    :param proc_identifier: 要转储的进程的名称或 PID。
    :param output_file: 保存内存转储的路径。
    :param vmm_args: 用于初始化 MemProcFS 的参数列表。
    '''
    try:
        # 初始化 VMM 实例
        vmm = memprocfs.Vmm(vmm_args)
        print(f"MemProcFS 已使用参数初始化: {vmm_args}")

        # 识别进程
        try:
            pid = int(proc_identifier)
            process = vmm.process(pid)
        except ValueError:
            process = vmm.process(proc_identifier)

        if not process:
            print(f"错误: 未找到进程 '{proc_identifier}'。")
            return

        print(f"找到进程: {process.name} (PID: {process.pid})")

        # 读取整个进程内存
        # 这会将虚拟内存作为单个连续块读取，类似于 vmemd 文件。
        print("正在读取进程内存... 这可能需要一些时间。")
        mem_data = process.memory.read(0, process.get_map_vmem().get('size', 0))

        if not mem_data:
            print("错误: 读取进程内存失败。")
            return

        # 将内存写入输出文件
        with open(output_file, 'wb') as f:
            f.write(mem_data)
        
        print(f"已成功将 {process.name} 的 {len(mem_data)} 字节内存转储到 {output_file}")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python dump_process_memory.py <进程名或PID> <输出文件> [vmm_args...]")
        print("示例: python dump_process_memory.py lsass.exe lsass.dmp -device memory.dmp")
        sys.exit(1)

    process_id = sys.argv[1]
    out_file = sys.argv[2]
    vmm_arguments = sys.argv[3:]

    if not vmm_arguments:
        print("错误: 需要 VMM 参数 (例如, '-device <转储路径>')。")
        sys.exit(1)

    dump_process_memory(process_id, out_file, vmm_arguments)
