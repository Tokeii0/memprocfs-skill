'''
此脚本通过收集关于内存镜像的关键信息来执行初始系统分类，
包括系统信息、运行进程、网络连接和用户帐户。

用法: python system_classification.py -device <内存源> [--output <报告文件>]
'''

import memprocfs
import sys
import json
from datetime import datetime

def system_classification(vmm_args, output_file=None):
    '''
    执行全面的系统分类。

    :param vmm_args: 用于初始化 MemProcFS 的参数列表。
    :param output_file: 可选的路径以将分类报告保存为 JSON。
    '''
    try:
        vmm = memprocfs.Vmm(vmm_args)
        print(f"MemProcFS 已使用参数初始化: {vmm_args}")

        classification_report = {
            'timestamp': datetime.now().isoformat(),
            'system_info': {},
            'processes': [],
            'network_connections': [],
            'users': []
        }

        # 1. 系统信息
        print("\n[*] 正在收集系统信息...")
        try:
            sysinfo_path = '/sys/sysinfo'
            sysinfo_data = vmm.vfs.readfile(sysinfo_path)
            classification_report['system_info'] = {
                'raw': sysinfo_data.decode('utf-8', errors='ignore')
            }
            print(f"    从 {sysinfo_path} 收集的系统信息")
        except Exception as e:
            print(f"    警告: 无法收集系统信息: {e}")

        # 2. 运行进程
        print("\n[*] 正在收集运行进程...")
        try:
            for process in vmm.process_all():
                process_info = {
                    'pid': process.pid,
                    'name': process.name,
                    'path': process.path,
                    'ppid': process.pid_parent
                }
                classification_report['processes'].append(process_info)
            print(f"    找到 {len(classification_report['processes'])} 个运行进程")
        except Exception as e:
            print(f"    警告: 无法收集进程列表: {e}")

        # 3. 网络连接
        print("\n[*] 正在收集网络连接...")
        try:
            net_path = '/sys/net'
            net_data = vmm.vfs.readfile(net_path)
            classification_report['network_connections'] = {
                'raw': net_data.decode('utf-8', errors='ignore')[:1000]  # 前 1000 个字符
            }
            print(f"    从 {net_path} 收集的网络信息")
        except Exception as e:
            print(f"    警告: 无法收集网络信息: {e}")

        # 4. 用户帐户
        print("\n[*] 正在收集用户帐户...")
        try:
            users_path = '/sys/users'
            users_data = vmm.vfs.readfile(users_path)
            classification_report['users'] = {
                'raw': users_data.decode('utf-8', errors='ignore')[:1000]
            }
            print(f"    从 {users_path} 收集的用户信息")
        except Exception as e:
            print(f"    警告: 无法收集用户信息: {e}")

        # 打印摘要
        print("\n" + "="*60)
        print("系统分类摘要")
        print("="*60)
        print(f"时间戳: {classification_report['timestamp']}")
        print(f"运行进程: {len(classification_report['processes'])}")
        print(f"网络连接: {'存在' if classification_report['network_connections'] else '不可用'}")
        print(f"用户帐户: {'存在' if classification_report['users'] else '不可用'}")

        # 打印顶部进程
        print("\n顶部进程 (按 PID):")
        for proc in sorted(classification_report['processes'], key=lambda x: x['pid'])[:10]:
            print(f"  - {proc['name']} (PID: {proc['pid']}, PPID: {proc['ppid']})")

        # 如果请求，保存报告
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(classification_report, f, indent=2, ensure_ascii=False)
            print(f"\n报告已保存到: {output_file}")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python system_classification.py -device <内存源> [--output <报告文件>]")
        print("示例: python system_classification.py -device memory.dmp --output classification.json")
        sys.exit(1)

    vmm_arguments = []
    output_file = None

    # 解析参数
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        else:
            vmm_arguments.append(sys.argv[i])
            i += 1

    if not vmm_arguments:
        print("错误: 需要 VMM 参数 (例如, '-device <转储路径>')。")
        sys.exit(1)

    system_classification(vmm_arguments, output_file)
