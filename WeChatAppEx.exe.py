# HOOK微信小程序

import os
import sys
import frida
import psutil


def on_message(message, data):
    if message["type"] == 'send':
        print(message['payload'])
    elif message["type"] == 'error':
        print(message['stack'])


def main():
    version = sys.argv[1].lower()
    bit = sys.argv[2].lower()

    addressSource = ""
    addressSourceHeadFilePath = os.path.join(os.path.dirname(__file__), 'Core', 'AddressSource.head')
    addressSourceEndFilePath = os.path.join(os.path.dirname(__file__), 'Core', 'AddressSource.end')

    addressFilePath = os.path.join(os.path.dirname(__file__), 'Core', 'WeChatAppEx.exe', f'address_{version}_{bit}.json')
    hookFilePath = os.path.join(os.path.dirname(__file__), 'Core', 'WeChatAppEx.exe', 'hook.js')

    if os.path.exists(addressFilePath):
        with open(addressSourceHeadFilePath, 'r', encoding='utf-8') as f:
            addressSource += f.read()
        with open(addressFilePath, 'r', encoding='utf-8') as f:
            addressSource += f.read()
        with open(addressSourceEndFilePath, 'r', encoding='utf-8') as f:
            addressSource += f.read()
        with open(hookFilePath, 'r', encoding='utf-8') as f:
            addressSource += f.read()
    else:
        print(f'暂不支持 {version}_{bit} 的版本!')
        return
    print("HOOK文件组装成功!")

    device = frida.get_local_device()
    processes = device.enumerate_processes()
    pid = -1
    for p_ in processes:
        if p_.name == 'WeChatAppEx.exe':
            commandLine = ' '.join(psutil.Process(p_.pid).cmdline())
            if '--type=' not in commandLine:
                pid = p_.pid
    if pid == -1:
        print("WeChatAppEx.exe 主进程未找到!")
        return

    session = frida.attach(pid)
    script = session.create_script(addressSource)
    script.on('message', on_message)
    script.load()
    sys.stdin.read()


if __name__ == '__main__':
    # python WeChatAppEx.exe.py 8447 x64
    main()
