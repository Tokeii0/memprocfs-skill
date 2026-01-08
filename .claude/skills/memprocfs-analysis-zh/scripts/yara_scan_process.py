'''
此脚本对指定进程执行 YARA 扫描。

用法: python yara_scan_process.py <进程名或PID> <yara_rule_file> [vmm_args...]
'''

import memprocfs
import sys

def yara_scan_process(proc_identifier, rule_file, vmm_args):
    '''
    对进程内存执行 YARA 扫描。

    :param proc_identifier: 要扫描的进程的名称或 PID。
    :param rule_file: YARA 规则文件的路径。
    :param vmm_args: 用于初始化 MemProcFS 的参数列表。
    '''
    try:
        # 读取 YARA 规则
        with open(rule_file, 'r') as f:
            yara_rules = f.read()

        # 初始化 VMM
        vmm = memprocfs.Vmm(vmm_args)
        print(f"MemProcFS 已使用参数初始化: {vmm_args}")

        # 查找进程
        try:
            pid = int(proc_identifier)
            process = vmm.process(pid)
        except ValueError:
            process = vmm.process(proc_identifier)

        if not process:
            print(f"错误: 未找到进程 '{proc_identifier}'。")
            return

        print(f"正在使用 {rule_file} 中的规则扫描进程: {process.name} (PID: {process.pid})")

        # 执行 YARA 扫描
        matches = process.search.yara(yara_rules)

        if not matches:
            print("未找到 YARA 匹配项。")
            return

        print("\n--- 发现 YARA 匹配项 ---")
        for match in matches:
            print(f"规则: {match['rule']}, 偏移量: {match['offset']:#x}")
            # 以可读格式打印匹配的数据
            try:
                print(f"  匹配的字符串: {match['data'].decode('utf-8', errors='ignore')}")
            except:
                print(f"  匹配的数据 (十六进制): {match['data'].hex()}")

    except FileNotFoundError:
        print(f"错误: 在 {rule_file} 未找到 YARA 规则文件")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python yara_scan_process.py <进程名或PID> <yara_rule_file> [vmm_args...]")
        print("示例: python yara_scan_process.py lsass.exe suspicious.yara -device memory.dmp")
        sys.exit(1)

    process_id = sys.argv[1]
    yara_file = sys.argv[2]
    vmm_arguments = sys.argv[3:]

    if not vmm_arguments:
        print("错误: 需要 VMM 参数 (例如, '-device <转储路径>')。")
        sys.exit(1)

    yara_scan_process(process_id, yara_file, vmm_arguments)
