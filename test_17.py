# /usr/bin/env python3
# -*-coding: utf-8 -*

import os
import pexpect
import json

BASE_PATH = '/home/xupeng/workspace/cfg_repos'  # /home/xupeng/workspace/cfg_repos/lczp/cfgs/lczp
NEW_TTS_PATH = '/home/new_cfgs/'
TTS_PATH = '/root/cfgs/'
PASSWD = '50xfswsscqdb@'


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


def search_json_files(path, file_pathes={}):
    if path:
        for rt, dirs, files in os.walk(path):
            for dir in dirs:
                json_file = dir + '/cfgs/' + dir + '/replace.json'
                json_file_path = os.path.join(rt, json_file)
                if os.path.isfile(json_file_path):
                    json_data = load_from_json(json_file_path)
                    # print(json_file_path)
                    speaker = json_data.get('use_speaker_flag', None)
                    if speaker and '2' in speaker:
                        print(dir)
                if os.path.isfile(json_file_path):
                    file_pathes[dir] = json_file_path
        return file_pathes

    else:
        raise 'invalid file_path'


def ssh_cmd(ip, passwd, cmd):
    ret = -1
    ssh = pexpect.spawn('ssh root@%s "%s"'%(ip, cmd))
    try:
        i = ssh.expect(['password:', 'continue connecting(yes/no)?'], timeout=3)
        if i == 0:
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password:')
            ssh.sendline(passwd)
        ssh.sendline(cmd)
        r = ssh.read()
        print('server code: %s', r)
        ret = 0
    except pexpect.EOF:
        print("EOF")
        ssh.close()
        ret = -1
    except pexpect.TIMEOUT:
        print('TIMEOUT')
        ssh.close()
        ret = -2
    return ret


def to_31_server(src_path, dst_path):
    SRC_IP = '127.0.0.1'
    DST_IP = '47.97.179.31'
    json_files = search_json_files(path=BASE_PATH)
    for key, val in json_files.items():
        if os.path.isfile(val):
            server_cmd = 'mkdir -p cfgs/%s' %(key)
            ssh_cmd(DST_IP, PASSWD, server_cmd)
            clinet_cmd = 'scp %s root@%s:/root/cfgs/%s' %(val, DST_IP, key)
            child = pexpect.spawn(clinet_cmd)
            child.expect('password:')
            child.sendline(PASSWD)
            child.read()

def main():
    to_31_server(None, None)
    print('------------------------------------------------------END')


if __name__ == '__main__':
    main()