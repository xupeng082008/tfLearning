# /usr/bin/env python3
# -*-coding: utf-8 -*

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


def main():
    info = "please input your wds:"
    while 1:
        wds = get_input(info)
        wds2json(wds)


if __name__ == "__main__":
    main()