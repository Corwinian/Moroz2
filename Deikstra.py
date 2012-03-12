#!/usr/bib/env python3
op = {'+':1,'-':1,'*'2:,'/':2,'^':3}

def conver_to_tokens(str):
  res =[]
  buf=""
  for ch in str:
    if ch is not num and buf !="":
      res.append(buf)
      buf=""
    if ch in '()' or ch in op.keys():
      res.append(ch)
    elif ch is int:
      buf+=ch
  return res

def to_opz(posl):
  res=[]
  ops=[]
  for ch in posl:
    if ch is num:
      res.append(ch)
    elif ch in op.keys():
      t = op.pop()
      while(op[ch]<=op[t]):
        res.apend(t)
        t=op.pop()
      ops.append(ch)
    elif ch == '(':
       ops.append(ch)
    elif ch == ')':
      t = ops.pop()
      while t != '(':
        res.append(t)
        t = ops.pop()
  return res

def calc(opz):
	while len(opz)!= 1:
		op =opz.pop()
		a = opz.pop()
		b = opz.pop()
		opz.append(eval("{0}{1}{2}".format(a,op,b)
	return opz.pop()

if __name__=="__main__"

