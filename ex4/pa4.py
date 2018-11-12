#coding:utf-8
#python2.7
import requests


charset = [chr(i) for i in range(256)]
url = 'http://crypto-class.appspot.com/po?er='
cipher = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'.decode('hex')


def str_xor(a, b):
    if len(a) > len(b):
        return ''.join([chr(ord(x)^ord(y)) for x, y in zip(a[:len(b)], b)])
    else:
        return ''.join([chr(ord(x)^ord(y)) for x, y in zip(a, b[:len(a)])])


def str_set_chr(s, idx, ch):
	s = list(s)
	s[idx] = ch
	return ''.join(s)

def div2blocks(cipher):
	out = []
	if len(cipher) % 16 != 0:
		return False
	else:
		number = len(cipher)/16
		for i in range(number):
			out.append(cipher[i*16:(i+1)*16])
	return out
def url_request(cipher):
	res = requests.get(url + cipher.encode('hex'))
	if res.status_code == 404:
		return True
	else:
		return False

def padding_oracle_attack(full_cipher):
	guess_plain = ''
	
	iv = full_cipher[:16] #取iv
	cipher = full_cipher[16:]
	cipher_blocks = div2blocks(cipher)

	for i in range(-1, len(cipher_blocks)-1): #块数，最后一块不管
		if i == -1: #第一块，取最初iv
			old_iv = iv
		else: #之后取上一密文块
			old_iv = cipher_blocks[i]

		guess_block = "\x00"*16 #猜测明文

		for j in range(1, len(iv)+1): #块内爆破，j对应块内偏移
			correct_pad = "\x00"*(16-j)+chr(j)*j # 正确填充，依次添加
			for char in charset:
				if char == '\x01' and i == len(cipher_blocks)-2: #最后一块不猜1
					continue
				guess_block = str_set_chr(guess_block, 16-j, char) #依次试验每一位的值，第j轮，试验相应位置
				# new_iv ^ middle = correct_pad
				# old_iv ^ middle = plain
				# so: 
				# correct_pad ^ plain = new_iv ^ old_iv
				# new_iv = correct_pad ^ plain ^ old_iv
				new_iv = str_xor(str_xor(guess_block, correct_pad), old_iv)
				if i == -1:
					iv = new_iv
				else:
					cipher_blocks[i] = new_iv
				#尝试访问
				print "Now test: ", (iv + ''.join(cipher_blocks[:i+2])).encode('hex')
				response = url_request(iv + ''.join(cipher_blocks[:i+2]))
				if response:
					break
		guess_plain += guess_block #明文
		print "guess_plain:",guess_plain
	return guess_plain

if __name__ == '__main__':
	correct_plain = padding_oracle_attack(cipher)
	print correct_plain
