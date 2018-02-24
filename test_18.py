# /usr/bin/env python3
# -*-coding: utf-8 -*

import os
import test_13

def get_input(info):
    return str(input(info))


def wds2json(wds):
    sentence = wds
    if not sentence:
        print('error!!!!')
    key_dict = dict()
    seg_flags = [',', '，']
    seg_sentence = []
    new_sentence = []
    temp_sentence = sentence.split(seg_flags[0])
    for temp in temp_sentence:
        seg_sentence += temp.split(seg_flags[1])
    for i in seg_sentence:
        if i not in new_sentence:
            new_sentence.append(i)
    for i in new_sentence:
        print('"' + str(i).replace(' ','') +'",')


def mergesim(path):
    if not os.path.exists(path):
         print("invalid path")
    out_put = 'sim_all.txt'
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            with open(file_path, encoding='utf-8') as sf:
                lines = sf.readlines()
                for line in lines:
                    wf = open(out_put, 'a')
                    wf.write(line + '\n')
                    wf.close()
    pass

def main():
    info = "please input your wds:"
    """while 1:
        wds = get_input(info)
        wds2json(wds)"""
    sim_path = '/Users/xupeng/cfg_repos/work/gjznhs/教学/新框架编程说明/simciku'
    mergesim(sim_path)
    test_13.txt_convTo_json('sim_all.txt')



if __name__ == "__main__":
    main()