#/usr/bin/env python3
# -*-coding: utf-8 -*-

import sys
import os
import json
from collections import OrderedDict
import pprint


BASE_CIKU = ['价格', '公司名称', '发信息', '多大', '拒绝', '机器人', '肯定', '问你个问题', '你太不专业了',
                 '公司地址', '否定', '怎么去你公司', '改天去你们公司看一下', '等一下', '贵姓', '骗子',
                 '你怎么知道我信息的', '公司规模', '在忙', '投诉', '有没有在听我说话', '考虑一下', '重复']
def load_from_json(js, keep_order=True):
    if os.path.exists(js):
        try:
            try:
                with open(js, encoding='utf-8') as f:
                    cfg = json.load(f, object_pairs_hook=OrderedDict if keep_order else None)
                return cfg
            except Exception as e:
                print("[load_from_json] Error: %s load json %s fail,trying to decrypt." % (e, js))
                """decrypter = Crypter()
                with open(js, 'rb') as f:
                    text = f.read()
                plaintext = decrypter.decrypt_string(text)
                if isinstance(plaintext, bytes):
                    plaintext = plaintext.decode('utf-8')
                return json.loads(plaintext)"""
                return None
        except Exception as e:
            print("[load_from_json] Error: %s  Error." % js)
            # traceback.print_exc()
            raise e
    else:
        print("[load_from_json] Error: %s  Error." % js)
        return {}


def ciku_parse(key_wd):
    all_ciku_dct = {}

    ciku_path = '/home/xupeng/workspace/cfg_repos/base_ciku/base_ciku'
    # ciku_path = '/Users/xupeng/cfg_repos/work/gjznhs/话术/关键词整理/sim_json_bak/base_ciku'
    for key in BASE_CIKU:
        key_json_name = str(key) + '/wds.json'
        key_json_path = os.path.join(ciku_path, key_json_name)
        json_data = load_from_json(key_json_path, False)
        for key_wds, key_val in json_data.items():
            if key_wds not in all_ciku_dct.keys():
                all_ciku_dct[key_wds] = [key_val]
            else:
                all_ciku_dct[key_wds] += list(key_val)
    """print key sim_list"""
    for key, val in all_ciku_dct.items():
        if key_wd in key:
            # print(all_ciku_dct[key])
            pprint.pprint(all_ciku_dct[key], indent=1, width=80, depth=100)


def get_input(info):
    return str(input(info))

def main():
    # key = sys.argv[1]
    print("base_ciku:", BASE_CIKU)
    info = 'please input you wanted key_words: '
    while 1:
        key_wds = get_input(info)
        ciku_parse(key_wds)



if __name__ == '__main__':
    main()
