#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
import json
import time
import requests
import argparse
from des_file_python3 import des_encode


def setup_parser():
    parser = argparse.ArgumentParser(description='Test a machine-request system.')
    parser.add_argument('-c', '--cfg', required=True, help='the path of cfg folder')
    parser.add_argument('-o', '--out', required=True,help='the path of output cfg folder')
    # python3 auto_encrypt_keyWord.py -c ../domain/cfg -o ../domain/cfg_psc
    return parser
    

def load_from_json(js):
    try:
        with open(js, encoding='utf-8') as f:
            cfg = json.load(f)
        return cfg
    except Exception as e:
        print(e)
        print("[DomainHelper] Opps! %s _load_from_json Error." % js)
        exit()


def main():
    parser = setup_parser()
    args = parser.parse_args()

    passwd_key='0f1571c947刘'

    output_root = args.out
    input_root = args.cfg

    shutil.copytree(input_root, output_root)

    for root, dirs, files in os.walk(output_root):
        for file in files:
            if file.endswith('.json'):
                srcPath = os.path.join(root, file)
                print('srcPath:', srcPath)
                with open(srcPath, 'r') as in_file:
                    chunk = in_file.read()
                    if len(chunk) == 0:
                        print('len(chunk) == 0')
                        break
                    passwd_str = des_encode(chunk, passwd_key)
                    with open(srcPath, 'w') as out_file:
                        out_file.write(passwd_str)
                    



if __name__ == '__main__':
    main()
