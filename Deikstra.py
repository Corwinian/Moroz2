#!/usr/bin/env python3
import sys
op = {'+':1,'-':1,'*':2,'/':2,'^':3, '(':0, ')':0}

def conver_to_tokens(str):
	is_num = lambda x: x in '0123456789'
	res=[]
	buf=""
	for ch in str:
		if not is_num(ch) and buf !="":
			res.append(int(buf))
			buf= ""
		if ch in '()' or ch in op.keys():
			res.append(ch)
		elif is_num(ch):
			buf+=ch

	if buf != "":
		res.append(int(buf))
	return res

def to_opz(posl):
	res=[]
	ops=[]
	for ch in posl:
		if ch in op.keys() and ch not in '()':
			while(len(ops) > 0 and op[ch]<=op[ops[-1]]):
				res.append(ops.pop())
			ops.append(ch)
		elif ch == '(':
			ops.append(ch)
		elif ch == ')':
			while ops[-1] != '(':
				res.append(ops.pop())
			ops.pop()
		else:
			res.append(ch)
	if len(ops):
		while (len(ops)):
			res.append(ops.pop())
	return res

def calc(opz):
	check_pow = lambda x: x if x != '^' else '**'
	st = []
	while len(opz) != 0:
		if opz[0] in op.keys():
			opz.insert(0, eval("{2}{1}{0}".format(st.pop(), check_pow(opz.pop(0)), st.pop())))
		else:
			st.append(opz.pop(0))
	return st.pop()

def main(argv):
	print("expression - {0}".format(argv[1]))
	tokens = conver_to_tokens(argv[1])
	print("tokens - {0}".format(tokens))
	opz = to_opz(tokens)
	print("opz - {0}".format(opz))
	res = calc(opz)
	print("res - {0}".format(res))


if __name__=="__main__":
	main(sys.argv)
