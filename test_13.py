#/usr/bin/env python3
# -*-coding: utf-8 -*-

import os
import json
from collections import OrderedDict
import pandas as pd

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


def json_convTo_csv(filename):
    data_dct = {}
    if filename.endswith('.json'):
        data_dct = load_from_json(filename, False)
    else:
        raise  Exception('bad json file!')

    csvfile = str(filename).replace('.json', '.csv')
    fcsv = open(csvfile, 'w', encoding='utf-8')
    for key, value in data_dct.items():
        new_value = '0.99' + ',' + ','.join(value)
        fcsv.write(new_value)
        new_value = ''
    fcsv.close()


def json_convTo_xls(filename, save_name):
    print("===================", save_name)
    data_dct = {}
    if filename.endswith('.json'):
        data_dct = load_from_json(filename, False)
    else:
        raise Exception('bad json file')

    xlsfile = str(filename).replace('.json', '.xls').replace('wds', save_name)
    fxls = pd.ExcelWriter(xlsfile)
    for key, value in data_dct.items():
        new_value = ['0.99'] + value
        # sheet_name = str(filename).split('/')[-1][:-5]
        sheet_name = str(save_name)
        pd.DataFrame(new_value).to_excel(fxls, sheet_name=sheet_name, index=False, header=False)
        new_value = []
    fxls.save()
    if os.path.isfile(xlsfile):
        os.system('cp %s /Users/xupeng/cfg_repos/work/gjznhs/话术/关键词整理/sim_json_bak/xls/' %(xlsfile))


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


def read_all_general_json(path):
    all_paths = []
    dir_path = '/home/xupeng/workspace'
    key_name_txt = os.path.join(dir_path, 'key_name.txt')

    try:
        with open(key_name_txt, encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = str(line).replace('\n', '')
                # path = os.path.join(dir_path, 'cfg_repos', line, 'cfgs', line, '/new_domain_cfg/一般问题.json')
                path = str(dir_path) + '/cfg_repos/' + str(line) + '/cfgs/' + str(line) + '/new_domain_cfg/一般问题.json'
                if os.path.exists(path):
                    all_paths += [str(path).replace('\n', '')]
    except Exception as e:
        print(str(e))
    out_put = 'general_all.txt'
    for sim_path in all_paths:
        if not os.path.isfile(sim_path):
            continue
        wf = open(out_put, 'a')
        wf.write(sim_path + '\n')
        wf.close()
        """with open(sim_path, encoding='utf-8') as sf:
            lines = sf.readlines()
            for line in lines:
                wf = open(out_put, 'a')
                wf.write(line + '\n')
                wf.close()"""
    return all_paths
    print('read general json end!')


def merge_general_json(paths):
    if not paths:
        print('bad path')
        return None
    merged_dct = {}
    ignore_keys = ['positive', 'negative']
    count = 0
    new_dct = {}
    for path in paths:
        if os.path.isfile(path):
            js_dct = load_from_json(path)
            special_dct = js_dct.get('一般问题').get('branch')
            # print(special_dct)
            for key, value in special_dct.items():
                if key not in ignore_keys:
                    new_key ='special_' + str(count)
                    new_dct[new_key] = value.get('keys')
                    count += 1
    # print(new_dct)
    dump_to_jsonfile(new_dct, 'all_general.json')
    pass


def txt_convTo_json(path):
    domain_dct = {}
    filename = path.split('/')[-1]
    if filename.endswith('.txt'):
        with open(path, encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if ":" not in line:
                    continue
                print(line)
                key, val = line.strip('\n').split(':')
                if key not in domain_dct.keys():
                    domain_dct[key] = val.split(' ')
                else:
                    domain_dct[key] += val.split(' ')
                # print(domain_dct)
    else:
        raise Exception('Bad txt!')
    jsonpath = str(path).replace('sim_txt', 'sim_json')
    jsonname = jsonpath.replace('.txt', '.json')
    new_dct = rm_repeat_wds(domain_dct)
    dump_to_jsonfile(new_dct, jsonname)


def json_convTo_simtxt(path, save_name):
    data_dct = {}
    filename = path
    if filename.endswith('.json'):
        data_dct = load_from_json(filename, False)
    else:
        raise Exception('bad json file')
    sim_txt = str(path).replace('.json', '.txt')
    with open(sim_txt, 'w', encoding='utf-8') as f:
        for key, val in data_dct.items():
            pass

def json_merge(path):
    all_dct = {}
    all_dct_name = os.path.join(path, 'ciku.json')

    for root, dirs, filename in os.walk(path):
        for dir in dirs:
            sub_path = os.path.join(path, dir)
            json_path = os.path.join(sub_path, 'wds.json')
            json_data = open(json_path, encoding='utf-8')
            json_dct = json.load(json_data)
            for key, val in json_dct.items():
                if key in all_dct.keys():
                    all_dct[key] += val
                else:
                    all_dct[key] = val
    dump_to_jsonfile(all_dct, all_dct_name)



def main():
    """DIR_PATH = '/Users/xupeng/cfg_repos/work/gjznhs/话术/关键词整理/sim_json_bak/base_ciku'
    for parent, dirnames, filenames in os.walk(DIR_PATH):
        for dirname in dirnames:
            foldername = os.path.join(parent, dirname)
            json_path = os.path.join(foldername, 'wds.json')
            json_convTo_xls(json_path, dirname)"""

    # json_convTo_csv(path)
    # txt_convTo_json(path)

    # read_all_temp_sim(path)
    path = ''
    json_paths = read_all_general_json(path)
    merge_general_json(json_paths)
    """
    for root, dirs, filename in os.walk(DIR_PATH):
        for dir in dirs:
            json_path = os.path.join(DIR_PATH, dir)
            ciku_dct = load_from_path(json_path)
            new_dct = rm_repeat_wds(ciku_dct)
            filename = os.path.join(json_path, 'wds.json')"""
            # all data_dict
            # dump_to_jsonfile(new_dct, filename)
    # sperate single data_dict
    """
    sub_dict = {}
    for key, val in new_dct.items():
        temp = 'single/' + str(key) + '.json'
        filename = os.path.join(json_path, temp)
        sub_dict[key] = val
        dump_to_jsonfile(sub_dict, filename)
        sub_dict = {}"""


if __name__ == '__main__':
    main()
