# -*- coding: utf-8 -*-
# MRZ:
#     12345678<8<<<1110182<111116?<<<<<<<<<<<<<<<4
#     
from Crypto.Cipher import AES
from Crypto.Hash import SHA
import base64
import re

def generateExpiry():
    #Check digit on date of expiry
    a = [7, 3, 1] * 2
    b = [1,1,1,1,1,6]
    c=sum([a[i] * b[i] for i in xrange(6)])%10
    return c
def generateKey():
    MRZ = '12345678<8<<<1110182<111116'+str(generateExpiry())+'<<<<<<<<<<<<<<<4'
    MRZNo = MRZ[:9]
    JNo = MRZ[9]
    Nationality = MRZ[10:13]
    Birthday = MRZ[13:19]
    JBir = MRZ[19]
    Sex = MRZ[20]
    MRZEnd = MRZ[21:27]
    JMRZEnd = MRZ[27]
    Others = MRZ[28:]
    Info = MRZNo+JNo+Birthday+JBir+MRZEnd+JMRZEnd
    print 
    h = SHA.new()
    h.update(Info)
    H_SHA1 = h.hexdigest()
    print H_SHA1
    K_seed = H_SHA1[:32]
    c = '00000001'
    D = K_seed + c
    D=D.decode('hex')
    h = SHA.new()
    h.update(D)
    H_SHA1_D = h.hexdigest()
    print H_SHA1_D
    key = H_SHA1_D[:32]
    ka = key[:16]
    ka=re.findall('.{2}',ka)
    k=[]
    for i in ka:
        if str(bin(int(i,16))[2:-1]).count('1')%2==0:
            k+=[hex(int(str(bin(int(i,16))[2:-1])+'0',2)+1)[2:].zfill(2)]
        else:
            k+=[hex(int(str(bin(int(i,16))[2:-1])+'0',2))[2:].zfill(2)]
    k1 = ''.join(k)
    kb=key[16:]
    kb=re.findall('.{2}',kb)
    k=[]
    for i in kb:
        if str(bin(int(i,16))[2:-1]).count('1')%2==0:
            k+=[hex(int(str(bin(int(i,16))[2:-1])+'0',2)+1)[2:].zfill(2)]
        else:
            k+=[hex(int(str(bin(int(i,16))[2:-1])+'0',2))[2:].zfill(2)]
    k2= ''.join(k)
    key = k1+k2
    return key

def main():
    msg = '9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jx aa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2N fNnWFBTXyf7SDI'
    msg = base64.b64decode(msg)
    key = generateKey()
    cipher = AES.new(key.decode('hex'), AES.MODE_CBC, ('0' * 32).decode('hex'))
    plaintext = cipher.decrypt(msg)
    print 'the plaintext is:', plaintext

if __name__ == '__main__':
    main()
