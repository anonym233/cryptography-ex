#coding:utf-8
#python2.7
import base64
import sys
import random
import re
from Crypto.Cipher import AES


key = ''.join([chr(random.randint(0,255)) for i in range(16)])


def str_xor(a, b):
    if len(a) > len(b):
        return ''.join([chr(ord(x)^ord(y)) for x, y in zip(a[:len(b)], b)])
    else:
        return ''.join([chr(ord(x)^ord(y)) for x, y in zip(a, b[:len(a)])])


def div2blocks(data, blocklen):
	out = []
	number = len(data)/blocklen
	for i in range(number):
		out.append(data[i*blocklen:(i+1)*blocklen])
	if len(data) % blocklen != 0:
		last_block = data[(i+1)*blocklen:]
		out.append(last_block)
	return out


def block_pad_PKCS7(block, blocklen):
	padlen = blocklen-len(block)
	return block + chr(padlen)*padlen


def data_pad_PKCS7(data, blocklen):
	blocks = div2blocks(data, blocklen)
	if len(blocks[-1]) < blocklen:
		blocks[-1] = block_pad_PKCS7(blocks[-1], blocklen)
	#整好，再补一个块
	else:
		blocks.append(chr(blocklen) * blocklen)
	return ''.join(blocks)


def enc_CBC_AES(data, blocklen, iv, key):
	data = data_pad_PKCS7(data, blocklen)
	cipher = AES.new(key, AES.MODE_ECB)
	result = iv
	for i in range(len(data)/blocklen):
		ciphertext = cipher.encrypt(str_xor(data[i*blocklen:(i+1)*blocklen],iv))
		iv = ciphertext
		result += ciphertext
	return result


def dec_CBC_AES(ciphertext, blocklen, key):
	cipher = AES.new(key, AES.MODE_ECB)
	iv = ciphertext[:blocklen] #密文的第一块，作为新的iv
	result=''
	for i in range(1,len(ciphertext)/blocklen): #对于每一块
		data = str_xor(cipher.decrypt(ciphertext[i*blocklen:(i+1)*blocklen]),iv)
		iv = ciphertext[i*blocklen:(i+1)*blocklen] #更新iV
		result += data
	pad = len(result)
	return result[:pad-ord(result[pad-1])]


def check_input(my_input):
	if re.match('.*?[=;].*?', my_input):
		return False
	else:
		return True


def enc_input(my_input):
	if not check_input(my_input):
		print "input contains : or ; !"
		return False
	data = "comment1=cooking%20MCs;userdata=" + my_input + ";comment2=%20like%20a%20pound%20of%20bacon"
	iv = ''.join([chr(random.randint(0,255)) for i in range(16)])
	return iv, enc_CBC_AES(data, 16, iv, key)


def dec_challenge(ciphertext):
	pt = dec_CBC_AES(ciphertext, 16, key)
	#print "dec_challenge:",pt
	if ";admin=true;" in pt:
		return True, pt
	else:
		return False, pt


def tamper_data(ciphertext, fakedata, oridata, idx):
	blocks = div2blocks(ciphertext, 16)
	blocks[idx-1] = str_xor(blocks[idx-1], str_xor(oridata, fakedata))#原先全是A，则^'a'^'b'，使a变为b
	return ''.join(blocks)

def main():
	iv,ct = enc_input("A"*32)
	#原密文
	print "origin ciphertext:\n",ct.encode('hex')
	new_ct = tamper_data(ct, ";admin=true;AAAA", "A"*16, 3)
	
	print "tampered ciphertext:\n",new_ct.encode('hex')
	result, pt = dec_challenge(new_ct)
	if result == True:
		print "success"
	else:
		print "failed"
	print pt
	
	#修补第二块
	error_block2 = pt[16:32]
	new_ct_2 = tamper_data(new_ct, "%20MCs;userdata=", error_block2, 2)
	result2, pt2 = dec_challenge(new_ct_2)
	if result2 == True:
		print "success"
	else:
		print "failed"
	print pt2
	
	#修补第一块
	error_block1 = pt2[:16]
	new_ct_1 = tamper_data(new_ct_2,  "comment1=cooking", error_block1, 1)
	result1, pt1 = dec_challenge(new_ct_1)
	if result1 == True:
		print "success"
	else:
		print "failed"
	print pt1

if __name__ == "__main__":
	main()
