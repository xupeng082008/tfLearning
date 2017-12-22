#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from simplecrypt import encrypt, decrypt
import base64


class Crypter(object):

    def __init__(self):
        self.password = 'toolwiz.com'

    def encrypt_string(self, string, safe=False):
        if safe:
            # return encrypt(self.password, string)
            pass
        else:
            return self.encode(string)

    def decrypt_string(self, string, safe=False):
        if safe:
            # return decrypt(self.password, string)
            pass
        else:
            return self.decode(string)

    def encode(self, clear):
        enc = []
        for i in range(len(clear)):
            key_c = self.password[i % len(self.password)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc).encode('utf-8'))

    def decode(self, enc):
        dec = []
        enc = base64.urlsafe_b64decode(enc)
        enc = enc.decode('utf-8')
        for i in range(len(enc)):
            key_c = self.password[i % len(self.password)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)


"""
def load_from_json(js):
    try:
        with open(js, encoding='utf-8') as f:
            cfg = json.load(f)
        return cfg
    except Exception as e:
        print(e)
        print("[DomainHelper] Opps! %s _load_from_json Error." % js)
        exit()


cfg = load_from_json('select.json')
ciphertext = encrypt('password', json.dumps(cfg))
with open('select_e.txt', 'wb') as f:
    f.write(ciphertext)

with open('select_e.txt', 'rb') as f:
    text = f.read()
plaintext = decrypt('password', text)

with open('select_d.json', 'w') as f:
    json.dump(json.loads(plaintext), f, indent=4, ensure_ascii=False)
"""
