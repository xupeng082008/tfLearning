#_*_ coding:utf-8 _*_

from . desstruct import *
import re
import sys
from binascii import hexlify

__all__=['desencode']
class DES_EN():
	'''des 加密'''
	def __init__(self):
		pass
	#加密
	def code(self,from_code,key,code_len,key_len):
		output=""
		trun_len=0
		
		#将密文和密钥转换为二进制
		code_string=self._functionCharToA(from_code,code_len)
		code_key=self._functionCharToA(key,key_len)
		
		#如果密钥长度不是16的整数倍则以增加0的方式变为16的整数倍
		if code_len%16!=0:
			real_len=(code_len//16)*16+16
		else:
			real_len=code_len
		
		if key_len%16!=0:
			key_len=(key_len//16)*16+16
		key_len*=4

		#每个16进制占4位
		trun_len=4*real_len
		#对每64位进行一次加密
		#print("trun_len %d" % (trun_len))
		for i in range(0,trun_len,64):
			run_code=code_string[i:i+64]
			l=i%key_len
			run_key=code_key[l:l+64]

			#64位明文、密钥初始置换
			run_code= self._codefirstchange(run_code)
			run_key= self._keyfirstchange(run_key)
			
			#16次迭代
			for j in range(16):
				
				#取出明文左右32位
				code_r=run_code[32:64]
				code_l=run_code[0:32]
					
				#64左右交换
				run_code=code_r
				
				#右边32位扩展置换
				code_r= self._functionE(code_r)
				
				#获取本轮子密钥
				key_l=run_key[0:28]
				key_r=run_key[28:56]
				key_l=key_l[d[j]:28]+key_l[0:d[j]]
				key_r=key_r[d[j]:28]+key_r[0:d[j]]
				run_key=key_l+key_r
				key_y= self._functionKeySecondChange(run_key)

				#异或
				code_r= self._codeyihuo(code_r,key_y)
				
				#S盒代替/选择
				code_r= self._functionS(code_r)
				
				#P转换
				code_r= self._functionP(code_r)
				
				#异或
				code_r= self._codeyihuo(code_l,code_r)
				run_code+=code_r
			#32互换
			code_r=run_code[32:64]
			code_l=run_code[0:32]
			run_code=code_r+code_l
			
			#将二进制转换为16进制、逆初始置换
			output+=self._functionCodeChange(run_code)
		return output

	#异或	
	@staticmethod
	def _codeyihuo(code, key):
		code_len=len(key)
		return_list=''
		for i in range(code_len):
			if code[i]==key[i]:
				return_list+='0'
			else:
				return_list+='1'
		return return_list

	#密文或明文初始置换		 		 							
	@staticmethod
	def _codefirstchange(code):
		changed_code=''
		for i in range(64):
			changed_code+=code[ip[i]-1]
		return changed_code

	#密钥初始置换
	@staticmethod
	def _keyfirstchange (key):
		changed_key=''
		#print("%d / %d" % (len(pc1), len(key)))
		for i in range(56):
			changed_key+=key[pc1[i]-1]
		return changed_key

	#逆初始置换
	@staticmethod
	def _functionCodeChange(code):
		lens=len(code)//4
		return_list=''
		for i in range(lens):
			strlist=''
			for j in range(4):
				strlist+=code[ip_1[i*4+j]-1]
			return_list+="%x" %int(strlist,2)
		return return_list
	
	#扩展置换	
	@staticmethod
	def _functionE(code):
		return_list=''
		for i in range(48):
			return_list+=code[e[i]-1]
		return return_list		
	
	#置换P		
	@staticmethod
	def _functionP(code):
		return_list=''
		for i in range(32):
			return_list+=code[p[i]-1]
		return return_list

	#S盒代替选择置换
	def _functionS(self, key):
		return_list=''
		for i in range(8):
			row=int( str(key[i*6])+str(key[i*6+5]),2)
			raw=int(str( key[i*6+1])+str(key[i*6+2])+str(key[i*6+3])+str(key[i*6+4]),2)
			return_list+=self._functionTos(s[i][row][raw],4)

		return return_list
		
	#密钥置换选择2
	@staticmethod
	def _functionKeySecondChange(key):
		return_list=''
		for i in range(48):
			return_list+=key[pc2[i]-1]
		return return_list
	
	#将十六进制转换为二进制字符串
	def _functionCharToA(self,code,lens):
		return_code=''
		lens=lens%16
		for key in code:
			code_ord=int(key,16)
			return_code+=self._functionTos(code_ord,4)		
		if lens!=0:
			return_code+='0'*(16-lens)*4
		return return_code
	
	#二进制转换
	@staticmethod
	def _functionTos(o, lens):
		return_code=''
		for i in range(lens):
			return_code=str(o>>i &1)+return_code
		return return_code


def tounicode(string):
	#print('string:', string)
	string_len=len(string)
	return_bytes = bytes(int(string[i:i+2],16) for i in range(0,string_len,2))
	#print('return_bytes:', return_bytes)
	result_str = return_bytes.decode('utf-8')
	#print('result_str:', result_str)
	return result_str


#将unicode字符转换为16进制
def tohex(string):
	string = string.encode('utf-8')
	return_string=''
	for i in string:
		#print(chr(i))
		return_string+="%02x"%ord(chr(i))
	return return_string


#入口函数
def des_encode(from_code,key):
	#转换为16进制
	from_code=tohex(from_code)
	key=tohex(key)
	
	des_en=DES_EN()
	key_len=len(key)
	string_len=len(from_code)		
		
	if string_len<1 or key_len<1:
		print('error input')
		return False
	key_code= des_en.code(from_code,key,string_len,key_len)
	return key_code


__all__=['desdecode']
class DES_DE():
	'''解密函数，DES加密与解密的方法相差不大
		只是在解密的时候所用的子密钥与加密的子密钥相反
	'''
	def __init__(self):
		pass
	
	def decode(self,string,key,key_len,string_len):
		output=""
		trun_len=0
		num=0
		
		#将密文转换为二进制
		code_string=self._functionCharToA(string,string_len)
		#获取字密钥
		code_key=self._getkey(key,key_len)
				
		
		#如果密钥长度不是16的整数倍则以增加0的方式变为16的整数倍
		real_len=(key_len//16)+1 if key_len%16!=0 else key_len//16
		trun_len=string_len*4
		#对每64位进行一次加密
		for i in range(0,trun_len,64):
			run_code=code_string[i:i+64]
			run_key=code_key[num%real_len]

			#64位明文初始置换
			run_code= self._codefirstchange(run_code)
			
			#16次迭代
			for j in range(16):
				
				code_r=run_code[32:64]
				code_l=run_code[0:32]
				
				#64左右交换	
				run_code=code_r
				
				#右边32位扩展置换
				code_r= self._functionE(code_r)
				
				#获取本轮子密钥
				key_y=run_key[15-j]

				#异或
				code_r= self._codeyihuo(code_r,key_y)
				
				#S盒代替/选择
				code_r= self._functionS(code_r)
				
				#P转换
				code_r= self._functionP(code_r)
				
				#异或
				code_r= self._codeyihuo(code_l,code_r)
				
				run_code+=code_r
			num+=1
			
			#32互换
			code_r=run_code[32:64]
			code_l=run_code[0:32]
			run_code=code_r+code_l
			
			#将二进制转换为16进制、逆初始置换
			output+=self._functionCodeChange(run_code)
		return output
	
	#获取子密钥
	def _getkey(self,key,key_len):
		
		#将密钥转换为二进制
		code_key=self._functionCharToA(key,key_len)
		
		a=['']*16
		real_len=(key_len//16)*16+16 if key_len%16!=0 else key_len

		b=['']*(real_len//16)
		for i in range(real_len//16):
			b[i]=a[:]
		num=0
		trun_len=4*key_len
		for i in range(0,trun_len,64):
			run_key=code_key[i:i+64]
			run_key= self._keyfirstchange(run_key)
			for j in range(16):
				key_l=run_key[0:28]
				key_r=run_key[28:56]
				key_l=key_l[d[j]:28]+key_l[0:d[j]]
				key_r=key_r[d[j]:28]+key_r[0:d[j]]
				run_key=key_l+key_r
				key_y= self._functionKeySecondChange(run_key)
				b[num][j]=key_y[:]
			num+=1

		return b	
		
	#异或	 							
	@staticmethod
	def _codeyihuo(code, key):
		code_len=len(key)
		return_list=''
		for i in range(code_len):
			if code[i]==key[i]:
				return_list+='0'
			else:
				return_list+='1'
		return return_list

	#密文或明文初始置换		 							
	@staticmethod
	def _codefirstchange(code):
		changed_code=''
		for i in range(64):
			changed_code+=code[ip[i]-1]
		return changed_code
		
	#密钥初始置换
	@staticmethod
	def _keyfirstchange (key):
		changed_key=''
		for i in range(56):
			changed_key+=key[pc1[i]-1]
		return changed_key
	
	#逆初始置换
	@staticmethod
	def _functionCodeChange(code):
		return_list=''
		for i in range(16):
			strlist=''
			for j in range(4):
				strlist+=code[ip_1[i*4+j]-1]
			return_list+="%x" %int(strlist,2)
		return return_list
	
	#扩展置换	
	@staticmethod
	def _functionE(code):
		return_list=''
		for i in range(48):
			return_list+=code[e[i]-1]
		return return_list		
	
	#置换P	
	@staticmethod
	def _functionP(code):
		return_list=''
		for i in range(32):
			return_list+=code[p[i]-1]
		return return_list

	#S盒代替选择置换	
	def _functionS(self, key):
		return_list=''
		for i in range(8):
			row=int( str(key[i*6])+str(key[i*6+5]),2)
			raw=int(str( key[i*6+1])+str(key[i*6+2])+str(key[i*6+3])+str(key[i*6+4]),2)
			return_list+=self._functionTos(s[i][row][raw],4)

		return return_list
	
	#密钥置换选择2
	@staticmethod
	def _functionKeySecondChange(key):
		return_list=''
		for i in range(48):
			return_list+=key[pc2[i]-1]
		return return_list
	
	#将十六进制转换为二进制字符串
	def _functionCharToA(self,code,lens):
		return_code=''
		lens=lens%16
		for key in code:
			code_ord=int(key,16)
			return_code+=self._functionTos(code_ord,4)
		
		if lens!=0:
			return_code+='0'*(16-lens)*4
		return return_code
	
	#二进制转换
	@staticmethod
	def _functionTos(o, lens):
		return_code=''
		for i in range(lens):
			return_code=str(o>>i &1)+return_code
		return return_code

	
#入口函数
def des_decode(from_code,key):
	key=tohex(key)

	des_de = DES_DE()
	
	key_len=len(key)
	string_len=len(from_code)
	if string_len%16!=0:
		return False
	if string_len<1 or key_len<1:
		return False

	key_code= des_de.decode(from_code,key,key_len,string_len)
	return tounicode(key_code)



