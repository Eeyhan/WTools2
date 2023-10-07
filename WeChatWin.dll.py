
import os
import sys
import json
import traceback


def main():
    version = sys.argv[1].lower()
    bit = sys.argv[2].lower()
    exePath = sys.argv[3].lower()

    if os.path.exists(os.path.join(exePath, 'WeChatWin_old.dll')):
        print('已经是替换后的WeChatWin.dll! 请勿重复运行')
        return

    addressFilePath = os.path.join(os.path.dirname(__file__), 'Core', 'WeChatWin.dll',  f'address_{version}_{bit}.json')

    if os.path.exists(addressFilePath):
        address = json.load(open(addressFilePath, 'r', encoding='utf-8'))
    else:
        print(f'暂不支持 {version}_{bit} 的版本!')
        return

    try:
        address['XwebEnableInspect'] = int(address['XwebEnableInspect'], 16) + 1
        with open(os.path.join(exePath, 'WeChatWin.dll'), 'rb') as f:
            WeChatWin = f.read()
        with open(os.path.join(exePath, 'WeChatWin_old.dll'), 'wb') as f:
            f.write(WeChatWin)
        print("WeChatWin.dll已备份!", os.path.join(exePath, "WeChatWin_old.dll"))
        with open(os.path.join(exePath, 'WeChatWin.dll'), 'wb') as f:
            f.write(WeChatWin[: address['XwebEnableInspect']] + bytes([0x85]) + WeChatWin[address['XwebEnableInspect'] + 1:])
        print("完成覆盖!")
    except:
        print(traceback.format_exc())


if __name__ == '__main__':
    # python WeChatWin.dll.py 3.9.7.29 x64 "C:/Program Files (x86)/Tencent/WeChat/[3.9.7.29]"
    main()
