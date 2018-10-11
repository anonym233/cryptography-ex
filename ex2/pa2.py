# -*- coding: cp936 -*-
from Crypto.Cipher import AES
from Crypto.Util import Counter

key1 = '140b41b22a29beb4061bda66b6747e14'.decode('hex')
ciphertext1 = ('4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee' 
              '2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81').decode('hex')
              
key2 = '140b41b22a29beb4061bda66b6747e14'.decode('hex')
ciphertext2 = ('5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48'
               'e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253').decode('hex')
               
key3 = '36f18357be4dbd77f050515c73fcf9f2'.decode('hex')
ciphertext3 = ('69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc3'
               '88d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329').decode('hex')
               
key4 = '36f18357be4dbd77f050515c73fcf9f2'.decode('hex')
ciphertext4 = ('770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa'
               '0e311bde9d4e01726d3184c34451').decode('hex')
#调用CBC与CTR    
def aes_decrypt_cbc_pc(ciphertext, key):
    block_len = len(key)
    IV = ciphertext[0:block_len]
    
    c = AES.new(key, mode=AES.MODE_CBC, IV=IV)
    return c.decrypt(ciphertext)[block_len:]
    
def aes_decrypt_ctr_pc(ciphertext, key):
    block_len = len(key)
    IV = ciphertext[0:block_len]
    counter = int(IV.encode('hex'), 16)
    c = AES.new(key, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=counter))
    return c.decrypt(ciphertext[block_len:])
#自写
def strxor(a, b):     # xor two strings of different lengths
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def aes_decrypt_cbc(ciphertext, key):
    block_len = len(key)
    c = AES.new(key)
    IV = ciphertext[0:block_len]
    message_blocks = []
    for i in range(len(ciphertext) / block_len - 1):
        ciphertext_block = ciphertext[block_len * (i + 1):block_len * (i + 2)]
        decrypted = c.decrypt(ciphertext_block)
        message_blocks.append(strxor(decrypted, IV))
        IV = ciphertext_block
        
    return ''.join(message_blocks)
     
    
def aes_decrypt_ctr(ciphertext, key):
    block_len = len(key)
    c = AES.new(key)
    IV = ciphertext[0:block_len]
    counter = int(IV.encode('hex'), 16)

    message_blocks = []
    for i in range(len(ciphertext) / block_len):
        ciphertext_block = ciphertext[block_len * (i + 1):block_len * (i + 2)]
        block_counter = ('%016x' % (counter + i)).decode('hex')
        message_blocks.append(strxor(ciphertext_block, c.encrypt(block_counter)))        
    return ''.join(message_blocks)
    
def main():

    print 'CBC(调用):%s' % aes_decrypt_cbc_pc(ciphertext1, key1)
    print 'CBC(调用):%s' % aes_decrypt_cbc_pc(ciphertext2, key2)

    print 'CTR(调用):%s' % aes_decrypt_ctr_pc(ciphertext3, key3)
    print 'CTR(调用):%s' % aes_decrypt_ctr_pc(ciphertext4, key4)

    print 'CBC:%s' % aes_decrypt_cbc(ciphertext1, key1)
    print 'CBC:%s' % aes_decrypt_cbc(ciphertext2, key2)
    
    print 'CTR:%s' % aes_decrypt_ctr(ciphertext3, key3)
    print 'CTR:%s' % aes_decrypt_ctr(ciphertext4, key4)
    
if __name__ == '__main__':
    main()
