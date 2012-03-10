#!/usr/bin/env python

import sys
import heapq
import functools

BITS_IN_BYTE=8

class Hafman(object):
	"""Hafman archivator"""

	class Tree(object):
		"""Tree node"""
		def __init__(self, weight, ch=None, left=None, right=None):
			#super(Tree, self).__init__()
			self.ch = ch
			self.left = left
			self.right = right
			self.weight = weight

		def __lt__(self, other):
			return self.weight < other.weight

		def __str__(self):
			return "w-{0} ch {1})".format(self.weight, self.ch)

		def hameChildren(self):
			return self.left != None or self.right != None

	bytes = None
	freq_table = {}
	hafman_table = {}

	def __init__(self, byteArray):
		self.bytes = byteArray

	def create_freq_table(self):
		d =0
		for byte in self.bytes:
			d +=1
			if byte in self.freq_table.keys():
				self.freq_table[byte] += 1
			else:
				self.freq_table[byte] = 1

	def make_tree(self):
		tree = [ self.Tree(v,k) for k, v in self.freq_table.items()]
		heapq.heapify(tree)
		while len(tree) > 1:
			left, right = heapq.heappop(tree), heapq.heappop(tree)
			parent = self.Tree(left.weight  + right.weight, left=left, right = right)
			heapq.heappush(tree, parent)

		def convert(tree, l):
			if tree.hameChildren():
				convert(tree.left, l+ [False])
				convert(tree.right, l+[True])
			else:
				self.hafman_table[tree.ch] = l
		a = []
		convert(tree[0], a)

	def encode_freq_table(self):
		res = bytearray([])
		for byte in self.freq_table.keys():
			res.append(byte)
			count = self.freq_table[byte]
			res.append(count//2**BITS_IN_BYTE)
			res.append(count%2**BITS_IN_BYTE)
		return res

	def	encode_file(self):
		bit_res = []
		for byte in self.bytes:
			bit_res.extend(self.hafman_table[byte])
		step = 0
		temp = 0
		res = bytearray ([])
		for bit in bit_res:
			if step == BITS_IN_BYTE:
				res.append(temp)
				step =0
				temp =0
			temp <<= 1
			temp |= bit
			step +=1

		if step != 0:
			while step != BITS_IN_BYTE:
				temp <<= 1
				step += 1
			res.append(temp)
		return res

	def encode(self):
		self.create_freq_table()
		self.make_tree()
		res = bytearray([len(self.freq_table)])
		res.extend(self.encode_freq_table())
		t = len(res)
		res.extend(self.encode_file())
		return res

	def load_freq_table(self, table_size):
		raw_data = self.bytes[1:table_size*3+1]
		i=0
		file_size =0
		while i + 2 < len(raw_data):
			self.freq_table[raw_data[i]] = raw_data[i+1]* (2 **BITS_IN_BYTE) + raw_data[i+2]
			file_size += self.freq_table[raw_data[i]]
			i+=3

		return file_size

	def make_decode_tree(self):
		self.make_tree()
		to_str = lambda z:(functools.reduce( lambda x, y:  x + ('1' if y == True else '0' ), z,'' ))
		return {to_str(v): k for k, v in self.hafman_table.items()}

	def decode_data(self, file_size, table_size, decode_tree):
		to_str = lambda z:(functools.reduce( lambda x, y:  x + ('1' if y == True else '0' ), z,'' ))
		data = self.bytes[table_size*3+1:]
		readed_byte = 0
		key = ''
		res = bytearray([])
		while len(res) < file_size:
			byte = data[readed_byte]
			bits = [(byte >> i) % 2 != 0 for i in range(0,8)]
			bits.reverse()

			for bit in to_str(bits):
				key += bit
				if key in decode_tree.keys() and len(res) < file_size:
					res.append(decode_tree[key])
					key=''
			readed_byte+=1
		return res

	def decode(self):
		table_size = self.bytes[0]
		file_size = self.load_freq_table(table_size)
		return	self.decode_data(file_size,table_size, self.make_decode_tree())
