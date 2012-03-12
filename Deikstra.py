#!/usr/bin/env python3
import sys
op = {'+':1,'-':1,'*':2,'/':2,'^':3}

def conver_to_tokens(str):
	is_num = lambda x: x in '0123456789'
	res =[]
	buf=""
	for ch in str:
		if not is_num(ch) and buf !="":
			res.append(int(buf))
			buf=""
		if ch in '()' or ch in op.keys():
			res.append(ch)
		elif is_num(ch):
			buf+=ch
			print("ch - {0}".format(ch))
			print("buf - {0}".format(buf))

	if buf != "":
		res.append(int(buf))
	return res

def to_opz(posl):
	res=[]
	ops=[]
	for ch in posl:
		if ch in op.keys():
			print ('ch - {0}'.format(ch))
			while(len(ops) > 0 and op[ch]<=op[ops[-1]]):
				t=ops.pop()
				res.apend(t)
			ops.append(ch)
		elif ch == '(':
			ops.append(ch)
		elif ch == ')':
			t = ops.pop()
			while t != '(':
				res.append(t)
				t = ops.pop()
		else:
			res.append(ch)
	if len(ops):
		while (len(ops)):
			res.append(ops.pop())
	return res

def calc(opz):
	st = []
	while len(opz) != 0:
		if opz[0] in op.keys():
			a = st.pop()
			b = st.pop()
			print("a - {0}".format(a))
			print("b - {0}".format(b))
			t =eval("{0}{1}{2}".format(b, opz.pop(0), a))
			print("t - {0}".format(t))
			opz.insert(0, t)
			print(opz)
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
