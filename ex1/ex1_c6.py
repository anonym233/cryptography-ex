# -*- coding: utf-8 -*-

import itertools
import linecache
def hamming_distance(s1,s2):
    dist=0
    for x,y in zip(s1,s2):
        b=bin(ord(x)^ord(y)) #转换为二进制
        dist+=b.count('1')
    return dist
def guess_keysize(string):
    normals=[]
    for keysize in range(2,40):
        blocks=[]
        cnt=0
        distance=0
        #四个block，得到hamming_distance。
        for i in range(0,len(string),keysize):
            cnt+=1
            blocks.append(string[i:i+keysize])
            if cnt==4:
                break
        pairs=itertools.combinations(blocks,2)
        for (x,y) in pairs:
            distance+=hamming_distance(x,y)
        #计算nomal_distance
        normal_distance=distance/keysize
        key={
        'keysize':keysize,
        'distance':normal_distance
        }
        normals.append(key)
        print key
    #选3个最小的为可能的keysize
    mkeysize=sorted(normals,key=lambda c:c['distance'])[0:3]
    print mkeysize
    return mkeysize
FREQ = {'a':0.08167,'b':0.01492, 'c':0.02782, 'd':0.04253,
                    'e':0.12702, 'f':0.02228, 'g':0.02015, 'h':0.06094,
                    'i':0.06966, 'j':0.00153, 'k':0.00772, 'l':0.04025,
                    'm':0.02406, 'n':0.06749, 'o':0.07507, 'p':0.01929,
                    'q':0.00095, 'r':0.05987, 's':0.06327, 't':0.09056,
                    'u':0.02758, 'v':0.00978, 'w':0.02360, 'x':0.00150,
                    'y':0.01974, 'z':0.00074,' ':1}

def get_score(string):
    score=0
    for char in string:
        char=char.lower()
        if char in FREQ:
            score+=FREQ[char]
    return score

def single_character_XOR(key,string):
    result=""
    for i in string:
        b=chr(key^ord(i))
        result+=b
    return result

def bianli(string):
    candidate=[]
    for i in range(256):
        plaintext=single_character_XOR(i,string)
        score=get_score(plaintext)
        result={
        'score':score,
        'plaintext':plaintext,
        'key':i
        }
        candidate.append(result)
    return sorted(candidate,key=lambda c:c['score'])[-1]
def guess_key(keysize,string):
    now_str=''
    key=''
    for i in range(keysize):
        now_str=''
        for index,ch in enumerate(string):
            if index%keysize==i:
                now_str+=ch

        key+=chr(bianli(now_str)['key'])
    print key
    return key
def repeating_key_XOR(key,string):
    key_len=len(key)
    result=''
    str_result=''
    for index,ch in enumerate(string):
        n=index%key_len
        b=chr(ord(key[n])^ord(ch))
        str_result+=b
    return str_result
def get_result(string):
    keysize_list=guess_keysize(string)
    candidate_key=[]
    possible_plaints=[]
    for keysize in keysize_list:
        key=guess_key(keysize['keysize'],string)
        possible_plaints.append((repeating_key_XOR(key,string),key))       
    return sorted(possible_plaints,key=lambda c:get_score(c[0]))[-1]
    
def main():
    contents=open('6.txt').read()
    string=str(contents).decode('base64')#以base64对字符串进行解码获得字符串
    result=get_result(string)
    print result[0]


if __name__ == '__main__':
    main()

