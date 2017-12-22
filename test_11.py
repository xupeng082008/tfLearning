#/usr/bin/env python3
#!-*- coding:utf-8 -*-

import json
import os


def load_from_json(js):
    import encrypt.encrypt
    try:
        try:
            with open(js, encoding='utf-8') as f:
                cfg = json.load(f)
            return cfg
        except:
            decrypter = encrypt.encrypt.Crypter()
            with open(js, 'rb') as f:
                text = f.read()
            plaintext = decrypter.decrypt_string(text)
            if isinstance(plaintext, bytes):
                plaintext = plaintext.decode('utf-8')
            return json.loads(plaintext)
    except Exception as e:
        print("Error: [DomainHelper] Opps! %s _load_from_json Error." % js)
        return None


def dump_to_jsonfile(jsondata, filename):
    if jsondata:
        with open(filename, 'w', encoding='utf-8') as fout:
            json.dump(jsondata, fout, sort_keys=True, ensure_ascii=False, indent=4)


def load_from_path(path):
    final_cfg = {}
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith('.json'):
                json_file = os.path.join(root, filename)
                cfg = load_from_json(json_file)
                if cfg is not None:
                    # final_cfg.update(cfg)
                    dump_to_jsonfile(cfg, str(json_file).replace('.json', '_.json'))
                else:
                    raise Exception('[load_from_path] Error: json %s format error' % filename)
    return final_cfg


def main():
    json_path = '/home/xupeng/Desktop/test/jhsw_en/jhsw_en/'
    load_from_path(json_path)


if __name__ == "__main__":
    main()