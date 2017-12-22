#/usr/bin/env python3
# -*-coding: utf-8 -*-

import os
import json
from collections import OrderedDict

def load_from_path(path):
    final_cfg = {}
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith('.json'):
                cfg = load_from_json(os.path.join(root, filename), keep_order=True)
                if cfg is not None:
                    final_cfg.update(cfg)
                else:
                    raise Exception('[load_from_path] Error: json %s format error' % filename)
    return final_cfg


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


def rm_repeat_lst(src_lst):
    new_lst = []
    temp = []
    if isinstance(src_lst, list):
        for i in src_lst:
            if isinstance(i, list):# 处理多关键词是否有相同的
                temp.append(set(i))
            else:
                if i not in new_lst:
                    new_lst.append(i)
        set_lst = []
        for j in temp:
            if j not in set_lst:
                set_lst.append(j)
        new_sub_lst = []
        for k in set_lst:
            new_sub_lst += list(k)

        if new_sub_lst:
            new_lst.append(new_sub_lst)
    return new_lst


def dump_to_jsonfile(jsondata, filename):
    if jsondata:
        with open(filename, 'w', encoding='utf-8') as fout:
            json.dump(jsondata, fout, sort_keys=True, ensure_ascii=False, indent=4)


def rm_repeat_wds(wds_dct):
    ciku_dct = wds_dct
    new_dct = {}
    for key, val in ciku_dct.items():
        new_dct[key] = rm_repeat_lst(val)

    return new_dct


def read_all_temp_sim(path):
    all_sim_paths = []
    dir_path = '/home/xupeng/workspace/'
    key_name_txt = os.path.join(dir_path, 'key_name.txt')

    try:
        with open(key_name_txt, encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                # /home/xupeng/workspace/cfg_repos/360jt/cfgs/360jt/sim_dict
                sim_path = dir_path + 'cfg_repos/' + line + '/cfgs/' + line + '/sim_dict/sim.txt'
                all_sim_paths += [str(sim_path).replace('\n', '')]

    except Exception as e:
        print(str(e))
    out_put = 'sim_all.txt'
    for sim_path in all_sim_paths:
        if not os.path.isfile(sim_path):
            continue
        with open(sim_path, encoding='utf-8') as sf:
            lines = sf.readlines()
            for line in lines:
                wf = open(out_put, 'a')
                wf.write(line + '\n')
                wf.close()
    print(all_sim_paths)
    pass


def main():
    path = ''
    read_all_temp_sim(path)
    """
    json_path = '/home/xupeng/Desktop/test/ciku/ciku'
    ciku_dct = load_from_path(json_path)
    new_dct = rm_repeat_wds(ciku_dct)
    filename = os.path.join(json_path, 'new_wds.json')
    # all data_dict
    dump_to_jsonfile(new_dct, filename)
    # sperate single data_dict
    sub_dict = {}
    for key, val in new_dct.items():
        temp = 'single/' + str(key) + '.json'
        filename = os.path.join(json_path, temp)
        sub_dict[key] = val
        dump_to_jsonfile(sub_dict, filename)
        sub_dict = {}"""


if __name__ == '__main__':
    main()
